"""Prepares and writes data to XML"""

from app.file_writer import FileWriter

import xml.etree.ElementTree as et
import xml.dom.minidom
from typing import Self

class XmlWriter(FileWriter):
    # prepares data in the tree form and returns a root
    def get_data(self: Self, dragonfly_name: str) -> et.Element:
        root = et.Element('Dragonfly')
        root.set('dragonfly', dragonfly_name)

        elements = {}

        elements['count'] = et.SubElement(root, 'Count')

        elements['total_count'] = et.SubElement(elements['count'], 'TotalCount')
        elements['total_count'].text = str(self.dragonfly.total_count)

        elements['total_count_by_year'] = {}
        count_by_year = et.SubElement(elements['count'], 'CountByYear')
        
        for key, val in self.dragonfly.count_by_year.items():
            elements['total_count_by_year'][key] = et.SubElement(count_by_year, 'Count')
            elements['total_count_by_year'][key].set('year', str(key))
            elements['total_count_by_year'][key].text = str(val)

        elements['total_count_by_square'] = {}
        count_by_square = et.SubElement(elements['count'], 'CountBySquare')

        for key, val in self.dragonfly.count_by_square.items():
            elements['total_count_by_square'][key] = et.SubElement(count_by_square, 'Count')
            elements['total_count_by_square'][key].set('square', str(key))
            elements['total_count_by_square'][key].text = str(val)

        elements['temperature'] = et.SubElement(root, 'Temperature')

        elements['avg_temp_by_year'] = {}
        avg_temp_by_year = et.SubElement(elements['temperature'], 'AvgTempByYear')

        for key, val in self.dragonfly.avg_temp_by_year.items():
            elements['avg_temp_by_year'][key] = et.SubElement(avg_temp_by_year, 'Temp')
            elements['avg_temp_by_year'][key].set('year', str(key))
            elements['avg_temp_by_year'][key].text = str(val)

        elements['square_year_temp'] = {}
        elements['square_year_temp']['root'] = et.SubElement(elements['temperature'], 'SquareYearTemp')
        squares = []

        for el in self.dragonfly.square_year_temp:
            if el['square'] not in squares:
                squares.append(el['square'])

                elements['square_year_temp'][el['square']] = et.SubElement(elements['square_year_temp']['root'], 'Square')
                elements['square_year_temp'][el['square']].set('square', str(el['square']))

            elements['square_year_temp'][str(el['square']) + str(el['year'])] = et.SubElement(elements['square_year_temp'][el['square']], 'Temperature')
            elements['square_year_temp'][str(el['square']) + str(el['year'])].set('year', str(el['year']))
            elements['square_year_temp'][str(el['square']) + str(el['year'])].text = str(el['temperature'])

        elements['avg_temp_by_square'] = {}
        avg_temp_by_square = et.SubElement(elements['temperature'], 'AvgTempBySquare')

        for key, val in self.dragonfly.avg_temp_by_square.items():
            elements['avg_temp_by_square'][key] = et.SubElement(avg_temp_by_square, 'Temp')
            elements['avg_temp_by_square'][key].set('square', str(key))
            elements['avg_temp_by_square'][key].text = str(val)

        elements['wind'] = et.SubElement(root, 'Wind')

        elements['avg_wind_by_year'] = {}
        avg_wind_by_year = et.SubElement(elements['wind'], 'AvgWindByYear')

        for key, val in self.dragonfly.avg_wind_by_year.items():
            elements['avg_wind_by_year'][key] = et.SubElement(avg_wind_by_year, 'Wind')
            elements['avg_wind_by_year'][key].set('year', str(key))
            elements['avg_wind_by_year'][key].text = str(val)

        elements['square_year_wind'] = {}
        elements['square_year_wind']['root'] = et.SubElement(elements['wind'], 'SquareYearWind')
        squares = []

        for el in self.dragonfly.square_year_wind:
            if el['square'] not in squares:
                squares.append(el['square'])

                elements['square_year_wind'][el['square']] = et.SubElement(elements['square_year_wind']['root'], 'Square')
                elements['square_year_wind'][el['square']].set('square', str(el['square']))

            elements['square_year_wind'][str(el['square']) + str(el['year'])] = et.SubElement(elements['square_year_wind'][el['square']], 'Wind')
            elements['square_year_wind'][str(el['square']) + str(el['year'])].set('year', str(el['year']))
            elements['square_year_wind'][str(el['square']) + str(el['year'])].text = str(el['wind'])

        elements['avg_wind_by_square'] = {}
        avg_wind_by_square = et.SubElement(elements['wind'], 'AvgWindBySquare')

        for key, val in self.dragonfly.avg_wind_by_square.items():
            elements['avg_wind_by_square'][key] = et.SubElement(avg_wind_by_square, 'Wind')
            elements['avg_wind_by_square'][key].set('square', str(key))
            elements['avg_wind_by_square'][key].text = str(val)

        elements['cloudiness'] = et.SubElement(root, 'Cloudiness')

        elements['avg_cloudiness_by_year'] = {}
        avg_cloudiness_by_year = et.SubElement(elements['cloudiness'], 'AvgCloudinessByYear')

        for key, val in self.dragonfly.avg_clouds_by_year.items():
            elements['avg_cloudiness_by_year'][key] = et.SubElement(avg_cloudiness_by_year, 'Cloudiness')
            elements['avg_cloudiness_by_year'][key].set('year', str(key))
            elements['avg_cloudiness_by_year'][key].text = str(val)

        elements['square_year_cloudiness'] = {}
        elements['square_year_cloudiness']['root'] = et.SubElement(elements['cloudiness'], 'SquareYearCloudiness')
        squares = []

        for el in self.dragonfly.square_year_clouds:
            if el['square'] not in squares:
                squares.append(el['square'])

                elements['square_year_cloudiness'][el['square']] = et.SubElement(elements['square_year_cloudiness']['root'], 'Square')
                elements['square_year_cloudiness'][el['square']].set('square', str(el['square']))

            elements['square_year_cloudiness'][str(el['square']) + str(el['year'])] = et.SubElement(elements['square_year_cloudiness'][el['square']], 'Cloudiness')
            elements['square_year_cloudiness'][str(el['square']) + str(el['year'])].set('year', str(el['year']))
            elements['square_year_cloudiness'][str(el['square']) + str(el['year'])].text = str(el['clouds'])

        elements['avg_cloudiness_by_square'] = {}
        avg_cloudiness_by_square = et.SubElement(elements['cloudiness'], 'AvgCloudinessBySquare')

        for key, val in self.dragonfly.avg_clouds_by_square.items():
            elements['avg_cloudiness_by_square'][key] = et.SubElement(avg_cloudiness_by_square, 'Cloudiness')
            elements['avg_cloudiness_by_square'][key].set('square', str(key))
            elements['avg_cloudiness_by_square'][key].text = str(val)

        elements['water'] = et.SubElement(root, 'Water')

        elements['year_water_types'] = {}
        elements['year_water_types']['root'] = et.SubElement(elements['water'], 'YearWaterTypes')

        for key, val in self.dragonfly.year_water_types.items():
            elements['year_water_types'][key] = et.SubElement(elements['year_water_types']['root'], 'Year')
            elements['year_water_types'][key].set('year', str(key))

            try:
                val['Tekoss'] = str(val['Tekoss'])
                elements['year_water_types']['Tekoss' + str(key)] = et.SubElement(elements['year_water_types'][key], 'Tekoss')
                elements['year_water_types']['Tekoss' + str(key)].text = val['Tekoss']
            except:
                pass

            try:
                val['Stavoss'] = str(val['Stavoss'])
                elements['year_water_types']['Stavoss' + str(key)] = et.SubElement(elements['year_water_types'][key], 'Stavoss')
                elements['year_water_types']['Stavoss' + str(key)].text = val['Stavoss']
            except:
                pass

        elements['square_year_water'] = {}
        elements['square_year_water']['root'] = et.SubElement(elements['water'], 'SquareYearWater')
        squares = []

        for el in self.dragonfly.square_year_water:
            if el['square'] not in squares:
                squares.append(el['square'])

                elements['square_year_water'][el['square']] = et.SubElement(elements['square_year_water']['root'], 'Square')
                elements['square_year_water'][el['square']].set('square', str(el['square']))

            elements['square_year_water'][str(el['square']) + str(el['year'])] = et.SubElement(elements['square_year_water'][el['square']], 'Water')
            elements['square_year_water'][str(el['square']) + str(el['year'])].set('year', str(el['year']))
            elements['square_year_water'][str(el['square']) + str(el['year'])].text = str(el['water'])

        elements['shading'] = et.SubElement(root, 'Shading')

        elements['year_shading_types'] = {}
        elements['year_shading_types']['root'] = et.SubElement(elements['shading'], 'YearShadingTypes')

        for key, val in self.dragonfly.year_shading_types.items():
            elements['year_shading_types'][key] = et.SubElement(elements['year_shading_types']['root'], 'Year')
            elements['year_shading_types'][key].set('year', str(key))

            try:
                val['Nav'] = str(val['Nav'])
                elements['year_shading_types']['Nav' + str(key)] = et.SubElement(elements['year_shading_types'][key], 'Nav')
                elements['year_shading_types']['Nav' + str(key)].text = val['Nav']
            except:
                pass

            try:
                val['Dalejs'] = str(val['Dalejs'])
                elements['year_shading_types']['Dalejs' + str(key)] = et.SubElement(elements['year_shading_types'][key], 'Dalejs')
                elements['year_shading_types']['Dalejs' + str(key)].text = val['Dalejs']
            except:
                pass

        elements['square_year_shading'] = {}
        elements['square_year_shading']['root'] = et.SubElement(elements['shading'], 'SquareYearShading')
        squares = []

        for el in self.dragonfly.square_year_shading:
            if el['square'] not in squares:
                squares.append(el['square'])

                elements['square_year_shading'][el['square']] = et.SubElement(elements['square_year_shading']['root'], 'Square')
                elements['square_year_shading'][el['square']].set('square', str(el['square']))

            elements['square_year_shading'][str(el['square']) + str(el['year'])] = et.SubElement(elements['square_year_shading'][el['square']], 'Shading')
            elements['square_year_shading'][str(el['square']) + str(el['year'])].set('year', str(el['year']))
            elements['square_year_shading'][str(el['square']) + str(el['year'])].text = str(el['shading'])

        return root

    # saves given tree to XML file
    @staticmethod
    def save(data: et.ElementTree, output_filename: str, min: bool):
        if min:
            data.write(output_filename, encoding = 'utf-8', xml_declaration = True)
        else:
            tree_string = et.tostring(data.getroot(), 'utf-8')

            reparsed = xml.dom.minidom.parseString(tree_string)
            pretty_xml = reparsed.toprettyxml(indent = '    ')

            with open(output_filename, 'w', encoding = 'utf-8') as file:
                file.write(pretty_xml)
