import pandas as pd
import sqlite3

# Read the csv file tips.csv
file_csv = 'tips.csv'
df = pd.read_csv(file_csv)

# Create a database named tips_database.db and establish a connection named conn. Load the data from tips.csv into the database
conn = sqlite3.connect('tips_database.db')
df.to_sql('tips', conn, if_exists='replace', index=False)

#issue 1
query1 = '''SELECT day, ROUND(SUM(tip)*100/SUM(total_bill), 2) AS avg_tip_percentage  FROM tips GROUP BY day;'''

df1 = pd.read_sql_query(query1, conn)
print('Issue 1: ')
print(df1)

#issue 2
query2 = '''SELECT MAX(total_bill) AS max_total_bill,  MIN(total_bill) AS min_total_bill  FROM tips;'''
    
df2 = pd.read_sql_query(query2, conn)
print('Issue 2: ')
print(df2)

#issue 3
query3 = '''SELECT size, COUNT(*) AS number_of_each_size FROM tips GROUP BY size;'''
    
df3 = pd.read_sql_query(query3, conn)
print('Issue 3: ')
print(df3)

#issue 4
query4 = '''SELECT total_bill, tip FROM tips WHERE size >= 4 AND (tip/total_bill)*100 > 15;'''
    
df4 = pd.read_sql_query(query4, conn)
print('Issue 4: ')
print(df4)

#issue 5
query5 = '''SELECT day, time, SUM(total_bill) AS sum_bill, SUM(tip) AS sum_tip, SUM(tip)*100/SUM(total_bill) AS tip_percentage FROM tips GROUP BY day, time ORDER BY (SUM(tip)*100/SUM(total_bill)) DESC;'''
    
df5 = pd.read_sql_query(query5, conn)
print('Issue 5: ')
print(df5)

#issue 6
query6 = '''SELECT day, time, smoker, SUM(tip)*100/SUM(total_bill) AS average_tip_percentage FROM tips GROUP BY day, time, smoker;'''
    
df6 = pd.read_sql_query(query6, conn)
print('Issue 6: ')
print(df6)

#issue 7
query7 = '''SELECT sex, SUM(total_bill), SUM(tip), SUM(tip)*100/SUM(total_bill) AS tip_percentage FROM tips GROUP BY sex ORDER BY SUM(total_bill) desc LIMIT 5;'''
    
df7 = pd.read_sql_query(query7, conn)
print('Issue 7: ')
print(df7)

#issue 8
query8 = '''SELECT day, time, sum_bill, sum_tip, tip_percentage  
FROM (SELECT day, time, SUM(total_bill) AS sum_bill, SUM(tip) AS sum_tip, SUM(tip)*100/SUM(total_bill) as tip_percentage FROM tips GROUP BY day, time) AS group_table 
WHERE tip_percentage = (SELECT MAX(tip_percentage) FROM(SELECT SUM(tip)*100/SUM(total_bill) as tip_percentage FROM tips GROUP BY day, time) AS group_max) 
OR tip_percentage = (SELECT MIN(tip_percentage) FROM(SELECT SUM(tip)*100/SUM(total_bill) AS tip_percentage FROM tips GROUP BY day, time) AS group_min);'''
    
df8 = pd.read_sql_query(query8, conn)
print('Issue 8: ')
print(df8)

#issue 9
query9 = '''SELECT total_bill, tip, tip*100/total_bill FROM tips WHERE size >= 4  AND tip*100/total_bill > 15 AND total_bill BETWEEN 50 AND 100;'''
    
df9 = pd.read_sql_query(query9, conn)
print('Issue 9: ')
print(df9)

#issue 10
query10 = '''SELECT day, time, smoker, SUM(tip)*100/SUM(total_bill) AS avg_tip_percentage FROM tips GROUP BY day, time, smoker HAVING COUNT(*) > 5;'''
    
df10 = pd.read_sql_query(query10, conn)
print('Issue 10: ')
print(df10)

#Additional queries
#UPDATE
cursor = conn.cursor()

update_query = '''UPDATE tips SET smoker = 'Yes' WHERE id = 10;'''
delete_query = '''DELETE FROM tipsWHERE total_bill < 10;'''

#update execution
try:
    cursor.execute(update_query)
    conn.commit()
except Exception as e:
    print(f'Update failed!{e}')

#delete execution
try:
    cursor.execute(delete_query)
    conn.commit()
except Exception as e:
    print(f'Delete failed!{e}')

#close the cursor and connection
cursor.close()    
conn.close()
    
