"""Define models module and used variables"""
from django.utils.translation import ugettext_lazy as _

# analysis trace states options:
RUNNING_STATE = 'running'
FINISHED_STATE = 'finished'
FAILED_STATE = 'failed'

ANALYSIS_TRACE_STATES = (
    (RUNNING_STATE, _('Running')),
    (FINISHED_STATE, _('Finished')),
    (FAILED_STATE, _('Failed')))

# analysis types
BASIC_ANALYSIS = 'basic'
STRING_ANALYSIS = 'string'
NUMBER_ANALYSIS = 'number'
DATE_ANALYSIS = 'date'

ANALYSIS_TYPES = (
    (BASIC_ANALYSIS, _('Basic-Analysis')),
    (STRING_ANALYSIS, _('String-Analysis')),
    (NUMBER_ANALYSIS, _('Number-Analysis')),
    (DATE_ANALYSIS, _('Date-Analysis')))