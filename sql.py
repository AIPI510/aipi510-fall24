import sqlite3
import pandas as pd

file = 'data/tips.csv'

df = pd.read_csv(file)

try:

    with sqlite3.connect('tips.db') as conn:


        # Write the dataFrame to the SQLite database
        df.to_sql('tips', conn, if_exists='replace', index=False)

        


        #1. Retrieve the average tip percentage for each day of the week
        query_1 = """
        SELECT day, AVG(ROUND((tip / total_bill) * 100,2)) AS avg_tip_percentage
        FROM tips
        GROUP BY day
        """
        
        #2. Find the maximum and minimum total bill amounts
        query_2 = """
        SELECT MAX(total_bill), MIN(total_bill) 
        FROM tips
        """

        #3. Count the number of parties for each size
        query_3 ="""
        SELECT size, COUNT(*) AS count_per_size 
        FROM tips 
        GROUP BY size
        """

        #4. Retrieve the total bill and tip for parties of size 4 or more, where the tip percentage is greater than 15%
        query_4="""
        SELECT SUM(total_bill), SUM(tip)
        FROM tips
        WHERE size > 4 AND ((tip / total_bill) * 100) > 15
        """

        #5. Retrieve the total bill, tip amount, and tip percentage for each combination of day and time, sorted by tip percentage in descending order
        query_5="""
        SELECT day, time, SUM(total_bill), SUM(tip), AVG(ROUND((tip / total_bill) * 100,2)) AS avg_tip_percentage
        FROM tips
        GROUP BY day, time
        ORDER BY avg_tip_percentage DESC;
        """

        #6. Find the average tip percentage for each combination of day, time, and smoker status
        query_6="""
        SELECT day,time,smoker, ROUND((tip / total_bill) * 100,2) as tip_percentage 
        FROM tips 
        GROUP BY day, time, smoker
        """

        #7. Retrieve the total bill, tip amount, and tip percentage for each sex, sorted by total bill in descending order, and limit the results to the top 5 records
        query_7="""

        """

        #8. Find the maximum and minimum tip percentage for each day and time combination, along with the corresponding total bill and tip amount
        query_8="""
        WITH tip_percents AS (
        SELECT day, time, total_bill, tip, ROUND((tip / total_bill) * 100,2) AS tip_percentage
        FROM tips), max_tips AS (
        SELECT
            day,
            time,
            MAX(tip_percentage) AS max_tip_percentage
        FROM
            tip_percents
        GROUP BY
            day, time
    ),
    min_tips AS (
        SELECT
            day,
            time,
            MIN(tip_percentage) AS min_tip_percentage
        FROM
            tip_percents
        GROUP BY
            day, time
    )
    SELECT
        tp.day,
        tp.time,
        tp.total_bill,
        tp.tip,
        tp.tip_percentage,
        'Max' AS tip_type
    FROM
        tip_percents as tp
    JOIN
        max_tips as mt
    ON
        tp.day = mt.day AND
        tp.time = mt.time AND
        tp.tip_percentage = mt.max_tip_percentage

    UNION ALL

    SELECT
        tp.day,
        tp.time,
        tp.total_bill,
        tp.tip,
        tp.tip_percentage,
        'Min' AS tip_type
    FROM
        tip_percents as tp
    JOIN
        min_tips as mit
    ON
        tp.day = mit.day AND
        tp.time = mit.time AND
        tp.tip_percentage = mit.min_tip_percentage
        """

        #9. Retrieve the total bill, tip amount, and tip percentage for parties of size 4 or more, where the tip percentage is greater than 15%, and the total bill is between $50 and $100
        query_9="""
        SELECT total_bill, tip, ROUND(tip/total_bill*100, 2) as tip_percentage
        FROM tips
        WHERE size >= 4 and tip/total_bill*100 > 15 and total_bill <= 100 and total_bill >= 50
        """

        #10. Find the average tip percentage for each combination of day, time, and smoker status, but only include combinations with more than 5 records
        query_10="""
        SELECT AVG(ROUND(tip/total_bill*100, 2)) as tip_percentage
        FROM tips
        GROUP BY day, time, smoker
        HAVING COUNT(*) > 5
        """

        # Retrieve the day and sex combination with the highest average tip percentage
        query_add_1="""
        SELECT day, sex, ROUND(AVG(tip/total_bill*100),2) AS avg_tip_percentage
        FROM tips
        GROUP BY day, sex
        ORDER BY avg_tip_percentage DESC
        LIMIT 1
        """

        # Retrieve the total bill and total tip amounts for each combination of sex and day
        query_add_2="""
        SELECT sex, day, SUM(total_bill), SUM(tip)
        FROM tips
        GROUP BY sex, day
        """

        #Finding the average percent tip between non-smokers and smokers
        query_add_3="""
        SELECT smoker, ROUND(AVG(tip/total_bill*100),2) as tip_percentage
        FROM tips
        GROUP BY smoker
        """

        #Ordering size by which group tips the most on average
        query_add_4="""
        SELECT size, ROUND(AVG(tip/total_bill*100),2) as tip_percentage
        FROM tips
        GROUP BY size
        ORDER BY tip_percentage DESC
        """

        #Seeing who tips the most based on sex and larger party sizes, 4 and up
        query_add_5="""
        SELECT sex, size, ROUND(AVG(tip/total_bill*100),2) as tip_percentage
        FROM tips
        WHERE size >= 4
        GROUP BY size, sex
        ORDER BY tip_percentage DESC
        """

        

        #update



        #Delete records from the database that have a total bill that is less than $10.
        query_del="""
        DELETE FROM tips
        WHERE total_bill < 10
        """

        # run the query
        result_1 = conn.execute(query_1).fetchall()
        result_2 = conn.execute(query_2).fetchall()
        result_3 = conn.execute(query_3).fetchall()
        result_4 = conn.execute(query_4).fetchall()
        result_5 = conn.execute(query_5).fetchall()
        result_6 = conn.execute(query_6).fetchall()
        #result_7 = conn.execute(query_7).fetchall()
        #result_8 = conn.execute(query_8).fetchall()
        result_9 = conn.execute(query_9).fetchall()
        #result_10 = conn.execute(query_10).fetchall()

        result_add_1 = conn.execute(query_add_1).fetchall()
        result_add_2 = conn.execute(query_add_2).fetchall()
        #result_add_3 = conn.execute(query_add_3).fetchall()
        #result_add_4 = conn.execute(query_add_4).fetchall()
        #result_add_5 = conn.execute(query_add_5).fetchall()

        


        # Print the results

        print('---Question1---')
        for row in result_1:
            day, avg_tip_percentage = row
            print(f"Day: {day}, Average Tip Percentage: {avg_tip_percentage:.2f}%")

        print('---Question2---')
        for row in result_2:
            maximum, minimum= row
            print(f"Maximim: {maximum}, Minimum: {minimum}")

        print('---Question3---')
        for row in result_3:
            size, count_per_size = row
            print(f"Size: {size}, number of parties: {count_per_size}")

        print('---Question4---')
        for row in result_4:
            bill, tip= row
            print(f"Total bill: {bill}, Total tip: {tip}")    

        print('---Question5---')
        for row in result_5:
            day, time, total_bill, total_tip, avg_tip_percentage = row
            print(f"Day: {day}, Time: {time}, Total Bill: ${total_bill:.2f}, Total Tip: ${total_tip:.2f}, Average Tip Percentage: {avg_tip_percentage:.2f}%")

        print('---Question6---')
        for row in result_6:
            day, time, smoke, avg_tip_percentage= row
            print(f"Day: {day}, Time: {time}, Smoke Status: {smoke}, Avg tip percentage:{avg_tip_percentage:.2f}")  

        
        print('---Question7---')
        # print Q7 ans

        print('---Question8---')
        # print Q8 ans

        print('---Question9---')
        for row in result_9:
            total_bill, tip, avg_tip_percentage= row
            print(f"Total bill: {total_bill}, Tip: {tip}, Avg tip percentage:{avg_tip_percentage:.2f}")

        print('---Question10---')
        #print Q10 ans

        print('---Additional Question1---')
        print("Below day and sex combination has highest average tip percentage")
        for row in result_add_1:
            day, sex, avg_tip_percentage= row
            print(f"Day: {day}, Sex: {sex}, Avg tip percentage: {avg_tip_percentage:.2f}%") 

        print('---Additional Question2---')
        print('Total bill and total tip amounts for each combination of sex and day')
        for row in result_add_2:
            sex, day, total_bill, total_tip= row
            print(f"Sex: {sex}, Day: {day}, Total bill: {total_bill}, Total tip:{total_tip}") 


        print('---Additional Question3---')
        print('---Additional Question4---')
        print('---Additional Question5---')
        

        # Execute the delete query
        conn.execute(query_del)
    
        # Commit the changes
        conn.commit()

        print("Records with total bill less than $10 have been deleted.")


# Error Handling
except sqlite3.DatabaseError as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


