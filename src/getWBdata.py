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

countries = ['CHE', 'GBR', 'ISR', 'IND', 'USA', 'FRA', 'DEU']

connect_indicators = sqlite3.connect('database/source.db')
cursor_indicators = connect_indicators.cursor()
indicator_list = cursor_indicators.execute(
    "select source, id, id_wb, name_wb from indicator where (max_year='2018' or max_year='2019') and average_datapoints > 25 and indicated_number=50;").fetchall()
connect_indicators.close()

print(len(indicator_list))
# print(indicator_list)

for country in countries:
    source_control_file = open('database/country_control.txt', 'a+')
    source_control = source_control_file.read()
    source_control.split(',')
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

    for indicator in indicator_list:
        print(indicator)
        try:
            data = wbdata.get_data(indicator[1], country=countries, convert_date=False, pandas=False)
        except TypeError:
            # print('TypeError1')
            continue
        except ValueError:
            # print('ValueError1')
            continue
        print(data)
        for point in data:
            print(point)
        """
        # append data to database
        while True:  # for multi use
            try:
                connect_data = sqlite3.connect('database/source.db')
                cursor_data = connect_data.cursor()
                # second check if indicator exists
                result = cursor_data.execute("select id_wb from indicator where id_wb=?", (indicator['id'],)).fetchall()
                if len(result) != 0:
                    print(indicator['id'], 'already in database')
                    break
                # insert indicator
                cursor_data.execute(
                    '''INSERT INTO indicator(source, id_wb, name_wb, rating, datapoints, average_datapoints, indicated_number, indicated_names, min_year, max_year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (source, indicator['id'], indicator['name'], rating, counter, average, indicated_number,
                     indicated_countries_str, min_date, max_date))
                connect_data.commit()
                connect_data.close()
                print(indicator['id'], 'appended to database')
                break
            except sqlite3.OperationalError:
                print('sqliteError2')
        """

        # progress
        indicator_counter += 1
        print('#', int(indicator_counter / number_of_indicators * 100), ' percent of the indicators done for',
              country, 'at', datetime.now().time())
