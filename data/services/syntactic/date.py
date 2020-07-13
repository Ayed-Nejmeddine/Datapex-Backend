from data.services.syntactic.interfaces import DateInterface
import pandas as pd
from data.services.syntactic.utils import check_format_for_dataframe


class DateAbstract(DateInterface):
    """ contains services for DateInterface """

    def compute_first_date_format(self, file):
        """ first format = MM/DD/YYYY or MM-DD-YYYY"""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            res_dash = check_format_for_dataframe(df=df, format='%m-%d-%Y')
            res_slash = check_format_for_dataframe(df=df, format='%m/%d/%Y')
        return res_dash + res_slash

    def compute_second_date_format(self, file):
        """ second format = MM/DD/YY or MM-DD-YY"""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            res_dash = check_format_for_dataframe(df=df, format='%m-%d-%y')
            res_slash = check_format_for_dataframe(df=df, format='%m/%d/%y')
        return res_dash + res_slash

    def compute_third_date_format(self, file):
        """ third format = DD MMM YYYY"""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            res = check_format_for_dataframe(df=df, format='%d %b %Y')
        return res

    def compute_french_date_format(self, file):
        """ french date format =  DD/MM/YYYY or DD-MM-YYYY"""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            res_dash = check_format_for_dataframe(df=df, format='%d-%m-%Y')
            res_slash = check_format_for_dataframe(df=df, format='%d/%m/%Y')
        return res_dash + res_slash

    def compute_iso_date_format(self, file):
        """ iso date format = YYYY-MM-DD or YYYY/MM/DD"""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            res_dash = check_format_for_dataframe(df=df, format='%Y-%m-%d')
            res_slash = check_format_for_dataframe(df=df, format='%Y/%m/%d')
        return res_dash + res_slash
