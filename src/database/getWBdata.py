from datetime import datetime
import sqlite3

from _pickle import UnpicklingError

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

connect_indicators = sqlite3.connect('source.db')
cursor_indicators = connect_indicators.cursor()
indicator_list = cursor_indicators.execute(
    "select source, id, id_wb, name_wb from indicator where (max_year='2018' or max_year='2019') and average_datapoints > 25 and indicated_number=50;").fetchall()
connect_indicators.close()
print(len(indicator_list))
# print(indicator_list)

for country in countries:
    source_control_file = open('database/country_control.txt', 'a+')
    source_control_file.seek(0)
    source_control = source_control_file.read()
    source_control = source_control.split(',')
    if country in source_control:
        print(country, 'already handled')
        continue
    else:
        source_control_file.write(',' + country)
    source_control_file.close()

    # init progress
    number_of_indicators = len(indicator_list)
    indicator_counter = 0

    print('###########################################################################################################')
    print('Starting', country)
    print('###########################################################################################################')

    connect_data = sqlite3.connect('data.db')
    cursor_data = connect_data.cursor()
    try:
        cursor_data.execute('CREATE TABLE ' + country + ' (pkey integer PRIMARY KEY, date text)')
    except sqlite3.OperationalError:
        pass
    for year in range(1960, 2020):
        cursor_data.execute('''INSERT INTO ''' + country + ''' (pkey, date) VALUES (?, ?)''', [year - 1959, year])

    connect_data.commit()
    connect_data.close()

    for indicator in indicator_list:
        print(indicator[2], country)
        try:
            data = wbdata.get_data(indicator[2], country=country)
        except TypeError:
            # print('TypeError1')
            continue
        except ValueError:
            # print('ValueError1')
            continue

        connect_data = sqlite3.connect('data.db')
        cursor_data = connect_data.cursor()

        try:
            cursor_data.execute('''ALTER TABLE ''' + country + ''' ADD COLUMN D_''' + str(indicator[1]) + ''' REAL''')
        except sqlite3.OperationalError:
            print('sqliteError1')

        for point in data:
            # append data to database
            while True:  # for multi use
                try:
                    # insert indicator
                    cursor_data.execute('UPDATE ' + country + ' SET D_' + str(indicator[1]) + '=? WHERE date=?',
                                        [point["value"], point["date"]])
                    break
                except sqlite3.OperationalError:
                    print('sqliteError2')

        connect_data.commit()
        connect_data.close()

        # progress
        indicator_counter += 1
        print('#', int(indicator_counter / number_of_indicators * 100), ' percent of the indicators done for',
              country, 'at', datetime.now().time())
