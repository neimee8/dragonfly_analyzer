import math
import re
from pathlib import Path
from openpyxl.utils import get_column_letter
from openpyxl.styles import Border, Side

from app.dragonfly_writer import DragonflyWriter
from app.error_collector import ErrorCollector
from openpyxl import Workbook

class XlsxFileEmployee:
    def __init__(self, error_collector):
        self.error_collector = error_collector
        self.files = []
        self.workbook_utility = None

    def set_workbook_utility(self, workbook_utility):
        self.workbook_utility = workbook_utility

    def write_to_excel(self, dragonfly_object):
        writer = DragonflyWriter(dragonfly_object, self.workbook_utility)
        # Count (quantity) 
        writer.write_total_count()
        writer.write_count_by_year()
        writer.write_count_by_square()
        writer.write_square_year_count()

        # Temperature 
        writer.write_avg_temp_by_year()
        writer.write_avg_temp_by_square()
        writer.write_square_year_temp()

        # Clouds 
        writer.write_avg_clouds_by_year()
        writer.write_avg_clouds_by_square()
        writer.write_square_year_clouds()

        # Wind
        writer.write_avg_wind_by_year()
        writer.write_avg_wind_by_square()
        writer.write_square_year_wind()
        
        # Water
        writer.write_year_water_types()
        writer.write_square_year_water()

        # Shading
        writer.write_year_shading_types()
        writer.write_square_year_shading()

    # name changed - from load_files
    def load_file(self, file):
        # cycle is in backend task, sorting by command
        self.files.append(Path(file))

    # name changed - public form, sorts files in object
    def sort_files(self):
        self.files =  sorted(self.files, key=lambda file: int(re.match(r"\d+", file.name).group()))
