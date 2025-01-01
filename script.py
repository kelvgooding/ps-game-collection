"""
Author: Kelvin Gooding
Date Created: 2023-05-16
Date Updated: 2023-07-13
Version: 1.2
"""

# Modules

import auth
from psnawp_api import PSNAWP
import sqlite3
import csv

# PSNAWP Variables

psnawp = PSNAWP(auth.api_auth['psn_token'])
psn_connect = psnawp.me()

# SQLite3 Variables

connection = sqlite3.connect('psn_game_collection.db')
c = connection.cursor()

# Delete data from all database tables before insetting new data.

c.execute('DELETE FROM PS4')
c.execute('DELETE FROM PS5')
c.execute('DELETE FROM COLLECTION')

# Iterate data and insert into all database tables.

for i in psn_connect.title_stats():

    # Temporary Fix - Insert data into the COLLECTION table, then use SQL to seperate data per console based on the title_id code.
    # Solution - This should be split by using the platform to stop the 200 limit being used.

    c.execute(f'INSERT INTO COLLECTION VALUES ("{i.title_id}", "{i.name.upper()}", "{str(i.first_played_date_time)[0:19]}", "{str(i.last_played_date_time)[0:19]}", "{str(i.category).replace("PlatformCategory.", "")}", "{i.play_count}", "{int(i.play_duration.seconds / 60)}", "{i.image_url}");')


import csv

# Open the CSV file in write mode
with open('collection_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow([
        'Title ID', 'Name', 'First Played Date', 'Last Played Date', 'Category', 'Play Count', 'Play Duration (mins)', 'Image URL'
    ])

    # Iterate through the title_stats and write rows
    for i in psn_connect.title_stats():
        writer.writerow([
            i.title_id,
            i.name.upper(),
            str(i.first_played_date_time)[0:19],
            str(i.last_played_date_time)[0:19],
            str(i.category).replace("PlatformCategory.", ""),
            i.play_count,
            int(i.play_duration.seconds / 60),
            i.image_url
        ])

print("Data successfully exported to 'collection_data.csv'")

# PS5 Table

c.execute('INSERT INTO PS5 SELECT * FROM COLLECTION WHERE title_id LIKE "%PPSA%";')
c.execute('UPDATE PS5 SET platform = "PS5" WHERE platform = "UNKNOWN"')

# PS4 Table

c.execute('INSERT INTO PS4 SELECT * FROM COLLECTION WHERE title_id LIKE "%CUSA%";')
c.execute('UPDATE PS4 SET platform = "PS4" WHERE platform = "UNKNOWN"')

connection.commit()