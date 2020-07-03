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

# sources 44 does not respond
# sources 34, 67, 71 only return ValueErrors

sources = ['2', '11', '12', '14', '16', '18', '20', '22', '23', '25', '27', '28', '29', '30', '31', '32', '33', '35',
           '36', '37', '38', '39', '40', '41', '43', '45', '46', '50', '54', '57', '58', '59', '60', '61', '62', '63',
           '64', '65', '66', '69', '70', '72', '73', '75']

data_date = (datetime(2000, 1, 1), datetime(2020, 1, 1))

countries_complete = ['AW', 'AF', 'AO', 'AX', 'AL', 'AD', 'AE', 'AR', 'AM', 'AS', 'TF', 'AG', 'AU', 'AT', 'AZ', 'BI',
                      'BE', 'BJ', 'BF', 'BD', 'BG', 'BH', 'BS', 'BA', 'BY', 'BZ', 'BM', 'BO', 'BR', 'BB', 'BN', 'BT',
                      'BW', 'CF', 'CA', 'CH', 'CL', 'CN', 'CI', 'CM', 'CD', 'CG', 'CO', 'KM', 'CV', 'CR', 'CU', 'CW',
                      'KY', 'CY', 'CZ', 'DE', 'DJ', 'DM', 'DK', 'DO', 'DZ', 'EC', 'EG', 'ER', 'ES', 'EE', 'ET', 'FI',
                      'FJ', 'FR', 'FO', 'FM', 'GA', 'GB', 'GE', 'GH', 'GI', 'GN', 'GM', 'GW', 'GQ', 'GR', 'GD', 'GL',
                      'GT', 'GU', 'GY', 'HK', 'HN', 'HR', 'HT', 'HU', 'ID', 'IM', 'IN', 'IE', 'IR', 'IQ', 'IS', 'IL',
                      'IT', 'JM', 'JO', 'JP', 'KZ', 'KE', 'KG', 'KH', 'KI', 'KN', 'KR', 'KW', 'LA', 'LB', 'LR', 'LY',
                      'LC', 'LI', 'LK', 'LS', 'LT', 'LU', 'LV', 'MO', 'MF', 'MA', 'MC', 'MD', 'MG', 'MV', 'MX', 'MH',
                      'MK', 'ML', 'MT', 'MM', 'ME', 'MN', 'MP', 'MZ', 'MR', 'MQ', 'MU', 'MW', 'MY', 'NA', 'NC', 'NE',
                      'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NZ', 'OM', 'PK', 'PA', 'PE', 'PH', 'PW', 'PG', 'PL', 'PR',
                      'KP', 'PT', 'PY', 'PS', 'PF', 'QA', 'RO', 'RU', 'RW', 'SA', 'SD', 'SN', 'SG', 'SH', 'SB', 'SL',
                      'SV', 'SM', 'SO', 'RS', 'SS', 'ST', 'SR', 'SK', 'SI', 'SE', 'SZ', 'SX', 'SC', 'SY', 'TC', 'TD',
                      'TG', 'TH', 'TJ', 'TM', 'TL', 'TO', 'TT', 'TN', 'TR', 'TV', 'TZ', 'UG', 'UA', 'UY', 'US', 'UZ',
                      'VC', 'VE', 'VG', 'VI', 'VN', 'VU', 'WS', 'YE', 'ZA', 'ZM', 'ZW']

countries_alpha_2 = ['AU', 'BG', 'BR', 'CA', 'CH', 'CN', 'CZ', 'DK', 'GB', 'HK', 'HR', 'HU', 'ID', 'IL', 'IN', 'JP',
                     'KR', 'MX', 'MY', 'NO', 'NZ', 'PH', 'PL', 'RO', 'RU', 'SE', 'SG', 'TH', 'TR', 'US', 'ZA', 'AT',
                     'BE', 'CY', 'EE', 'FI', 'FR', 'DE', 'GR', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PT', 'SK',
                     'SI', 'ES']

countries = ['AUS', 'BGR', 'BRA', 'CAN', 'CHE', 'CHN', 'CZE', 'DNK', 'GBR', 'HKG', 'HRV', 'HUN', 'IDN', 'ISR', 'IND',
             'JPN', 'KOR', 'MEX', 'MYS', 'NOR', 'NZL', 'PHL', 'POL', 'ROU', 'RUS', 'SWE', 'SGP', 'THA', 'TUR', 'USA',
             'ZAF', 'AUT', 'BEL', 'CYP', 'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'IRL', 'ITA', 'LVA', 'LTU', 'LUX', 'MLT',
             'NLD', 'PRT', 'SVK', 'SVN', 'ESP']

number_of_countries = int(len(countries))

process_id = str(uuid4())
print('###########################################################################################################')
print('Process id', process_id)
print('###########################################################################################################')

for source in sources:
    # control if source is already handled

    source_control_file = open('Properties/source_control.txt', 'r+')
    source_control = source_control_file.read()
    if int(source_control) >= int(source):
        print(source, 'already handled')
        continue
    else:
        source_control_file.seek(0)
        source_control_file.write(source)
    source_control_file.close()

    # get indicators
    indicators = wbdata.get_indicator(source=source)
    # init progress
    number_of_indicators = len(indicators)
    indicator_counter = 0

    print('###########################################################################################################')
    print('Starting source', source, 'with', number_of_indicators, 'indicators')
    print('###########################################################################################################')

    for indicator in indicators:
        counter = 0  # count valid data points per indicator
        indicated_countries = []  # all countries with valid values
        date_range = []  # range of year of sampling of data

        while True:  # for multi use
            try:
                connect = sqlite3.connect('database/source.db')
                cursor = connect.cursor()
                # check if indicator is already inserted
                result = cursor.execute("select id_wb from indicator where id_wb=?", (indicator['id'],)).fetchall()
                connect.close()
                if len(result) != 0:
                    print(indicator['id'], 'already in database')
                    in_database = True
                else:
                    in_database = False
                break

            except sqlite3.OperationalError:
                print('sqliteError1')

        if in_database is True:
            # progress
            indicator_counter += 1
            print('#', int(indicator_counter / number_of_indicators * 100), ' percent of the indicators done in source',
                  source, 'at', datetime.now().time())
            continue

        try:
            data = wbdata.get_data(indicator['id'], country=countries, convert_date=False, pandas=False)
        except TypeError:
            # print('TypeError1')
            continue
        except ValueError:
            # print('ValueError1')
            continue

        for country in countries_alpha_2:
            # filter data
            for i in data:
                if i['country']['id'] == country:
                    try:
                        point = float(i['value'])
                        # print(point)
                        # print(type(point))

                        if point == 0:
                            # mostly not measured values
                            # print('zero')
                            pass
                        else:
                            # valid data points
                            counter += 1
                            indicated_countries.append(country)
                            date_range.append(i['date'])

                    except TypeError:
                        # print('TypeError2')
                        pass
                    except ValueError:
                        # print('ValueError2')
                        pass
                    except IndexError:
                        # print('IndexError2')
                        pass
                    except http.client.InvalidURL:
                        # print('ConnectionError2')
                        pass

        # check quality of indicator
        indicated_number_list = list(set(indicated_countries))  # remove duplicates
        indicated_number = len(indicated_number_list)  # number of countries with valid data points
        indicated_countries_str = ','.join(indicated_number_list)

        try:
            max_date = max(date_range)
            min_date = min(date_range)
        except ValueError:
            max_date = None
            min_date = None

        try:
            average = counter / indicated_number  # average data points collected per country
        except ZeroDivisionError:
            average = 0  # if no data points were collected

        print(indicated_number, 'of', number_of_countries, 'countries indicated from', min_date, 'to', max_date)
        print(average, 'average datapoints')

        rating = ''

        # filter indicators and distribute rating
        if indicated_number >= (number_of_countries * 1) and average >= 30 and max_date == '2019':
            rating = 'A'

        elif indicated_number >= (number_of_countries * 1) and average >= 20 and max_date == '2019':
            rating = 'B'

        elif indicated_number >= (number_of_countries * 1) and average >= 10 and max_date == '2019':
            rating = 'C'

        elif indicated_number >= (number_of_countries * 1) and average >= 2 and max_date == '2019':
            rating = 'D'

        elif indicated_number >= (number_of_countries * 1) and average >= 30:
            rating = 'E'

        elif indicated_number >= (number_of_countries * 1) and average >= 20:
            rating = 'F'

        elif indicated_number >= (number_of_countries * 1) and average >= 10:
            rating = 'G'

        elif indicated_number >= (number_of_countries * 0.9) and average >= 30:
            rating = 'H'

        elif indicated_number >= (number_of_countries * 0.9) and average >= 20:
            rating = 'I'

        elif indicated_number >= (number_of_countries * 0.9) and average >= 20:
            rating = 'J'

        elif indicated_number >= (number_of_countries * 0.8) and average >= 30:
            rating = 'K'

        elif indicated_number >= (number_of_countries * 0.8) and average >= 20:
            rating = 'L'

        # low quality indicators
        else:
            rating = 'X'

        # append indicator to database
        while True:  # for multi use
            try:
                connect = sqlite3.connect('database/source.db')
                cursor = connect.cursor()
                # second check if indicator exists
                result = cursor.execute("select id_wb from indicator where id_wb=?", (indicator['id'],)).fetchall()
                if len(result) != 0:
                    print(indicator['id'], 'already in database')
                    break
                # insert indicator
                cursor.execute(
                    '''INSERT INTO indicator(source, id_wb, name_wb, rating, datapoints, average_datapoints, indicated_number, indicated_names, min_year, max_year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (source, indicator['id'], indicator['name'], rating, counter, average, indicated_number,
                     indicated_countries_str, min_date, max_date))
                connect.commit()
                connect.close()
                print(indicator['id'], 'appended to database')
                break
            except sqlite3.OperationalError:
                print('sqliteError2')

        # progress
        indicator_counter += 1
        print('#', int(indicator_counter / number_of_indicators * 100), ' percent of the indicators done in source',
              source,
              'at', datetime.now().time())
