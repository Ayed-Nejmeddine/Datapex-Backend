import pandas as pd
from data.services.syntactic.abstracts import BaseAbstract
from data.services.syntactic.string import StringAnalyser
from data.services.syntactic.number import NumberAnalyser
from data.services.syntactic.date import DateAnalyser


class Analyser(BaseAbstract):

    def __init__(self, file):
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            self.df = df.convert_dtypes()
        self.string_analyser = StringAnalyser(df)
        self.number_analyser = NumberAnalyser(df)
        self.date_analyser = DateAnalyser(df)
