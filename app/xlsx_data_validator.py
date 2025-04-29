import numbers
import pandas as pd

class XlsxDataValidator:
    ERROR_TYPE = "validation"
    def __init__(self, error_collector):
        # Expect ErrorCollector object
        self.error_collector = error_collector

    def all_columns_correct(self, correct_columns, columns_from_excel, log=True, addition_info=""):
        return self._validate(correct_columns == columns_from_excel[:len(correct_columns)], f"{self.__class__.__name__}: {correct_columns} not equal {columns_from_excel}, additional info: {addition_info}", log)

    def is_greater_or_equal(self, value, comparison, log=True, addition_info=""):
        return self._validate(value >= comparison, f"{self.__class__.__name__}: '{value}' < '{comparison}', additional info: {addition_info}", log)

    def not_empty(self, value, log=True, addition_info=""):
        return self._validate(not pd.isna(value), f"{self.__class__.__name__}: '{value}' is none, additional: info {addition_info}", log)

    def is_data(self, value, log=True, addition_info=""):
        return self._validate(not value == "NO DATA", f"{self.__class__.__name__}: 'WARNING: none cell was changed to {value}', additional: info {addition_info}", log)
        
    def is_numeric(self, value, log=True, addition_info=""):
        return self._validate(isinstance(value, numbers.Number), f"{self.__class__.__name__}: '{value}' is not numeric, additional: info {addition_info}", log)

    def match_any(self, value, collection, log=True, addition_info=""):
        return self._validate(value in collection, f"{self.__class__.__name__}: '{value}' not in {collection}, additional info: {addition_info}", log)

    def _log(self, message):
        self.error_collector.add(message, self.ERROR_TYPE)

    def _validate(self, condition, message, log):
        if condition:
            return True
        if log:
            self._log(message)
        return False
