import sys

from os import startfile as run  # lubuntu issue: cannot import module
from os.path import isfile

from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QWidget, QGridLayout, QLineEdit, \
    QSizePolicy, QCheckBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

try:
    # Include in try/except block for Mac/Linux
    # noinspection PyUnresolvedReferences
    from PyQt5.QtWinExtras import QtWin
    app_id = 'marbl.forex.forex.0.0.3'
    QtWin.setCurrentProcessExplicitAppUserModelID(app_id)
except ImportError:
    pass

import matplotlib.figure as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# LUbuntu only
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import sqlite3

from uuid import uuid4

from datetime import datetime

# Handle high resolution displays:
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

css_colors = ['lightsalmon', 'salmon', 'darksalmon', 'lightcoral', 'indianred', 'crimson', 'firebrick', 'red',
              'darkred', 'coral', 'tomato', 'orangered', 'gold', 'orange', 'darkorange', 'lawngreen', 'chartreuse',
              'limegreen', 'lime', 'forestgreen', 'green', 'darkgreen', 'greenyellow', 'yellowgreen', 'springgreen',
              'mediumspringgreen', 'lightgreen', 'palegreen', 'darkseagreen', 'mediumseagreen', 'seagreen', 'olive',
              'darkolivegreen', 'olivedrab', 'lightcyan', 'cyan', 'aqua', 'aquamarine', 'mediumaquamarine',
              'paleturquoise', 'turquoise', 'mediumturquoise', 'darkturquoise', 'lightseagreen', 'cadetblue',
              'darkcyan', 'teal', 'powderblue', 'lightblue', 'lightskyblue', 'skyblue', 'deepskyblue', 'lightsteelblue',
              'dodgerblue', 'cornflowerblue', 'steelblue', 'royalblue', 'blue', 'mediumblue', 'darkblue', 'navy',
              'midnightblue', 'mediumslateblue', 'slateblue', 'darkslateblue']

currencies = ['IDR', 'BGN', 'EUR', 'ILS', 'GBP', 'DKK', 'CAD', 'JPY', 'HUF', 'RON', 'MYR', 'SEK', 'SGD', 'HKD', 'AUD',
              'CHF', 'KRW', 'CNY', 'TRY', 'HRK', 'NZD', 'THB', 'USD', 'NOK', 'RUB', 'INR', 'MXN', 'CZK', 'BRL', 'PLN',
              'PHP', 'ZAR']

currencies_combo = ['AUD-$  -Australian dollar', 'BGN-BGN-Bulgarian lev', 'BRL-R$ -Brazilian real',
                    'CAD-$  -Canadian dollar',
                    'CHF-Fr.-Swiss franc', 'CNY-¥  -Chinese/Yuan renminbi', 'CZK-Kč -Czech koruna',
                    'DKK-Kr -Danish krone',
                    'EUR-€  -European Euro', 'GBP-£  -British pound', 'HKD-HK$-Hong Kong dollar',
                    'HRK-kn -Croatian kuna',
                    'HUF-Ft -Hungarian forint', 'IDR-Rp -Indonesian rupiah', 'ILS-₪  -Israeli new sheqel',
                    'INR-₹  -Indian rupee',
                    'JPY-¥  -Japanese yen', 'KRW-W  -South Korean won', 'MXN-$  -Mexican peso',
                    'MYR-RM -Malaysian ringgit',
                    'NOK-kr -Norwegian krone', 'NZD-NZ$-New Zealand dollar', 'PHP-₱  -Philippine peso',
                    'PLN-zł -Polish zloty',
                    'RON-L  -Romanian leu', 'RUB-R  -Russian ruble', 'SEK-kr -Swedish krona',
                    'SGD-S$ -Singapore dollar',
                    'THB-฿  -Thai baht', 'TRY-TRY-Turkish new lira', 'USD-US$-United States dollar',
                    'ZAR-R  -South African rand']

countries_combo = ['AUS - Australia', 'AUT - Austria', 'BEL - Belgium', 'BGR - Bulgaria', 'BRA - Brazil',
                   'CAN - Canada', 'CHE - Switzerland', 'CHN - China', 'CYP - Cyprus', 'CZE - Czechia', 'DEU - Germany',
                   'DNK - Denmark', 'ESP - Spain', 'EST - Estonia', 'FIN - Finland', 'FRA - France',
                   'GBR - United Kingdom', 'GRC - Greece', 'HKG - Hong Kong', 'HRV - Croatia', 'HUN - Hungary',
                   'IDN - Indonesia', 'IND - India', 'IRL - Ireland', 'ISR - Israel', 'ITA - Italy', 'JPN - Japan',
                   'KOR - Korea, Republic of', 'LTU - Lithuania', 'LUX - Luxembourg', 'LVA - Latvia', 'MEX - Mexico',
                   'MLT - Malta', 'MYS - Malaysia', 'NLD - Netherlands', 'NOR - Norway', 'NZL - New Zealand',
                   'PHL - Philippines', 'POL - Poland', 'PRT - Portugal', 'ROU - Romania', 'RUS - Russian Federation',
                   'SGP - Singapore', 'SVK - Slovakia', 'SVN - Slovenia', 'SWE - Sweden', 'THA - Thailand',
                   'TUR - Turkey', 'USA - United States', 'ZAF - South Africa']

connect_indicators = sqlite3.connect('database/source.db')
cursor_indicators = connect_indicators.cursor()
dataset_combo = cursor_indicators.execute("SELECT id, name_wb FROM indicator WHERE status=1;").fetchall()
connect_indicators.close()

dataset_combo = ['D_' + str(i[0]) + ': ' + i[1] for i in dataset_combo]


class App(QMainWindow):
    def __init__(self):
        # noinspection PyArgumentList
        super().__init__()
        self.title = 'FOReign EXchange'
        self.font = QFont('Courier', 10)
        self.setWindowIcon(QIcon('Icon/favicon.ico'))

        # self.setWindowState(Qt.WindowMaximized)

        self.move(50, 50)

        # set properties
        self.setWindowTitle(self.title)
        self.setFont(self.font)

        # create main widget and grid layout
        self.mainWidget = QWidget()
        self.gridLayout = QGridLayout(self.mainWidget)
        self.gridLayout.setSpacing(2)

        self.setCentralWidget(self.mainWidget)

        self.dict = {}

        # initialize widgets
        self.base_currency = QComboBox()
        self.base_currency.setToolTip('Select base currency')
        self.base_currency.addItems(currencies_combo)

        self.quote_currency = QComboBox()
        self.quote_currency.setToolTip('Select quote currency')
        self.quote_currency.addItems(currencies_combo)
        self.check1 = QCheckBox("show")

        self.base_currency1 = QComboBox()
        self.base_currency1.setToolTip('Select base currency')
        self.base_currency1.addItems(currencies_combo)

        self.quote_currency1 = QComboBox()
        self.quote_currency1.setToolTip('Select quote currency')
        self.quote_currency1.addItems(currencies_combo)
        self.check2 = QCheckBox("show")

        self.country1 = QComboBox()
        self.country1.setToolTip('Select country')
        self.country1.addItems(countries_combo)

        self.data1 = QComboBox()
        self.data1.setToolTip('Select data set')
        self.data1.addItems(dataset_combo)
        self.check3 = QCheckBox("show")

        self.country2 = QComboBox()
        self.country2.setToolTip('Select country')
        self.country2.addItems(countries_combo)

        self.data2 = QComboBox()
        self.data2.setToolTip('Select data set')
        self.data2.addItems(dataset_combo)
        self.check4 = QCheckBox("show")

        self.plot_button = QPushButton(self)
        self.plot_button.setText('Plot')
        self.plot_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.plot_button.clicked.connect(self.callback)

        self.command_line = QLineEdit()
        self.command_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.cmd_button = QPushButton(self)
        self.cmd_button.setText('cmd')
        self.cmd_button.clicked.connect(lambda: CommandParser(self.command_line.text()))

        self.plot_widget = PlotCanvas(self.mainWidget)

        # add widgets to window
        self.gridLayout.addWidget(self.base_currency, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.quote_currency, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.check1, 2, 0, 1, 1)

        self.gridLayout.addWidget(self.base_currency1, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.quote_currency1, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.check2, 2, 1, 1, 1)

        self.gridLayout.addWidget(self.country1, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.data1, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.check3, 2, 2, 1, 1)

        self.gridLayout.addWidget(self.country2, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.data2, 1, 3, 1, 1)
        self.gridLayout.addWidget(self.check4, 2, 3, 1, 1)

        self.gridLayout.addWidget(self.plot_button, 0, 4, 2, 1)

        for widget in [self.base_currency, self.quote_currency, self.base_currency1, self.quote_currency1]:
            widget.setMinimumWidth(190)
            widget.setMaximumWidth(320)

        for widget in [self.country1, self.data1, self.country2, self.data2]:
            widget.setMinimumWidth(200)
            widget.setMaximumWidth(600)

        self.gridLayout.addWidget(self.command_line, 3, 0, 1, 4)
        self.gridLayout.addWidget(self.cmd_button, 3, 4, 1, 1)

        self.gridLayout.addWidget(self.plot_widget, 4, 0, 1, 5)

        self.show()

    def callback(self):
        bc1 = self.base_currency.currentText()
        qc1 = self.quote_currency.currentText()
        exc1 = self.check1.isChecked()

        bc2 = self.base_currency1.currentText()
        qc2 = self.quote_currency1.currentText()
        exc2 = self.check2.isChecked()

        co1 = self.country1.currentText()
        da1 = self.data1.currentText()
        dac1 = self.check3.isChecked()

        co2 = self.country2.currentText()
        da2 = self.data2.currentText()
        dac2 = self.check4.isChecked()

        self.dict = {'bc1': [bc1], 'qc1': [qc1], 'exc1': [exc1], 'bc2': [bc2], 'qc2': [qc2], 'exc2': [exc2],
                     'co1': [co1], 'da1': [da1], 'dac1': [dac1], 'co2': [co2], 'da2': [da2], 'dac2': [dac2]}

        if exc1 or exc2 or dac1 or dac2:
            self.plot_widget.plot(self.dict)


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=6, post_data=None):
        # LUbuntu only (otherwise no image can be printed on lubuntu)
        # canvas = FigureCanvas(self)
        self.fig = plt.Figure(figsize=(width, height))
        FigureCanvas.__init__(self, self.fig)
        if post_data is not None:
            FigureCanvas.updateGeometry(self)
            self.setParent(parent)

        # colors for plots
        self.color_control = len(css_colors) - 1
        self.colors = css_colors
        self.color_counter = 0

        # initialize lists
        self.dataset_legend = []
        self.currency_legend = []

        self.currency_values = []
        self.dataset_values = []

        self.currency_dates = []
        self.dataset_dates = []

        self.image_path = ''

        self.plot_data = post_data

        self.dataset_plot = self.fig.add_subplot(111)
        self.currency_plot = self.dataset_plot.twinx()

    def __str__(self):
        # save output png image for further use (web app)
        random_filename = str(uuid4())
        self.plot(self.plot_data)

        self.image_path += 'Images\\' + random_filename + '.png'
        self.fig.savefig(self.image_path, dpi=200, bbox_inches='tight')
        return self.image_path

    def plot(self, args):
        # set font
        plt.rcParams['font.serif'] = "Times New Roman"
        plt.rcParams['font.family'] = "serif"

        self.dataset_plot.cla()
        self.currency_plot.cla()

        self.dataset_legend = []
        self.currency_legend = []

        self.currency_values = []
        self.currency_dates = []

        self.dataset_values = []
        self.dataset_dates = []

        # make args to attribute (from post request)
        self.plot_data = args

        # retrieve data from database
        self.retrieve_currency_data()
        self.retrieve_dataset_data()

        # create output image
        self.plot_Image()

    def plot_Image(self):
        if not (not self.currency_legend):
            self.currency_plot.set_ylabel('Exchange rates')
            for item in self.currency_values:
                self.currency_plot.plot(self.currency_dates[self.currency_values.index(item)], item, linewidth=0.2,
                                        color=self.colors[self.color_counter])
                self.color_controller()
            self.currency_plot.legend(self.currency_legend, loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.1))

        if not (not self.dataset_legend):
            self.dataset_plot.set_ylabel('Datasets')
            for item in self.dataset_values:
                self.dataset_plot.plot(self.dataset_dates[self.dataset_values.index(item)], item, linewidth=0.2,
                                       color=self.colors[self.color_counter])
                self.color_controller()

                self.dataset_plot.legend(self.dataset_legend, loc='upper center', ncol=2, bbox_to_anchor=(0.5, -0.05))
        self.draw()

    def retrieve_currency_data(self):
        connect = sqlite3.connect('database/currencies.db')
        cursor = connect.cursor()
        flow_control = [['exc1', 'bc1', 'qc1'], ['exc2', 'bc2', 'qc2']]
        for option in flow_control:
            try:
                if self.plot_data[option[0]][0] in ['true', True]:
                    base_currency = self.plot_data[option[1]][0][:3]
                    quote_currency = self.plot_data[option[2]][0][:3]

                    if base_currency == quote_currency:
                        continue

                    rate = cursor.execute(
                        "SELECT date," + quote_currency + '_' + base_currency + " FROM " + base_currency).fetchall()

                    valid_values = [value[1] for value in rate if value[1] != 0]
                    valid_dates = [datetime.strptime(value[0], '%Y-%m-%d') for value in rate if value[1] != 0]

                    self.currency_values.append(valid_values)
                    self.currency_dates.append(valid_dates)
                    self.currency_legend.append(quote_currency + '/' + base_currency)
            except KeyError:
                pass
        connect.close()

    def retrieve_dataset_data(self):
        flow_control = [['dac1', 'co1', 'da1'], ['dac2', 'co2', 'da2']]
        for option in flow_control:
            try:
                if self.plot_data[option[0]][0] in ['true', True]:
                    country = self.plot_data[option[1]][0][:3]

                    dataset_key = self.plot_data[option[2]][0].split(': ')
                    dataset = dataset_key[1]
                    indicator_key = dataset_key[0]

                    connect = sqlite3.connect("database/data.db")
                    cursor = connect.cursor()
                    data = cursor.execute("SELECT date, " + indicator_key + " FROM " + country).fetchall()
                    connect.close()

                    valid_values = [value[1] for value in data]
                    valid_dates = [datetime.strptime(value[0] + '-12-31', '%Y-%m-%d') for value in data]

                    self.dataset_values.append(valid_values)
                    self.dataset_dates.append(valid_dates)
                    self.dataset_legend.append(dataset + ' - ' + country)
            except KeyError:
                pass

    def color_controller(self):
        self.color_counter += 21
        if (self.color_counter // self.color_control) > 0:
            self.color_counter = self.color_counter % self.color_control


class CommandParser(str):
    def __init__(self, cmd_str):
        super().__init__()
        self.cmd = str(cmd_str).lower().replace(' ', '').split('--')  # filter string and split to list
        try:
            self.cmd.remove('')  # remove empty strings from list
        except ValueError:
            pass

        self.tmp = []
        self.tmp_del = []
        for cmd in self.cmd:
            print(cmd)
            if cmd.find('-') != -1:
                self.tmp_del.append(cmd)
                cmd = cmd.replace('-', '')
                self.tmp.append(cmd)

        self.cmd = [cmd for cmd in self.cmd if (cmd not in self.tmp_del)]

        self.cmd.extend(self.tmp)
        self.tmp.clear()
        self.tmp_del.clear()

        if not (not self.cmd):
            if 'update' in self.cmd:
                if isfile('updateData.exe'):
                    run('updateData.exe')
                elif isfile('updateData.py'):
                    print('no executable updater available, runs with python ')
                    exec(open("updateData.py").read())
                else:
                    print("no updater available")
                self.cmd.remove('update')

            if 'help' in self.cmd:
                self.cmd.remove('help')

        if not (not self.cmd):
            for item in self.cmd:
                print('Command not found:', item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
