import sqlite3
import pandas as pd

def csv_to_sql(csv_filename):
    csv = csv_filename
    df = pd.read_csv(csv)

    connection = sqlite3.connect('tips_data.db')

    df.to_sql('tips_table', connection, if_exists='replace', index = False)

    connection.commit()
    connection.close()

## csv_to_sql('data/tips.csv') done once


def create_tip_pct():
    with sqlite3.connect('tips_data.db') as connection:
        try:
            # Try to add the new column 'tip_pct'
            connection.execute("ALTER TABLE tips_table ADD COLUMN tip_pct FLOAT")
        except sqlite3.OperationalError as e:
            # Handle the case where the column already exists
            if 'duplicate column name' in str(e).lower():
                print("Column 'tip_pct' already exists, skipping.")
            else:
                print(f"An error occurred: {e}")

        try:
            # populate column
            bill_tip_list = connection.execute("SELECT ROWID, tip, total_bill FROM tips_table")

            for bill_tip in bill_tip_list:
                row_id = bill_tip[0]
                pct_tip = (bill_tip[1] /bill_tip[2]) * 100
                connection.execute("UPDATE tips_table SET tip_pct = ? WHERE ROWID = ?", (pct_tip, row_id))

        except sqlite3.OperationalError as e:
            print(f"an error occurred: {e}")


def Q_one():
    with sqlite3.connect('tips_data.db') as connection:
        days_short = ['Thur','Fri','Sat','Sun'] # only days in dataset through inspection
        
        for day_short in days_short:
            
            avg_pct = connection.execute("SELECT AVG(tip_pct) FROM tips_table WHERE day = ?", (day_short,))
            avg_pct = avg_pct.fetchone()[0]
            
            if(day_short == "Thur"):
                day_short = "Thurs"
            if(day_short == "Sat"):
                day_short = "Satur"
            
            print("the average tip percentage for", day_short + "day", "is", avg_pct)

def Q_two():
    with sqlite3.connect('tips_data.db') as connection:
        max = connection.execute("SELECT MAX(total_bill) FROM tips_table")
        min = connection.execute("SELECT MIN(total_bill) FROM tips_table")

        maxstring = str(max.fetchone()[0])
        minstring = str(min.fetchone()[0])

        print("The maximum total bill was:", "$" + maxstring, "The minimum total bill was", "$" + minstring)

def Q_three():
    with sqlite3.connect('tips_data.db') as connection:

        max = connection.execute("SELECT MAX(size) from tips_table")
        max = max.fetchone()[0]
        min = connection.execute("SELECT MIN(size) from tips_table")
        min = min.fetchone()[0]

        for i in range(min,max):
            count = connection.execute("SELECT COUNT(*) FROM tips_table WHERE size=?", (i,))

            print("The number of parties of size", i, "was", count.fetchone()[0])

        


def Q_four():
    with sqlite3.connect('tips_data.db') as connection:

        bill_tip_sql = connection.execute("SELECT total_bill, tip FROM tips_table WHERE size > 3 AND tip_pct > 15")
        
        print(bill_tip_sql.fetchall())
                

def Q_five():
    with sqlite3.connect('tips_data.db') as connection:

        days_short = ['Thur','Fri','Sat','Sun']
        times = ["Lunch","Dinner"]

        print("data is in the form (bill total, tip, tip percentage)")

        for day in days_short:
            for time in times:
                cursor = connection.execute("SELECT total_bill, tip, tip_pct FROM tips_table WHERE day = ? AND time = ? ORDER BY tip_pct DESC",(day,time,))
                data = cursor.fetchall()

                if(day == "Thur"):
                    day = "Thurs"
                if(day == "Sat"):
                    day = "Satur"

                if len(data) == 0:
                    print("No data for", day + "day", time, "looks like they are closed")
                else:
                    print("Data for", day + "day", time, data)

def Q_six():
    with sqlite3.connect('tips_data.db') as connection:
        days_short = ['Thur','Fri','Sat','Sun']
        times = ["Lunch","Dinner"]
        smoker = ["Yes", "No"]

        for day in days_short:
            for time in times:
                for yorn in smoker:
                    avg = connection.execute("SELECT AVG(tip_pct) FROM tips_table WHERE day = ? AND time = ?",(day,time,))
                    avg = avg.fetchone()[0]

                    if(day == "Thur"):
                        day = "Thurs"
                    if(day == "Sat"):
                        day = "Satur"

                    if(avg == None):
                        print("No data for", day + "day", time, "smoking status =", yorn)
                    else:
                        avg = round(avg,2)
                        if(yorn == "Yes"):
                            print("The average tip percentage for smokers on", day + "day", "at", time, "is", avg)
                        else:
                            print("The average tip percentage for non smokers on", day + "day", "at", time, "is", avg)

def Q_seven():
    with sqlite3.connect('tips_data.db') as connection:
        sexes = ["Male","Female"]

        print("data is in format (total bill, tip, tip percentage)")

        for sex in sexes:
            results = connection.execute("SELECT total_bill, tip, tip_pct FROM tips_table WHERE sex = ? ORDER BY total_bill DESC LIMIT 5", (sex,))

            print("For", sex, "the top 5 results are:", results.fetchall())

def Q_eight():
    with sqlite3.connect('tips_data.db') as connection:

        days_short = ['Thur','Fri','Sat','Sun']
        times = ["Lunch","Dinner"]

        for day in days_short:
            for time in times:
                rowids_sql = connection.execute("SELECT MAX(tip_pct), ROWID from tips_table WHERE day = ? AND time = ?", (day,time,))
                rowids_maxtip = rowids_sql.fetchone()
                if(rowids_maxtip is None or rowids_maxtip[0] is None):
                    print("No data for", day + "day", time)
                else:
                    collect_others = connection.execute("SELECT total_bill, tip from tips_table WHERE ROWID = ?",(rowids_maxtip[1],))
                    data = collect_others.fetchall()
                    
                    if(day == "Thur"):
                        day = "Thurs"
                    if(day == "Sat"):
                        day = "Satur"
                    
                    print("The maxmimum tip percentage for", day + "day", time, "was", round(rowids_maxtip[0],2),"with a bill and tip of", data)

def Q_Nine():
    with sqlite3.connect('tips_data.db') as connection:
        data = connection.execute("SELECT total_bill, tip, tip_pct FROM tips_table WHERE tip_pct > 15 AND size > 3 AND total_bill BETWEEN 50 AND 100")

        print(data.fetchall())



def Q_ten():
    with sqlite3.connect('tips_data.db') as connection:
        days_short = ['Thur','Fri','Sat','Sun']
        times = ["Lunch","Dinner"]
        smoker = ["Yes", "No"]

        for day in days_short:
            for time in times:
                for yorn in smoker:
                    data_curs = connection.execute("SELECT COUNT(*), AVG(tip_pct) FROM tips_table WHERE day = ? AND time = ? and Smoker = ?", (day,time,yorn,))
                    data = data_curs.fetchone()

                    if(day == "Thur"):
                        day = "Thurs"
                    if(day == "Sat"):
                        day = "Satur"

                    if(data is None or data[0] < 5):

                        print("Not enough data for", day + "day", time, "smoker =", yorn)
                    else:
                        print("Average tip percentage for", day + "day", time, "smoker =", yorn, "is", round(data[1],2))

Q_one()
Q_two()
Q_three()
Q_four()
Q_five()
Q_six()
Q_seven()
Q_eight()
Q_Nine()
Q_ten()