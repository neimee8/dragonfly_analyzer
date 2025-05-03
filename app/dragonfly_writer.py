class DragonflyWriter:
    def __init__(self, dragonfly, workbook_utility):
        self.dragonfly = dragonfly
        self.wu = workbook_utility
        self.ws = self.wu.add_sheet(self.dragonfly.file_name)

    # Count (quantity)
    def write_total_count(self):
        self.ws.cell(1, self.wu.call_column(), "Total")
        self.ws.cell(1, self.wu.call_column(), self.dragonfly.total_count)
        self._add_spacing_column()

    def write_count_by_year(self):
        # Calling current column number without changing for title
        self.ws.cell(1, self.wu.current_column, "Quantity by year")
        self._two_column_table(self.dragonfly.count_by_year)
        self._add_spacing_column()

    def write_count_by_square(self):
        self.ws.cell(1, self.wu.current_column, "Quantity by square")
        self._two_column_table(self.dragonfly.count_by_square)
        self._add_spacing_column()

    def write_square_year_count(self):
        self.ws.cell(1, self.wu.current_column, "Quantity dynamics through years")
        self._three_column_table(self.dragonfly.square_year_count, "count")
        self._add_spacing_column()

    # Temperature
    def write_avg_temp_by_year(self):
        self.ws.cell(1, self.wu.current_column, "Avg temp. by year")
        self._two_column_table(self.dragonfly.avg_temp_by_year)
        self._add_spacing_column()

    def write_avg_temp_by_square(self):
        self.ws.cell(1, self.wu.current_column, "Avg temp. by square")
        self._two_column_table(self.dragonfly.avg_temp_by_square)
        self._add_spacing_column()

    def write_square_year_temp(self):
        self.ws.cell(1, self.wu.current_column, "Temp. dynamics through years")
        self._three_column_table(self.dragonfly.square_year_temp, "temperature")
        self._add_spacing_column()

    # Wind
    def write_avg_wind_by_year(self):
        self.ws.cell(1, self.wu.current_column, "Avg wind by year")
        self._two_column_table(self.dragonfly.avg_wind_by_year)
        self._add_spacing_column()

    def write_avg_wind_by_square(self):
        self.ws.cell(1, self.wu.current_column, "Avg wind by square")
        self._two_column_table(self.dragonfly.avg_wind_by_square)
        self._add_spacing_column()

    def write_square_year_wind(self):
        self.ws.cell(1, self.wu.current_column, "Wind dynamics through years")
        self._three_column_table(self.dragonfly.square_year_wind, "wind")
        self._add_spacing_column()

    # Clouds 
    def write_avg_clouds_by_year(self):
        self.ws.cell(1, self.wu.current_column, "Avg cloudiness by year")
        self._two_column_table(self.dragonfly.avg_clouds_by_year)
        self._add_spacing_column()

    def write_avg_clouds_by_square(self):
        self.ws.cell(1, self.wu.current_column, "Avg cloudiness by square")
        self._two_column_table(self.dragonfly.avg_clouds_by_square)
        self._add_spacing_column()

    def write_square_year_clouds(self):
        self.ws.cell(1, self.wu.current_column, "Cloudiness dynamics through years")
        self._three_column_table(self.dragonfly.square_year_clouds, "clouds")
        self._add_spacing_column()

    # Water
    def write_year_water_types(self):
        self.ws.cell(1, self.wu.current_column, "Predominant water conditions")
        self.ws.cell(2, self.wu.current_column, "Year")
        self.ws.cell(2, self.wu.current_column + 1, "Tekoss")
        self.ws.cell(2, self.wu.current_column + 2, "Stavoss")
        self._three_column_table_special(self.dragonfly.year_water_types, "Tekoss", "Stavoss")
        self._add_spacing_column()

    def write_square_year_water(self):
        self.ws.cell(1, self.wu.current_column, "Water conditions dynamics")
        self._three_column_table(self.dragonfly.square_year_water, "water")
        self._add_spacing_column()

    # Shading 
    def write_year_shading_types(self):
        self.ws.cell(1, self.wu.current_column, "Predominant shading conditions")
        self.ws.cell(2, self.wu.current_column, "Year")
        self.ws.cell(2, self.wu.current_column + 1, "Dalejs")
        self.ws.cell(2, self.wu.current_column + 2, "Nav")
        self._three_column_table_special(self.dragonfly.year_shading_types, "Dalejs", "Nav")
        self._add_spacing_column()

    def write_square_year_shading(self):
        self.ws.cell(1, self.wu.current_column, "Shading conditions dynamics")
        self._three_column_table(self.dragonfly.square_year_shading, "shading")
        self._add_spacing_column()
    
    # Protected methods 
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
