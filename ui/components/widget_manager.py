"""Tkinter widget manager - stores widgets and packs each in a single call"""

from app.structures.HashTable.hash_table import HashTable

import tkinter as tk
from tkinter import ttk
from typing import Union, Self

class WidgetManager:
    def __init__(self: Self) -> None:
        self._widgets: HashTable = HashTable()
        self._params: HashTable = HashTable()

    # adding widget
    def add(
        self: Self,
        widget: Union[tk.Widget, ttk.Widget],
        name: str = None,
        params: HashTable = None
    ) -> None:
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
    def pack(self: Self) -> None:
        for key, widget in self._widgets.items():
            params = {}

            try:
                params = self._params[key]
            except:
                pass

            widget.pack(**params)

    # standart getter
    def __getitem__(self: Self, name: str) -> Union[tk.Widget, ttk.Widget]:
        return self._widgets[name]
