import math
import re
from pathlib import Path
from openpyxl.utils import get_column_letter
from openpyxl.styles import Border, Side

from dragonfly_writer import DragonflyWriter
from error_collector import ErrorCollector
from openpyxl import Workbook


class XlsxFileEmployee:
    def __init__(self, error_collector):
        self.error_collector = error_collector
        self.files = []
        self.dragonfly_writer = None

    def write_to_excel(self, dragonfly_object, result_file):
        self.dragonfly_writer = DragonflyWriter(dragonfly_object, result_file)
        # кол-во
        self.dragonfly_writer.write_total_count()
        self.dragonfly_writer.write_count_by_year()
        self.dragonfly_writer.write_count_by_square()
        self.dragonfly_writer.write_square_year_count()

        # температура
        self.dragonfly_writer.write_avg_temp_by_year()
        self.dragonfly_writer.write_avg_temp_by_square()
        self.dragonfly_writer.write_square_year_temp()

        # ветер
        self.dragonfly_writer.write_avg_wind_by_year()
        self.dragonfly_writer.write_avg_wind_by_square()
        self.dragonfly_writer.write_square_year_wind()

        # облачность
        self.dragonfly_writer.write_avg_cloudy_by_year()
        self.dragonfly_writer.write_avg_cloudy_by_square()
        self.dragonfly_writer.write_square_year_cloudy()

        # вода
        self.dragonfly_writer.write_year_water_types()
        self.dragonfly_writer.write_square_year_water()

        # затенение
        self.dragonfly_writer.write_year_shading_types()
        self.dragonfly_writer.write_square_year_shading()
        self.dragonfly_writer.save()

    def load_files(self, map_name, sort=False):
        try:
            self.files = list(Path(map_name).iterdir())
            if sort:
                self.files = self._sort_files(self.files)
        except FileNotFoundError as error:
            self.error_collector.add(f"{self.__class__.__name__}: {error}", "FileNotFoundError")

    def _sort_files(self, files):
        return sorted(files, key=lambda file: int(re.match(r"\d+", file.name).group()))
