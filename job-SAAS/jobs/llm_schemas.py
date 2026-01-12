from typing import Optional
from pydantic import BaseModel, Field

class JobListing(BaseModel):
    title:str = Field(..., description='')
    job_url:str = Field(..., description = '')
    job_type :Optional[str]= Field(...,description='')
    level:Optional[str]= Field(..., description= '')
    summary : Optional[str] = Field(..., Description = '')
    posted : Optional[str] = Field(..., Description ='')
    applicants : Optional[int]= Field(..., Description = '')



class Joblistings(BaseModel):
    list[JobListing] 