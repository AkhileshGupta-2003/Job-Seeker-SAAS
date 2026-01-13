import os , time
import json
import requests
from langchain.agents import create_agent
from langchain.tools import tool
from .models import SnapShot, LLMResult







@tool('search_jobs_on_linkedin', description = 'Search jobs on linkedin for job listings using parameters (location , keyword, country,job_type, experience_level, on_site, comapny, location_radius) based on user input. This functions returns all job listings found on linkedin ')
def search_jobs_on_linkedin(
                            llm_result_id : int,
                            location :str,
                            keyword: str,
                            country : str,
                            job_type: str,
                            experience_level : str,
                            on_site : str,
                            company: str,
                            location_radius:str,
                            time_range: str = 'past_month'):
    
    url = '"https://api.brightdata.com/datasets/v3/scrape?dataset_id=gd_lpfll7v5hcqtkxl6l&notify=false&include_errors=true&type=discover_new&discover_by=keyword&limit_per_input=5"'
    headers = {
    "Authorization": "Bearer BRIGHT_DATA_SECRET_KEY",
    "Content-Type": "application/json"}

    data = json.dumps({"input": [{
        "location":location,
        "keyword":keyword,
        "country":country,
        "time_range":time_range,
        "job_type":job_type,
        "experience_level":experience_level,
        "remote": on_site,
        "company":company,
        "location_radius":location_radius}]})

    response = requests.post(url,headers = headers, data = data)
    response.raise_for_status()
    snapshot_id = response.json()['snapshot_id']
    snapshot = SnapShot(
        snapshot_id = snapshot_id,
        ready = False,
        llm_result_id = llm_result_id,
        data ={})
    snapshot.save()
    return "Succesfully Created Snapshot."
    



@tool('search_jobs_on_glassdoor', description = 'Search jobs on Glassdoor for job listings using parameters (location , keyword, country) based on user input. This function returns all the job listings found on glassdoor.when providing the country code always provide the code (e.g. FR, AT, IT and so on)')
def search_jobs_on_glassdoor(llm_result_id : int,
                            location :str,
                            keyword: str,
                            country : str,
                            time_range: str = 'past_month'):
    url = '"https://api.brightdata.com/datasets/v3/scrape?dataset_id=gd_l7j0bx501ockwldaqf&notify=false&include_errors=true&type=discover_new&discover_by=keyword&limit_per_input=5"'
    headers = {
    "Authorization": "Bearer BRIGHT_DATA_SECRET_KEY",
    "Content-Type": "application/json"}

    data = json.dumps({"input": [{
        "location":location,
        "keyword":keyword,
        "country":country}]})

    response = requests.post(url,headers = headers, data = data)
    response.raise_for_status()
    snapshot_id = response.json()['snapshot_id']
    Snapshot = SnapShot(
        snapshot_id = snapshot_id,
        ready = False,
        llm_result_id = llm_result_id,
        data = {}
    )
    Snapshot.save()
    return "Succesfully Created Snapshot"

@tool('set_results_title', description = 'Set the title of the llmresult in the database for asynchronous processing')
def set_results_title(llm_result_id : int, title : str)-> str:
    llm_results = LLMResult.objects.get(id = llm_result_id)
    llm_results.title = title
    llm_results.save()
    return 'Succes'


def search_jobs_agent(llm_result_id : int,prompt : str) -> str: 
    agent = create_agent(
        model = 'gpt-4.1-mini',
        tools = [search_jobs_on_linkedin, search_jobs_on_glassdoor]
    )
    response = agent.invoke(
        {'messages':
            [{'role' : 'system' , 'content':' You are a helpful assistant that helps users search for job listings on linkedin and glassdoor based on their preferences'},
            {'role' : 'user', 'content' : f'The id of the llm result is {llm_result_id}.Always use the tool for setting the title of the given result id first. Always pass the result id when calling tools.User request : {prompt}'}]}
    )
    return response['messages'][-1].content

def is_ready(snapshot_id :str) -> bool:
    url = f'https://api.brightdata.com/datasets/V3/trigger/{snapshot_id}'
    headers = {
    "Authorization": "Bearer BRIGHT_DATA_SECRET_KEY",
    "Content-Type": "application/json"}

    return requests.get(url, headers = headers).json()['status'] == 'ready'



def get_data(snapshot_id:str)-> dict:
    url =  f'https://api.brightdata.com/datasets/V3/trigger/{snapshot_id}'
    headers = {
    "Authorization": "Bearer BRIGHT_DATA_SECRET_KEY",
    "Content-Type": "application/json"}
    response = requests.get(url,headers=headers)

    response.raise_for_status()
    
    return response.json()
