"""Manages styles in JSON format"""

from tkinter import ttk
import json

from config import Config

cnf = Config()

class StyleManager:
    """Loads styles from style JSON data files by the name of file"""

    # uploads the json style data
    def __init__(self, name: str) -> None:
        """Initialize StyleManager with name of json style file"""

        self.path: str = f'{cnf.STYLES_DIR + name}.json'

    # returns ready-to-use style object
    def get(self) -> ttk.Style:
        """Returns ready-to-use ttk.Style object that may be used in project"""
        
        style = ttk.Style()
        
        with open(self.path, 'r', encoding = 'utf-8') as file:
            loaded_styles = json.load(file)

        for name, params in loaded_styles.items():
            style.configure(name, **params)

        return style    
