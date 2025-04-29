"""Tooltip widget - extension for tkinter"""

from ui.components.style_manager import StyleManager

import tkinter as tk
from tkinter import ttk
from typing import Union

class Tooltip:
    def __init__(self, widget: Union[tk.Widget, ttk.Widget], text, listen_mouse_enter: bool = True):
        self.widget = widget
        self.text = text
        self.tooltip_container = None

        if listen_mouse_enter:
            self.widget.bind('<Enter>', self.show)
            self.widget.bind('<Leave>', self.hide)

    def show(self, event):
        # creates toplevel window without controls
        shift = (event.x_root + 20, event.y_root + 20)
        self.tooltip_container = tk.Toplevel(self.widget)

        styles = StyleManager('tooltip').get()

        self.tooltip_container.wm_overrideredirect(True)
        self.tooltip_container.wm_geometry(f'+{shift[0]}+{shift[1]}')

        # packs text label into window
        tooltip_label = ttk.Label(self.tooltip_container, text = self.text, style = 'Tooltip.TLabel')
        tooltip_label.pack()

    def hide(self, event):
        if self.tooltip_container:
            self.tooltip_container.destroy()
            self.tooltip_container = None
