import pandas as pd
import warnings

from app.xlsx_data_validator import XlsxDataValidator
from app.dragonfly import Dragonfly
from app.check_helper import CheckHelper
from app.structures.hash_table import HashTable

warnings.simplefilter("ignore", UserWarning)

class DragonflyAnalyzer:
    def __init__(self, error_collector):
        self.error_collector = error_collector
        self.xlsx_validator = XlsxDataValidator(error_collector)
        self.check_helper = CheckHelper(error_collector)

        self.analyzed_dragonflies = HashTable()
        self.xlsx_file = None
        self.current_dragonfly = None
        self.xlsx_file_name = None

    def set_file(self, file, sheet_name):
        try:
            self.xlsx_file = pd.read_excel(file, sheet_name=sheet_name)
            self.xlsx_file_name = file
            self.current_dragonfly = Dragonfly(error_collector=self.error_collector, file_name=file.name)
            self.check_helper.xlsx_file_name = file
        except FileNotFoundError as error:
            self.error_collector.add(f"{self.__class__.__name__}: {error}", "FileNotFoundError")

    def analyze(self, columns, row_action):
        # Check file existence
        if self.xlsx_file is None:
            self.error_collector.add(f"{self.__class__.__name__}: file not set", "file-is-none-error")
            return
        # Check if all required columns are present
        if not self.xlsx_validator.all_columns_correct(columns, self.xlsx_file.columns.tolist()):
            return

        year, square, temperature, clouds, wind, water, shading, dragonfly_name = self.xlsx_file.columns.tolist()[:len(columns)]
        self.current_dragonfly.name = dragonfly_name
        for index, row in self.xlsx_file.iterrows():
            row_index = index + 2
            # Check if year is empty or < 2018
            if self.check_helper.check_year(row[year], row_index) == "invalid":
                return
            elif self.check_helper.check_year(row[year], row_index) == "skip":
                continue

            # Fill empty cells with "NO DATA". "NO DATA" cells are considered warnings, not critical errors
            row = row.fillna('NO DATA')

            # Validation checks. Don't stop program execution, just log information for debugging
            self.check_helper.check_square(row[square], row_index),
            self.check_helper.check_temperature(row[temperature], row_index),
            self.check_helper.check_clouds(row[clouds], row_index),
            self.check_helper.check_wind(row[wind], row_index),
            self.check_helper.check_shading(row[shading], row_index, ["Dalejs", "Nav"]),
            self.check_helper.check_count(row[dragonfly_name], row_index)

            # Check if water type is missing "s" at the end and fix if necessary
            fixed_water = self.check_helper.check_water(row[water], row_index, ["Stavoss", "Tekoss"])

            row_action(row, self.current_dragonfly, dragonfly_name, year, square, temperature, clouds, wind, fixed_water, shading)

        self.current_dragonfly.finalize()
        self.analyzed_dragonflies[self.current_dragonfly.name] = self.current_dragonfly

    def analyze_count(self, row, current_dragonfly, dragonfly_name, year, square, temperature, clouds, wind, water, shading):
        # Total species count across all years and all squares (2018–2024)
        current_dragonfly.add_count(row[dragonfly_name])
        # Species count for a specific year across all squares
        current_dragonfly.add_dict("count_by_year", row[year], row[dragonfly_name])
        # Species count for a specific square across all years
        current_dragonfly.add_dict("count_by_square", row[square], row[dragonfly_name])
        # Dynamics of count changes across all years
        current_dragonfly.add_list_with_dict("square_year_count", square=row[square], year=row[year], count=row[dragonfly_name])

    def analyze_temperature(self, row, current_dragonfly, dragonfly_name, year, square, temperature, clouds, wind, water, shading):
        # Average temperature across all squares for each year (e.g., average temperature for 2018, 2019, etc.)
        current_dragonfly.add_avg_source("avg_temp_by_year", row[year], row[temperature])
        # Temperature at a specific square across all years (e.g., temperature at square 1 for 2018, 2019, etc.)
        current_dragonfly.add_list_with_dict("square_year_temp", square=row[square], year=row[year], temperature=row[temperature])
        # Average temperature across all years for a specific square
        current_dragonfly.add_avg_source("avg_temp_by_square", row[square], row[temperature])

    def analyze_wind(self, row, current_dragonfly, dragonfly_name, year, square, temperature, clouds, wind, water, shading):
        # Average wind speed across all squares for each year
        current_dragonfly.add_avg_source("avg_wind_by_year", row[year], row[wind])
        # Wind speed at a specific square across all years
        current_dragonfly.add_list_with_dict("square_year_wind", square=row[square], year=row[year], wind=row[wind])
        # Average wind speed across all years for a specific square
        current_dragonfly.add_avg_source("avg_wind_by_square", row[square], row[wind])

    def analyze_clouds(self, row, current_dragonfly, dragonfly_name, year, square, temperature, clouds, wind, water, shading):
        # Average cloudiness across all squares for each year
        current_dragonfly.add_avg_source("avg_clouds_by_year", row[year], row[clouds])
        # Cloudiness at a specific square for each year of observation
        current_dragonfly.add_list_with_dict("square_year_clouds", square=row[square], year=row[year], clouds=row[clouds])
        # Average cloudiness across all years for a specific square
        current_dragonfly.add_avg_source("avg_clouds_by_square", row[square], row[clouds])

    def analyze_water(self, row, current_dragonfly, dragonfly_name, year, square, temperature, clouds, wind, fixed_water, shading):
        # Predominant water condition across all squares for each year (e.g., in 2018: 25 flowing, 5 still water)
        current_dragonfly.add_dict_with_inner_key("year_water_types", row[year], fixed_water)
        # Water condition at a specific square across all years
        current_dragonfly.add_list_with_dict("square_year_water", square=row[square], year=row[year], water=fixed_water)

    def analyze_shading(self, row, current_dragonfly, dragonfly_name, year, square, temperature, clouds, wind, water, shading):
        # Predominant shading condition across all squares for each year
        current_dragonfly.add_dict_with_inner_key("year_shading_types", row[year], row[shading])
        # Shading condition at a specific square across all years
        current_dragonfly.add_list_with_dict("square_year_shading", square=row[square], year=row[year], shading=row[shading])
