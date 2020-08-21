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

# rules:
M100_3 = 'M100 [3]'  # Number of NULL values
M101_4 = 'M101 [4]'  # Number of NOT NULL values
M102_5 = 'M102 [5]'  # Number of distinct values
M103_6 = 'M103 [6]'  # Number of unique values
M104_7 = 'M104 [7]'  # Number of duplicate values
M105_8 = 'M105 [8]'  # Number of Words
M106_9 = 'M106 [9]'  # Data Frequency
M107_10 = 'M107 [10]'  # Model Data Frequency
M108_11 = 'M108 [11]'  # Number of values of the STRING TYPE
M109_12 = 'M109 [12]'  # Number of values of the NUMBER TYPE
M110_13 = 'M110 [13]'  # Number of values of the DATE TYPE
M111_14 = 'M111 [14]'  # Number of values of the BOOLEAN TYPE
M112_15 = 'M112 [15]'  # Number of values of the NULL TYPE
M102_17 = 'M102 [17]'  # Min length for string
M103_18 = 'M103 [18]'  # Max Length for string
M104_19 = 'M104 [19]'  # Average Length for string
M102_20 = 'M102 [20]'  # Min of numeric values
M103_20 = 'M103 [20]'  # Max of numeric values
M103_21 = 'M103 [21]'  # Average of numeric values
M104_22 = 'M104 [22]'  # Mode
M105_23 = 'M105 [23]'  # Median
M112 = 'M112'  # Date MM DD YYYY
M113 = 'M113'  # Date MM DD YY
M114 = 'M114'  # Date DD MMM YYYY
M115 = 'M115'  # French Date
M116 = 'M116'  # ISO Date
M117 = 'M117'  # 24 Hour Time
M118 = 'M118'  # DateTime mm/dd/yyyy hh:mm
M119 = 'M119'  # DateTime mm/dd/yyyy hh:mm:ss
M120 = 'M120'  # Month
M121 = 'M121'  # Week Day
M102_25 = 'M102 [25]'  # Number of valid values according to regexp.
M102_26 = 'M102 [26]'  # Number of valid values according to the data dictionary.
M103_25 = 'M103 [25]'  # Number of invalid values according to regexp.
M103_26 = 'M103 [26]'  # Number of invalid values according to the data dictionary.
