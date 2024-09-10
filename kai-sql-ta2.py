import sqlite3
import pandas as pd

def load_csv_to_sqlite(csv_file, db_connection):
    """Load CSV into SQLite and handle errors."""
    try:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file)

        # Use the context manager to handle the connection
        with db_connection:
            # Write the DataFrame to an SQLite table
            df.to_sql('tips.db', db_connection, index=False, if_exists='replace')
        print("CSV loaded into SQLite successfully!")
    except Exception as e:
        print(f"Error occurred while loading CSV: {e}")


def run_query(conn, query):
    try:
        c = conn.cursor()  # Create a cursor object to execute SQL queries
        c.execute(query)  # Execute the query
        results = c.fetchall()  # Fetch all results
        c.close()  # Close the cursor
        return results
    except sqlite3.Error as e:
        print("SQLite error occurred:", e)
        return None

# Function to execute the alter query
def execute_query(conn, query):
    try:
        c = conn.cursor()  # Create cursor
        c.execute(query)  # Execute the query
        conn.commit()  # Commit the changes
        print("Database is updated!")
    except sqlite3.Error as e:
        print(f"SQLite error occurred: {e}")
    finally:
        c.close()  # Ensure the cursor is closed


# Main logic to load and query the CSV file using SQL
def main():
    csv_file = 'data/tips.csv'

    # Use a context manager to ensure the database connection is closed properly
    try:
        with sqlite3.connect('tips.db') as conn:
            # Load CSV into SQLite
            load_csv_to_sqlite(csv_file, conn)

            # 1. SQL query to retrieve the average tip percentage for each day of the week
            query1 =  '''
            SELECT 
                day, 
                AVG((tip / total_bill) * 100) AS avg_tip_percentage
            FROM 
                tips
            GROUP BY 
                day;
            '''
            results = run_query(conn, query1)

            # Print the results
            print('\nQuestion1:')
            if results:
                for row in results:
                    
                    print(row)
            
            # 2. 
            query2 = '''
            SELECT MAX(total_bill) AS max_total_bill, MIN(total_bill) AS min_total_bill
            FROM tips;
            '''
            results = run_query(conn, query2)

            # Print the results
            print('\nQuestion2:')
            if results:
                for row in results:
                    print(row)

            # 3. 
            query3 = '''
            SELECT size, COUNT(*) AS number_of_parties
            FROM tips
            GROUP BY size;
            '''
            results = run_query(conn, query3)

            # Print the results
            print('\nQuestion3:')
            if results:
                for row in results:
                    print(row)
            
            # 4. 
            query4 = '''
            SELECT total_bill, tip
            FROM tips
            WHERE size >= 4 AND (tip / total_bill) * 100 > 15;
            '''
            results = run_query(conn, query4)

            # Print the results
            print('\nQuestion4:')
            if results:
                for row in results:
                    print(row)

            # 5. 
            query5 = '''
            SELECT day, time, total_bill, tip, (tip / total_bill) * 100 AS tip_percentage
            FROM tips
            ORDER BY tip_percentage DESC;
            '''
            results = run_query(conn, query5)

            # Print the results
            print('\nQuestion5:')
            if results:
                for row in results:
                    print(row)
                
            # 6. 
            query6 = '''
            SELECT day, time, smoker, AVG((tip / total_bill) * 100) AS avg_tip_percentage
            FROM tips
            GROUP BY day, time, smoker;
            '''
            results = run_query(conn, query6)

            # Print the results
            print('\nQuestion6:')
            if results:
                for row in results:
                    print(row)
            
            # 7. 
            query7 = '''
            SELECT sex, total_bill, tip, (tip / total_bill) * 100 AS tip_percentage
            FROM tips
            ORDER BY total_bill DESC
            LIMIT 5;
            '''
            results = run_query(conn, query7)

            # Print the results
            print('\nQuestion7:')
            if results:
                for row in results:
                    print(row)
              
            # 8. 
            query8 = '''
            WITH min_max_tip AS
            (SELECT day, time, MAX((tip / total_bill) * 100) AS max_tip_percentage, MIN((tip / total_bill) * 100) AS min_tip_percentage
            FROM tips
            GROUP BY day, time
            )
            SELECT t.day, t.time, t.total_bill, t.tip, (t.tip / t.total_bill) * 100 AS tip_percentage
            FROM tips t
            JOIN min_max_tip mmt
            ON t.day = mmt.day AND t.time = mmt.time
            WHERE (t.tip / t.total_bill) * 100 = mmt.max_tip_percentage
               OR (t.tip / t.total_bill) * 100 = mmt.min_tip_percentage;
            '''
            results = run_query(conn, query8)

            # Print the results
            print('\nQuestion8:')
            if results:
                for row in results:
                    print(row)
                    

            # 9. 
            query9 = '''
            SELECT total_bill, tip, (tip / total_bill) * 100 AS tip_percentage
            FROM tips
            WHERE size >= 4 
            AND (tip / total_bill) * 100 > 15
            AND total_bill BETWEEN 50 AND 100;
            '''
            results = run_query(conn, query9)

            # Print the results
            print('\nQuestion9:')
            if results:
                for row in results:
                    print(row)
                
            # 10. 
            query10 = '''
            WITH avg_tip AS (SELECT day, time, smoker, AVG((tip / total_bill) * 100) AS avg_tip_percentage, COUNT(*) AS record_count
            FROM tips
            GROUP BY day, time, smoker)
            SELECT day, time, smoker, avg_tip_percentage
            FROM avg_tip
            WHERE record_count > 5;
            '''
            results = run_query(conn, query10)

            # Print the results
            print('\nQuestion10:')
            if results:
                for row in results:
                    print(row)


            # Additional Query1:
            # Retrieve the total number of records for each day and time combination
            query_add1 = '''
            SELECT day, time, COUNT(*) AS total_records
            FROM tips
            GROUP BY day, time;
            '''
            results = run_query(conn, query_add1)
            # Print the results
            print('\nAdditional Query1:')
            if results:
                for row in results:
                    print(row)

            # Additional Query2:
            # Retrieve the average tip for each time
            query_add2 = '''
            SELECT time, AVG(tip)
            FROM tips
            GROUP BY time;
            '''
            results = run_query(conn, query_add2)
            # Print the results
            print('\nAdditional Query2:')
            if results:
                for row in results:
                    print(row)

            # Additional Query3:
            # Retrive the number of smoker and non-smoker
            query_add3 = '''
            SELECT smoker, COUNT(*) AS count
            FROM tips
            GROUP BY smoker;
            '''
            results = run_query(conn, query_add3)
            # Print the results
            print('\nAdditional Query3:')
            if results:
                for row in results:
                    print(row)
                    
            # Additional Query4:
            # Retrieve the top 3 largest parties (by size) for each day
            query_add4 = '''
            SELECT day, total_bill, tip, size
            FROM tips
            WHERE size IN (
                SELECT MAX(size)
                FROM tips AS sub
                WHERE sub.day = tips.day
            )
            ORDER BY day, size DESC
            LIMIT 3;
            '''
            results = run_query(conn, query_add4)
            # Print the results
            print('\nAdditional Query4:')
            if results:
                for row in results:
                    print(row)
                    
            # Additional Query5:
            # Retrieve tip percentage of male and female grouped by time
            query_add5 = '''
            SELECT sex, time, AVG((tip / total_bill) * 100) AS avg_tip_percentage
            FROM tips
            GROUP BY sex, time;
            '''
            results = run_query(conn, query_add5)
            # Print the results
            print('\nAdditional Query5:')
            if results:
                for row in results:
                    print(row)
            
            
            
            # Define the SQL update query for UPDATE

            # Step1: Add a column named ID
            addColumn_query = '''
            ALTER TABLE tips
            ADD ID;
            '''
            execute_query(conn, addColumn_query)

            # Step2: Add sequential numbers to ID column
            update_id_query = '''
            UPDATE tips
            SET ID = rowid;
            '''
            execute_query(conn, update_id_query)

            # Step3: Update ID=10 smoker status
            update_query = '''
            UPDATE tips
            SET smoker = 'Yes'
            WHERE ID = 10;
            '''
            execute_query(conn, update_query)

            # Query to print data in the table
            print("\nTable data after the delete:")
            delete_query_test = '''
            SELECT smoker 
            FROM tips 
            WHERE ID = 10;
            '''
            results = run_query(conn, delete_query_test)
            if results:
                for row in results:
                    print(row)

            # Define the SQL delete query for DELETE
            delete_query = '''
            DELETE 
            FROM tips
            WHERE total_bill < 10;
            '''

            execute_query(conn, delete_query)

            # Query to print data in the table
            print("\nTable data after the delete:")
            delete_query_test = '''
            SELECT * 
            FROM tips 
            WHERE total_bill < 10;
            '''
            results = run_query(conn, delete_query_test)
            if results:
                for row in results:
                    print(row)
     
    except sqlite3.Error as e:
        print(f"Connection error: {e}")
# Close the database connection when done
        conn.close()

if __name__ == "__main__":
    main()
