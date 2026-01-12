from celery import shared_task
from .models import LLMResult, SnapShot
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
            SystemMessage(content = ''),
            HumanMessage(content=''+ data_string)
        ])

    except:
        pass


