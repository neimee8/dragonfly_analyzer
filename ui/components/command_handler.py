"""Handles frontend events, makes controls work properly"""

from config import Config
from ui.components.tooltip import Tooltip

from app.dragonfly_analyzer import DragonflyAnalyzer
from app.workbook_utility import WorkbookUtility
from app.xlsx_file_employee import XlsxFileEmployee
from app.error_collector import ErrorCollector
from app.json_writer import JsonWriter
from app.xml_writer import XmlWriter

from app.structures.ProcessSafeQueue.process_safe_queue import ProcessSafeQueue, EmptyProcessSafeQueueError
from app.structures.HashTable.hash_table import HashTable

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import multiprocessing
import os
import time
from pathlib import Path
from typing import Dict, Union, Tuple, Callable
import xml.etree.ElementTree as et

import openpyxl

cnf = Config()

class UICommandHandler:
    selected_files = ()
    check = HashTable(
        error = False,
        report = True
    )

    # updates file selection state label file count
    @classmethod
    def update_file_selection_state_label_file_count(cls, window: tk.Tk, state_label: ttk.Label):
        text = f'{len(cls.selected_files)} file'
        text += 's' if len(cls.selected_files) != 1 else ''
        text += ' selected'

        state_label.configure(text = text)

        window.update()
        window.update_idletasks()
    
    # updates the style of file selection state label
    @classmethod
    def update_file_selection_state_label_style(cls, window: tk.Tk, state_label: ttk.Label):
        if len(cls.selected_files) == 0:
            state_label.configure(style = 'InvalidFileSelectionState.TLabel')
        else:
            state_label.configure(style = 'ValidFileSelectionState.TLabel')
        
        window.update()
        window.update_idletasks()

    # makes possible to select multiple input files
    @classmethod
    def select_files(cls, window: tk.Tk, state_label: ttk.Label, event = None):
        filenames = filedialog.askopenfilenames(title = 'Select files', filetypes = cnf.input_filetypes)

        if len(filenames) > 0:
            cls.selected_files = filenames

            # updating file selection state label
            cls.update_file_selection_state_label_file_count(window, state_label)
            cls.update_file_selection_state_label_style(window, state_label)

    # hover effect for file selection state label
    @classmethod
    def file_selection_state_label_make_hover(cls, event, window: tk.Tk, state_label: ttk.Label, tooltip: Tooltip, action: str):
        if action == 'enter':
            state_label.configure(style = 'HoverFileSelectionState.TLabel')

            tooltip.show(event)
        elif action == 'leave':
            cls.update_file_selection_state_label_style(window, state_label)

            tooltip.hide(event)

    # clears file selection by click on label
    @classmethod
    def clear_file_selection(cls, window: tk.Tk, state_label: ttk.Label, event = None):
        cls.selected_files = ()
        cls.update_file_selection_state_label_file_count(window, state_label)

    # makes checkbuttons work properly
    @classmethod
    def on_check(cls, checkbox_identifier: str, checkbox: ttk.Checkbutton, *args):
        # toggles checkbutton state by XOR with True
        match checkbox_identifier:
            case 'error':
                cls.check['error'] ^= True
            case 'report':
                cls.check['report'] ^= True

        # if one of checkbuttons is unchecked - disables another
        if cls.check['error'] ^ cls.check['report']:
            checkbox.configure(state = tk.DISABLED)
        else:
            checkbox.configure(state = tk.NORMAL)

    # makes minify mode checkbutton disabled when Excel is selected
    @staticmethod
    def on_check_minify(output_filetype: str, checkbutton: ttk.Checkbutton, *args):
        if output_filetype == 'xlsx':
            checkbutton.configure(state = tk.DISABLED)
        else:
            checkbutton.configure(state = tk.NORMAL)

    # makes minify mode checkbutton hidden when Excel isnt selected
    @staticmethod
    def check_minify_enter(output_filetype: str, tooltip: Tooltip, event):
        if output_filetype == 'xlsx':
            tooltip.show(event)

    @staticmethod
    def check_minify_leave(tooltip: Tooltip, event):
        tooltip.hide(event)

    # prints message to logger
    @classmethod
    def cout(cls, window: tk.Tk, console_widget: tk.Text, type: str, msg: str):
        msg = f'\n{msg}\n'

        condition = cls.check['error'] and type == 'file_validation_error'
        condition = condition or (cls.check['report'] and type == 'report')
        condition = condition or type in ('msg', 'error', 'strong_error', 'bold_error', 'separator')

        # checks for message type
        if condition:
            # writes to widget
            console_widget.configure(state = tk.NORMAL)
            console_widget.insert(tk.END, msg, type)
            console_widget.configure(state = tk.DISABLED)

            # scrolls bottom
            console_widget.see(tk.END)

        window.update()
        window.update_idletasks()

    # prints separator to logger
    @classmethod
    def csep(cls, window: tk.Tk, console_widget: tk.Text):
        cls.cout(window, console_widget, 'msg', cnf.console_separator)

    # updates progessbar
    @staticmethod
    def update_progressbar(window: tk.Tk, progressbar: ttk.Progressbar, value: Union[float, int]):
        progressbar.configure(value = value)

        window.update()
        window.update_idletasks()

    # makes progressbar show 100 percent when called after finished task
    @classmethod
    def finish_progressbar(cls, window: tk.Tk, progressbar: ttk.Progressbar):
        need_to_progress = 100 - progressbar['value']
        time_to_finish = cnf.progressbar_finish_time
        iterations = int(need_to_progress // 0.5)

        for i in range(iterations):
            cls.update_progressbar(window, progressbar, progressbar['value'] + (i + 1) / iterations)
            time.sleep(time_to_finish / iterations)

    # main logic
    @classmethod
    def parallel_backend_task(
        cls,
        queue,
        selected_files: Tuple[str],
        output_filetype: str,
        check: Dict[str, bool],
        min_mode: bool,
        result_file: str,
        operation_weights: Dict[str, int]
    ):
        # put whole method into try catch to avoid a crash caused by unexpected unhandled exceptions
        try:
            queue.put({
                'key': 'console',
                'data': {
                    'type': 'separator',
                    'msg': None
                }
            })
            queue.put({
                'key': 'console',
                'data': {
                    'type': 'msg',
                    'msg': 'Validation finished'
                }
            })
            queue.put({
                'key': 'console',
                'data': {
                    'type': 'msg',
                    'msg': 'Running process...'
                }
            })

            msg = f'Files: {len(selected_files)}\nOutput file type: '
            msg += 'Excel' if output_filetype == 'xlsx' else output_filetype.upper()

            queue.put({
                'key': 'console',
                'data': {
                    'type': 'msg',
                    'msg': msg
                }
            })

            # initializing and uploading files
            main_error_collector = ErrorCollector()
            main_xlsx_file_employee = XlsxFileEmployee(main_error_collector)

            for i, file in enumerate(selected_files):
                main_xlsx_file_employee.load_file(file)

                progress = (i + 1) / len(selected_files) * operation_weights['file_loading']
                progress += operation_weights['file_validation']

                queue.put({
                    'key': 'progressbar',
                    'data': progress
                })

            main_xlsx_file_employee.sort_files()

            main_dragonfly_analyzer = DragonflyAnalyzer(main_error_collector)
            start_time = time.perf_counter()

            queue.put({
                'key': 'console',
                'data': {
                    'type': 'msg',
                    'msg': 'Files uploaded successfully!'
                }
            })
            queue.put({
                'key': 'console',
                'data': {
                    'type': 'separator',
                    'msg': None
                }
            })

            # start file analyzing
            for i, file in enumerate(main_xlsx_file_employee.files):
                correct_columns = cnf.input_excel_correct_columns + [file.name.split('.')[0].split('_')[1]]
                main_dragonfly_analyzer.set_file(file, sheet_name = cnf.input_excel_sheet_name)

                main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_count)
                main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_temperature)
                main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_wind)
                main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_clouds)
                main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_water)
                main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_shading)

                queue.put({
                    'key': 'console',
                    'data': {
                        'type': 'report',
                        'msg': f'{file} analyzed successfully!'
                    }
                })

                progress = (i + 1) / len(selected_files) * operation_weights['file_analyzing']
                progress += sum([
                    operation_weights['file_validation'],
                    operation_weights['file_loading']
                ])

                queue.put({
                    'key': 'progressbar',
                    'data': progress
                })

            if check['report']:
                queue.put({
                    'key': 'console',
                    'data': {
                        'type': 'separator',
                        'msg': None
                    }
                })

            # file validation errors output
            for i, error in enumerate(main_error_collector.errors):
                queue.put({
                    'key': 'console',
                    'data': {
                        'type': 'file_validation_error',
                        'msg': error
                    }
                })

                progress = (i + 1) / len(selected_files) * operation_weights['error_output']
                progress += sum([
                    operation_weights['file_validation'],
                    operation_weights['file_loading'],
                    operation_weights['file_analyzing']
                ])

                queue.put({
                    'key': 'progressbar',
                    'data': progress
                })

            if len(main_error_collector.errors) > 0 and check['error']:
                queue.put({
                    'key': 'console',
                    'data': {
                        'type': 'separator',
                        'msg': None
                    }
                })

            msg = 'Beginning '
            msg += 'Excel' if output_filetype == 'xlsx' else output_filetype.upper()
            msg += ' file assembly'

            queue.put({
                'key': 'console',
                'data': {
                    'type': 'msg',
                    'msg': msg
                }
            })

            queue.put({
                'key': 'console',
                'data': {
                    'type': 'separator',
                    'msg': None
                }
            })

            # delets old file by the path if exist
            if os.path.exists(result_file):
                try:
                    os.remove(result_file)
                except:
                    pass

            # writes to result file
            match output_filetype:
                # writes to excel
                case 'xlsx':
                    workbook_util = WorkbookUtility(result_file)
                    main_xlsx_file_employee.set_workbook_utility(workbook_util)

                    for i, dragonfly in enumerate(main_dragonfly_analyzer.analyzed_dragonflies.values()):
                        main_xlsx_file_employee.write_to_excel(dragonfly)
                        queue.put({
                            'key': 'console',
                            'data': {
                                'type': 'report',
                                'msg': f'{dragonfly.file_name} loaded to result Excel file successfully!'
                            }
                        })

                        progress = (i + 1) / len(selected_files) * operation_weights['file_assembly']

                        progress += sum([
                            operation_weights['file_validation'],
                            operation_weights['file_loading'],
                            operation_weights['file_analyzing'],
                            operation_weights['error_output']
                        ])

                        queue.put({
                            'key': 'progressbar',
                            'data': progress
                        })

                    workbook_util.save()

                # writes to json
                case 'json':
                    data = {}
                    i = 0

                    for name, dragonfly in main_dragonfly_analyzer.analyzed_dragonflies.items():
                        data[name] = JsonWriter(dragonfly).get_data()

                        queue.put({
                            'key': 'console',
                            'data': {
                                'type': 'report',
                                'msg': f'{dragonfly.file_name} loaded to result JSON file successfully!'
                            }
                        })
                        
                        progress = (i + 1) / len(selected_files) * operation_weights['file_assembly']
                        progress += sum([
                            operation_weights['file_validation'],
                            operation_weights['file_loading'],
                            operation_weights['file_analyzing'],
                            operation_weights['error_output']
                        ])

                        queue.put({
                            'key': 'progressbar',
                            'data': progress
                        })

                        i += 1

                    JsonWriter.save(data, result_file, min = min_mode)

                # writes to xml
                case 'xml':
                    root = et.Element('Dragonflies')
                    i = 0

                    for name, dragonfly in main_dragonfly_analyzer.analyzed_dragonflies.items():
                        root.append(XmlWriter(dragonfly).get_data(name))

                        queue.put({
                            'key': 'console',
                            'data': {
                                'type': 'report',
                                'msg': f'{dragonfly.file_name} loaded to result XML file successfully!'
                            }
                        })
                        
                        progress = (i + 1) / len(selected_files) * operation_weights['file_assembly']
                        progress += sum([
                            operation_weights['file_validation'],
                            operation_weights['file_loading'],
                            operation_weights['file_analyzing'],
                            operation_weights['error_output']
                        ])

                        queue.put({
                            'key': 'progressbar',
                            'data': progress
                        })

                        i += 1

                    tree = et.ElementTree(root)
                    XmlWriter.save(tree, result_file, min = min_mode)

            queue.put({
                'key': 'progressbar',
                'data': 'finish'
            })

            if check['report']:
                queue.put({
                    'key': 'console',
                    'data': {
                        'type': 'separator',
                        'msg': None
                    }
                })

            # preparing result file size for printing in logger widget
            size = os.path.getsize(result_file)
            units = ['B', 'KB', 'MB']
            units_index = 0

            while size >= 1024 and units_index < (len(units) - 1):
                size /= 1024
                units_index += 1

            queue.put({
                'key': 'console',
                'data': {
                    'type': 'msg',
                    'msg': f'{Path(result_file).name} ({round(size, 2)} {units[units_index]}) assembled successfully!'
                }
            })
            queue.put({
                'key': 'console',
                'data': {
                    'type': 'msg',
                    'msg': f'Execution time: {time.perf_counter() - start_time: .2f} seconds'
                }
            })

            # triggers the termination of the periodic UI update method
            queue.put('END')

        # behavior in case of an unexpected error
        except:
            queue.put({
                'key': 'console',
                'data': {
                    'type': 'separator',
                    'msg': None
                }
            })
            queue.put({
                'key': 'console',
                'data': {
                    'type': 'bold_error',
                    'msg': f'Execution have stopped: incompatible data file'
                }
            })
            queue.put({
                'key': 'progressbar',
                'data': 'finish'
            })
            queue.put('END')
            
    # periodic UI updating by listening the queue
    @classmethod
    def periodic_update_ui(
        cls,
        window: tk.Tk,
        console_widget: tk.Text,
        progressbar: ttk.Progressbar,
        q: ProcessSafeQueue,
        finalize: Callable[[], None]
    ):
        try:
            while True:
                # gets data from queue
                data = q.get_nowait()

                if data:
                    # ends the method when backend finished
                    if data == 'END':
                        finalize()

                        return

                    if data['key'] == 'progressbar':
                        if data['data'] == 'finish':
                            cls.finish_progressbar(window, progressbar)
                        else:
                            cls.update_progressbar(window, progressbar, data['data'])
                    elif data['key'] == 'console':
                        if data['data']['type'] == 'separator':
                            cls.csep(window, console_widget)
                        else:
                            cls.cout(window, console_widget, data['data']['type'], data['data']['msg'])
                else:
                    break
        except EmptyProcessSafeQueueError:
            pass

        window.update()
        window.update_idletasks()

        # plans next check
        window.after(
            cnf.ui_update_interval,
            lambda: cls.periodic_update_ui(window, console_widget, progressbar, q, finalize)
        )

    # main operations
    @classmethod
    def execute(
        cls,
        window: tk.Tk,
        console_widget: tk.Text,
        progressbar: ttk.Progressbar,
        state_label: ttk.Label,
        output_filetype: str,
        elements_to_toggle: HashTable,
        min_mode: bool,
        event
    ):
        # toggles buttons between disabled/enabled state
        def toggle_ui(state: str):
            for name, element in elements_to_toggle.items():
                if state == tk.NORMAL:
                    if 'checkbox' in name and False in cls.check.values() \
                        and cls.check[name.removesuffix('_checkbox')]:
                        element.configure(state = tk.DISABLED)
                    elif name == 'min_mode_checkbutton' and output_filetype == 'xlsx':
                        element.configure(state = tk.DISABLED)
                    else:
                        element.configure(state = state)
                else:
                    element.configure(state = state)

            window.update()
            window.update_idletasks()

        # finalize execution after backend process is over
        def finalize():
            toggle_ui(tk.NORMAL)

        operation_weights = cnf.operation_weights
        progressbar.configure(value = 0)

        cls.csep(window, console_widget)

        # validation
        if len(cls.selected_files) == 0:
            cls.cout(
                window,
                console_widget,
                'bold_error',
                'Execution cannot be started: you have to select at least 1 file!'
            )

            return
        
        toggle_ui(tk.DISABLED)
        cls.cout(window, console_widget, 'msg', 'Validation start...')

        # validation
        valid_files = []
        doesnt_exist = []
        invalid_files = []

        for i, file in enumerate(cls.selected_files):
            # check if exists
            if not os.path.isfile(file):
                doesnt_exist.append(file)
            else:
                # check if has xlsx extension
                if not file.lower().endswith('.xlsx'):
                    invalid_files.append(file)

                    continue

                # check if is a valid workbook
                try:
                    wb = openpyxl.load_workbook(file)
                    wb.close()
                except:
                    invalid_files.append(file)

                    continue

                valid_files.append(file) 

            progress = (i + 1) / len(cls.selected_files) * operation_weights['file_validation']

            cls.update_progressbar(window, progressbar, progress)
            
        # error throwing
        for i, file in enumerate(doesnt_exist + invalid_files):
            line_break = '\n' if i == 0 else ''

            if file in doesnt_exist:
                cls.cout(
                    window,
                    console_widget,
                    'strong_error',
                    f'{line_break}File {file} was not found'
                )
            else:
                cls.cout(
                    window,
                    console_widget,
                    'strong_error',
                    f'{line_break}File {file} is not valid xlsx file'
                )
        
        # if no valid files - stop execution, throw error
        if len(valid_files) == 0:
            cls.cout(
                window,
                console_widget,
                'bold_error',
                '\nExecution have stopped: no valid files found'
            )

            toggle_ui(tk.NORMAL)
            cls.finish_progressbar(window, progressbar)

            return
        
        # asking user to choose output filename
        initialfile = 'Excel' if output_filetype == 'xlsx' else output_filetype.upper()
        initialfile = f'Dragonfly analyzer result ({initialfile})'
        initialfile += '.min' if min_mode else ''
        initialfile += f'.{output_filetype}'

        filetype_name = 'Excel' if output_filetype == 'xlsx' else output_filetype.upper()
        filetype_name += ' files'
        filetype_extension = f'*.{output_filetype}'

        result_file = filedialog.asksaveasfilename(
            title = f'Save *.{output_filetype} file',
            filetypes = (
                (filetype_name, filetype_extension),
                ('All files', '*.*')
            ),
            initialfile = initialfile
        )

        # validation output filename
        if not result_file:
            cls.cout(
                window,
                console_widget,
                'bold_error',
                'Execution have stopped: you must select an output filename to continue!'
            )

            toggle_ui(tk.NORMAL)
            cls.finish_progressbar(window, progressbar)

            return

        # passing through only validated files
        if len(cls.selected_files) != len(valid_files):
            cls.selected_files = () if len(valid_files) == 0 else tuple(valid_files)

            cls.update_file_selection_state_label_file_count(window, state_label)
            cls.update_file_selection_state_label_style(window, state_label)

        manager = multiprocessing.Manager()
        shared_list = manager.list()
        shared_head = manager.Value('i', -1)
        shared_tail = manager.Value('i', -1)
        shared_lock = multiprocessing.Lock()

        queue = ProcessSafeQueue(shared_list, shared_head, shared_tail, shared_lock)

        # runs the task in a separate process to avoid blocking the UI thread while task executing
        task_process = multiprocessing.Process(
            target = cls.parallel_backend_task,
            args = (
                queue,
                cls.selected_files,
                output_filetype,
                cls.check.to_dict(),
                min_mode,
                result_file,
                operation_weights.to_dict()
            )
        )
        task_process.start()

        # periodically cheсking the queue to apply UI updates
        cls.periodic_update_ui(window, console_widget, progressbar, queue, finalize)
