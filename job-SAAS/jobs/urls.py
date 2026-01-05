from django.urls import path 
from .views import search_job_view
urlpatterns = [ 
    path('search', search_job_view, name = 'Search')
]