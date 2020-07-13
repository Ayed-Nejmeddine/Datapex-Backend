class BaseInterface:
    """ Base interface definition """
    def compute_null_values(self, file):
        """
        Indicator of number of NULL values.
        :param file:
        :return:
        """
        pass

    def compute_not_null_values(self, file):
        """
        Indicator of number of NOT NULL values.
        :param file:
        :return:
        """
        pass

    def compute_distinct_values(self, file):
        """
        Indicator of number of distinct values.
        :param file:
        :return:
        """
        pass

    def compute_unique_values(self, file):
        """
        Indicator of number of unique values.
        :param file:
        :return:
        """
        pass

    def compute_duplicated_values(self, file):
        """
        Indicator of number of duplicated values.
        :param file:
        :return:
        """
        pass

    def compute_number_of_words(self, file):
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

    def compute_model_data_frequency(self, file):
        """
        Indicator of Model Data Frequency.
        :param file:
        :return:
        """
        pass

    def compute_number_of_string_type_values(self, file):
        """
        Indicator of Number of values of the STRING TYPE.
        :param file:
        :return:
        """
        pass

    def compute_number_of_number_type_values(self, file):
        """
        Indicator of Number of values of the NUMBER TYPE.
        :param file:
        :return:
        """
        pass

    def compute_number_of_date_type_values(self, file):
        """
        Indicator of Number of values of the DATE TYPE.
        :param file:
        :return:
        """
        pass

    def compute_number_of_boolean_type_values(self, file):
        """
        Indicator of Number of values of the BOOLEAN TYPE.
        :param file:
        :return:
        """
        pass

    def compute_number_of_null_type_values(self, file):
        """
        Indicator of Number of values of the NULL TYPE.
        :param file:
        :return:
        """
        pass

    def compute_number_of_different_values(self, file):
        """
        Indicator of Number of DIFFERENT values.
        :param file:
        :return:
        """
        pass


class StringInterface(BaseInterface):
    """ String interface definition """
    def compute_min_length(self, file):
        """
        Indicator of Min length.
        :param file:
        :return:
        """
        pass

    def compute_max_length(self, file):
        """
        Indicator of Max Length.
        :param file:
        :return:
        """
        pass

    def compute_average_length(self, file):
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
    def compute_first_date_format(self, file):
        """
        compute date format  MM DD YYYY
        :param file:
        :return:
        """
        pass

    def compute_second_date_format(self, file):
        """
        compute date format  MM DD YY
        :param file:
        :return:
        """
        pass

    def compute_third_date_format(self, file):
        """
        compute date format DD MMM YYYY
        :param file:
        :return:
        """
        pass

    def compute_french_date_format(self, file):
        """
        compute date format DD MM YYYY
        :param file:
        :return:
        """
        pass

    def compute_iso_date_format(self, file):
        """
        compute ISO date format YYYY MM DD
        :param file:
        :return:
        """
        pass

    def compute_24_hour_time(self, file):
        """
        compute 24 Hour Time.
        :param file:
        :return:
        """
        pass

    def compute_first_datetime_format(self, file):
        """
        compute instances of the following dateTime format: mm/dd/yyyy hh:mm
        :param file:
        :return:
        """
        pass

    def compute_second_datetime_format(self, file):
        """
        compute the following dateTime format: mm/dd/yyyy hh:mm:ss
        :param file:
        :return:
        """
        pass

    def compute_month(self, file):
        """
        Month Indicator.
        :param file:
        :return:
        """
        pass

    def compute_weekday(self, file):
        """
        Week Day Indicator.
        :param file:
        :return:
        """
        pass
