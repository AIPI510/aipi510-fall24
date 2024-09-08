#Import required libraries
import pandas as pd
import numpy as np
import os
import sqlite3

# First let's do a check and make sure our file exists. If it exists then we proceed with loading the csv file.
data_file_path = "data/tips.csv"
if os.path.exists(data_file_path):
    print("Data File Exists")
    pd.set_option("display.max_rows", None)
    theData = pd.read_csv("data/tips.csv") #This loads a CSV file tips.csv which I added to the project folder.
else:
    print("Data File not found")

# Let's work with the database now that we have loaded the data.
try:
    # Create a new database called tips.db or connect to it if it exists
    with sqlite3.connect('tips.db') as conn:
    # Let's write the data from the CSV file into the database we just created
        theData.to_sql('tips', conn, if_exists='replace', index=False)
    # Save (commit) the changes to the database
    conn.commit()
except sqlite3.Error as e:
     print("An error occurred with the SQLite database: {}".format(e))

#The blocks of code below are just copy and paste and the only thing that will change is the SQL statement we are executing against the data
# We will use try except blocks for each.
# We will parameterize some SQL statements that make sense to parameterized. Some don't need it. 
# For this homework and to show that we understand parameterization, we parameterized Operation 9, Additional Operation 5, and Additional Operation 6 SQL statements. 

# Operation 1: Retrieve the average tip percentage from each day the week
print("Operation 1: Retrieve the average tip percentage from each day the week")
try:
    #Reconnect to the SQLite database tips.db
    with sqlite3.connect('tips.db') as conn:
    #SQl Statement applied to the data
        df = pd.read_sql('SELECT day, AVG((tip / total_bill) * 100) AS avg_tip_percentage FROM tips GROUP BY day;', conn)
    #Option to display the full data set returned
    with pd.option_context('display.max_rows', None,):
        print(df)
except sqlite3.Error as e:
     print("An error occurred with the SQLite database: {}".format(e))

# Operation 2: Find the maximum and minimum total bill amounts
print("Operation 2: Find the maximum and minimum total bill amounts")
try:
    #Reconnect to the SQLite database tips.db
    with sqlite3.connect('tips.db') as conn:
    #SQl Statement applied to the data
        df = pd.read_sql('SELECT MAX(total_bill) AS max_total_bill, MIN(total_bill) AS min_total_bill FROM tips;', conn)
    #Option to display the full data set returned
    with pd.option_context('display.max_rows', None,):
        print(df)
except sqlite3.Error as e:
     print("An error occurred with the SQLite database: {}".format(e))

# Operation 3: Count the number of parties for each size
print("Operation 3: Count the number of parties for each size")
try:
    #Reconnect to the SQLite database tips.db
    with sqlite3.connect('tips.db') as conn:
    #SQl Statement applied to the data
        df = pd.read_sql('SELECT size, COUNT(*) AS party_count FROM tips GROUP BY size;', conn)
    #Option to display the full data set returned
    with pd.option_context('display.max_rows', None,):
        print(df)
except sqlite3.Error as e:
     print("An error occurred with the SQLite database: {}".format(e))

# Operation 4: Retrieve the total bill and tip for parties of size 4 or more, where the tip percentage is greater than 15%
print("Operation 4: Retrieve the total bill and tip for parties of size 4 or more, where the tip percentage is greater than 15%")
try:
    #Reconnect to the SQLite database tips.db
    with sqlite3.connect('tips.db') as conn:
    #SQl Statement applied to the data
        df = pd.read_sql('SELECT total_bill, tip FROM tips WHERE size >= 4 AND (tip / total_bill) * 100 > 15;', conn)
    #Option to display the full data set returned
    with pd.option_context('display.max_rows', None,):
        print(df)
except sqlite3.Error as e:
     print("An error occurred with the SQLite database: {}".format(e))

# Operation 5: Retrieve the total bill, tip amount, and tip percentage for each combination of day and time, sorted by tip percentage in descending order
print("Operation 5:Retrieve the total bill, tip amount, and tip percentage for each combination of day and time, sorted by tip percentage in descending order")
try:
    #Reconnect to the SQLite database tips.db
    with sqlite3.connect('tips.db') as conn:
    #SQl Statement applied to the data
        df = pd.read_sql('SELECT day, time, total_bill, tip, (tip / total_bill) * 100 AS tip_percentage FROM tips ORDER BY tip_percentage DESC;', conn)
    #Option to display the full data set returned
    with pd.option_context('display.max_rows', None,):
        print(df)
except sqlite3.Error as e:
     print("An error occurred with the SQLite database: {}".format(e))

# Operation 6: Find the average tip percentage for each combination of day, time, and smoker status
print("Operation 6: Find the average tip percentage for each combination of day, time, and smoker status")
try:
    #Reconnect to the SQLite database tips.db
    with sqlite3.connect('tips.db') as conn:
    #SQl Statement applied to the data
        df = pd.read_sql('SELECT day, time, smoker, AVG((tip / total_bill) * 100) AS avg_tip_percentage FROM tips GROUP BY day, time, smoker;', conn)
    #Option to display the full data set returned
    with pd.option_context('display.max_rows', None,):
        print(df)
except sqlite3.Error as e:
     print("An error occurred with the SQLite database: {}".format(e))

# Operation 7: Retrieve the total bill, tip amount, and tip percentage for each sex, sorted by total bill in descending order, and limit the results to the top 5 records
print("Operation 7: Retrieve the total bill, tip amount, and tip percentage for each sex, sorted by total bill in descending order, and limit the results to the top 5 records")
try:
    with sqlite3.connect('tips.db') as conn:
    #SQl Statement applied to the data
        df = pd.read_sql('SELECT sex, total_bill, tip, (tip / total_bill) * 100 AS tip_percentage FROM tips ORDER BY total_bill DESC LIMIT 5;', conn)
    #Option to display the full data set returned
    with pd.option_context('display.max_rows', None,):
        print(df)
except sqlite3.Error as e:
     print("An error occurred with the SQLite database: {}".format(e))

# Operation 8: Find the maximum and minimum tip percentage for each day and time combination, along with the corresponding total bill and tip amount
print("Operation 8: Find the maximum and minimum tip percentage for each day and time combination, along with the corresponding total bill and tip amount")
try:
    #Reconnect to the SQLite database tips.db
    with sqlite3.connect('tips.db') as conn:
    #SQl Statement applied to the data
        df = pd.read_sql('SELECT day, time, MAX((tip / total_bill) * 100) AS max_tip_percentage, MIN((tip / total_bill) * 100) AS min_tip_percentage, total_bill, tip FROM tips GROUP BY day, time;', conn)
    #Option to display the full data set returned
    with pd.option_context('display.max_rows', None,):
        print(df)
except sqlite3.Error as e:
     print("An error occurred with the SQLite database: {}".format(e))

# Operation 9: Retrieve the total bill, tip amount, and tip percentage for parties of size 4 or more, where the tip percentage is greater than 15%, and the total bill is between $50 and $100
# The query below will be parameterized. We will turn the 50 and 100 into parameters.
min_total_bill = 50
max_total_bill = 100
print("Operation 9: Retrieve the total bill, tip amount, and tip percentage for parties of size 4 or more, where the tip percentage is greater than 15%, and the total bill is between $50 and $100")
try:
    #Reconnect to the SQLite database tips.db
    with sqlite3.connect('tips.db') as conn:
    #SQl Statement applied to the data where the ? represents a parameter to be accepted during execution. 
        query = '''SELECT total_bill, tip, (tip / total_bill) * 100 AS tip_percentage FROM tips WHERE size >= 4 AND (tip / total_bill) * 100 > 15 AND total_bill BETWEEN ? AND ?;'''
        # Execute the query with parameters
        df = pd.read_sql(query, conn, params=(min_total_bill, max_total_bill))
    #Option to display the full data set returned
    with pd.option_context('display.max_rows', None,):
        print(df)
except sqlite3.Error as e:
     print("An error occurred with the SQLite database: {}".format(e))

# Operation 10: Find the average tip percentage for each combination of day, time, and smoker status, but only include combinations with more than 5 records
print("Operation 10: Find the average tip percentage for each combination of day, time, and smoker status, but only include combinations with more than 5 records")
try:
    #Reconnect to the SQLite database tips.db
    with sqlite3.connect('tips.db') as conn:
    #SQl Statement applied to the data
        df = pd.read_sql('SELECT day, time, smoker, AVG((tip / total_bill) * 100) AS avg_tip_percentage, COUNT(*) AS record_count FROM tips GROUP BY day, time, smoker HAVING record_count > 5;', conn)
    #Option to display the full data set returned
    with pd.option_context('display.max_rows', None,):
        print(df)
except sqlite3.Error as e:
     print("An error occurred with the SQLite database: {}".format(e))

#Additional queries of our own. We added 6. The queries below use the same connection. So we will add a single try--except block.

try:
    with sqlite3.connect('tips.db') as conn: #Open the connection
        cursor = conn.cursor()
    # Find the average total bill for groups by sex and time
    print("Additional Operation 1")
    additional_1 = '''SELECT AVG(total_bill) AS average_total_bill, sex, time
                    FROM tips
                    GROUP BY sex, time
                    HAVING AVG(total_bill) BETWEEN 10 AND 20'''
    additional_question_1 = pd.read_sql_query(additional_1, conn)
    print(additional_question_1)

    #Find the highest male tip and female tip
    print("Additional Operation 2")
    additional_2 = '''SELECT MAX(tip) AS highest_tip, sex, time, total_bill
                    FROM tips
                    GROUP BY sex, time'''
    additional_question_2 = pd.read_sql_query(additional_2, conn)
    print(additional_question_2)

    #Do smokers have less money to tip due to their addictions? Lets find out
    print("Additional Operation 3")
    additional_3 = '''SELECT (tip / total_bill) * 100 AS tip_percentage, day, time
                    FROM tips
                    WHERE smoker = 'Yes'
                    ORDER BY tip_percentage DESC'''
    additional_question_3 = pd.read_sql_query(additional_3, conn)
    print(additional_question_3)

    #Compare against non smokers
    print("Additional Operation 4")
    additional_4 = '''SELECT (tip / total_bill) * 100 AS tip_percentage, day, time
                    FROM tips
                    WHERE smoker = 'No'
                    ORDER BY tip_percentage DESC'''
    additional_question_4 = pd.read_sql_query(additional_4, conn)
    print(additional_question_4)

    #It would seem that smokers pay a higher tip!
    #We are now curious to determine which time of day the higher tips reside.
    print("Additional Operation 5")
    time_value='Dinner'
    additional_5 = '''SELECT (tip / total_bill) * 100 AS tip_percentage, time
                    FROM tips
                    WHERE time = ?
                    ORDER BY tip_percentage DESC'''
    additional_question_5 = pd.read_sql_query(additional_5, conn, params=(time_value,))
    print(additional_question_5)

    print("Additional Operation 6")
    time_value='Lunch'
    additional_6 = '''SELECT (tip / total_bill) * 100 AS tip_percentage, time
                    FROM tips
                    WHERE time = ?
                    ORDER BY tip_percentage DESC'''
    additional_question_6 = pd.read_sql_query(additional_6, conn, params=(time_value,))
    print(additional_question_6)

    #The data suggest that the highest tip percentages are from the Dinner timeframe

    # Update the record with rowid=10 and set smoker to 'Yes'
    update_query = '''UPDATE tips 
                    SET smoker = 'Yes'
                    WHERE rowid = 10'''
    cursor.execute(update_query)

    # Commit the changes to the database
    conn.commit()

    # Verify the update rowid=10
    print("Verifyng the update: It was determined that there was an error in the database. Please update the record that corresponds to id=10 and set smoker to Yes.")
    verify_query = '''SELECT * FROM tips WHERE rowid = 10'''
    cursor.execute(verify_query)
    updated_record = cursor.fetchone()
    print(updated_record)

    #Delete records from the database with total bill <10
    print("Deleting Operation: Delete records from the database that have a total bill that is less than $10")
    delete='''DELETE FROM tips
            WHERE total_bill < 10'''
    cursor.execute(delete)
    conn.commit()
    #If we want to verify
    print("Verifying the deletion")
    delete_verify='''SELECT * FROM tips WHERE total_bill < 10'''
    delete_ver=pd.read_sql_query(delete_verify, conn)
    print(delete_ver) #THIS SHOULD BE EMPTY
except sqlite3.Error as e:
     print("An error occurred with the SQLite database: {}".format(e))