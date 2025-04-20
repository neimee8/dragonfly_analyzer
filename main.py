from dragonfly_analizer import DragonflyAnalyzer
from xlsx_file_employee import XlsxFileEmployee
from error_collector import ErrorCollector

def main():
    # Объект ошибок
    main_error_collector = ErrorCollector()
    # Объект содержащий все файлы
    main_xlsx_file_employee = XlsxFileEmployee(main_error_collector)
    main_xlsx_file_employee.load_files("files", sort=True)
    # Объект для анализа
    main_dragonfly_analyzer = DragonflyAnalyzer(main_error_collector)

    if not main_error_collector.errors:
        print("Files loaded successfully")

    # Анализируем все файлы
    for file in main_xlsx_file_employee.files:
        correct_columns = ["Gads", "Kvadrats", "Temperatura", "Makonainiba", "Vejs", "udens", "Noenojums", file.name.split(".")[0].split("_")[1]]
        main_dragonfly_analyzer.set_file(file, sheet_name="Datu tabula")
        main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_count)
        main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_temperature)
        main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_wind)
        main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_cloudy)
        main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_water)
        main_dragonfly_analyzer.analyze(correct_columns, main_dragonfly_analyzer.analyze_shading)

    # Смотрим ошибки
    for error in main_error_collector.errors:
        print(error)

    # Файлов проанализированно
    print(len(main_dragonfly_analyzer.analyzed_dragonflies))

    # Запихиваем все в excel
    for dragonfly in main_dragonfly_analyzer.analyzed_dragonflies:
        main_xlsx_file_employee.write_to_excel(main_dragonfly_analyzer.analyzed_dragonflies[dragonfly], "dragonfly_results.xlsx")
        print(f"✅ Файл {main_dragonfly_analyzer.analyzed_dragonflies[dragonfly].file_name} загружен в excel! 🐉📊")
main()
