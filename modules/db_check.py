#!/usr/bin/python3

"""
Author: Kelv Gooding
Created: 2023-11-27
Updated: 2023-12-08
Version: 1.1.0
"""

# Modules

import sqlite3
import os

# Script

def check_db(base_path, database_name, sql_script):
    
    if database_name in os.listdir(base_path):
        print('Database already exists. No action required.')
    else:
        print('this file does not exist. Creating database.')
        connection = sqlite3.connect(f'{os.path.join(base_path, database_name)}')

        print(f'Creating database tables based on {sql_script}')
        c = connection.cursor()
        with open(sql_script, 'r') as file:
            sql_script = file.read()
        c.executescript(sql_script)