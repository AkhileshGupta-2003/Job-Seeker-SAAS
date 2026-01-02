import os , time
import json
import requests
from langchain.agents import create_agent
from langchain.tools import tool








@tool('search_jobs_on_linkedin', description = 'Search jobs on linkedin for job listings using parameters (location , keyword, country,job_type, experience_level, on_site, comapny, location_radius) based on user input. This functions returns all job listings found on linkedin ')
def search_jobs_on_linkedin(location :str,
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
    url = f'https://api.brightdata.com/datasets/V3/trigger/{snapshot_id}'
    while requests.get(url, headers = headers).json()['status'] != 'ready':
        time.sleep(5)
    url = f'https://api.brightdata.com/datasets/V3/trigger/{snapshot_id}?format=json'
    response = requests.get(url,headers=headers)
    response.raise_for_status()
    return response.json()





@tool('search_jobs_on_glassdoor', description = 'Search jobs on Glassdoor for job listings using parameters (location , keyword, country) based on user input. This function returns all the job listings found on glassdoor.when providing the country code always provide the code (e.g. FR, AT, IT and so on)')
def search_jobs_on_glassdoor(location :str,
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
    url = f'https://api.brightdata.com/datasets/V3/trigger/{snapshot_id}'
    while requests.get(url, headers = headers).json()['status'] != 'ready':
        time.sleep(5)
    url = f'https://api.brightdata.com/datasets/V3/trigger/{snapshot_id}?format=json'
    response = requests.get(url,headers=headers)
    response.raise_for_status()
    return response.json()

def search_jobs_agent(prompt : str) -> str: 
    agent = create_agent(
        model = 'gpt-4.1-mini',
        tools = [search_jobs_on_linkedin, search_jobs_on_glassdoor]
    )
    response = agent.invoke(
        {'messages':
            [{'role' : 'system' , 'content':' You are a helpful assistant that helps users search for job listings on linkedin and glassdoor based on their preferences'},
             {'role' : 'user', 'content' : prompt}]}
    )
    return response['messages'][-1].content
