from xlsx_data_validator import XlsxDataValidator

class Dragonfly:
    def __init__(self, error_collector, file_name, dragonfly_name="Unnamed"):
        self.name = dragonfly_name
        self.total_count = 0
        self.file_name = file_name
        self.finalized_avg_keys = set()
        self.xlsx_validator = XlsxDataValidator(error_collector)

    def add_count(self, count):
        if self.xlsx_validator.is_data(count, log=False) and self.xlsx_validator.is_numeric(count, log=False):
            self.total_count += count

    def add_dict(self, dict_name, key, value):
        specific_dict = self._init_data_structure(dict_name, dict)
        value = 0 if (not self.xlsx_validator.is_data(value, log=False) and not self.xlsx_validator.is_numeric(value, log=False)) else value

        if key not in specific_dict:
            specific_dict[key] = value
        else:
            specific_dict[key] += value

    def add_list_with_dict(self, list_name, **attributes):
        specific_list = self._init_data_structure(list_name, list)
        specific_list.append(attributes)

    def add_dict_with_inner_key(self, dict_name, general_key, inner_key):
        specific_dict = self._init_data_structure(dict_name, dict)

        if general_key not in specific_dict:
            specific_dict[general_key] = {}

        if inner_key not in specific_dict[general_key]:
            specific_dict[general_key][inner_key] = 1
        else:
            specific_dict[general_key][inner_key] += 1

    def add_avg_source(self, dict_name, key, value):
        specific_dict = self._init_data_structure(dict_name, dict)
        value = 0 if (not self.xlsx_validator.is_data(value, log=False) and not self.xlsx_validator.is_numeric(value, log=False)) else value

        if key not in specific_dict:
            specific_dict[key] = [0, 0]

        specific_dict[key][0] += value
        specific_dict[key][1] += 1

    def finalize(self):
        for attr_name in dir(self):
            if attr_name.startswith("avg") and attr_name not in self.finalized_avg_keys:
                original = getattr(self, attr_name)
                for key in original:
                    original[key] = self._find_avg(original[key][0], original[key][1])
                self.finalized_avg_keys.add(attr_name)

    def _init_data_structure(self, name, typ):
        if not hasattr(self, name):
            setattr(self, name, typ())
        return getattr(self, name)

    def _find_avg(self, value, value_count):
        return round(float(value) / value_count, 2)
