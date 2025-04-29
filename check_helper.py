from xlsx_data_validator import XlsxDataValidator

class CheckHelper:
    def __init__(self, error_collector):
        self.error_collector = error_collector
        self.error_template = lambda column, index: f"row {index} in {self.xlsx_file_name}: {column}"
        self.xlsx_validator = XlsxDataValidator(error_collector)
        self.xlsx_file_name = None

    def check_year(self, year, row_index):
        if not self.xlsx_validator.not_empty(year, addition_info=self.error_template("year", row_index)):
            return "invalid"
        if not self.xlsx_validator.is_numeric(year, addition_info=self.error_template("year", row_index)):
            return "invalid"
        if not self.xlsx_validator.is_greater_or_equal(year, 2018, log=False, addition_info=self.error_template("year", row_index)):
            return "skip"
        return "ok"

    def check_square(self, square, row_index):
        return self._check_data_and_numeric(square, "square", row_index)

    def check_temperature(self, temperature, row_index):
        return self._check_data_and_numeric(temperature, "temperature", row_index)

    def check_clouds(self, clouds, row_index):
        return self._check_data_and_numeric(clouds, "clouds", row_index)

    def check_wind(self, wind, row_index):
        return self._check_data_and_numeric(wind, "wind", row_index)

    def check_count(self, count, row_index):
        return self._check_data_and_numeric(count, "count", row_index)

    def check_water(self, water, row_index, options):
        if self._check_match_any(water, "water", row_index, options, log_type=False):
            return water

        fixed_water = f"{water}s"
        if self._check_match_any(fixed_water, "water", row_index, options):
            return fixed_water
        return water

    def check_shading(self, shading, row_index, options):
        return self._check_match_any(shading, "shading", row_index, options)

    def _check_match_any(self, value, value_name, row_index, options, log_type=True):
        return self.xlsx_validator.match_any(value, options, log=log_type, addition_info=self.error_template(value_name, row_index))

    def _check_data_and_numeric(self, value, value_name, row_index, log_type=True):
        return (
                self.xlsx_validator.is_data(value, log=log_type, addition_info=self.error_template(value_name, row_index)) and
                self.xlsx_validator.is_numeric(value, log=log_type, addition_info=self.error_template(value_name, row_index))
        )

