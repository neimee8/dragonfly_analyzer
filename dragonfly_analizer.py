import pandas as pd
import warnings
warnings.simplefilter("ignore", UserWarning)

from xlsx_data_validator import XlsxDataValidator
from dragonfly import Dragonfly

class DragonflyAnalyzer:
    def __init__(self, error_collector):
        self.error_collector = error_collector
        self.xlsx_validator = XlsxDataValidator(error_collector)
        self.analyzed_dragonflies = {}
        self.xlsx_file = None
        self.current_dragonfly = None
        self.xlsx_file_name = None
        self.error_template = lambda column, index: f"row {index} in {self.xlsx_file_name}: {column}"

    def set_file(self, file, sheet_name):
        try:
            self.xlsx_file = pd.read_excel(file, sheet_name=sheet_name)
            self.xlsx_file_name = file
            self.current_dragonfly = Dragonfly(file_name=file.name)
        except FileNotFoundError as error:
            self.error_collector.add(f"{self.__class__.__name__}: {error}", "FileNotFoundError")

    def analyze(self, columns, row_action):
        # Проверяем наличие файла
        if self.xlsx_file is None:
            self.error_collector.add(f"{self.__class__.__name__}: file don't set", "file-is-none-error")
            return
        # Проверяем что все нужные колонки на месте
        if not self.xlsx_validator.all_columns_correct(columns, self.xlsx_file.columns.tolist()):
            return

        year, square, temperature, cloudy, wind, water, shading, dragonfly_name = self.xlsx_file.columns.tolist()[:len(columns)]
        self.current_dragonfly.name = dragonfly_name
        for index, row in self.xlsx_file.iterrows():
            row_index = index + 2
            # Проверка что год валидный и больше 2018
            if self._check_year(row[year], row_index) == "invalid":
                return
            elif self._check_year(row[year], row_index) == "skip":
                continue

            # Проверки
            if not all([
                self._check_square(row[square], row_index),
                self._check_temperature(row[temperature], row_index),
                self._check_cloudy(row[cloudy], row_index),
                self._check_wind(row[wind], row_index),
                self._check_shading(row[shading], row_index, ["Dalejs", "Nav"]),
                self._check_count(row[dragonfly_name], row_index)
            ]):
                return

            # Проверяем что никакой далбоеб не проебал сука вторую букву s
            is_valid_water, fixed_water = self._check_water(row[water], row_index, ["Stavoss", "Tekoss"])
            if not is_valid_water:
                return

            row_action(row, self.current_dragonfly, dragonfly_name, year, square, temperature, cloudy, wind, fixed_water, shading)

        self.current_dragonfly.finalize()
        self.analyzed_dragonflies[self.current_dragonfly.name] = self.current_dragonfly

    def analyze_count(self, row, current_dragonfly, dragonfly_name, year, square, temperature, cloudy, wind, water, shading):
        # Количество вида за все года наблюдения на всех квадратах (2018 - 2024)
        current_dragonfly.add_count(row[dragonfly_name])
        # Количество вида за конкретный год на всех квадратах
        current_dragonfly.add_dict("count_by_year", row[year], row[dragonfly_name])
        # Количество вида за все года на конкретном квадрате
        current_dragonfly.add_dict("count_by_square", row[square], row[dragonfly_name])
        # Динамика изменения стрекоз по годам на квадратах
        current_dragonfly.add_list_with_dict("square_year_count", square=row[square], year=row[year], count=row[dragonfly_name])

    def analyze_temperature(self, row, current_dragonfly, dragonfly_name, year, square, temperature, cloudy, wind, water, shading):
        # Среднее арифметическое значение со всех квадрантов за весь год (какая в среднем была температура за весь 2018, весь 2019 и так далее)
        current_dragonfly.add_avg_source("avg_temp_by_year", row[year], row[temperature])
        # Температура на одном квадранте за все года (температура на квадранте номер 1 за 2018 год, за 2019 год и так далее)
        current_dragonfly.add_list_with_dict("square_year_temp", square=row[square], year=row[year], temperature=row[temperature])
        # Среднее арифметическое значение температуры за все года с одного квадранта
        current_dragonfly.add_avg_source("avg_temp_by_square", row[square], row[temperature])

    def analyze_wind(self, row, current_dragonfly, dragonfly_name, year, square, temperature, cloudy, wind, water, shading):
        # Среднее арифметическое значение со всех квадрантов за весь год (какая в среднем была ветренность за весь 2018, весь 2019 и так далее)
        current_dragonfly.add_avg_source("avg_wind_by_year", row[year], row[wind])
        # Ветренность на одном квадранте за все года (температура на квадранте номер 1 за 2018 год, за 2019 год и так далее)
        current_dragonfly.add_list_with_dict("square_year_wind", square=row[square], year=row[year], wind=row[wind])
        # Среднее арифметическое значение температуры за все года с одного квадранта
        current_dragonfly.add_avg_source("avg_wind_by_square", row[square], row[wind])

    def analyze_cloudy(self, row, current_dragonfly, dragonfly_name, year, square, temperature, cloudy, wind, water, shading):
        # Среднее арифметическое значение облачности за весь год со всех квадрантов
        current_dragonfly.add_avg_source("avg_cloudy_by_year", row[year], row[cloudy])
        # Значение облачности на одном и том же квадранте за каждый год наблюдений (конкретно за 2018, за 2019, за 2020 и т.д.)
        current_dragonfly.add_list_with_dict("square_year_cloudy", square=row[square], year=row[year], cloudy=row[cloudy])
        # Среднее арифметическое значение облачности на одном и том же квадранте за все года наблюдений (средняя облачность на квадранте 1 за все года наблюдений равняется 33 единицам, за 2019 - 57 единицам и т.д.)
        current_dragonfly.add_avg_source("avg_cloudy_by_square", row[square], row[cloudy])

    def analyze_water(self, row, current_dragonfly, dragonfly_name, year, square, temperature, cloudy, wind, fixed_water, shading):
        # Преобладающее состояние воды за весь год со всех квадрантов (в 2018 году на 25 из 30 квадрантов вода была текучая, а на 5 стоячая; в 2019 году на 15 квадрантах вода была текучая, на 15 стоячая и т.д.)
        current_dragonfly.add_dict_with_inner_key("year_water_types", row[year], fixed_water)
        # Состояние воды на одном квадранте за все года (на квадранте 1 в 2018 году вода была стоячая, в 2019 стоячая, в 2020 стоячая, а в 2021 текучая)
        current_dragonfly.add_list_with_dict("square_year_water", square=row[square], year=row[year], water=fixed_water)

    def analyze_shading(self, row, current_dragonfly, dragonfly_name, year, square, temperature, cloudy, wind, water, shading):
        # Преобладающее состояние затенения за весь год со всех квадрантов
        current_dragonfly.add_dict_with_inner_key("year_shading_types", row[year], row[shading])
        # Состояние затенения на одном квадранте за все года
        current_dragonfly.add_list_with_dict("square_year_shading", square=row[square], year=row[year], shading=row[shading])

    error_template = f""
    def _check_year(self, year, row_index):
        if not self.xlsx_validator.not_empty(year, addition_info=self.error_template("year", row_index)):
            return "invalid"
        if not self.xlsx_validator.is_numeric(year, addition_info=self.error_template("year", row_index)):
            return "invalid"
        if not self.xlsx_validator.is_greater_or_equal(year, 2018, log=False, addition_info=self.error_template("year", row_index)):
            return "skip"
        return "ok"

    def _check_square(self, square, row_index):
        return self._check_empty_and_numeric(square, "square", row_index)

    def _check_temperature(self, temperature, row_index):
        return self._check_empty_and_numeric(temperature, "temperature", row_index)

    def _check_cloudy(self, cloudy, row_index):
        return self._check_empty_and_numeric(cloudy, "cloudy", row_index)

    def _check_wind(self, wind, row_index):
        return self._check_empty_and_numeric(wind, "wind", row_index)

    def _check_count(self, count, row_index):
        return self._check_empty_and_numeric(count, "count", row_index)

    def _check_water(self, water, row_index, options):
        if self._check_match_any(water, "water", row_index, options, log_type=False):
           return True, water

        fixed_water = f"{water}s"
        if self._check_match_any(fixed_water, "water", row_index, options):
            return True, fixed_water
        return False, water

    def _check_shading(self, shading, row_index, options):
        return self._check_match_any(shading, "shading", row_index, options)

    def _check_match_any(self, value, value_name, row_index, options, log_type=True):
        return self.xlsx_validator.match_any(value, options, log=log_type, addition_info=self.error_template(value_name, row_index))

    def _check_empty_and_numeric(self, value, value_name, row_index, log_type=True):
        return (
                self.xlsx_validator.not_empty(value, log=log_type, addition_info=self.error_template(value_name, row_index)) and
                self.xlsx_validator.is_numeric(value, log=log_type, addition_info=self.error_template(value_name, row_index))
        )

