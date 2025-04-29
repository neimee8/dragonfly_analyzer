from dragonfly_analyzer import DragonflyAnalyzer
from workbook_utility import WorkbookUtility
from xlsx_file_employee import XlsxFileEmployee
from error_collector import ErrorCollector
import time

def main():
    result_file = "dragonfly_results.xlsx"
    # Object with all errors
    main_error_collector = ErrorCollector()
    # Object which provides work with xlsx files
    main_xlsx_file_employee = XlsxFileEmployee(main_error_collector)
    main_xlsx_file_employee.load_files("files", sort=True)
    # Object with all logic of analysis
    main_dragonfly_analyzer = DragonflyAnalyzer(main_error_collector)

    if not main_error_collector.errors:
        print("Files loaded successfully")

    # Analysis of all files
    for file in main_xlsx_file_employee.files:
        correct_columns = ["Gads", "Kvadrats", "Temperatura", "Makonainiba", "Vejs", "udens", "Noenojums", file.name.split(".")[0].split("_")[1]]
        main_dragonfly_analyzer.set_file(file, sheet_name="Datu tabula")
        main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_count)
        main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_temperature)
        main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_wind)
        main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_clouds)
        main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_water)
        main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_shading)

    # Show errors if they was during analysis
    for error in main_error_collector.errors:
        print(error)

    # Analyzed files count
    print(len(main_dragonfly_analyzer.analyzed_dragonflies))

    # Object for writing in excel files
    workbook_util = WorkbookUtility(result_file)
    main_xlsx_file_employee.set_workbook_utility(workbook_util)

    # Write all data to excel file 
    time_all = 0
    for dragonfly in main_dragonfly_analyzer.analyzed_dragonflies.values():
        start_time = time.time()
        main_xlsx_file_employee.write_to_excel(dragonfly)
        elapsed_time = time.time() - start_time
        print(f"✅ File {dragonfly.file_name} loaded to excel in {elapsed_time} seconds! 🐉📊")
        time_all += elapsed_time
    workbook_util.save()
    print(f"⌛ All loading time: {time_all:.2f} seconds")
    print(f"📄 Average time for file writing to excel: {time_all / len(main_dragonfly_analyzer.analyzed_dragonflies):.2f} seconds")
main()
