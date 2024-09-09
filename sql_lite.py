import sqlite3
import pandas as pd
import os

#please cd to aipi510-fall24 folder to load the csv file correctly
file_path = os.path.join(os.getcwd(), "data/tips.csv")

try:
    #connecting to the database : 
    #adjusted with context manager to follow best practices
    with sqlite3.connect("tips.db") as conn:
        cursor = conn.cursor()


    # reading the tips database using the pandas library:

    df = pd.read_csv(file_path)
    df.head()


    # Loading the data file to the SQL database :

    df.to_sql("tips", conn, if_exists = "replace")  ## name of the db table(new), connection variable, command to work out what happens when the data/ table exits already.


    # Everytime you want to send in a query, you have to create a cursor object:

    cursor = conn.cursor() # its essentially a pointer


    # printing all the values in as a table before working on them:

    cursor.execute("SELECT * FROM tips")
    items = cursor.fetchone()

    for item in items:
        print(item)

    print("-------------------")
    cursor.execute("SELECT rowid, * FROM tips")
    items = cursor.fetchmany()

    for item in items:
        print(item)

    print("-------------------")

    # 1. Retrieve the average tip percentage for each day of the week

    query = """
    SELECT 
        day,
        AVG((tip / total_bill) * 100) AS average_tip_percentage
    FROM 
        tips
    GROUP BY 
        day
    ORDER BY 
        CASE day
            WHEN 'Sun' THEN 1
            WHEN 'Mon' THEN 2
            WHEN 'Tue' THEN 3
            WHEN 'Wed' THEN 4
            WHEN 'Thu' THEN 5
            WHEN 'Fri' THEN 6
            WHEN 'Sat' THEN 7
        END;
    """
    cursor.execute(query)

    results = cursor.fetchall()
    for row in results:
        print(f"{row[0]}: {row[1]:.2f}% average tip")


    print("-----------")

    # 2. Find the maximum and minimum total bull amounts

    query = """
    SELECT MAX(total_bill),
    MIN(total_bill)
    FROM tips

    """

    cursor.execute(query)
    results = cursor.fetchall()

    print(f"maximum = {results[0][0]} and minimum = {results[0][1]}")
    print("-----------")

    # 3. Count the number of parties for each size

    query = """
    SELECT 
        size, 
        COUNT(*) AS party_count
    FROM 
        tips
    GROUP BY 
        size;
    """

    cursor.execute(query)
    results = cursor.fetchall()


    for size,count in results:
        print(f"size = {size} and count = {count}")
    print("-----------")

    # 4. Retrieve the total bill and tip for parties of size 4 or more, where the tip percentage is greater than 15%

    query = """
    SELECT 
        total_bill, 
        tip 
    FROM
        tips
    WHERE 
    size > 4 
    AND 
    (tip / total_bill) * 100 > 15;

    """

    cursor.execute(query)
    results = cursor.fetchall()

    for i in results:
        print(f"total bill = {i[0]} and tips = {i[1]}")
    print("-----------")


    # 5. Retrieve the total bill, tip amount, and tip percentage for each combination of day and time, sorted by tip percentage in descending order

    query = """
    SELECT 
        total_bill,
        tip,
        (tip / total_bill) * 100 as tip_percentage,
        day,
        time
    FROM 
        tips
    ORDER BY 
        tip_percentage DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    for i in results:
        print(f"Day: {i[3]}, Time: {i[4]}, Total Bill: {i[0]}, Tip: {i[1]}, Tip Percentage: {i[2]:.2f}%")
    print("-----------")


    # 6. Find the average tip percentage for each combination of day, time, and smoker status
    query = """
    SELECT 
        AVG((tip / total_bill) * 100) as avg_tip_percentage,
        day,
        time,
        smoker
    FROM 
        tips
    GROUP BY
        day,
        time,
        smoker;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    for i in results:
        print(f"Average tip percentage = {i[0]} day = {i[1]}, time = {i[2]}, smoker = {i[3]}")
    print("_______")


    # 7. Retrieve the total bill, tip amount, 
    # and tip percentage for each sex, sorted by total bill in descending order, and limit the results to the top 5 records

    query = """
    SELECT 
        total_bill,
        tip,
        (tip / total_bill) * 100 as tip_percentage,
        sex
    FROM 
        tips
    GROUP BY
        sex
    ORDER BY
        total_bill;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    for i in results:
        print(f"sex = {i[3]}, total bill = {i[0]} , tip = {i[1]}, tip_percentage = {i[2]}")
    print("_______")

    # 8. Find the maximum and minimum tip percentage for each day and time combination, along with the corresponding total bill and tip amount

    query = """
    SELECT 
        day,
        time,
        total_bill,
        tip,
        (tip / total_bill) * 100 AS tip_percentage
    FROM 
        tips
    WHERE 
        (day, time, (tip / total_bill) * 100) IN (
            SELECT 
                day,
                time,
                MAX((tip / total_bill) * 100)
            FROM 
                tips
            GROUP BY 
                day, time
            UNION ALL
            SELECT 
                day,
                time,
                MIN((tip / total_bill) * 100)
            FROM 
                tips
            GROUP BY 
                day, time
        )
    ORDER BY 
        day, time, tip_percentage DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print("Max and Min Tip Percentage for Each Day and Time Combination:")
    for row in results:
        print(row)
    print("-----------")

    # 9. Retrieve the total bill, tip amount, and tip percentage for parties of size 4 or more, 
    # where the tip percentage is greater than 15%, and the total bill is between $50 and $100
    query = """
    SELECT 
        total_bill,
        tip,
        (tip / total_bill) * 100 AS tip_percentage
    FROM 
        tips
    WHERE 
        size >= 4 
        AND (tip / total_bill) * 100 > 15 
        AND total_bill BETWEEN 50 AND 100;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print("Total Bill, Tip, and Tip Percentage for Parties of Size 4 or More:")
    for row in results:
        print(row)
    print("-----------")

    # 10. Find the average tip percentage for each combination of day, time, and smoker status, but only include combinations with more than 5 records

    query = """
    SELECT 
        day,
        time,
        smoker,
        AVG((tip / total_bill) * 100) AS average_tip_percentage,
        COUNT(*) AS record_count
    FROM 
        tips
    GROUP BY 
        day, time, smoker
    HAVING 
        COUNT(*) > 5;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print("Average Tip Percentage for Each Day, Time, and Smoker Combination:")
    for row in results:
        print(row)
    print("-----------")

    #11 Retrieve the total number of parties for each sex and the average size of the party.

    query = """
    SELECT 
        sex,
        COUNT(*) AS number_of_parties,
        AVG(size) AS average_party_size
    FROM 
        tips
    GROUP BY 
        sex;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(f"Sex: {row[0]}, Number of Parties: {row[1]}, Average Party Size: {row[2]:.2f}")
    print("-----------")

    #12 Find the average tip percentage for each party size where the total bill exceeds $30.

    query = """
    SELECT 
        size,
        AVG((tip / total_bill) * 100) AS average_tip_percentage
    FROM 
        tips
    WHERE 
        total_bill > 30
    GROUP BY 
        size;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print(f"Party Size: {row[0]}, Average Tip Percentage: {row[1]:.2f}%")
    print("-----------")

    #13 Find the median total bill for each day of the week.

    query = """
    WITH BillRanks AS (
        SELECT 
            day, 
            total_bill,
            ROW_NUMBER() OVER (PARTITION BY day ORDER BY total_bill) AS rank,
            COUNT(*) OVER (PARTITION BY day) AS total_count
        FROM 
            tips
    )
    SELECT 
        day,
        AVG(total_bill) AS median_total_bill
    FROM 
        BillRanks
    WHERE 
        rank IN ((total_count + 1) / 2, (total_count + 2) / 2)
    GROUP BY 
        day;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print(f"Day: {row[0]}, Median Total Bill: {row[1]:.2f}")
    print("-----------")

    #14 Find the total number of non-smokers vs. smokers for each time (Lunch/Dinner) and their average tip percentage

    query = """
    SELECT 
        smoker,
        time,
        COUNT(*) AS number_of_customers,
        AVG((tip / total_bill) * 100) AS average_tip_percentage
    FROM 
        tips
    GROUP BY 
        smoker, time;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print(f"Smoker: {row[0]}, Time: {row[1]}, Number of Customers: {row[2]}, Average Tip Percentage: {row[3]:.2f}%")
    print("-----------")

    #15 Find the top 3 party sizes by frequency and their corresponding average tip percentage.

    query = """
    SELECT 
        size,
        COUNT(*) AS frequency,
        AVG((tip / total_bill) * 100) AS average_tip_percentage
    FROM 
        tips
    GROUP BY 
        size
    ORDER BY 
        frequency DESC
    LIMIT 3;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print(f"Party Size: {row[0]}, Frequency: {row[1]}, Average Tip Percentage: {row[2]:.2f}%")
    print("-----------")

    #UPDATE, Changing row id 10's smoker status to Yes
    update_query = """
    UPDATE tips
    SET smoker = 'Yes'
    WHERE rowid = 10;
    """
    cursor.execute(update_query)
    #change auto commits

    #To confirm to the executor that the change has been made
    print("Record with rowid=10 has been updated to set smoker to Yes.")

    #DELETE, deleting records for the database where total bill is less than $10
    delete_query = """
    DELETE FROM tips
    WHERE total_bill < 10;
    """
    cursor.execute(delete_query)
    #change auto commits

    # Confirm again to the executor that the change has been made
    print("Records with total bill less than $10 have been deleted.")


#best practice error handling
except sqlite3.Error as e:
    print(f"An error occurred: {e}")

#connection automatically closes