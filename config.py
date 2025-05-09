"""Stores all useful constants"""

import os
import PIL
import PIL.Image
from typing import Tuple, List

from app.structures.HashTable import *

# saves needed paths
_CONSTS = HashTable()
_CONSTS['ASSETS_DIR'] = 'ui/assets/'
_CONSTS['IMG_DIR'] = f'{_CONSTS["ASSETS_DIR"]}img/'
_CONSTS['STYLES_DIR'] = f'{_CONSTS["ASSETS_DIR"]}styles/'

# class for specific image
class Img:
    """Stores data about specific image"""

    def __init__(self, name: str) -> None:
        """Initialize Img with name of json style file"""

        self.path: str = _CONSTS['IMG_DIR'] + name

        img = PIL.Image.open(self.path)
        self.size: Tuple[int] = img.size

# class for all images
class Imgs:
    """Stores data about all images"""

    def __init__(self) -> None:
        """Initialize Imgs by loading all files from the img directory and creating an Img object for each one"""

        for filename in os.listdir(_CONSTS['IMG_DIR']):
            setattr(self, filename.split('.')[0].lower(), Img(filename))

# all data in one class
class Config:
    """Stores all useful constants"""
    
    def __init__(self) -> None:
        """Initialize Config with all useful data"""

        self.img: Imgs = Imgs()
        self.window_size: Tuple[int] = (600, 930)
        self.default_start_msg: str = '\r\nHello!!!'
        self.window_title = 'Dragonfly analyzer'
        self.ui_update_interval: int = 25    # in ms
        self.logger_padding: int = 15
        self.psq_max_elements_before_cleanup: int = 1000    # approx. 700 KB RAM threshold for cleanup
        self.input_filetypes: Tuple[Tuple[str]] = (
            ('Excel files', '*.xlsx'),
            ('All files', '*.*')
        )
        self.input_excel_sheet_name: str = 'Datu tabula'
        self.input_excel_correct_columns: List[str] = [
            'Gads',
            'Kvadrats',
            'Temperatura',
            'Makonainiba',
            'Vejs',
            'udens',
            'Noenojums'
        ]
        self.console_separator: str = '-' * 40
        self.progressbar_finish_time: float = 0.5
        self.operation_weights: HashTable = HashTable(
            file_validation = 22,
            file_loading = 2,
            file_analyzing = 63,
            error_output = 1,
            file_assembly = 4
        )

        for name, value in _CONSTS.items():
            setattr(self, name, value)
