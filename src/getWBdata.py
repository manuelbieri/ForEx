from datetime import datetime
import http.client
import sqlite3

from _pickle import UnpicklingError

from uuid import uuid4

# avoid possible error when importing wbdata
while True:
    try:
        import wbdata

        break
    except PermissionError:
        pass
    except UnpicklingError:
        pass
    except EOFError:
        pass
    except UnicodeDecodeError:
        pass
    except FileNotFoundError:
        pass

countries = ['AUS', 'BGR', 'BRA', 'CAN', 'CHE', 'CHN', 'CZE', 'DNK', 'GBR', 'HKG', 'HRV', 'HUN', 'IDN', 'ISR', 'IND',
             'JPN', 'KOR', 'MEX', 'MYS', 'NOR', 'NZL', 'PHL', 'POL', 'ROU', 'RUS', 'SWE', 'SGP', 'THA', 'TUR', 'USA',
             'ZAF', 'AUT', 'BEL', 'CYP', 'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'IRL', 'ITA', 'LVA', 'LTU', 'LUX', 'MLT',
             'NLD', 'PRT', 'SVK', 'SVN', 'ESP']

connect_indicators = sqlite3.connect('database/source.db')
cursor_indicators = connect_indicators.cursor()
indicator_list = cursor_indicators.execute(
    "select source, id, id_wb, name_wb from indicator where (max_year='2018' or max_year='2019') and average_datapoints > 25 and indicated_number=50;").fetchall()
connect_indicators.close()

connect_data = sqlite3.connect('database/datasets.db')
cursor_data = connect_data.cursor()

print(len(indicator_list))

for country in countries:
    print('###################################################################################################')
    for indicator in indicator_list:
        pass