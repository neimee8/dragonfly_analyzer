"""Stores all useful constants"""

import os
import PIL
import PIL.Image

# saves needed paths
_CONSTS = {}
_CONSTS['ASSETS_DIR'] = 'ui/assets/'
_CONSTS['IMG_DIR'] = f'{_CONSTS["ASSETS_DIR"]}img/'
_CONSTS['STYLES_DIR'] = f'{_CONSTS["ASSETS_DIR"]}styles/'

# class for specific image
class Img:
    def __init__(self, name):
        self.path = _CONSTS['IMG_DIR'] + name

        img = PIL.Image.open(self.path)
        self.size = img.size

# class for all images
class Imgs:
    def __init__(self):
        for filename in os.listdir(_CONSTS['IMG_DIR']):
            setattr(self, filename.split('.')[0].lower(), Img(filename))

# all data in one class
class Config:
    def __init__(self):
        self.img = Imgs()
        self.window_size = (600, 930)
        self.default_start_msg = '\nHello!!!'
        self.ui_update_interval = 25
        self.logger_padding = 15
        self.input_filetypes = (('Excel files', '*.xlsx'), ('All files', '*.*'))
        self.input_excel_sheet_name = 'Datu tabula'
        self.input_excel_correct_columns = ['Gads', 'Kvadrats', 'Temperatura', 'Makonainiba', 'Vejs', 'udens', 'Noenojums']
        self.console_separator = '-' * 40
        self.progressbar_finish_time = 0.5
        self.operation_weights = {
            'file_validation': 22,
            'file_loading': 2,
            'file_analyzing': 63,
            'error_output': 1,
            'file_assembly': 4
        }

        for name, value in _CONSTS.items():
            setattr(self, name, value)
            
