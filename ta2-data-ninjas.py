''' 
Author:
Jesse Warren & Haochen Li
'''

import sqlite3 # 3.41.2
import csv # came with python package

## CREATE
conn = sqlite3.connect('ta2_tips.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tips (
    total_bill REAL,
    tip REAL,
    sex TEXT,
    smoker TEXT,
    day TEXT,                      
    time TEXT,           
    size INTEGER                             
)
''')

## READ


