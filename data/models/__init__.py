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
M100_3 = {'rule': 'M100 [3]','signification': 'Number of NULL values'}
M101_4 = {'rule': 'M101 [4]', 'signification': 'Number of NOT NULL values'}
M102_5 = {'rule': 'M102 [5]', 'signification': 'Number of distinct values'}
M103_6 = {'rule': 'M103 [6]', 'signification': 'Number of unique values'}
M104_7 = {'rule': 'M104 [7]', 'signification': 'Number of duplicate values'}
M105_8 = {'rule': 'M105 [8]', 'signification': 'Number of Words'}
M106_9 = {'rule': 'M106 [9]', 'signification': 'Data Frequency (number of occurrences and percentages)'}
M107_10 = {'rule': 'M107 [10]', 'signification': 'Model Data Frequency'}
M108_11 = {'rule': 'M108 [11]', 'signification': 'Number of values of the STRING TYPE'}
M109_12 = {'rule': 'M109 [12]', 'signification': 'Number of values of the NUMBER TYPE'}
M110_13 = {'rule':'M110 [13]', 'signification': 'Number of values of the DATE TYPE'}
M111_14 = {'rule': 'M111 [14]', 'signification': 'Number of values of the BOOLEAN TYPE'}
M112_15 = {'rule': 'M112 [15]', 'signification': 'Number of values of the NULL TYPE'}
M102_17 = {'rule': 'M102 [17]', 'signification': 'Min length for string'}
M103_18 = {'rule': 'M103 [18]', 'signification': 'Max Length for string'}
M104_19 = {'rule': 'M104 [19]', 'signification': 'Average Length for string'}
M102_20 = {'rule': 'M102 [20]', 'signification': ' Min of numeric values'}
M103_20 = {'rule': 'M103 [20]', 'signification': 'Max of numeric values'}
M103_21 = {'rule': 'M103 [21]', 'signification': 'Average of numeric values'}
M104_22 = {'rule': 'M104 [22]', 'signification': 'Mode'}
M105_23 = {'rule': 'M105 [23]', 'signification': 'Median'}
M112 = {'rule': 'M112', 'signification': 'Date MM DD YYYY'}
M113 = {'rule': 'M113', 'signification': 'Date MM DD YY'}
M114 = {'rule': 'M114', 'signification': 'Date DD MMM YYYY'}
M115 = {'rule': 'M115', 'signification': 'French Date'}
M116 = {'rule': 'M116', 'signification': 'ISO Date'}
M117 = {'rule': 'M117', 'signification': '24 Hour Time'}
M118 = {'rule': 'M118', 'signification': 'DateTime mm/dd/yyyy hh:mm'}
M119 = {'rule': 'M119', 'signification': 'DateTime mm/dd/yyyy hh:mm:ss'}
M120 = {'rule': 'M120', 'signification': 'Month'}
M121 = {'rule': 'M121', 'signification': 'Week Day'}
M102_25 = {'rule': 'M102 [25]', 'signification': 'Number of valid values according to regexp'}
M102_26 = {'rule': 'M102 [26]', 'signification': 'Number of valid values according to the data dictionary'}
M103_25 = {'rule': 'M103 [25]', 'signification': 'Number of invalid values according to regexp'}
M103_26 = {'rule': 'M103 [26]', 'signification': 'Number of invalid values according to the data dictionary'}
DATA_TYPES = {'rule': 'Data-types', 'signification': 'Data types and their respectful percentages'}


# links between date type columns
AFTER = 'after'
BEFORE = 'before'
EQUALS = 'equals'
DATE_LINK_OPTIONS = (
    (AFTER, _('After')),
    (BEFORE, _('Before')),
    (EQUALS, _('Equals')))
