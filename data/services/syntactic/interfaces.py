class BaseInterface:
    """ Base interface definition """
    def count_null_values(self):
        """
        Indicator of number of NULL values.
        """
        pass

    def count_distinct_values(self):
        """
        Indicator of number of distinct values.:
        """
        pass

    def count_unique_values(self):
        """
        Indicator of number of unique values.
        """
        pass

    def count_duplicated_values(self):
        """
        Indicator of number of duplicated values.
        """
        pass

    def compute_data_frequency(self):
        """
        Indicator of data frequecy.
        """
        pass

    def model_data_frequency(self):
        """
        Indicator of Model Data Frequency.
        """
        pass

    def count_boolean_type_values(self):
        """
        Indicator of Number of values of the BOOLEAN TYPE.
        """
        pass

    def count_null_type_values(self):
        """
        Indicator of Number of values of the NULL TYPE.
        """
        pass

    def count_the_different_values(self):
        """
        Indicator of Number of DIFFERENT values.
        """
        pass

    def count_syntactically_valid_values(self, invalid=False):
        """
        count the syntactically valid and invalid values.
        :param invalid:
        :return:
        """
        pass


class StringInterface(BaseInterface):
    """ String interface definition """
    def get_min_length(self):
        """
        Indicator of Min length.
        """
        pass

    def get_max_length(self):
        """
        Indicator of Max Length.
        """
        pass

    def get_average_length(self):
        """
        Average Length Indicator.
        """
        pass

    def count_number_of_words(self):
        """
        Indicator of number of words.
        """
        pass

    def count_values(self):
        """
        count the number of values of the STRING TYPE.
        """
        pass


class NumberInterface(BaseInterface):
    """ Number Interface definition"""
    def compute_min_value(self):
        """
        Min value indicator
        """
        pass

    def compute_max_value(self):
        """
        Max value indicator
        """
        pass

    def compute_average_value(self):
        """
        Average value indicator.
        """
        pass

    def compute_mode_value(self):
        """
        Mode value indicator.
        """
        pass

    def compute_median_value(self):
        """
        Median value indicator.
        """
        pass

    def count_values(self):
        """
        count the number of values of the NUMBER TYPE.
        """
        pass


class DateInterface(BaseInterface):
    """ Date Interface definition"""

    def check_format_for_dataframe(self, date_format='%m-%d-%Y'):
        """
        Indicator for the date and datetime format and for the weekday and the month.
        The date format can be :
                -MM DD YYYY
                -MM DD YY
                -DD MM YYYY (french date format)
                -DD MMM YYYY (french date format with the month in letters, exp:Jan, Feb)
                -YYYY MM DD (ISO date format)
        The datetime format can be :
                - hh:mm
                - mm/dd/yyyy hh:mm
                - mm/dd/yyyy hh:mm:ss
        The format for the month: %B or %b
        The format for weekday: %A or %a
        :param date_format:
        :return:
        """
        pass

    def count_values(self):
        """
        count the number of values of the DATE TYPE.
        """
        pass
