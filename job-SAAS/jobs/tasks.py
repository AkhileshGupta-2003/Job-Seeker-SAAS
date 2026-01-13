from celery import shared_task
from .models import LLMResult, SnapShot, JoblistingResult
from .services import get_data
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage
from .llm_schemas import Joblistings

@shared_task
def process_snapshot_and_summarise(llm_result_id):
    try:
        llm_result = LLMResult.objects.get(id = llm_result_id)
        llm_result.status = 'processing'
        llm_result.save()

        snapshots = SnapShot.objects.get(llm_result_id = llm_result_id)
        data_string = ""
        for snapshot in snapshots:
            snapshot.data = get_data(snapshot.snapshot_id)
            snapshot.save()
            data_string += str(snapshot.data)
            data_string += '\n'
        chat_model = init_chat_model('gpt-4o-mini')
        structured_chat = chat_model.with_structured_output(Joblistings)
        result = structured_chat.invoke([
            SystemMessage(content = 'You are helpful assistant that extracts job listings from the provided data. Please provide the output in the specified structured format.'),
            HumanMessage(content='Summarize the following job Search results'+ data_string)
        ])

        for job_listing in result.listings:
            job_listing_result = JoblistingResult(
                llm_result = llm_result,
                title = job_listing.title,
                job_url = job_listing.job_url,
                job_type = job_listing.job_type,
                level = job_listing.level,
                salary = job_listing.salary,
                summary = job_listing.summary,
                location = job_listing.location,
                posted = job_listing.posted,
                applicants = job_listing.applicants
            )
            job_listing_result.save()
            llm_result.status = 'completed'
            llm_result.save()
            return f"Succesfully processed and summarised the LLM Result with id : {llm_result_id}"
    except Exception as e:
        print(str(e))
        raise


