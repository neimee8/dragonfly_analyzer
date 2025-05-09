"""Main file with tkinter window"""

import tkinter as tk
from tkinter import ttk
import PIL
import PIL.Image
import PIL.ImageTk

from config import Config

from ui.components.tooltip import Tooltip
from ui.components.command_handler import UICommandHandler
from ui.components.widget_manager import WidgetManager
from ui.components.style_manager import StyleManager

from app.structures.HashTable import *

if __name__ == '__main__':
    # initializing objects
    cnf = Config()
    handler = UICommandHandler()
    main_widgets = WidgetManager()

    # get started with styles and window
    root = tk.Tk()
    root.title(cnf.window_title)
    styles = StyleManager('main').get()

    screen_size = (
        root.winfo_screenwidth(),
        root.winfo_screenheight()
    )
    window_shift = (
        (screen_size[0] // 2) - (cnf.window_size[0] // 2),
        int((screen_size[1] // 2) - (cnf.window_size[1] // 1.85))
    )

    root.geometry(f'{cnf.window_size[0]}x{cnf.window_size[1]}+{window_shift[0]}+{window_shift[1]}')
    root.minsize(cnf.window_size[0], cnf.window_size[1])

    # initializing tkinter variables
    error_checkbox_var = tk.BooleanVar()
    report_checkbox_var = tk.BooleanVar()
    output_filetype_var = tk.StringVar()
    min_mode_var = tk.BooleanVar()

    # default values
    report_checkbox_var.set(1)
    output_filetype_var.set('xlsx')
    min_mode_var.set(0)

    # dictionary with tkinter registered variable names
    checkbox_identifier = HashTable()
    checkbox_identifier[error_checkbox_var._name] = 'error'
    checkbox_identifier[report_checkbox_var._name] = 'report'

    favicon = PIL.Image.open(cnf.img.favicon.path)
    favicon = PIL.ImageTk.PhotoImage(favicon)
    root.iconphoto(False, favicon)

    dragonfly_img = PIL.Image.open(cnf.img.dragonfly.path)
    dragonfly_img = dragonfly_img.resize(tuple(map(lambda size: size // 10, cnf.img.dragonfly.size)))
    dragonfly_img = PIL.ImageTk.PhotoImage(dragonfly_img)

    main_widgets.add(ttk.Label(root, image = dragonfly_img), params = HashTable(pady = (40, 5)))

    main_widgets.add(ttk.Label(root, text = 'dragonfly analyzer', style = 'Header.TLabel'))
    main_widgets.add(
        ttk.Button(root, text = 'Select files'),
        name = 'file_selection_button',
        params = HashTable(pady = (50, 10))
    )

    main_widgets.add(
        ttk.Label(root, text = '0 files selected', style = 'InvalidFileSelectionState.TLabel'),
        name = 'file_selection_state_label'
    )
    file_selection_state_label_tooltip = Tooltip(
        main_widgets['file_selection_state_label'],
        'Click to clear file selection',
        listen_mouse_enter = False
    )

    # hover effect - cursor pointer
    main_widgets['file_selection_state_label'].configure(cursor = 'hand2')

    # listens file selection state label mouse hover and click
    main_widgets['file_selection_state_label'].bind(
        '<Enter>',
        lambda event: handler.file_selection_state_label_make_hover(
            event,
            root,
            main_widgets['file_selection_state_label'],
            file_selection_state_label_tooltip,
            'enter'
        )
    )
    main_widgets['file_selection_state_label'].bind(
        '<Leave>',
        lambda event: handler.file_selection_state_label_make_hover(
            event,
            root,
            main_widgets['file_selection_state_label'],
            file_selection_state_label_tooltip,
            'leave'
        )
    )
    main_widgets['file_selection_state_label'].bind(
        '<Button-1>',
        lambda event: handler.clear_file_selection(
            root,
            main_widgets['file_selection_state_label'],
            event
        )
    )

    # listens file selection button click
    main_widgets['file_selection_button'].bind(
        '<Button-1>',
        lambda event: handler.select_files(root, main_widgets['file_selection_state_label'])
    )

    main_widgets.add(
        ttk.Progressbar(root, orient = tk.HORIZONTAL, mode = 'determinate', length = 450),
        name = 'progressbar',
        params = HashTable(pady = (50, 30))
    )

    # adding a frame to pack checkboxes in one frame with tk.Text logger-widget
    main_widgets.add(ttk.Frame(root, width = 450, height = 300), name = 'console_frame')
    main_widgets['console_frame'].pack_propagate(False)

    console_widgets = WidgetManager()

    # adding a frame to connect tk.Text logger with vertical scrollbar
    console_widgets.add(
        ttk.Frame(main_widgets['console_frame']),
        name = 'text_frame',
        params = HashTable(pady = (0, 15))
    )

    # logger widget
    text_widget = tk.Text(
        console_widgets['text_frame'],
        wrap = 'word',
        height = 15,
        width = 61,
        highlightthickness = 0,
        relief = 'flat',
        font = ('Courier', 9)
    )
    text_widget.grid(row = 0, column = 0, stick = tk.NSEW)
    
    # tags to prettify text inside
    text_widget.tag_configure(
        'msg',
        justify = 'center',
        foreground = 'purple',
        lmargin1 = cnf.logger_padding,
        lmargin2 = cnf.logger_padding,
        rmargin = cnf.logger_padding
    )
    text_widget.tag_configure(
        'strong_error',
        justify = 'center',
        foreground = 'red',
        lmargin1 = cnf.logger_padding,
        lmargin2 = cnf.logger_padding,
        rmargin = cnf.logger_padding
    )
    text_widget.tag_configure(
        'file_validation_error',
        justify = 'center',
        foreground = '#ff4d4d',
        lmargin1 = cnf.logger_padding,
        lmargin2 = cnf.logger_padding,
        rmargin = cnf.logger_padding
    )
    text_widget.tag_configure(
        'bold_error',
        justify = 'center',
        foreground = 'red',
        font = ('Courier', 9, 'bold'),
        lmargin1 = cnf.logger_padding,
        lmargin2 = cnf.logger_padding,
        rmargin = cnf.logger_padding
    )
    text_widget.tag_configure(
        'report',
        justify = 'center',
        foreground = 'blue',
        lmargin1 = cnf.logger_padding,
        lmargin2 = cnf.logger_padding,
        rmargin = cnf.logger_padding
    )

    # write default start message into loger
    handler.cout(root, text_widget, 'msg', cnf.default_start_msg)

    text_widget.configure(state = tk.DISABLED)

    vscroll = ttk.Scrollbar(console_widgets['text_frame'], orient = tk.VERTICAL, command = text_widget.yview)
    vscroll.grid(row = 0, column = 1, sticky = tk.NS)

    # linking scrollbar to logger
    text_widget.configure(yscrollcommand = vscroll.set)

    console_widgets.add(
        ttk.Checkbutton(
            main_widgets['console_frame'],
            text = 'Output file validation errors',
            variable = error_checkbox_var
        ),
        name = 'error_checkbox',
        params = HashTable(anchor = tk.W)
    )
    console_widgets.add(
        ttk.Checkbutton(
            main_widgets['console_frame'],
            text = 'Output file operation reports',
            variable = report_checkbox_var
        ),
        name = 'report_checkbox',
        params = HashTable(anchor = tk.W)
    )
    console_widgets['report_checkbox'].configure(state = tk.DISABLED)

    # listens checkbutton variable change
    error_checkbox_var.trace_add(
        'write',
        lambda varname, *args: handler.on_check(
            checkbox_identifier[varname],
            console_widgets['report_checkbox'],
            varname,
            *args
        )
    )
    report_checkbox_var.trace_add(
        'write',
        lambda varname, *args: handler.on_check(
            checkbox_identifier[varname],
            console_widgets['error_checkbox'],
            varname,
            *args
        )
    )

    # packing widgets into frame
    console_widgets.pack()

    main_widgets.add(
        ttk.Label(root, text = 'Choose output file type:'),
        params = HashTable(pady = (30, 15))
    )
    main_widgets.add(
        ttk.Radiobutton(
            root,
            text = 'Excel',
            variable = output_filetype_var,
            value = "xlsx"
        ),
        name = 'radio_excel'
    )
    main_widgets.add(
        ttk.Radiobutton(
            root,
            text = 'JSON',
            variable = output_filetype_var,
            value = "json"
        ),
        name = 'radio_json'
    )
    main_widgets.add(
        ttk.Radiobutton(
            root,
            text = 'XML',
            variable = output_filetype_var,
            value = "xml"
        ),
        name = 'radio_xml'
    )

    # сheckbox that lets the user choose a minified output format
    main_widgets.add(
        ttk.Checkbutton(
            root,
            text = 'Minify',
            variable = min_mode_var
        ),
        name = 'min_mode_checkbutton',
        params = HashTable(pady = (15, 50))
    )
    min_mode_checkbutton_tooltip = Tooltip(
        main_widgets['min_mode_checkbutton'],
        'Not available for Excel',
        listen_mouse_enter = False
    )

    # listens mouse enter on min mode checkbutton to hide it when Excel isnt selected
    main_widgets['min_mode_checkbutton'].bind(
        '<Enter>',
        lambda event: handler.check_minify_enter(output_filetype_var.get(), min_mode_checkbutton_tooltip, event)
    )
    main_widgets['min_mode_checkbutton'].bind(
        '<Leave>',
        lambda event: handler.check_minify_leave(min_mode_checkbutton_tooltip, event)
    )

    # listens output filetype variable change to disable checkbutton when Excel is selected
    output_filetype_var.trace_add(
        'write',
        lambda *args: handler.on_check_minify(
            output_filetype_var.get(),
            main_widgets['min_mode_checkbutton'],
            *args
        )
    )

    main_widgets['min_mode_checkbutton'].configure(state = tk.DISABLED)
    
    main_widgets.add(
        ttk.Button(
            root,
            text = 'Execute',
            width = 20,
            style = 'Execute.TButton'
        ),
        name = 'execute_button'
    )

    # saving elemnts that need to be disabled/enabled depending on backend task execution
    elements_to_toggle = HashTable(
        file_selection_button = main_widgets['file_selection_button'],
        error_checkbox = console_widgets['error_checkbox'],
        report_checkbox = console_widgets['report_checkbox'],
        radio_excel = main_widgets['radio_excel'],
        radio_json = main_widgets['radio_json'],
        radio_xml = main_widgets['radio_xml'],
        execute_button = main_widgets['execute_button'],
        min_mode_checkbutton = main_widgets['min_mode_checkbutton']
    )

    # listens execute button click
    main_widgets['execute_button'].bind(
        '<Button-1>',
        lambda event: handler.execute(
            root,
            text_widget,
            main_widgets['progressbar'],
            main_widgets['file_selection_state_label'],
            output_filetype_var.get(),
            elements_to_toggle,
            min_mode_var.get(),
            event
        )
    )

    # packing main widgets into window and starting main loop
    main_widgets.pack()
    root.mainloop()
