import os 
from dotenv import load_dotenv
load_dotenv('job-saas/.env')  



import requests
import json

headers = {
    "Authorization": "Bearer BRIGHT_DATA_SECRET_KEY",
    "Content-Type": "application/json",
}

data = json.dumps({
    "input": [{"location":"paris","keyword":"product manager","country":"FR","time_range":"Past month","job_type":"Full-time","experience_level":"Internship","remote":"On-site","company":"","location_radius":""}]
})

response = requests.post(
    "https://api.brightdata.com/datasets/v3/scrape?dataset_id=gd_lpfll7v5hcqtkxl6l&notify=false&include_errors=true&type=discover_new&discover_by=keyword&limit_per_input=5",
    headers=headers,
    data=data
)

print(response.json())


'''
import requests
import json

headers = {
    "Authorization": "Bearer 7f4c8e79-3a7c-4723-aaf4-9ff337659411",
    "Content-Type": "application/json",
}

data = json.dumps({
    "input": [{"location":"paris","keyword":"product manager","country":"FR","time_range":"Past month","job_type":"Full-time","experience_level":"Internship","remote":"On-site","company":"","location_radius":""},{"location":"New York","keyword":"\"python developer\"","experience_level":"Executive","country":"","time_range":"","job_type":"","remote":"","company":"","location_radius":""}],
})

response = requests.post(
    "https://api.brightdata.com/datasets/v3/scrape?dataset_id=gd_lpfll7v5hcqtkxl6l&notify=false&include_errors=true&type=discover_new&discover_by=keyword",
    headers=headers,
    data=data
)

print(response.json())'''