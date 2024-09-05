import sqlite3
import pandas as pd

file = 'data/tips.csv'

df = pd.read_csv(file)

try:

    with sqlite3.connect('tips.db') as conn:

        df.to_sql('tips', conn, if_exists='replace', index=False)

        df['tip_percentage'] = df['tip']/df['total_bill']

        query = "SELECT AVG(tip) FROM tips"
        avg_total_bill = conn.execute(query).fetchone()[0]

        print(f"The average tip percentage for each day of the week is: {avg_total_bill:.2f}")
except sqlite3.DatabaseError as e:
    print('f"Database error: {e}"')
except Exception as e:
    print(f"An unexpected error occurred: {e}")

