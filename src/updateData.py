from forex_python.converter import CurrencyRates
import forex_python

from http.client import HTTPConnection
from socket import gaierror

from datetime import datetime, date, timedelta
import sqlite3

from sys import exit

print('###############################################################################################################')
print("Start update")
print('###############################################################################################################')

c = CurrencyRates()
"""
Supported currencies:
EUR - Euro Member Countries
IDR - Indonesia Rupiah
BGN - Bulgaria Lev
ILS - Israel Shekel
GBP - United Kingdom Pound
DKK - Denmark Krone
CAD - Canada Dollar
JPY - Japan Yen
HUF - Hungary Forint
RON - Romania New Leu
MYR - Malaysia Ringgit
SEK - Sweden Krona
SGD - Singapore Dollar
HKD - Hong Kong Dollar
AUD - Australia Dollar
CHF - Switzerland Franc
KRW - Korea (South) Won
CNY - China Yuan Renminbi
TRY - Turkey Lira
HRK - Croatia Kuna
NZD - New Zealand Dollar
THB - Thailand Baht
USD - United States Dollar
NOK - Norway Krone
RUB - Russia Ruble
INR - India Rupee
MXN - Mexico Peso
CZK - Czech Republic Koruna
BRL - Brazil Real
PLN - Poland Zloty
PHP - Philippines Peso
ZAR - South Africa Rand
"""

currencies = ['IDR', 'BGN', 'EUR', 'ILS', 'GBP', 'DKK', 'CAD', 'JPY', 'HUF', 'RON', 'MYR', 'SEK', 'SGD', 'HKD', 'AUD',
              'CHF', 'KRW', 'CNY', 'TRY', 'HRK', 'NZD', 'THB', 'USD', 'NOK', 'RUB', 'INR', 'MXN', 'CZK', 'BRL', 'PLN',
              'PHP', 'ZAR']

delta = timedelta(days=1)

online = False

while online is False:
    try:
        connection_test = HTTPConnection('www.ecb.europa.eu', timeout=3)
        connection_test.request("HEAD", "/")
        connection_test.close()
        online = True
    except gaierror:
        retry = input('No connection available. Retry? [y/n]')
        if retry.lower() == 'n':
            exit('Aborted. No connection possible')

connect = sqlite3.connect('database/currencies.db')
cursor = connect.cursor()

for base_currency in currencies:
    print('###################################################################################################')
    print(base_currency)
    print('###################################################################################################')

    # set other date than in database to correct mistakes
    # latest_update = datetime.strptime('2020-03-21', '%Y-%m-%d').date() + delta

    latest_update = datetime.strptime(cursor.execute('SELECT date FROM ' + base_currency).fetchall()[-1][0],
                                      '%Y-%m-%d').date() + delta

    today = date.today()

    if today > latest_update:
        while today > latest_update:
            print('###################################################################################################')
            print(latest_update)
            print('###################################################################################################')

            cursor.execute("insert into " + base_currency + "(date) values (?)", [str(latest_update)])

            try:
                currencies_date = c.get_rates(base_currency, latest_update)
                for quote_currency in currencies_date:
                    if quote_currency == base_currency:
                        continue
                    if quote_currency in currencies:
                        cursor.execute("UPDATE " + base_currency + " SET " + quote_currency + '_' + base_currency + " = ? WHERE date = ?",
                                       (currencies_date[quote_currency], str(latest_update)))

            except forex_python.converter.RatesNotAvailableError:
                print(latest_update)
                print("NO DATA available")

            latest_update += delta
    else:
        print("No update necessary")

    print(base_currency + " is up-to-date and saved")

connect.commit()
connect.close()
print('###################################################################################################')
print("Update done")
print('###################################################################################################')
