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

# Create a new database called tips.db or connect to it if it exists
conn = sqlite3.connect('tips.db')
# Let's write the data from the CSV file into the database we just created
theData.to_sql('tips', conn, if_exists='replace', index=False)
# Save (commit) the changes to the database
conn.commit()  
# And let's not forget to close the connection
conn.close()   

#The blocks of code below are just copy and paste and the only thing that will change is the SQL statement we are executing against the data

# Operation 1: Retrieve the average tip percentage from each day the week
print("Operation 1: Retrieve the average tip percentage from each day the week")
#Reconnect to the SQLite database tips.db
conn = sqlite3.connect('tips.db')
#SQl Statement applied to the data
df = pd.read_sql('SELECT day, AVG((tip / total_bill) * 100) AS avg_tip_percentage FROM tips GROUP BY day;', conn)
#Option to display the full data set returned
with pd.option_context('display.max_rows', None,):
    print(df)
#Close the connection
conn.close()

# Operation 2: Find the maximum and minimum total bull amounts
print("Operation 2: Find the maximum and minimum total bull amounts")
#Reconnect to the SQLite database tips.db
conn = sqlite3.connect('tips.db')
#SQl Statement applied to the data
df = pd.read_sql('SELECT MAX(total_bill) AS max_total_bill, MIN(total_bill) AS min_total_bill FROM tips;', conn)
#Option to display the full data set returned
with pd.option_context('display.max_rows', None,):
    print(df)
#Close the connection
conn.close()

# Operation 3: Count the number of parties for each size
print("Operation 3: Count the number of parties for each size")
#Reconnect to the SQLite database tips.db
conn = sqlite3.connect('tips.db')
#SQl Statement applied to the data
df = pd.read_sql('SELECT size, COUNT(*) AS party_count FROM tips GROUP BY size;', conn)
#Option to display the full data set returned
with pd.option_context('display.max_rows', None,):
    print(df)
#Close the connection
conn.close()

# Operation 4: Retrieve the total bill and tip for parties of size 4 or more, where the tip percentage is greater than 15%
print("Operation 4: Retrieve the total bill and tip for parties of size 4 or more, where the tip percentage is greater than 15%")
#Reconnect to the SQLite database tips.db
conn = sqlite3.connect('tips.db')
#SQl Statement applied to the data
df = pd.read_sql('SELECT total_bill, tip FROM tips WHERE size >= 4 AND (tip / total_bill) * 100 > 15;', conn)
#Option to display the full data set returned
with pd.option_context('display.max_rows', None,):
    print(df)
#Close the connection
conn.close()

# Operation 5: Retrieve the total bill, tip amount, and tip percentage for each combination of day and time, sorted by tip percentage in descending order
print("Operation 5:Retrieve the total bill, tip amount, and tip percentage for each combination of day and time, sorted by tip percentage in descending order")
#Reconnect to the SQLite database tips.db
conn = sqlite3.connect('tips.db')
#SQl Statement applied to the data
df = pd.read_sql('SELECT day, time, total_bill, tip, (tip / total_bill) * 100 AS tip_percentage FROM tips ORDER BY tip_percentage DESC;', conn)
#Option to display the full data set returned
with pd.option_context('display.max_rows', None,):
    print(df)
#Close the connection
conn.close()

# Operation 6: Find the average tip percentage for each combination of day, time, and smoker status
print("Operation 6: Find the average tip percentage for each combination of day, time, and smoker status")
#Reconnect to the SQLite database tips.db
conn = sqlite3.connect('tips.db')
#SQl Statement applied to the data
df = pd.read_sql('SELECT day, time, smoker, AVG((tip / total_bill) * 100) AS avg_tip_percentage FROM tips GROUP BY day, time, smoker;', conn)
#Option to display the full data set returned
with pd.option_context('display.max_rows', None,):
    print(df)
#Close the connection
conn.close()

# Operation 7: Retrieve the total bill, tip amount, and tip percentage for each sex, sorted by total bill in descending order, and limit the results to the top 5 records
print("Operation 7: Retrieve the total bill, tip amount, and tip percentage for each sex, sorted by total bill in descending order, and limit the results to the top 5 records")
conn = sqlite3.connect('tips.db')
#SQl Statement applied to the data
df = pd.read_sql('SELECT sex, total_bill, tip, (tip / total_bill) * 100 AS tip_percentage FROM tips ORDER BY total_bill DESC LIMIT 5;', conn)
#Option to display the full data set returned
with pd.option_context('display.max_rows', None,):
    print(df)
#Close the connection
conn.close()

# Operation 8: Find the maximum and minimum tip percentage for each day and time combination, along with the corresponding total bill and tip amount
print("Operation 8: Find the maximum and minimum tip percentage for each day and time combination, along with the corresponding total bill and tip amount")
#Reconnect to the SQLite database tips.db
conn = sqlite3.connect('tips.db')
#SQl Statement applied to the data
df = pd.read_sql('SELECT day, time, MAX((tip / total_bill) * 100) AS max_tip_percentage, MIN((tip / total_bill) * 100) AS min_tip_percentage, total_bill, tip FROM tips GROUP BY day, time;', conn)
#Option to display the full data set returned
with pd.option_context('display.max_rows', None,):
    print(df)
#Close the connection
conn.close()

# Operation 9: Retrieve the total bill, tip amount, and tip percentage for parties of size 4 or more, where the tip percentage is greater than 15%, and the total bill is between $50 and $100
print("Operation 9: Retrieve the total bill, tip amount, and tip percentage for parties of size 4 or more, where the tip percentage is greater than 15%, and the total bill is between $50 and $100")
#Reconnect to the SQLite database tips.db
conn = sqlite3.connect('tips.db')
#SQl Statement applied to the data
df = pd.read_sql('SELECT total_bill, tip, (tip / total_bill) * 100 AS tip_percentage FROM tips WHERE size >= 4 AND (tip / total_bill) * 100 > 15 AND total_bill BETWEEN 50 AND 100;', conn)
#Option to display the full data set returned
with pd.option_context('display.max_rows', None,):
    print(df)
#Close the connection
conn.close()

# Operation 10: Find the average tip percentage for each combination of day, time, and smoker status, but only include combinations with more than 5 records
print("Operation 10: Find the average tip percentage for each combination of day, time, and smoker status, but only include combinations with more than 5 records")
#Reconnect to the SQLite database tips.db
conn = sqlite3.connect('tips.db')
#SQl Statement applied to the data
df = pd.read_sql('SELECT day, time, smoker, AVG((tip / total_bill) * 100) AS avg_tip_percentage, COUNT(*) AS record_count FROM tips GROUP BY day, time, smoker HAVING record_count > 5;', conn)
#Option to display the full data set returned
with pd.option_context('display.max_rows', None,):
    print(df)
#Close the connection
conn.close()