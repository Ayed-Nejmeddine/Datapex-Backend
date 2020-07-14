class BaseInterface:
    """ Base interface definition """
    def count_null_values(self, file):
        """
        Indicator of number of NULL values.
        :param file:
        :return:
        """
        pass

    def count_distinct_values(self, file):
        """
        Indicator of number of distinct values.
        :param file:
        :return:
        """
        pass

    def count_unique_values(self, file):
        """
        Indicator of number of unique values.
        :param file:
        :return:
        """
        pass

    def count_duplicated_values(self, file):
        """
        Indicator of number of duplicated values.
        :param file:
        :return:
        """
        pass

    def count_number_of_words(self, file):
        """
        Indicator of number of words.
        :param file:
        :return:
        """
        pass

    def compute_data_frequency(self, file):
        """
        Indicator of data frequecy.
        :param file:
        :return:
        """
        pass

    def model_data_frequency(self, file):
        """
        Indicator of Model Data Frequency.
        :param file:
        :return:
        """
        pass

    def count_string_type_values(self, file):
        """
        Indicator of Number of values of the STRING TYPE.
        :param file:
        :return:
        """
        pass

    def count_numeric_values(self, file):
        """
        Indicator of Number of values of the NUMBER TYPE.
        :param file:
        :return:
        """
        pass

    def count_date_type_values(self, file):
        """
        Indicator of Number of values of the DATE TYPE.
        :param file:
        :return:
        """
        pass

    def count_boolean_type_values(self, file):
        """
        Indicator of Number of values of the BOOLEAN TYPE.
        :param file:
        :return:
        """
        pass

    def count_null_type_values(self, file):
        """
        Indicator of Number of values of the NULL TYPE.
        :param file:
        :return:
        """
        pass

    def count_the_different_values(self, file):
        """
        Indicator of Number of DIFFERENT values.
        :param file:
        :return:
        """
        pass


class StringInterface(BaseInterface):
    """ String interface definition """
    def get_min_length(self, file):
        """
        Indicator of Min length.
        :param file:
        :return:
        """
        pass

    def get_max_length(self, file):
        """
        Indicator of Max Length.
        :param file:
        :return:
        """
        pass

    def get_average_length(self, file):
        """
        Average Length Indicator.
        :param file:
        :return:
        """
        pass


class NumberInterface(BaseInterface):
    """ Number Interface definition"""
    def compute_min_value(self, file):
        """
        Min value indicator
        :param file:
        :return:
        """
        pass

    def compute_max_value(self, file):
        """
        Max value indicator
        :param file:
        :return:
        """
        pass

    def compute_average_value(self, file):
        """
        Average value indicator.
        :param file:
        :return:
        """
        pass

    def compute_mode_value(self, file):
        """
        Mode value indicator.
        :param file:
        :return:
        """
        pass

    def compute_median_value(self, file):
        """
        Median value indicator.
        :param file:
        :return:
        """
        pass


class DateInterface(BaseInterface):
    """ Date Interface definition"""

    def check_format_for_dataframe(self, file, format='%m-%d-%Y'):
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
        :param file:
        :param format:
        :return:
        """
        pass
