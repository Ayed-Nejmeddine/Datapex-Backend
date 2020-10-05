from data.models import RUNNING_STATE
from data.models.basic_models import AnalysisTrace, Document
from data.services.syntactic import Analyser
from background_task import background
from django.utils import timezone


@background(schedule=timezone.now())
def trace_threads():
    """
    Check if there is an unfinished syntactic analysis thread that hasn't finished running or was interrupted
    """
    interrupted_analysis = AnalysisTrace.objects.filter(state=RUNNING_STATE).values('document', 'analysis_type').distinct()
    for i in interrupted_analysis:
        analyser = Analyser(document=Document.objects.get(id=i['document']))
        if i['analysis_type'] == 'basic':
            analyser.start()
        elif i['analysis_type'] == 'string':
            analyser.string_analyser.start()
        elif i['analysis_type'] == 'number':
            analyser.number_analyser.start()
        elif i['analysis_type'] == 'date':
            analyser.date_analyser.start()
