''' 
Author:
Jesse Warren & Haochen Li
'''

import sqlite3 # 3.41.2
import csv # came with python package
import os

class SQL_QUERY():
    def __init__(self) -> None:

        ## delete the previous db 
        if os.path.exists("ta2_tips.db"):
            os.remove("ta2_tips.db")

        ## CREATE
        self.conn = sqlite3.connect('ta2_tips.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tips (
            total_bill REAL,
            tip REAL,
            sex TEXT,
            smoker TEXT,
            day TEXT,                      
            time TEXT,           
            size INTEGER                             
        )
        ''')

        ## READ
        with open(os.path.join("data","tips.csv"),"r") as table:
            reader = csv.reader(table)
            for i ,row in enumerate(reader):
                if i == 0: # skip the header
                    continue
                else:
                    self.cursor.execute(
                        "INSERT INTO tips (total_bill, tip, sex, smoker, day, time, size) VALUES (?,?,?,?,?,?,?)",
                        row
                    )
        self.conn.commit()

    '''Function to execute sql query and print results'''
    def execute(self, query):
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(e)

    '''Function to close the connection'''
    def finish(self):
        ## CLOSE
        self.conn.commit()
        self.conn.close()

    '''Functions that implements sql query questions'''
    # Q1 Retrieve the average tip percentage for each day of the week
    def q1(self):
        # use group by
        query = '''
        SELECT day, AVG(tip/total_bill) AS avg_tip_percent
        FROM tips
        GROUP BY day;
        '''
        self.execute(query)

    # Q2 Find the maximum and minimum total bull amounts
    def q2(self):
        query = '''
        SELECT MAX(total_bill), MIN(total_bill)
        FROM tips;
        '''
        self.execute(query)

    # Q3 Count the number of parties for each size
    def q3(self):
        query = '''
        SELECT size, count(size)
        FROM tips
        GROUP BY size;
        '''
        self.execute(query)
    
    # Q4 Retrieve the total bill and tip for parties of size 4 or more, where the tip percentage is greater than 15%
    def q4(self):
        query = '''
        SELECT total_bill, tip
        FROM tips
        WHERE size >=4 and tip > (total_bill*0.15)
        '''
        self.execute(query)
    
    # Q5 Retrieve the total bill, tip amount, and tip percentage for each combination of day and time, sorted by tip percentage in descending order
    def q5(self):
        query = '''
        SELECT total_bill, tip, tip/total_bill AS tip_percent
        FROM tips
        GROUP BY day, time
        ORDER BY tip_percent DESC
        '''
        self.execute(query)

    # Q6 Find the average tip percentage for each combination of day, time, and smoker status
    def q6(self):
        
        query = '''
        SELECT tip/total_bill AS tip_percent
        FROM tips
        GROUP BY day, time, smoker
        '''
        self.execute(query) 

    # Q7 Retrieve the total bill, tip amount, and tip percentage for each sex, sorted by total bill in descending order, and limit the results to the top 5 records
    def q7(self):
        print("Male top 5")
        query1 = '''
        SELECT total_bill, tip, tip/total_bill AS tip_percent
        FROM tips
        WHERE sex = 'Male'
        ORDER BY total_bill DESC
        LIMIT 5
        '''
        self.execute(query1) 

        print("Female top 5")
        query2 = '''
        SELECT total_bill, tip, tip/total_bill AS tip_percent
        FROM tips
        WHERE sex = 'Female'
        ORDER BY total_bill DESC
        LIMIT 5
        '''
        self.execute(query2) 

    # Q8 Find the maximum and minimum tip percentage for each day and time combination, along with the corresponding total bill and tip amount
    def q8(self):
        print("MAX:")
        query = '''
        SELECT MAX(tip/total_bill) AS max_tip_percent, total_bill, tip
        FROM tips
        GROUP BY day, time
        '''
        self.execute(query) 
        print("MIN:")
        query2 = '''
        SELECT MIN(tip/total_bill) AS max_tip_percent, total_bill, tip
        FROM tips
        GROUP BY day, time
        '''
        self.execute(query2) 

    # Q9 Retrieve the total bill, tip amount, and tip percentage for parties of size 4 or more, where the tip percentage is greater than 15%, and the total bill is between $50 and $100
    def q9(self):
        
        query = '''
        SELECT total_bill, tip, tip/total_bill AS tip_percent
        FROM tips
        WHERE size >= 4 AND tip_percent > 0.15 AND total_bill >= 50 AND total_bill <= 100
        '''
        self.execute(query) # the result should return an empty table 
    
    # Q10 Find the average tip percentage for each combination of day, time, and smoker status, but only include combinations with more than 5 records
    def q10(self):
        
        query = '''
        SELECT day, time, smoker, AVG(tip/total_bill) as avg_tip_percent
        FROM tips
        GROUP BY day, time, smoker
        HAVING count(*) > 5 
        '''
        self.execute(query) 

    # Q11 Count the record for each combination of day, time, smoker status
    def q11(self):
        query = '''
        SELECT COUNT(*)
        FROM tips
        GROUP BY day, time, smoker
        '''
        self.execute(query)

    # Q12 Find the average tip percentage for smokers and non smokers
    def q12(self):
        query = '''
        SELECT smoker, AVG(tip/total_bill) AS avg_tip_percent
        FROM tips
        GROUP BY smoker
        '''
        self.execute(query)
    
    # Q13 Find the average bill per person along with day and time group by day and time, then sort by descending order
    def q13(self):
        query = '''
        SELECT total_bill/size AS avg_bill, day, time
        FROM tips
        GROUP BY day, time
        ORDER BY avg_bill DESC
        '''
        self.execute(query)

    # Q14 Find the most popular day and time of the week in descending order
    def q14(self):
        query = '''
        SELECT day, time, count(*)
        FROM tips
        GROUP BY day, time
        ORDER BY count(*) DESC
        '''
        self.execute(query)

    # Q15 Find the smoker number and tip percentage group by size, order smoker count in descending order
    def q15(self):
        query = '''
        SELECT size, count(smoker), tip/total_bill AS tip_percent
        FROM tips
        GROUP BY size
        ORDER BY count(smoker) DESC
        '''
        self.execute(query)

    ## UPDATE
    def update(self):
        query='''
        UPDATE tips
        SET smoker = 'Yes'
        WHERE ROWID=10
        '''
        self.execute(query)

    ## DELETE
    def delete(self):
        query = '''
        DELETE FROM tips WHERE total_bill < 10
        '''
        self.execute(query)

def main():
    # CREATE
    query = SQL_QUERY()

    # READ
    query.q1()
    query.q2()
    query.q3()
    query.q4()
    query.q5()
    query.q6()
    query.q7()
    query.q8()
    query.q9()
    query.q10()
    # additional queries
    query.q11()
    query.q12()
    query.q13()
    query.q14()
    query.q15()

    # UPDATE
    query.update()

    # DELETE
    query.delete()

    query.finish()

if __name__ == '__main__':
    main()
