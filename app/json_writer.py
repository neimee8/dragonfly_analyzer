"""Prepares and writes data to JSON"""

from app.file_writer import FileWriter

from typing import Dict, Any
import json

class JsonWriter(FileWriter):
    # prepares data in the dictionary form
    def get_data(self) -> Dict[str, Any]:
        data = {}

        data['count'] = {}
        data['count']['total_count'] = self.dragonfly.total_count
        data['count']['count_by_year'] = self.dragonfly.count_by_year.to_dict()
        data['count']['count_by_square'] = self.dragonfly.count_by_square.to_dict()

        data['temperature'] = {}
        data['temperature']['avg_temp_by_year'] = self.dragonfly.avg_temp_by_year.to_dict()
        data['temperature']['square_year_temp'] = self.dragonfly.square_year_temp
        data['temperature']['avg_temp_by_square'] = self.dragonfly.avg_temp_by_square.to_dict()

        data['wind'] = {}
        data['wind']['avg_wind_by_year'] = self.dragonfly.avg_wind_by_year.to_dict()
        data['wind']['square_year_wind'] = self.dragonfly.square_year_wind
        data['wind']['avg_wind_by_square'] = self.dragonfly.avg_wind_by_square.to_dict()

        data['cloudiness'] = {}
        data['cloudiness']['avg_cloudiness_by_year'] = self.dragonfly.avg_clouds_by_year.to_dict()
        data['cloudiness']['square_year_cloudiness'] = self.dragonfly.square_year_clouds
        data['cloudiness']['avg_cloudiness_by_square'] = self.dragonfly.avg_clouds_by_square.to_dict()

        data['water'] = {}
        data['water']['year_water_types'] = self.dragonfly.year_water_types.to_dict()
        data['water']['square_year_water'] = self.dragonfly.square_year_water

        data['shading'] = {}
        data['shading']['year_shading_types'] = self.dragonfly.year_shading_types.to_dict()
        data['shading']['square_year_shading'] = self.dragonfly.square_year_shading

        return data
    
    # saves given dictionary to JSON file
    @staticmethod
    def save(data: Dict[str, Any], output_filename: str, min: bool = False):
        with open(output_filename, 'w', encoding = 'utf-8') as file:
            if min:
                json.dump(data, file, separators = (',', ':'))
            else:
                json.dump(data, file, indent = 4, ensure_ascii = False)
