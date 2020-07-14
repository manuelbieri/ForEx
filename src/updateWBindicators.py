import sqlite3

connect_1 = sqlite3.connect('database/data.db')
cursor_1 = connect_1.cursor()
indicator_list = cursor_1.execute('PRAGMA table_info(CHE)').fetchall()
connect_1.close()

print(indicator_list)

"""
connect_2 = sqlite3.connect('database/source.db')
cursor_2 = connect_2.cursor()

connect_2.close()
connect_2.commit()
"""
