def main():
    
    # Used the following you tube vidieo for help on how to connect to sqllite db - https://www.youtube.com/watch?v=UZIhVmkrAEs
    import sqlite3
    import pandas as pd

    df = pd.read_csv("data/tips.csv")

    print(df)

    connection = sqlite3.connect('ta2-grok-and-bert.db')

    print("hi")
    df.to_sql('tips', connection, if_exists = "replace")
    print("hi")

    cur = connection.cursor()
    
    #SELECT FUNCTION

    #QUESTION 1
    
    print("Answer to Question 1 from SELECT statements")
    #cur.execute("""SELECT day, count(1) as total_number_of_days, sum(total_bill), sum(tip), ((sum(total_bill) + sum(tip))/sum(total_bill)) as average FROM 'tips' group by "day" """)
    cur.execute("""SELECT day, (((sum(tip))/sum(total_bill))* 100) as average FROM 'tips' group by "day" """)
    rows = cur.fetchall()
    df1 = pd.DataFrame(rows, columns=["Day","Average Tip %"])
    print(df1)
    print("\n\n\n")

    #QUESTION 2
    
    print("Answer to Question 2 from SELECT statements")
    #cur.execute("""SELECT day, count(1) as total_number_of_days, sum(total_bill), sum(tip), ((sum(total_bill) + sum(tip))/sum(total_bill)) as average FROM 'tips' group by "day" """)
    cur.execute("""select Max(total_bill), min(total_bill) from tips """)
    rows = cur.fetchall()
    df2 = pd.DataFrame(rows, columns=["Max Total Bill","Min Total Bill"])
    print(df2)
    print("\n\n\n")

    #QUESTION 3
    
    print("Answer to Question 3 from SELECT statements")
    cur.execute("""select size, count(1) from tips group by size """)
    rows = cur.fetchall()
    df3 = pd.DataFrame(rows, columns=["Size","Number of Parties"])
    print(df3)
    print("\n\n\n")

    #QUESTION 4
    
    print("Answer to Question 4 from SELECT statements")
    cur.execute("""select total_bill, tip from tips where size >= 4 and ((tip*100/total_bill) > 15)""")
    rows = cur.fetchall()
    df4 = pd.DataFrame(rows, columns=["Total Bill","Tip"])
    print(df4)
    print("\n\n\n")

    #QUESTION 5
    
    print("Answer to Question 5 from SELECT statements")
    cur.execute("""select day, time, sum(total_bill), sum(tip), (sum(tip)*100/sum(total_bill))  from tips group by day, time order by (sum(tip)*100/sum(total_bill)) desc""")
    rows = cur.fetchall()
    df5 = pd.DataFrame(rows, columns=["Day","Time", "sum(total_bill)", "sum(tip)", "Total Tip Percent"])
    print(df5)
    print("\n\n\n")

    #QUESTION 6
    
    print("Answer to Question 6 from SELECT statements")
    cur.execute("""select day, time, smoker, (sum(tip)*100/sum(total_bill))  from tips group by day, time, smoker""")
    rows = cur.fetchall()
    df6 = pd.DataFrame(rows, columns=["Day","Time","Smoker", "Total Tip Percent"])
    print(df6)
    print("\n\n\n")

    #QUESTION 7
    
    print("Answer to Question 7 from SELECT statements")
    cur.execute("""select total_bill, tip, tip*100/total_bill  from tips order by total_bill desc LIMIT 0,5""")
    rows = cur.fetchall()
    df7 = pd.DataFrame(rows, columns=["Total bill","Tip","Tip Percent"])
    print(df7)
    print("\n\n\n")

    #QUESTION 8
    
    print("Answer to Question 8 from SELECT statements")
    cur.execute("""select sum(total_bill), sum(tip), max(tip*100/total_bill), min(tip*100/total_bill), day, time  from tips group by day, time""")
    rows = cur.fetchall()
    df8 = pd.DataFrame(rows, columns=["Total bill","Total Tip","Max Tip Percent","Min Tip Percent", "Day", "Time"])
    print(df8)
    print("\n\n\n")

    #QUESTION 9
    
    print("Answer to Question 9 from SELECT statements")
    cur.execute("""select total_bill, tip, tip*100/total_bill from tips where size >= 4 and (tip*100/total_bill) > 15 and total_bill between 50 and 100""")
    rows = cur.fetchall()
    df9 = pd.DataFrame(rows, columns=["Total bill","Tip","Tip Percent"])
    print(df9)
    print("\n\n\n")

    #QUESTION 10
    
    print("Answer to Question 10 from SELECT statements")
    cur.execute("""select day, time, smoker, sum(tip)*100/sum(total_bill), count(*) as combination_count from tips group by day, time, smoker having combination_count > 5""")
    rows = cur.fetchall()
    df10 = pd.DataFrame(rows, columns=["Day","Time","Smoker", "Average Tip Percent", "Combiation Count"])
    print(df10)
    print("\n\n\n")


if __name__ == "__main__":
    main()