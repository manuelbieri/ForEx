import sqlite3

"""
connect_1 = sqlite3.connect('database/data.db')
cursor_1 = connect_1.cursor()
indicator_list = cursor_1.execute('PRAGMA table_info(CHE)').fetchall()
connect_1.close()

connect_2 = sqlite3.connect('database/source.db')
cursor_2 = connect_2.cursor()

for indicator in indicator_list[2:]:
    id = indicator[1].split('_')[1]
    print(id)

    cursor_2.execute('UPDATE indicator SET status=? WHERE id=?', [1, id])

connect_2.commit()
connect_2.close()
"""

connect_indicators = sqlite3.connect('database/source.db')
cursor_indicators = connect_indicators.cursor()
dataset_combo = cursor_indicators.execute("SELECT id, name_wb FROM indicator WHERE status=1;").fetchall()
connect_indicators.close()

dataset_combo = ['D_' + str(i[0]) + ': ' + i[1] for i in dataset_combo]

print(dataset_combo)


