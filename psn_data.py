"""
Author: Kelv Gooding
Date Created: 2023-05-16
Date Updated: 2025-01-03
Version: 1.6
"""

# Modules

from modules import db_check
from openpyxl import Workbook
from psnawp_api import PSNAWP
import auth
import csv
import os
import sqlite3

# SQLite3 Variables

base_path = os.path.dirname(os.path.abspath(__file__))
filename = 'psn_game_collection'
sql_script = f'{base_path}/scripts/sql/create_tables.sql'
db_check.check_db(f'{base_path}', f'{filename}.db', f'{sql_script}')
conn = db_check.sqlite3.connect(os.path.join(f'{base_path}', f'{filename}.db'), check_same_thread=False)
c = conn.cursor()

# PSNAWP Variables

psnawp = PSNAWP(auth.api_auth['psn_token'])
psn_connect = psnawp.me()

def generate_game_data():
    c.execute('DELETE FROM COLLECTION')
    for i in psn_connect.title_stats():
        c.execute(f'INSERT INTO COLLECTION VALUES ("{i.title_id}", "{i.name.upper()}", "{str(i.first_played_date_time)[0:19]}", "{str(i.last_played_date_time)[0:19]}", "{str(i.category).replace("PlatformCategory.", "")}", "{i.play_count}", "{int(i.play_duration.seconds / 60)}", "{i.image_url}");')

def game_data_db(console, product_code):
    c.execute(f'DELETE FROM {console}')
    c.execute(f'INSERT INTO {console} SELECT * FROM COLLECTION WHERE title_id LIKE "%{product_code}%";')
    c.execute(f'UPDATE {console} SET platform = "{console}" WHERE platform = "UNKNOWN"')
    conn.commit()

def game_data_xlsx(base_path):

    xlsx_filename = os.path.join(f'{base_path}', f'{filename}.xlsx')
    workbook = Workbook()

    tables = ['COLLECTION', 'PS4', 'PS5']

    for idx, table in enumerate(tables):
        if idx == 0:
            sheet = workbook.active
            sheet.title = table
        else:
            sheet = workbook.create_sheet(title=table)

        c.execute(f"SELECT * FROM {table}")
        rows = c.fetchall()
        headers = [description[0] for description in c.description]
        sheet.append(headers)
        for row in rows:
            sheet.append(row)

    workbook.save(xlsx_filename)

generate_game_data()
game_data_db('PS4', 'CUSA')
game_data_db('PS5', 'PPSA')
game_data_xlsx(base_path)

print(f'COMPLETE!')
