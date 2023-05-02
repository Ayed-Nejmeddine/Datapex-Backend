"""Define models module and used variables"""
from django.utils.translation import gettext_lazy as _

# analysis trace states options:
RUNNING_STATE = "running"
FINISHED_STATE = "finished"
FAILED_STATE = "failed"

ANALYSIS_TRACE_STATES = (
    (RUNNING_STATE, _("Running")),
    (FINISHED_STATE, _("Finished")),
    (FAILED_STATE, _("Failed")),
)

# analysis types
BASIC_ANALYSIS = "basic"
STRING_ANALYSIS = "string"
NUMBER_ANALYSIS = "number"
BOOLEAN_ANALYSIS = "boolean"
DATE_ANALYSIS = "date"


ANALYSIS_TYPES = (
    (BASIC_ANALYSIS, _("Basic-Analysis")),
    (STRING_ANALYSIS, _("String-Analysis")),
    (NUMBER_ANALYSIS, _("Number-Analysis")),
    (BOOLEAN_ANALYSIS, _("Boolean-Analysis")),
    (DATE_ANALYSIS, _("Date-Analysis")),
)

# rules for the syntactic analysis:
M100_3 = {"rule": "M100 [3]", "signification": "Number of NULL values"}
M101_4 = {"rule": "M101 [4]", "signification": "Number of NOT NULL values"}
M102_5 = {"rule": "M102 [5]", "signification": "Number of distinct values"}
M103_6 = {"rule": "M103 [6]", "signification": "Number of unique values"}
M103_8 = {"rule": "M103 [8]", "signification": "Number of values in the dataset"}
M103_7 = {"rule": "M103 [7]", "signification": "Number of different values"}
M104_7 = {"rule": "M104 [7]", "signification": "Number of duplicate values"}
M105_8 = {"rule": "M105 [8]", "signification": "Number of Words"}
M106_9 = {
    "rule": "M106 [9]",
    "signification": "Data Frequency (number of occurrences and percentages)",
}
M107_10 = {"rule": "M107 [10]", "signification": "Model Data Frequency"}
M108_11 = {"rule": "M108 [11]", "signification": "Number of values of the STRING TYPE"}
M109_12 = {"rule": "M109 [12]", "signification": "Number of values of the NUMBER TYPE"}
M110_13 = {"rule": "M110 [13]", "signification": "Number of values of the DATE TYPE"}
M111_14 = {"rule": "M111 [14]", "signification": "Number of values of the BOOLEAN TYPE"}
M111_12 = {"rule": "M111 [12]", "signification": "Number of true and false values of the BOOLEAN TYPE"}
M112_15 = {"rule": "M112 [15]", "signification": "Number of values of the NULL TYPE"}
M113_16 = {"rule": "M113 [16]", "signification": "Number of rows"}
M114_17 = {"rule": "M114 [17]", "signification": "Number of data type"}
M115_18 = {"rule": "M115 [18]", "signification": "Number of lowercase values"}
M102_17 = {"rule": "M102 [17]", "signification": "Min length for string"}
M103_18 = {"rule": "M103 [18]", "signification": "Max Length for string"}
M104_19 = {"rule": "M104 [19]", "signification": "Average Length for string"}
M104_20 = {"rule": "M104 [20]", "signification": "Number of uppercase values"}
M104_21 = {"rule": "M104 [20]", "signification": "Number of Mixcasse values"}
M105_20 = {"rule": "M105 [20]", "signification": "Frequency Table"}
M102_20 = {"rule": "M102 [20]", "signification": " Min of numeric values"}
M103_20 = {"rule": "M103 [20]", "signification": "Max of numeric values"}
M103_21 = {"rule": "M103 [21]", "signification": "Average of numeric values"}
M104_22 = {"rule": "M104 [22]", "signification": "Mode"}
M105_23 = {"rule": "M105 [23]", "signification": "Median"}
M112 = {"rule": "M112", "signification": "Date MM DD YYYY"}
M113 = {"rule": "M113", "signification": "Date MM DD YY"}
M114 = {"rule": "M114", "signification": "Date DD MMM YYYY"}
M115 = {"rule": "M115", "signification": "French Date"}
M116 = {"rule": "M116", "signification": "ISO Date"}
M117 = {"rule": "M117", "signification": "24 Hour Time"}
M118 = {"rule": "M118", "signification": "DateTime mm/dd/yyyy hh:mm"}
M119 = {"rule": "M119", "signification": "DateTime mm/dd/yyyy hh:mm:ss"}
M120 = {"rule": "M120", "signification": "Month"}
M121 = {"rule": "M121", "signification": "Week Day"}
M102_25 = {"rule": "M102 [25]", "signification": "Number of valid values according to regexp"}
M102_26 = {
    "rule": "M102 [26]",
    "signification": "Number of valid values according to the data dictionary",
}
M103_25 = {"rule": "M103 [25]", "signification": "Number of invalid values according to regexp"}
M103_26 = {
    "rule": "M103 [26]",
    "signification": "Number of invalid values according to the data dictionary",
}
M130_1 = {"rule": "M130 [1]", "signification": "Number of columns"}
M130_2 = {"rule": "M130 [2]", "signification": "values length"}
M130_3 = {"rule": "M130 [3]", "signification": "Number of CapCase values"}


DATA_TYPES = {"rule": "Data-types", "signification": "Data types and their respectful percentages"}
TOTAL = {"rule": "Total", "signification": "Total number of values(NULL values and NOT NULL values"}
MATCHED_EXPRESSIONS = {
    "rule": "Matched-regexp",
    "signification": "Matched regular expressions and their respectful percentages",
}
COLUMN_TYPE = {"rule": "Column-type", "signification": "An estimate of the column type"}
# rules for the semantic analysis:
M101_1 = {"rule": "M101 [1]", "signification": "Number of categories in each column"}
M102_2 = {"rule": "M102 [2]", "signification": "Number of subcategories in each column"}
M103_3 = {
    "rule": "M103 [3]",
    "signification": "Number of semantically valid values according to the dominant category",
}
M104_4 = {
    "rule": "M104 [4]",
    "signification": "Number of semantically invalid values according to the dominant category",
}
M105_5 = {
    "rule": "M105 [5]",
    "signification": "Number of "
    "semantically valid "
    "values according to the dominant subcategory",
}
M106_6 = {
    "rule": "M106 [6]",
    "signification": "Number of "
    "semantically invalid"
    " values according to the"
    " dominant subcategory",
}

# links between date type columns

AFTER = "after"
BEFORE = "before"
EQUALS = "equals"
DATE_LINK_OPTIONS = ((AFTER, _("After")), (BEFORE, _("Before")), (EQUALS, _("Equals")))

# links between numeric type columns
GREATER_THAN = "greater-than"
LESS_THAN = "less-then"
NUMERIC_LINK_OPTIONS = (
    (GREATER_THAN, _("Greater-than")),
    (LESS_THAN, _("Less-then")),
    (EQUALS, _("Equals")),
)

# Language choices
FRENCH = "fr"
ENGLISH = "en"
LANGUAGE_OPTIONS = (
    (FRENCH, _("French")),
    (ENGLISH, _("English")),
)

# Dictionnaire de translation des jours respectivement dans
# les langues:English, Frensh, Spanish, Portuguese, Indonesian, German, Italian
DAYS_TRANSLATOR = {
    "MONDAY": ("monday", "lundi", "lunes", "segunda-feira", "senin", "montag", "lunedi"),
    "TUESDAY": ("tuesday", "mardi", "martes", "terca-feira", "selasa", "dienstag", "martedi"),
    "WEDNESDAY": (
        "wednesday",
        "mercredi",
        "mircoles",
        "quarta-feira",
        "rabu",
        "mittwoch",
        "mercoledi",
    ),
    "THURSDAY": ("thursday", "jeudi", "juves", "quinta-feira", "kamis", "donnerstag", "giovedi"),
    "FRIDAY": ("friday", "vendredi", "viernes", "sexta-feira", "jumat", "freitag", "venerdi"),
    "SATURDAY": ("saturday", "samedi", "sabado", "sabado", "sabtu", "samstag", "sabato"),
    "SUNDAY": ("sunday", "dimanche", "domingo", "domingo", "minggu", "sonntag", "domenica"),
}

# Dictionnaire de translation des mois respectivement dans
# les langues:English, Frensh, Spanish, Portuguese, Indonesian, German, Italian
MONTHS_TRANSLATOR = {
    "JANUARY": ("january", "janvier", "enero", "janeiro", "Januari", "Januar", "gennaio"),
    "FEBRUARY": ("february", "février", "febrero", "fevereiro", "februari", "februar", "febbraio"),
    "MARCH": ("march", "mars", "marzo", "março", "maret", "märz", "marzo"),
    "APRIL": ("april", "avril", "abril", "abril", "april", "april", "aprile"),
    "MAY": ("may", "mai", "mayo", "maio", "mei", "mai", "maggio"),
    "JUNE": ("june", "juin", "junio", "junho", "juni", "juni", "giugno"),
    "JULY": ("july", "juillet", "julio", "julho", "juli", "juli", "luglio"),
    "AUGUST": ("august", "août", "agosto", "agosto", "agustus", "august", "agosto"),
    "SEPTEMBER": (
        "september",
        "septembre",
        "septiembre",
        "setembro",
        "september",
        "september",
        "settembre",
    ),
    "OCTOBER": ("october", "octobre", "octubre", "outubro", "oktober", "oktober", "ottobre"),
    "NOVEMBER": (
        "november",
        "novembre",
        "noviembre",
        "novembro",
        "november",
        "november",
        "novembre",
    ),
    "DECEMBER": (
        "december",
        "décembre",
        "diciembre",
        "dezembro",
        "desember",
        "dezember",
        "dicembre",
    ),
}
