"""Tkinter widget manager - stores widgets and packs each in a single call"""

from app.structures.hash_table import HashTable

import tkinter as tk
from tkinter import ttk
from typing import Union

class WidgetManager:
    def __init__(self):
        self._widgets = HashTable()
        self._params = HashTable()

    # adding widget
    def add(self, widget: Union[tk.Widget, ttk.Widget], name: str = None, params: HashTable = None):
        # if name is given - saving with name as key, otherwise selects an ascending int
        if name:
            self._widgets[name] = widget
        
            if params:
                self._params[name] = params
        else:
            key = 0

            for k in self._widgets.keys():
                if isinstance(k, int):
                    key = k

            self._widgets[key + 1] = widget

            if params:
                self._params[key + 1] = params

    # pack each widget with specified parametres
    def pack(self):
        for key, widget in self._widgets.items():
            params = self._params.get(key, {})
            widget.pack(**params)

    # standart getter
    def __getitem__(self, name: str):
        return self._widgets[name]
