""" Akhil Chintalapati & John Rohan Ernest Jayaraj 

██████   █████  ██████      ██████   █████  ████████  █████      ██████  ██    ██ ███████ ████████ ███████ ██████  ███████ 
██   ██ ██   ██ ██   ██     ██   ██ ██   ██    ██    ██   ██     ██   ██ ██    ██ ██         ██    ██      ██   ██ ██      
██████  ███████ ██   ██     ██   ██ ███████    ██    ███████     ██████  ██    ██ ███████    ██    █████   ██████  ███████ 
██   ██ ██   ██ ██   ██     ██   ██ ██   ██    ██    ██   ██     ██   ██ ██    ██      ██    ██    ██      ██   ██      ██ 
██████  ██   ██ ██████      ██████  ██   ██    ██    ██   ██     ██████   ██████  ███████    ██    ███████ ██   ██ ███████ 
                                                                                                                           
                                                                                                                           
███████  ██████  ██████       █████  ██ ██████  ██ ███████  ██  ██████                                                     
██      ██    ██ ██   ██     ██   ██ ██ ██   ██ ██ ██      ███ ██  ████                                                    
█████   ██    ██ ██████      ███████ ██ ██████  ██ ███████  ██ ██ ██ ██                                                    
██      ██    ██ ██   ██     ██   ██ ██ ██      ██      ██  ██ ████  ██                                                    
██       ██████  ██   ██     ██   ██ ██ ██      ██ ███████  ██  ██████                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

"""


import sqlite3  # Importing SQLite3 to interact with the SQLite database in Python, making it easy to use SQL databases without external dependencies.
import pandas as pd  # Pandas is used to load and manage CSV files and handle data efficiently. It simplifies data manipulation for analysis and database insertion.

# Constants for consistent formatting and table names
LINE_SEPARATOR = "#****************************************************************************************************************************************#"
# Separating sections with a constant line of stars to maintain visual clarity and formatting in the output.
DEFAULT_DB_NAME = 'data_storage_access.db'  # Defining a default database name for simplicity and reuse.
DEFAULT_TABLE_NAME = 'table_name'  # Default name for the table created in the database, making the code more flexible.
DEFAULT_CSV_PATH = 'tips.csv'  # Path to the CSV file, allowing flexibility in case the file is stored elsewhere.

#***********************************************************************************************************************************************#

def create_database(db_name=DEFAULT_DB_NAME, table_name=DEFAULT_TABLE_NAME, csv_path=DEFAULT_CSV_PATH):
    """
    Function to create a SQLite database from a CSV file.
    Adds an 'id' column to the DataFrame to ensure each row has a unique identifier.
    """
    try:
        # Loading the CSV file into a DataFrame to easily manage and manipulate the data using Pandas.
        df = pd.read_csv(csv_path)
        # Adding an 'id' column to the DataFrame starting from 0, ensuring each row has a unique ID for database indexing.
        df['id'] = range(0, len(df))
        # Reordering columns so 'id' comes first, followed by the rest of the original columns.
        df = df[['id'] + [col for col in df.columns if col != 'id']]

        # Using a context manager to ensure the database connection is safely opened and closed.
        with sqlite3.connect(db_name) as conn:
            # Writing the DataFrame into a SQL table. If the table exists, it will be replaced to avoid conflicts.
            df.to_sql(table_name, conn, if_exists='replace', index=False)

            # Providing a formatted message to confirm successful database creation and showing the first few rows.
            print(f"Database '{db_name}' created and populated successfully with table '{table_name}': \n")
            print(df.head())  # Displaying the first 5 rows of the DataFrame for a quick preview.
            print(f"\n{LINE_SEPARATOR}\n")

    except Exception as e:
        # Catching any exceptions that occur during the process and providing an error message.
        print(f"Error creating database: {e}")

create_database()  # Creating the database and populating it with data from the CSV file.

#***********************************************************************************************************************************************#

def execute_query_and_display(query, params=None, db_name=DEFAULT_DB_NAME, table_name=DEFAULT_TABLE_NAME):
    """
    Executes a SQL query and fetches results, displaying them as a Pandas DataFrame for clarity and readability.
    """
    try:
        # Using a context manager to manage the connection and ensure it closes properly after execution.
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()  # Creating a cursor object to execute the SQL query.

            # If query parameters are provided, execute a parameterized query to avoid SQL injection risks.
            if params:
                cursor.execute(query, params)
            else:
                # Otherwise, executing the query as it is.
                cursor.execute(query)

            rows = cursor.fetchall()  # Fetching all the results of the query.

            # If no results were returned, inform the user.
            if not rows:
                print(f"\n No results found \n{LINE_SEPARATOR}\n")
                return

            # If results are found and the cursor contains metadata (column names), display them as a DataFrame.
            if cursor.description:
                col_names = [desc[0] for desc in cursor.description]  # Extracting column names from the cursor.
                result_df = pd.DataFrame(rows, columns=col_names)  # Creating a DataFrame from the query results.
                print(result_df)  # Displaying the query results in a tabular format.
                print(f"\n{LINE_SEPARATOR}\n")
            else:
                # Inform the user if no column information is available in the query result.
                print(f"\nQuery executed, but no column information was available.\n")

    except sqlite3.Error as e:
        # Handling SQLite-specific errors.
        print(f"SQLite error occurred: {e}")
    except Exception as e:
        # Handling general exceptions to provide feedback if something goes wrong.
        print(f"Error executing query: {e}")

#***********************************************************************************************************************************************#

def update_record(record_id=10, db_name=DEFAULT_DB_NAME, table_name=DEFAULT_TABLE_NAME):
    """
    Updates a specific record in the table by changing the 'smoker' status to 'Yes'.
    The record is identified by its 'id', and the function provides feedback on success or failure.
    """
    try:
        query = f"""
            UPDATE {table_name}
            SET smoker = 'Yes'
            WHERE id = :id;
        """  # SQL query to update the 'smoker' field for a specific record identified by 'id'.
        params = {"id": record_id}  # Defining parameters to prevent SQL injection and safely inject the 'id'.

        # Using a context manager to handle the connection.
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()  # Creating a cursor to execute the query.
            cursor.execute(query, params)  # Executing the parameterized query with the given 'id'.
            conn.commit()  # Committing the transaction to save changes.

            # Checking if any rows were affected (i.e., whether the record was found and updated).
            if cursor.rowcount > 0:
                print(f"\n Record with id={record_id} successfully updated.\n")
            else:
                print(f"\n\nNo record found with id={record_id} to update.\n")

            # Displaying the updated database head to confirm changes.
            print("\nDatabase Head After Update: \n")
            select_query = f"SELECT * FROM {table_name} LIMIT 11"  # Query to retrieve the first few records.
            execute_query_and_display(select_query)  # Reusing the function to display the query results.

    except Exception as e:
        # Handling errors during the update process and printing a meaningful error message.
        print(f"Error updating record with id={record_id}: {e}")

#***********************************************************************************************************************************************#

def delete_records(db_name=DEFAULT_DB_NAME, table_name=DEFAULT_TABLE_NAME):
    """
    Deletes records from the table where the total bill is less than $10.
    Provides feedback on whether records were deleted or no matching records were found.
    """
    query = f"""
        DELETE FROM {table_name}
        WHERE total_bill < 10;
    """  # SQL query to delete records where the total bill is less than $10.

    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()  # Creating a cursor to execute the delete query.
            cursor.execute(query)  # Executing the deletion.
            conn.commit()  # Committing the transaction to apply changes.

            # Checking if any rows were deleted and providing feedback to the user.
            if cursor.rowcount > 0:
                print(f"\nRecord(s) deleted successfully.\n")
            else:
                print(f"\nNo records found matching the given criteria.\n")

            # Displaying the remaining data after deletion.
            print("\nDatabase Head After Deletion of Given Criteria Record(s): \n")
            select_query = f"SELECT * FROM {table_name} LIMIT 11"  # Query to retrieve the first few records.
            execute_query_and_display(select_query)  # Display the query results using the helper function.

    except Exception as e:
        # Handling errors during the deletion process and printing an appropriate error message.
        print(f"Error deleting records: {e}")

#***********************************************************************************************************************************************#

# Now, let's reuse the execute_query_and_display to perform the various queries:

# 1. Retrieve the average tip percentage for each day of the week
# Here, we are calculating the average tip percentage for each day of the week.
# The formula (tip / total_bill) * 100 gives us the percentage of the tip relative to the bill.
# GROUP BY day ensures that we calculate the average for each distinct day.
query = f"""
    SELECT day, AVG((tip/total_bill) * 100) AS avg_tip_percentage
    FROM {DEFAULT_TABLE_NAME}
    GROUP BY day;

"""
print("Average tip percentage for each day of the week: \n")
execute_query_and_display(query)

#***********************************************************************************************************************************************#

# 2. Find the maximum and minimum total bill amounts
# This query uses SQL's aggregation functions MAX() and MIN() to retrieve the largest and smallest total bills.
# These functions scan all rows and return the respective values without any need for grouping.
query = f"""
    SELECT MAX(total_bill) AS max_total_bill, MIN(total_bill) AS min_total_bill
    FROM {DEFAULT_TABLE_NAME};
"""
print("Maximum and minimum total bill amounts: \n")
execute_query_and_display(query)

#***********************************************************************************************************************************************#

# 3. Count the number of parties for each size
# Here, we want to know how many parties are present for each unique group size. We use GROUP BY size to
# categorize the records by size, and then we use COUNT(*) to count how many rows belong to each group size.
query = f"""
    SELECT size, COUNT(*) AS number_of_parties
    FROM {DEFAULT_TABLE_NAME}
    GROUP BY size;
"""
print("Number of parties for each size: \n")
execute_query_and_display(query)

#***********************************************************************************************************************************************#

# 4. Retrieve the total bill and tip for parties of size 4 or more where the tip percentage is greater than 15%
# We are filtering the data to only show parties with a size of 4 or more AND where the tip percentage exceeds 15%.
# This query uses a combination of WHERE to filter for conditions and calculates the tip percentage with (tip/total_bill) * 100.
query = f"""
    SELECT total_bill, tip
    FROM {DEFAULT_TABLE_NAME}
    WHERE size >= 4 AND (tip/total_bill) * 100 > 15;
"""
print("Total bill and tip for parties of size 4 or more where the tip percentage is greater than 15%: \n")
execute_query_and_display(query)

#***********************************************************************************************************************************************#

# 5. Retrieve the total bill, tip amount, and tip percentage for each combination of day and time, sorted by tip percentage in descending order
# This query calculates the total bill, total tip, and the overall tip percentage for each combination of day and time.
# It then sorts the results by tip percentage in descending order to show the highest percentages first.

query = f"""
    SELECT day, time,
           SUM(total_bill) AS total_bill_sum,    -- Sum of all total bills for the specific combination of day and time
           SUM(tip) AS total_tip_sum,            -- Sum of all tips for the specific combination of day and time
           (SUM(tip) / SUM(total_bill)) * 100 AS tip_percentage  -- Calculate the tip percentage for the combination using the summed values of tips and total bills
    FROM {DEFAULT_TABLE_NAME}
    GROUP BY day, time                           -- Grouping by both day and time ensures we get the sums for each combination of day and time
    ORDER BY tip_percentage DESC;                -- Sorting the result by tip percentage in descending order to show the highest tip percentages first
"""

# Executing and displaying the query
print("Total bill, total tip amount, and tip percentage for each combination of day and time, sorted by tip percentage: \n")
execute_query_and_display(query)

#***********************************************************************************************************************************************#

# 6. Find the average tip percentage for each combination of day, time, and smoker status
# This query calculates the average tip percentage for each group of day, time, and smoker status.
# It uses AVG to calculate the average of the tip percentage for each group.

query = f"""
    SELECT day, time, smoker,                                 -- Selects the day, time, and smoker status columns for grouping
           AVG((tip / total_bill) * 100) AS avg_tip_percentage  -- Calculates the average tip percentage for each group of day, time, and smoker
    FROM {DEFAULT_TABLE_NAME}
    GROUP BY day, time, smoker;                               -- Groups the records by day, time, and smoker status to calculate the average tip percentage for each group
"""

# Executing and displaying the query
print("Average tip percentage for each combination of day, time, and smoker status: \n")
execute_query_and_display(query)

#***********************************************************************************************************************************************#

# 7. Retrieve the total bill, tip amount, and tip percentage for each sex, sorted by total bill in descending order, and limit to top 5 records
# This query retrieves the total bill, tip amount, and tip percentage for each sex (Male or Female).
# It then sorts the results by total bill in descending order and limits the result to the top 5 records.

query = f"""
    SELECT sex,                                         -- Selects the sex (Male or Female) column
           total_bill,                                  -- Selects the total bill amount
           tip,                                         -- Selects the tip amount
           (tip / total_bill) * 100 AS tip_percentage   -- Calculates the tip percentage for each record
    FROM {DEFAULT_TABLE_NAME}
    ORDER BY total_bill DESC                            -- Orders the results by total bill in descending order, so the highest bills come first
    LIMIT 5;                                            -- Limits the result to the top 5 records (highest bills)
"""

# Executing and displaying the query
print("Total bill, tip amount, and tip percentage for each sex (Top 5 records by total bill): \n")
execute_query_and_display(query)

#***********************************************************************************************************************************************#

# 8. Find the maximum and minimum tip percentage for each day and time combination, along with the corresponding total bill and tip amount
# This query finds the maximum and minimum tip percentage for each day and time combination.
# It also retrieves the corresponding total bill and tip amount for both the maximum and minimum percentages.

query = f"""
    SELECT day, time,                                   -- Selects the day and time columns for grouping
           MAX((tip / total_bill) * 100) AS max_tip_percentage,  -- Calculates the maximum tip percentage for the day and time combination
           MIN((tip / total_bill) * 100) AS min_tip_percentage,  -- Calculates the minimum tip percentage for the day and time combination
           MAX(total_bill) AS max_total_bill,                   -- Retrieves the total bill corresponding to the maximum tip percentage
           MIN(total_bill) AS min_total_bill,                   -- Retrieves the total bill corresponding to the minimum tip percentage
           MAX(tip) AS max_tip_amount,                          -- Retrieves the tip amount corresponding to the maximum tip percentage
           MIN(tip) AS min_tip_amount                           -- Retrieves the tip amount corresponding to the minimum tip percentage
    FROM {DEFAULT_TABLE_NAME}
    GROUP BY day, time;                              -- Groups the data by day and time
"""

# Executing and displaying the query
print("Maximum and minimum tip percentage for each day and time combination, along with corresponding total bill and tip amount: \n")
execute_query_and_display(query)

#***********************************************************************************************************************************************#

# 9. Retrieve the total bill, tip amount, and tip percentage for parties of size 4 or more, where the tip percentage is greater than 15%, and the total bill is between $50 and $100
# This query applies multiple conditions with WHERE to ensure that the party size is 4 or more, tip percentage is greater than 15%,
# and the total bill falls between $50 and $100.
query = f"""
    SELECT total_bill, tip, (tip/total_bill) * 100 AS tip_percentage
    FROM {DEFAULT_TABLE_NAME}
    WHERE size >= 4 AND (tip/total_bill) * 100 > 15 AND total_bill BETWEEN 50 AND 100;
"""
print("Total bill, tip amount, and tip percentage for parties of size 4 or more with tips > 15% and total bill between $50 and $100: \n")
execute_query_and_display(query)

#***********************************************************************************************************************************************#

# 10. Find the average tip percentage for each combination of day, time, and smoker status, but only include combinations with more than 5 records
# This query calculates the average tip percentage for each combination of day, time, and smoker status.
# It includes only those combinations where there are more than 5 records.

query = f"""
    SELECT day, time, smoker,                            -- Selects the day, time, and smoker status for grouping
           AVG((tip / total_bill) * 100) AS avg_tip_percentage  -- Calculates the average tip percentage for each combination
    FROM {DEFAULT_TABLE_NAME}
    GROUP BY day, time, smoker                           -- Groups the data by day, time, and smoker status
    HAVING COUNT(*) > 5;                                -- Includes only combinations that have more than 5 records
"""

# Executing and displaying the query
print("Average tip percentage for each combination of day, time, and smoker status, for combinations with more than 5 records: \n")
execute_query_and_display(query)

#***********************************************************************************************************************************************#

# ADVANCED AND COMPLEX FUN OPERATIONS

# 11. Find the most generous tipper (highest tip percentage)
# This query identifies the most generous tipper by calculating the tip percentage and ordering by it in descending order.
# LIMIT 1 ensures we only get the top result with the highest tip percentage.
query = f"""
    SELECT total_bill, tip, (tip/total_bill) * 100 AS tip_percentage
    FROM {DEFAULT_TABLE_NAME}
    ORDER BY tip_percentage DESC
    LIMIT 1;
"""
print("Most generous tipper (highest tip percentage): \n")
execute_query_and_display(query)

#***********************************************************************************************************************************************#

# 12. Find the total amount of tips given on weekends (Saturday and Sunday)
# This query calculates the total amount of tips given on weekends (Saturday and Sunday) using SUM() on the tip column.
# We use WHERE day IN ('Sat', 'Sun') to filter the results to only show weekend days.
query = f"""
    SELECT day, SUM(tip) AS total_tips
    FROM {DEFAULT_TABLE_NAME}
    WHERE day IN ('Sat', 'Sun')
    GROUP BY day;
"""
print("Total tips given on weekends (Saturday and Sunday): \n")
execute_query_and_display(query)

#***********************************************************************************************************************************************#

# 13. Ranking customers by total bill amount using a window function
# This query uses the RANK() window function to rank customers based on their total bill.
# The result assigns a rank to each customer based on their bill, starting with the highest bills at rank 1.
query = f"""
    SELECT id, total_bill, RANK() OVER (ORDER BY total_bill DESC) AS rank
    FROM {DEFAULT_TABLE_NAME};
"""
print("Ranking customers by total bill amount: \n")
execute_query_and_display(query)

#***********************************************************************************************************************************************#

# 14. Find the longest streak of consecutive days where the tip percentage was greater than 20%
# This query is a bit tricky: it detects consecutive days where the tip percentage was above 20%.
# We use a window function (LAG) to look at the previous row and compare it to find consecutive days.
query = f"""
    WITH tip_streaks AS (
        SELECT day,
               (tip / total_bill) * 100 AS tip_percentage,
               LAG(day) OVER (ORDER BY day) AS prev_day
        FROM {DEFAULT_TABLE_NAME}
    )
    SELECT COUNT(*) AS consecutive_days_above_20
    FROM tip_streaks
    WHERE tip_percentage > 20 AND prev_day IS NOT NULL;
"""
print("Longest streak of consecutive days where the tip percentage was greater than 20%: \n")
execute_query_and_display(query)

#***********************************************************************************************************************************************#

# 15. Detecting Outliers in Tip Amounts using IQR Method
# This query identifies tips that are unusually high or low (outliers) based on an approximation of quartiles.
# Since SQLite doesn't support PERCENTILE_CONT(), we calculate Q1 and Q3 using the rank-based method.

query = f"""
    -- Step 1: Rank the tips to calculate Q1 and Q3
    WITH ranked_tips AS (
        SELECT tip,
               NTILE(4) OVER (ORDER BY tip) AS quartile -- NTILE(4) divides the data into 4 quartiles
        FROM {DEFAULT_TABLE_NAME}
    ),

    -- Step 2: Calculate Q1, Q3, and the IQR
    stats AS (
        SELECT
            MIN(CASE WHEN quartile = 1 THEN tip END) AS q1,  -- Approximation of Q1 (25th percentile)
            MIN(CASE WHEN quartile = 3 THEN tip END) AS q3   -- Approximation of Q3 (75th percentile)
        FROM ranked_tips
    ),

    -- Step 3: Calculate the lower and upper bounds for outliers
    outlier_bounds AS (
        SELECT
            q1, q3,
            q1 - 1.5 * (q3 - q1) AS lower_bound,  -- Lower bound: Q1 - 1.5 * IQR
            q3 + 1.5 * (q3 - q1) AS upper_bound   -- Upper bound: Q3 + 1.5 * IQR
        FROM stats
    )

    -- Step 4: Identify and select the outliers
    SELECT *
    FROM {DEFAULT_TABLE_NAME}, outlier_bounds
    WHERE tip < lower_bound OR tip > upper_bound;  -- Tips below the lower bound or above the upper bound are outliers
"""

# Executing and displaying the outlier detection query
print("Outlier detection based on IQR method (Identifying unusually high or low tips): \n")
execute_query_and_display(query)

update_record() # Updating a specific record in the database.
delete_records() # Deleting records where the total bill is less than $10.

#***********************************************************************************************************************************************#