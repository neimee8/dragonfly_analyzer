"""Tkinter widget manager - stores widgets and packs each in a single call"""

import tkinter as tk
from tkinter import ttk
from typing import Union

from app.structures.HashTable import *

class WidgetManager:
    """Stores tkinter widgets, packs all widgets in it by one call of pack()"""
    
    def __init__(self) -> None:
        """Initialize WidgetManager with empty HashTable's for widgets and pack params for each one"""

        self._widgets: HashTable = HashTable()
        self._params: HashTable = HashTable()

    # adding widget
    def add(
        self,
        widget: Union[tk.Widget, ttk.Widget],
        name: str = None,
        params: HashTable = None
    ) -> None:
        """Adds widgets into objects, also can be added name of widget and widget.pack() parametres like pady, padx, anchor etc, as HashTable"""

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
    def pack(self) -> None:
        """Applies widget.pack() to all widgets that stored in"""

        for key, widget in self._widgets.items():
            params = {}

            try:
                params = self._params[key]
            except:
                pass

            widget.pack(**params)

    # standart getter
    def __getitem__(self, name: str) -> Union[tk.Widget, ttk.Widget]:
        """Returns item by key from _widgets HashTable"""
    
        return self._widgets[name]
