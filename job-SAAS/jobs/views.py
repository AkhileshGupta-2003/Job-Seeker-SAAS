from django.shortcuts import render
from .services import search_jobs_agent
from .models import LLMResult
from django.contrib.auth.decorators import login_required


@login_required
def search_job_view(request):
    context = {}
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        if prompt:
            try:
                llm_result= LLMResult(
                    title = 'New Job Search',
                    prompt = prompt,
                    status= 'pending',
                    owner = request.user
                )
                llm_result.save()
                result = search_jobs_agent(llm_result.id, prompt)
                context['result'] = result
                context['prompt'] = prompt
            except Exception as e:
                context['error'] = str(e)
    return render(request, 'search.html', context)