def main():
    """
        Overview: This script imports tip data from a CSV, stores it in an SQLite database,
        performs various SQL queries to analyze tip and bill data, updates and deletes records, and prints the results.

        Param: None

        Return: None

        Function Logs: This script does not return anything, just prints out query's made from using python and sql.
    """

    # NOTE: Used the following you tube video for help on how to connect to sqllite db - https://www.youtube.com/watch?v=UZIhVmkrAEs

    import sqlite3
    import pandas as pd
    try:
        df = pd.read_csv("data/tips.csv")
        df['id'] = df.index + 1
        print(df)

        with sqlite3.connect('ta2-grok-and-bert.db') as connection:
            # no index column, we want id for the sake of update problem
            df.to_sql('tips', connection, if_exists="replace", index=False)
            cur = connection.cursor()

        #QUESTION 1
            try:
                print("Answer to Question 1 from SELECT statements")
                cur.execute("""SELECT day, round((((sum(tip))/sum(total_bill))* 100),2) as average FROM 'tips' group by "day" """)
                rows = cur.fetchall()
                df1 = pd.DataFrame(rows, columns=["Day","Average Tip %"])
                print(df1)

            except Exception as e:
                print(f"Error in Question 1: {e}")
            print("\n\n\n")


        #QUESTION 2
            try:
                print("Answer to Question 2 from SELECT statements")
                cur.execute("""select Max(total_bill), min(total_bill) from tips """)
                rows = cur.fetchall()
                df2 = pd.DataFrame(rows, columns=["Max Total Bill","Min Total Bill"])
                print(df2)
            except Exception as e:
                print(f"Error in Question 2: {e}")
            print("\n\n\n")


        #QUESTION 3
            try:
                print("Answer to Question 3 from SELECT statements")
                cur.execute("""select size, count(1) from tips group by size """)
                rows = cur.fetchall()
                df3 = pd.DataFrame(rows, columns=["Size","Number of Parties"])
                print(df3)
            except Exception as e:
                print(f"Error in Question 3: {e}")
            print("\n\n\n")


        #QUESTION 4
            try:
                print("Answer to Question 4 from SELECT statements")
                cur.execute("""select total_bill, tip from tips where size >= 4 and ((tip*100/total_bill) > 15)""")
                rows = cur.fetchall()
                df4 = pd.DataFrame(rows, columns=["Total Bill","Tip"])
                print(df4)
            except Exception as e:
                print(f"Error in Question 4: {e}")
            print("\n\n\n")


        #QUESTION 5
            try:
                print("Answer to Question 5 from SELECT statements")
                cur.execute("""select day, time, sum(total_bill), sum(tip), round((sum(tip)*100/sum(total_bill)),2)  from tips group by day, time order by (sum(tip)*100/sum(total_bill)) desc""")
                rows = cur.fetchall()
                df5 = pd.DataFrame(rows, columns=["Day","Time", "sum(total_bill)", "sum(tip)", "Total Tip Percent"])
                print(df5)
            except Exception as e:
                print(f"Error in Question 5: {e}")
            print("\n\n\n")


        #QUESTION 6
            try:
                print("Answer to Question 6 from SELECT statements")
                cur.execute("""select day, time, smoker, round((sum(tip)*100/sum(total_bill)),2)  from tips group by day, time, smoker""")
                rows = cur.fetchall()
                df6 = pd.DataFrame(rows, columns=["Day","Time","Smoker", "Total Tip Percent"])
                print(df6)
            except Exception as e:
                print(f"Error in Question 6: {e}")
            print("\n\n\n")


        #QUESTION 7
            try:
                print("Answer to Question 7 from SELECT statements")
                cur.execute("""select total_bill, tip, round(tip*100/total_bill, 2)  from tips order by total_bill desc LIMIT 0,5""")
                rows = cur.fetchall()
                df7 = pd.DataFrame(rows, columns=["Total bill","Tip","Tip Percent"])
                print(df7)
            except Exception as e:
                print(f"Error in Question 7: {e}")
            print("\n\n\n")


        # QUESTION 8
            try:
                print("Answer to Question 8 from SELECT statements")
                cur.execute("""select sum(total_bill), sum(tip), round(max(tip*100/total_bill),2), round(min(tip*100/total_bill),2), day, time  from tips group by day, time""")
                rows = cur.fetchall()
                df8 = pd.DataFrame(rows, columns=["Total bill","Total Tip","Max Tip Percent","Min Tip Percent", "Day", "Time"])
                print(df8)
            except Exception as e:
                print(f"Error in Question 8: {e}")
            print("\n\n\n")


        #QUESTION 9
            try:
                print("Answer to Question 9 from SELECT statements")
                cur.execute("""select total_bill, tip, tip*100/total_bill from tips where size >= 4 and (tip*100/total_bill) > 15 and total_bill between 50 and 100""")
                rows = cur.fetchall()
                df9 = pd.DataFrame(rows, columns=["Total bill","Tip","Tip Percent"])
                print(df9)
            except Exception as e:
                print(f"Error in Question 9: {e}")
            print("\n\n\n")

        #QUESTION 10
            try:
                print("Answer to Question 10 from SELECT statements")
                cur.execute("""select day, time, smoker, round(sum(tip)*100/sum(total_bill),2), count(*) as combination_count from tips group by day, time, smoker having combination_count > 5""")
                rows = cur.fetchall()
                df10 = pd.DataFrame(rows, columns=["Day","Time","Smoker", "Average Tip Percent", "Combiation Count"])
                print(df10)
            except Exception as e:
                print(f"Error in Question 10: {e}")
            print("\n\n\n")


        # unique 1
            try:
                print("The average tip % based on gender and smoking")
                cur.execute("""select sex, smoker, round(avg(tip * 100 / total_bill), 2) as avg_tip_percent from tips group by sex, smoker order by avg_tip_percent desc; """)
                rows = cur.fetchall()
                df11 = pd.DataFrame(rows, columns=["Sex", "Smoker", "Average Tip Percent"])
                print(df11)
            except Exception as e:
                print(f"Error in unique 1: {e}")
            print("\n\n\n")


        # unique 2
            try:
                print("The average price each gender spends on lunch and dinner")
                cur.execute("""select sex, time, round(avg(total_bill), 2) as avg_spent from tips group by sex, time order by sex, time; """)
                rows = cur.fetchall()
                df12 = pd.DataFrame(rows, columns=["Gender", "Time", "Average Spent"])
                print(df12)
            except Exception as e:
                print(f"Error in unique 2: {e}")
            print("\n\n\n")


        # unique 3
            try:
                print("The average amount each gender spends each day of the week")
                cur.execute("""select sex, day, round(avg(total_bill), 2) as avg_spent from tips group by sex, day order by sex, day;""")
                rows = cur.fetchall()
                df13 = pd.DataFrame(rows, columns=["Gender", "Day", "Average Spent"])
                print(df13)
            except Exception as e:
                print(f"Error in unique 3: {e}")
            print("\n\n\n")


        # unique 4
            try:
                print("The average tip percent for each gender, day, and time")
                cur.execute("""select sex, day, time, round(avg(tip * 100.0 / total_bill), 2) as avg_tip_percent from tips group by sex, day, time order by sex, day, time; """)
                rows = cur.fetchall()
                df14 = pd.DataFrame(rows, columns=["Gender", "Day", "Time", "Average Tip Percent"])
                print(df14)
            except Exception as e:
                print(f"Error in unique 4: {e}")
            print("\n\n\n")


        # unique 5
            try:
                print("The average bill amount for different bill ranges")
                cur.execute("""select case when total_bill < 25 then 'Less than $25'
                                            when total_bill >= 25 and total_bill < 50 then '$25 - $50'
                                            when total_bill >= 50 and total_bill < 75 then '$50 - $75'
                                            when total_bill >= 75 and total_bill < 100 then '$75 - $100'
                                            else '$100+' end as bill_range, round(avg(total_bill),2) as avg_bill from tips group by bill_range;""")
                rows = cur.fetchall()
                df15 = pd.DataFrame(rows, columns=["Bill Range", "Average Bill Amount"])
                print(df15)
            except Exception as e:
                print(f"Error in unique 5: {e}")
            print("\n\n\n")


        # update
            try:
                print("Update Query")
                cur.execute("""update tips set smoker = 'Yes' where id = 10""")
                connection.commit()
            except Exception as e:
                print(f"There was an error in the update process: {e}")


            # verify
            try:
                cur.execute("select * from tips where id = 10")
                rows = cur.fetchall()
                if rows:
                    dfVerifyUpdate = pd.DataFrame(rows, columns=df.columns)
                    print(dfVerifyUpdate)
                else:
                    print("No data found for verification.")
            except Exception as e:
                print(f"There was an error in the verification process: {e}")
            print("\n\n\n")

        # delete
            try:
                print("Delete query")
                cur.execute("delete from tips where total_bill < 10")
                connection.commit()
            except Exception as e:
                print(f"There was an error in the delete process: {e}")


            # verify
            try:
                # set to 15 to prove that deletion acc works
                cur.execute("select * from tips where total_bill < 10")
                rows = cur.fetchall()
                # no rows under 10 created conditional to prevent error
                if not rows:
                    print("No totals that have less than $10")
                else:
                    dfVerifyDelete = pd.DataFrame(rows, columns=df.columns)
                    print(dfVerifyDelete)
            except Exception as e:
                print(f"There was an error in the verification process: {e}")



    # end of file catch
    except sqlite3.Error as e:
        print(f"Error from SQL: {e}")
    except Exception as e:
        print(f"Theres a error in the main code: {e}")

if __name__ == "__main__":
    main()