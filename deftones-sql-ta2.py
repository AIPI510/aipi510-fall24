"""
The script file deftones-sql-ta2.py is used to perform the different queries included in the assignment description, using sqlite3. 
Furthermore, it is used to perform the following 5 queries that we came up with.
"""

import sqlite3
import pandas as pd
import os

def create_tips_db_and_load_db(df, conn):
    """
    Create the database tips.db and load the data into it from the csv

    Parameters:
    df : pandas dataframe that holds the data from the csv file tips.csv
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    create_table_query = f'CREATE TABLE tips ({get_create_query(df)});'
    cursor.execute(create_table_query)
    conn.commit()

    #load the data into the db
    df.to_sql('tips', conn, if_exists = 'append', index = False)

def get_create_query(df):
    """
    Return the string corresponding to the primary key of the database, column names, and data types.
    This string will be used in the CREATE query to create the tips table in the database

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor

    Returns:
    str: string representing the primary key of the database, column names, and data types to be used in the CREATE query.
    """

    df_columns = df.columns
    df_columns_types = df.dtypes
    dtypes_to_sql_mapping = {
        'int64': 'INTEGER',
        'float64': 'FLOAT',
        'object': 'TEXT'
    }

    #Creating the the string that corresponds to the sql table columns to be used in a parametrized CREATE query for creating the table
    sql_table_columns = ", ".join([f"{col} {dtypes_to_sql_mapping[str(dtype)]}" for col, dtype in zip(df_columns, df_columns_types)])
    return "id INTEGER PRIMARY KEY, " + sql_table_columns

def execute_queries(conn):
    """
    Executes all the queries from the assignment description + our custom queries that we came up with.

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    #Question 1
    print_question_number(1)
    get_avg_tip(conn)

    #Question 2
    print_question_number(2)
    get_max_total_bill_amount(conn)
    get_min_total_bill_amount(conn)
    
    #Question 3
    print_question_number(3)
    count_num_parties(conn)

    #Question 4
    print_question_number(4)
    get_total_bill_and_tip_for_parties_of_size_four(conn)

    #Question 5
    print_question_number(5)
    tip_percent_sort_desc(conn)

    #Question 6
    print_question_number(6)
    get_avg_tip_percentage_for_each_combination(conn)

    #Question 7
    print_question_number(7)
    top_5_bill_sort_desc(conn)

    #Question 8
    print_question_number(8)
    get_max_min_tip_percentage_for_each_day_time_combination(conn)

    #Question 9
    print_question_number(9)
    parties_more_than_4(conn)

    #Question 10
    print_question_number(10)
    get_avg_tip_percentage_for_each_day_time_smoker_combination(conn)

    #Custom Query 1: Get the average party size for smokers vs non-smokers
    print_question_number(1.1)
    print('Retrive the average party size for smokers vs non-smokers')
    get_avg_party_size_for_smokers_non_smokers(conn)

    #Custom Query 2: Get the most common meal time by sex
    print_question_number(1.2)
    get_most_meals_by_time_and_sex(conn)

    #Custom Query 3: Find the average table size for each combination of day and time 
    print_question_number(1.3)
    print('Find the average table size for each combination of day and time')
    get_avg_party_size_for_each_combination_of_day_time(conn)

    #Custom Query 4: Get the average tip percentage for each combination of day, time, and sex
    print_question_number(1.4)
    get_avg_tip_percentage_for_each_combination_sex(conn)

    #Custom Query 5: Find the average tip percentage for each party size 
    print_question_number(1.5)
    print('Find the average tip percentage for each party size ')
    get_avg_tip_percentage_for_each_party_size(conn)
    
    #Update Question
    print_question_number("Update")
    update_db(conn)

    #Delete Question
    print_question_number("Delete")
    delete_records(conn)

#Question 1
def get_avg_tip(conn):
    """
    Retrieves the average tip percentage for each day of the week

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    query = 'SELECT avg(tip) AS average_tip, day FROM tips GROUP BY day'
    cursor.execute(query)
    print_query_results(cursor)
    
# Question 2: Part 1
def get_max_total_bill_amount(conn):
    """
    Finds the maximum total bill amounts

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    query = 'SELECT MAX(total_bill) FROM tips'
    cursor.execute(query)
    res = cursor.fetchone()
    print(f"The maximum total bill is: {res[0]}")

#Question 2: Part 2
def get_min_total_bill_amount(conn):
    """
    Finds the minimum total bill amounts

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    query = 'SELECT MIN(total_bill) FROM tips'
    cursor.execute(query)
    res = cursor.fetchone()
    print(f"The minimum total bill is: {res[0]}")

#Question 3
def count_num_parties(conn):
    """
    Counts the number of parties for each size

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    query = 'SELECT size, COUNT(*) as count FROM tips GROUP BY size'
    cursor.execute(query)
    print_query_results(cursor)

#Question 4
def get_total_bill_and_tip_for_parties_of_size_four(conn):
    """
    Retrieves the total bill and tip amounts for parties of size 4 or more where the tip percentage is greater than 15%

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    query = '''
    SELECT total_bill, tip
    FROM tips 
    WHERE size = :size AND (tip / total_bill)*100 > :tip_percentage
    '''
    params = {'size' : 4, 'tip_percentage' : 15}
    cursor.execute(query, params)
    print_query_results(cursor)

#Question 5
def tip_percent_sort_desc(conn):
    """
    Retrieves the total bill, tip amount, and tip percentage for each combination of day and time, 
    sorted by tip percentage in descending order

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    query = '''SELECT day, time, 
                SUM(total_bill) AS bill, 
                SUM(tip) AS tip, 
                SUM(tip)/SUM(total_bill) AS tip_percentage 
            FROM tips GROUP BY day, time
            ORDER BY tip_percentage DESC'''
    cursor.execute(query)
    print_query_results(cursor)

#Question 6
def get_avg_tip_percentage_for_each_combination(conn):
    """
    Finds the average tip percentage for each combination of day, time, and smoker status

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    query = '''
            SELECT 
                day,
                time,
                smoker,
                AVG((tip / total_bill) * 100) AS avg_tip_percentage
            FROM tips
            GROUP BY day, time, smoker;
            '''
    cursor.execute(query)
    print_query_results(cursor)

#Question 7
def top_5_bill_sort_desc(conn):
    """
    Retrieves the total bill, tip amount, and tip percentage for each sex, sorted by total bill in descending order, and limits
    the results to the top 5 records

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()

    #got query from https://www.geeksforgeeks.org/how-to-select-top-n-rows-for-each-group-in-sql-server/
    query = '''
            WITH CTE AS (
            SELECT  
                sex, 
                total_bill, 
                tip, 
                tip/total_bill AS tip_percentage,
                ROW_NUMBER() OVER (PARTITION BY sex ORDER BY total_bill DESC) AS row_num
            FROM tips)
            SELECT * FROM CTE WHERE row_num <= 5;
            '''
    cursor.execute(query)
    print_query_results(cursor)

#Question 8
def get_max_min_tip_percentage_for_each_day_time_combination(conn):
    """
    Find the maximum and minimum tip percentage for each day and time combination, along with the 
    corresponding total bill and tip amount

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    query = '''
            WITH tip_percentage_cte AS (
            SELECT 
                day,
                time,
                total_bill,
                tip,
                (tip / total_bill) * 100 AS tip_percentage
            FROM tips),
            
            max_tip_percentage_cte AS (
            SELECT
                day,
                time,
                MAX(tip_percentage) AS max_tip_percentage
            FROM tip_percentage_cte
            GROUP BY day, time),

            min_tip_percentage_cte AS (
            SELECT
                day,
                time,
                MIN(tip_percentage) AS min_tip_percentage
            FROM tip_percentage_cte
            GROUP BY day, time)

            SELECT 
                tp.day,
                tp.time,
                max_tip.max_tip_percentage,
                tp.total_bill AS max_total_bill,
                tp.tip AS max_tip,
                min_tip.min_tip_percentage,
                tp2.total_bill AS min_total_bill,
                tp2.tip AS min_tip
            FROM 
                tip_percentage_cte tp
                JOIN max_tip_percentage_cte max_tip ON tp.day = max_tip.day AND tp.time = max_tip.time AND tp.tip_percentage = max_tip.max_tip_percentage
                JOIN min_tip_percentage_cte min_tip ON tp.time = min_tip.time AND tp.day = min_tip.day
                JOIN tip_percentage_cte tp2 ON tp2.day = min_tip.day AND tp2.time = min_tip.time AND tp2.tip_percentage = min_tip.min_tip_percentage;
            '''
    cursor.execute(query)
    print_query_results(cursor)

#Question 9
def parties_more_than_4(conn):
    """
    Retrieves the total bill, tip amount, and tip percentage for parties of size 4 or more where the tip percentage is 
    greater than 15% and the total bill is between $50 and $100

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    params = {'size' : 4, 
              'tip_percentage' : 0.15, 
              'total_bill_min' : 50,
              'total_bill_max' : 100}
    query = '''
            SELECT  
                size,
                total_bill, 
                tip, 
                tip/total_bill AS tip_percentage
            FROM tips
            WHERE size >= :size
            AND tip_percentage > :tip_percentage
            AND total_bill >= :total_bill_min
            AND total_bill <= :total_bill_max
            '''
    cursor.execute(query, params)
    print_query_results(cursor)

#Question 10
def get_avg_tip_percentage_for_each_day_time_smoker_combination(conn):
    """
    Finds the average tip percentage for each combination of day, time, and smoker status, but only include combinations 
    with more than 5 records

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    query = '''
            SELECT
                day,
                time,
                smoker,
                AVG((tip / total_bill) * 100) AS avg_tip_percentage,
                COUNT(*) AS count
            FROM tips
            GROUP BY day, time, smoker
            HAVING COUNT(*) > 5
            '''
    cursor.execute(query)
    print_query_results(cursor)


#Custom Query 1
def get_avg_party_size_for_smokers_non_smokers(conn):
    """
    Gets the average party size for smokers vs non-smokers

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    query = '''
            SELECT 
                smoker,
                AVG(size) AS avg_party_size
            FROM tips
            GROUP BY smoker
            '''
    cursor.execute(query)
    print_query_results(cursor)

#Custom Query 2
def get_most_meals_by_time_and_sex(conn):
    """
    Gets the most common meal time for each sex

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    query = '''
            SELECT sex, time
            FROM (
                SELECT sex, time, COUNT(*) as count,
                ROW_NUMBER() OVER (PARTITION BY sex ORDER BY COUNT(*) DESC) as rn
                FROM tips
                GROUP BY sex, time
            ) as ranked
            WHERE rn = 1;
            '''
    cursor.execute(query)
    print_query_results(cursor)

#Custom Query 3
def get_avg_party_size_for_each_combination_of_day_time(conn):
    """
    Finds the average table size for each combination of day and time 

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    query = '''
            SELECT 
                day,
                time,
                AVG(size) AS avg_party_size
            FROM tips
            GROUP BY day, time;
            '''
    cursor.execute(query)
    print_query_results(cursor)

#Custom Query 4
def get_avg_tip_percentage_for_each_combination_sex(conn):
    """
    Gets the average tip percentage for each combination of day, time, and sex 

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    query = '''
            SELECT 
                day,
                time,
                sex,
                AVG((tip / total_bill) * 100) AS avg_tip_percentage
            FROM tips
            GROUP BY day, time, sex;
            '''
    cursor.execute(query)
    print_query_results(cursor)

#Custom Query 5
def get_avg_tip_percentage_for_each_party_size(conn):
    """
    Finds the average tip percentage for each party size 

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    query = '''
            SELECT 
                size AS party_size,
                AVG((tip / total_bill ) * 100) AS avg_tip_percentage
            FROM tips
            GROUP BY size;
            '''
    cursor.execute(query)
    print_query_results(cursor)
    
#Update Question
def update_db(conn):
    """
    Updates the record that corresponds to id 10 and sets the smoker value to Yes.

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    params = {'id' : 10}
    query = f'UPDATE tips SET smoker="Yes" WHERE id=:id'
    cursor.execute(query, params)
    conn.commit()

#Delete Question
def delete_records(conn):
    """
    Deletes records from the database that have a total bill that is less than $10

    Parameters:
    conn (sqlite3.Connection): the connection object used to create the cursor
    """

    cursor = conn.cursor()
    params = {'total_bill' : 10}
    query = '''
            DELETE FROM tips
            WHERE total_bill < :total_bill
            '''
    cursor.execute(query, params)
    conn.commit()

def print_question_number(question_number):
    """
    Print the question's number for better output visibility

    Parameters:
    question_number: integer representing the question's number. The order of the questions follows the one in the assignment description.
    """

    print('-' * 20 + f'Question {str(question_number)}' + '-' * 20 + '\n')

def print_query_results(cursor):
    """
    Prints the query results in the cursor passed in as argument.

    Parameters:
    cursor (sqlite3.Cursor): cursor instance used to execute the SQL queries
    """

    column_names = [column_name[0] for column_name in cursor.description]
    print(column_names)
    res = cursor.fetchall()
    if not res:
        print("No records to return")
    else:
        for row in res:
            print(row)

def main():
    if os.path.exists("tips.db"):
        os.remove("tips.db")
        print(f"Deleted file")
    else:
        print(f"No file to delete")

    df = pd.read_csv('data/tips.csv')

    try:
        with sqlite3.connect('tips.db') as conn:
            create_tips_db_and_load_db(df, conn)
            execute_queries(conn)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()