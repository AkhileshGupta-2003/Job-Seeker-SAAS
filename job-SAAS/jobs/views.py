from django.shortcuts import render
from .services import search_jobs_agent


def search_job_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        result = search_jobs_agent(prompt)
        return render(request, 'jobs/results.html', {'result' : result})
    else:
        return render(request, 'jobs/search.html')

# Create your views here.
