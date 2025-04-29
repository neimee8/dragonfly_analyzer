"""Manages styles in JSON format"""

from config import Config

from tkinter import ttk
import json

cnf = Config()

class StyleManager:
    # uploads the json style data
    def __init__(self, name: str):
        self.path = f'{cnf.STYLES_DIR + name}.json'

    # returns ready-to-use style object
    def get(self) -> ttk.Style:
        style = ttk.Style()
        
        with open(self.path, 'r', encoding = 'utf-8') as file:
            loaded_styles = json.load(file)

        for name, params in loaded_styles.items():
            style.configure(name, **params)

        return style    
 
