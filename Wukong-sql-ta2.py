import sqlite3
import pandas as pd

def execute_query(query, params=None):
    """
    Executes a given SQL query and returns the result as a pandas DataFrame.
    
    Args:
        query (str): SQL query string.
        params (tuple, optional): Parameters for parameterized queries. Defaults to None.
        
    Returns:
        pd.DataFrame: Query result as a pandas DataFrame.
    """
    with sqlite3.connect('tips_database.db') as conn:
        try:
            if params:
                df = pd.read_sql_query(query, conn, params=params)
            else:
                df = pd.read_sql_query(query, conn)
            return df
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")            
            return None


def main():
    # Load the data from CSV and write to the database
    df = pd.read_csv('data/tips.csv')
    with sqlite3.connect('tips_database.db') as conn:
        df.to_sql('tips', conn, if_exists='replace', index=False)

    # Issue 1: Calculate the average tip percentage per day
    query1 = '''SELECT day, ROUND(SUM(tip) * 100 / SUM(total_bill), 2) AS avg_tip_percentage FROM tips GROUP BY day;'''
    df1 = execute_query(query1)
    print('Issue 1: ', df1)

    # Issue 2: Find the maximum and minimum total bill
    query2 = '''SELECT MAX(total_bill) AS max_total_bill, MIN(total_bill) AS min_total_bill FROM tips;'''
    df2 = execute_query(query2)
    print('Issue 2: ', df2)

    # Issue 3: Count the number of records for each size
    query3 = '''SELECT size, COUNT(*) AS number_of_each_size FROM tips GROUP BY size;'''
    df3 = execute_query(query3)
    print('Issue 3: ', df3)

    # Issue 4: Select total_bill and tip where size >= 4 and tip percentage > 15%
    query4 = '''SELECT total_bill, tip FROM tips WHERE size >= 4 AND (tip / total_bill) * 100 > 15;'''
    df4 = execute_query(query4)
    print('Issue 4: ', df4)

    # Issue 5: Calculate the tip percentage per day and time
    query5 = '''SELECT day, time, SUM(total_bill) AS sum_bill, SUM(tip) AS sum_tip, 
                SUM(tip) * 100 / SUM(total_bill) AS tip_percentage 
                FROM tips GROUP BY day, time ORDER BY tip_percentage DESC;'''
    df5 = execute_query(query5)
    print('Issue 5: ', df5)

    # Issue 6: Calculate the average tip percentage per day, time, and smoker status
    query6 = '''SELECT day, time, smoker, SUM(tip) * 100 / SUM(total_bill) AS average_tip_percentage 
                FROM tips GROUP BY day, time, smoker;'''
    df6 = execute_query(query6)
    print('Issue 6: ', df6)

    # Issue 7: Calculate the sum of total_bill and tip for each gender
    query7 = '''SELECT sex, SUM(total_bill), SUM(tip), SUM(tip) * 100 / SUM(total_bill) AS tip_percentage 
                FROM tips GROUP BY sex ORDER BY SUM(total_bill) DESC LIMIT 5;'''
    df7 = execute_query(query7)
    print('Issue 7: ', df7)

    # Issue 8: Find the day and time with the highest and lowest tip percentage
    query8 = '''SELECT day, time, sum_bill, sum_tip, tip_percentage  
                FROM (SELECT day, time, SUM(total_bill) AS sum_bill, SUM(tip) AS sum_tip, 
                      SUM(tip) * 100 / SUM(total_bill) as tip_percentage 
                      FROM tips GROUP BY day, time) AS group_table 
                WHERE tip_percentage = (SELECT MAX(tip_percentage) FROM 
                      (SELECT SUM(tip) * 100 / SUM(total_bill) as tip_percentage FROM tips GROUP BY day, time)) 
                OR tip_percentage = (SELECT MIN(tip_percentage) FROM 
                      (SELECT SUM(tip) * 100 / SUM(total_bill) AS tip_percentage FROM tips GROUP BY day, time));'''
    df8 = execute_query(query8)
    print('Issue 8: ', df8)

    # Issue 9: Find records where size >= 4 and tip percentage > 15% and total bill is between 50 and 100
    query9 = '''SELECT total_bill, tip, tip * 100 / total_bill AS tip_percentage 
                FROM tips WHERE size >= 4 AND tip * 100 / total_bill > 15 AND total_bill BETWEEN 50 AND 100;'''
    df9 = execute_query(query9)
    print('Issue 9: ', df9)

    # Issue 10: Calculate the average tip percentage where there are more than 5 records
    query10 = '''SELECT day, time, smoker, SUM(tip) * 100 / SUM(total_bill) AS avg_tip_percentage 
                 FROM tips GROUP BY day, time, smoker HAVING COUNT(*) > 5;'''
    df10 = execute_query(query10)
    print('Issue 10: ', df10)

    # Additional queries

    # 1. Find the top three tips given by females at Dinner with a size of 2
    query11 = '''SELECT total_bill, tip, size
    FROM tips WHERE sex = 'Female' AND time = 'Dinner' AND size = 2 
    ORDER BY tip DESC 
    LIMIT 3;'''
    df11 = execute_query(query11)
    print('Issue 11: ', df11)

    # 2. Find the total tip amount for each sex and smoker combination
    query12 = '''SELECT sex, smoker, SUM(tip) AS total_tip 
    FROM tips
    GROUP BY sex, smoker;'''
    df12 = execute_query(query12)
    print('Issue 12: ', df12)

    # 3. Find the number of women that give tips over 5 for each day and time combination
    query13 = '''SELECT day, time, COUNT(*) AS number_of_women 
    FROM tips 
    WHERE sex = 'Female' AND tip > 5 
    GROUP BY day, time;'''
    df13 = execute_query(query13)
    print('Issue 13: ', df13)

    # 4. Find the number of records where the tip is greater than 20% of the total bill
    query14 = '''SELECT COUNT(*) 
    FROM tips
    WHERE (tip / total_bill) * 100 > 20;'''
    df14 = execute_query(query14)
    print('Issue 14: ', df14)

    # 5. Find the number of times that females pay tips for each day and time combination
    query15 = '''SELECT day, time, COUNT(*) AS count_female_pay_tips 
    FROM tips 
    WHERE sex = 'Female' 
    GROUP BY day, time;'''
    df15 = execute_query(query15)
    print('Issue 15: ', df15)

# Update and Delete operations
    update_query = '''UPDATE tips SET smoker = 'Yes' WHERE rowid = 10;'''
    delete_query = '''DELETE FROM tips WHERE total_bill < 10;'''

    # Execute Update and Delete
    try:
        with sqlite3.connect('tips_database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(update_query)
            print("Update successful.")
            conn.commit()
            cursor.execute(delete_query)
            conn.commit()
            print("Delete successful.")
            cursor.close()
    except sqlite3.Error as e:
        print(f"Error during update or delete operation: {e}")

 
if __name__ == '__main__':
    main()
