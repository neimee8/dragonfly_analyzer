from workbook_utility import WorkbookUtility

class DragonflyWriter:
    def __init__(self, dragonfly, result_file):
        self.dragonfly = dragonfly
        self.result_file = result_file
        self.wu = WorkbookUtility(dragonfly.file_name, result_file)
        self.ws = self.wu.ws

    # кол-во
    def write_total_count(self):
        self.ws.cell(1, self.wu.call_column(), "Всего")
        self.ws.cell(1, self.wu.call_column(), self.dragonfly.total_count)
        self._add_spacing_column()

    def write_count_by_year(self):
        # Вызываем текущую колонку без изменения для заголовка таблички
        self.ws.cell(1, self.wu.current_column, "Кол-во за год")
        self._two_column_table(self.dragonfly.count_by_year)
        self._add_spacing_column()

    def write_count_by_square(self):
        self.ws.cell(1, self.wu.current_column, "Кол-во за квадрат")
        self._two_column_table(self.dragonfly.count_by_square)
        self._add_spacing_column()

    def write_square_year_count(self):
        self.ws.cell(1, self.wu.current_column, "Динамика кол-ва на кв.")
        self._three_column_table(self.dragonfly.square_year_count, "count")
        self._add_spacing_column()

    # температура
    def write_avg_temp_by_year(self):
        self.ws.cell(1, self.wu.current_column, "Средняя темп./год")
        self._two_column_table(self.dragonfly.avg_temp_by_year)
        self._add_spacing_column()

    def write_avg_temp_by_square(self):
        self.ws.cell(1, self.wu.current_column, "Средняя темп./кв.")
        self._two_column_table(self.dragonfly.avg_temp_by_square)
        self._add_spacing_column()

    def write_square_year_temp(self):
        self.ws.cell(1, self.wu.current_column, "Динамика темп на кв.")
        self._three_column_table(self.dragonfly.square_year_temp, "temperature")
        self._add_spacing_column()

    # ветер
    def write_avg_wind_by_year(self):
        self.ws.cell(1, self.wu.current_column, "Средний ветер/год")
        self._two_column_table(self.dragonfly.avg_wind_by_year)
        self._add_spacing_column()

    def write_avg_wind_by_square(self):
        self.ws.cell(1, self.wu.current_column, "Средний ветер/кв.")
        self._two_column_table(self.dragonfly.avg_wind_by_square)
        self._add_spacing_column()

    def write_square_year_wind(self):
        self.ws.cell(1, self.wu.current_column, "Динамика ветра на кв.")
        self._three_column_table(self.dragonfly.square_year_wind, "wind")
        self._add_spacing_column()

    # облачность
    def write_avg_cloudy_by_year(self):
        self.ws.cell(1, self.wu.current_column, "Средняя облачн./год")
        self._two_column_table(self.dragonfly.avg_cloudy_by_year)
        self._add_spacing_column()

    def write_avg_cloudy_by_square(self):
        self.ws.cell(1, self.wu.current_column, "Средння облачн./кв.")
        self._two_column_table(self.dragonfly.avg_cloudy_by_square)
        self._add_spacing_column()

    def write_square_year_cloudy(self):
        self.ws.cell(1, self.wu.current_column, "Динамика облачн. на кв.")
        self._three_column_table(self.dragonfly.square_year_cloudy, "cloudy")
        self._add_spacing_column()

    # вода
    def write_year_water_types(self):
        self.ws.cell(1, self.wu.current_column, "Преобладающее состояние воды")
        self.ws.cell(2, self.wu.current_column, "Год")
        self.ws.cell(2, self.wu.current_column + 1, "Tekoss")
        self.ws.cell(2, self.wu.current_column + 2, "Stavoss")
        self._three_column_table_special(self.dragonfly.year_water_types, "Tekoss", "Stavoss")
        self._add_spacing_column()

    def write_square_year_water(self):
        self.ws.cell(1, self.wu.current_column, "Состояния воды")
        self._three_column_table(self.dragonfly.square_year_water, "water")
        self._add_spacing_column()

    # затенение
    def write_year_shading_types(self):
        self.ws.cell(1, self.wu.current_column, "Преобладающие состояния затенения")
        self.ws.cell(2, self.wu.current_column, "Год")
        self.ws.cell(2, self.wu.current_column + 1, "Dalejs")
        self.ws.cell(2, self.wu.current_column + 2, "Nav")
        self._three_column_table_special(self.dragonfly.year_shading_types, "Dalejs", "Nav")
        self._add_spacing_column()

    def write_square_year_shading(self):
        self.ws.cell(1, self.wu.current_column, "Состояния тени")
        self._three_column_table(self.dragonfly.square_year_shading, "shading")
        self._add_spacing_column()

    def save(self):
        self.wu.wb.save(self.result_file)

    def _add_spacing_column(self):
        self.ws.cell(1, self.wu.call_column(), "")

    def _two_column_table(self, data):
        column = self.wu.call_column()
        next_column = self.wu.call_column()

        for index, key in enumerate(data):
            self.ws.cell(index + 2, column, key)
            self.ws.cell(index + 2, next_column, data[key])

    def _three_column_table(self, data, key3):
        data = sorted(data, key=lambda x: (x["square"], x["year"]))
        column1 = self.wu.call_column()
        column2 = self.wu.call_column()
        column3 = self.wu.call_column()
        uniq_squares = []

        for index, dictionary in enumerate(data):
            if dictionary["square"] not in uniq_squares:
                self.ws.cell(index + 2, column1, dictionary["square"])
                uniq_squares.append(dictionary["square"])

            self.ws.cell(index + 2, column2, dictionary["year"])
            self.ws.cell(index + 2, column3, dictionary[key3])

    def _three_column_table_special(self, data, in_key1, in_key2):
        column1 = self.wu.call_column()
        column2 = self.wu.call_column()
        column3 = self.wu.call_column()

        for index, gen_key in enumerate(data):
            self.ws.cell(index + 3, column1, gen_key)
            try:
                self.ws.cell(index + 3, column2, data[gen_key][in_key1])
            except KeyError:
                self.ws.cell(index + 3, column2, 0)

            try:
                self.ws.cell(index + 3, column3, data[gen_key][in_key2])
            except KeyError:
                self.ws.cell(index + 3, column3, 0)

# def _write_to_cell(self, row, column, value):
#     self.ws.cell(row, column, value)
#     self._connect_columns(column, value)
#     self._black_borders(self.ws.cell(row, column))
#

#
# def _connect_columns(self, column, value):
#     start_column = get_column_letter(column)
#     span = int(round(len(str(value)) / 10, 0))
#     end_column_index = column + span
#     end_column = get_column_letter(end_column_index)
#
#     self.ws.merge_cells(f"{start_column}1:{end_column}1")
#
#     for col in range(column, end_column_index + 1):
#         cell = self.ws.cell(row=1, column=col)
#         self._black_borders(cell)
#     self.current_column += span
#
#
# def _black_borders(self, cell):
#     black_borders = Border(
#         left=Side(style='thin', color='000000'),
#         right=Side(style='thin', color='000000'),
#         top=Side(style='thin', color='000000'),
#         bottom=Side(style='thin', color='000000')
#     )
#     cell.border = black_borders