"""
Author: Kelv Gooding
Date Created: 2023-05-16
Date Updated: 2025-01-01
Version: 1.4
"""

# Modules

from modules import db_check
from psnawp_api import PSNAWP
import auth
import csv
import os
import sqlite3

# General Variables

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

c.execute('DELETE FROM COLLECTION')

def game_data_db(console):

    c.execute(f'DELETE FROM {console}')

    for i in psn_connect.title_stats():

        # Temporary Fix - Insert data into the COLLECTION table, then use SQL to seperate data per console based on the title_id code.
        # Solution - This should be split by using the platform to stop the 200 limit being used.

        c.execute(f'INSERT INTO COLLECTION VALUES ("{i.title_id}", "{i.name.upper()}", "{str(i.first_played_date_time)[0:19]}", "{str(i.last_played_date_time)[0:19]}", "{str(i.category).replace("PlatformCategory.", "")}", "{i.play_count}", "{int(i.play_duration.seconds / 60)}", "{i.image_url}");')

    c.execute(f'INSERT INTO {console} SELECT * FROM COLLECTION WHERE title_id LIKE "%PPSA%";')
    c.execute(f'UPDATE {console} SET platform = "{console}" WHERE platform = "UNKNOWN"')

    conn.commit()

game_data_db('PS4')
game_data_db('PS5')

print(f'COMPLETE! {os.path.join(base_path, db_filename)}')
