"""Prepares and writes data to JSON"""

from app.file_writer import FileWriter

from app.structures.HashTable import *

from typing import Dict, Any, Self
import json

class JsonWriter(FileWriter):
    """Preparing data and writing to json result file"""

    # prepares data in the dictionary form
    def get_data(self: Self) -> Dict[str, Any]:
        """Prepares data about specific dragonfly in dictionary structure"""

        data = {}
        square_year_data = HashTable()

        square_year_data['temp'] = self.dragonfly.square_year_temp
        square_year_data['wind'] = self.dragonfly.square_year_wind
        square_year_data['clouds'] = self.dragonfly.square_year_clouds
        square_year_data['water'] = self.dragonfly.square_year_water
        square_year_data['shading'] = self.dragonfly.square_year_shading

        data['count'] = {}
        data['count']['total_count'] = self.dragonfly.total_count
        data['count']['count_by_year'] = self.dragonfly.count_by_year.to_dict()
        data['count']['count_by_square'] = self.dragonfly.count_by_square.to_dict()

        data['temperature'] = {}
        data['temperature']['avg_temp_by_year'] = self.dragonfly.avg_temp_by_year.to_dict()
        data['temperature']['square_year_temp'] = square_year_data.to_dict()['temp']
        data['temperature']['avg_temp_by_square'] = self.dragonfly.avg_temp_by_square.to_dict()

        data['wind'] = {}
        data['wind']['avg_wind_by_year'] = self.dragonfly.avg_wind_by_year.to_dict()
        data['wind']['square_year_wind'] = square_year_data.to_dict()['wind']
        data['wind']['avg_wind_by_square'] = self.dragonfly.avg_wind_by_square.to_dict()

        data['cloudiness'] = {}
        data['cloudiness']['avg_cloudiness_by_year'] = self.dragonfly.avg_clouds_by_year.to_dict()
        data['cloudiness']['square_year_cloudiness'] = square_year_data.to_dict()['clouds']
        data['cloudiness']['avg_cloudiness_by_square'] = self.dragonfly.avg_clouds_by_square.to_dict()

        data['water'] = {}
        data['water']['year_water_types'] = self.dragonfly.year_water_types.to_dict()
        data['water']['square_year_water'] = square_year_data.to_dict()['water']

        data['shading'] = {}
        data['shading']['year_shading_types'] = self.dragonfly.year_shading_types.to_dict()
        data['shading']['square_year_shading'] = square_year_data.to_dict()['shading']

        return data
    
    # saves given dictionary to JSON file
    @staticmethod
    def save(data: Dict[str, Any], output_filename: str, min: bool = False) -> None:
        """Saves into result file"""
        
        with open(output_filename, 'w', encoding = 'utf-8') as file:
            if min:
                json.dump(data, file, separators = (',', ':'))
            else:
                json.dump(data, file, indent = 4, ensure_ascii = False)
