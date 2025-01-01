"""
Author: Kelv Gooding
Date Created: 2023-05-16
Date Updated: 2025-01-01
Version: 1.3
"""

# Modules

from modules import db_check
from psnawp_api import PSNAWP
import auth
import os
import sqlite3

# General Variables

# Default base path is root. Update the base path based on your environment.

base_path = os.path.dirname(os.path.abspath(__file__))
db_filename = 'psn_game_collection.db'
sql_script = f'{base_path}/scripts/sql/create_tables.sql'

# SQLite3 Variables

db_check.check_db(f'{base_path}', f'{db_filename}', f'{sql_script}')
conn = db_check.sqlite3.connect(os.path.join(base_path, db_filename), check_same_thread=False)
c = conn.cursor()

# PSNAWP Variables

psnawp = PSNAWP(auth.api_auth['psn_token'])
psn_connect = psnawp.me()

# Delete data from all database tables before insetting new data.

c.execute('DELETE FROM PS4')
c.execute('DELETE FROM PS5')
c.execute('DELETE FROM COLLECTION')

# Iterate data and insert into all database tables.

for i in psn_connect.title_stats():

    # Temporary Fix - Insert data into the COLLECTION table, then use SQL to seperate data per console based on the title_id code.
    # Solution - This should be split by using the platform to stop the 200 limit being used.

    c.execute(f'INSERT INTO COLLECTION VALUES ("{i.title_id}", "{i.name.upper()}", "{str(i.first_played_date_time)[0:19]}", "{str(i.last_played_date_time)[0:19]}", "{str(i.category).replace("PlatformCategory.", "")}", "{i.play_count}", "{int(i.play_duration.seconds / 60)}", "{i.image_url}");')

# PS5 Table

c.execute('INSERT INTO PS5 SELECT * FROM COLLECTION WHERE title_id LIKE "%PPSA%";')
c.execute('UPDATE PS5 SET platform = "PS5" WHERE platform = "UNKNOWN"')

# PS4 Table

c.execute('INSERT INTO PS4 SELECT * FROM COLLECTION WHERE title_id LIKE "%CUSA%";')
c.execute('UPDATE PS4 SET platform = "PS4" WHERE platform = "UNKNOWN"')

conn.commit()
