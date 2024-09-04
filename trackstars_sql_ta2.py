import sqlite3
import pandas as pd

def csv_to_sql(csv_filename):
    csv = csv_filename
    df = pd.read_csv(csv)

    connection = sqlite3.connect('tips_data.db')

    df.to_sql('tips_table', connection, if_exists='replace', index = False)

    connection.commit()
    connection.close()

csv_to_sql('data/tips.csv')