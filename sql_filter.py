import sqlite3
from functions import convert_csv_to_db

connection = sqlite3.connect("event_data.db")
cursor = connection.cursor()

"""
cursor.execute("SELECT * FROM events WHERE date='2088.10.15'")
rows = cursor.fetchall()
print(rows)

new_rows = [('Black Cats', 'Cat City', '2088.11.16.'),
            ('Blue Dinos', 'Dino City', '2088.10.20.')]

cursor.executemany("INSERT INTO events VALUES (?,?,?)", new_rows)
connection.commit()


SQL SCRIPT
add new row in the table
INSERT INTO events VALUES ('Tigers', 'Tiger City', '2088.10.14.')
INSERT INTO temperature VALUES ('25-05-20-08-07-00', 19)
select particular values
SELECT * FROM events WHERE date = '2088.10.15'

data = convert_csv_to_db("fake_temp_data.csv")
print(data)
"""
