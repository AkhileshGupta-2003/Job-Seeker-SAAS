import os , time
import json
import requests
def search_jobs_on_linkedin(location :str,
                            keyword: str,
                            country : str,
                            time_range: str,
                            job_type: str,
                            experience_level : str,
                            on_site : str,
                            company: str,
                            location_radius:str):
    url = 'https://api.brightdata.com/datasets/V3/trigger'
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


