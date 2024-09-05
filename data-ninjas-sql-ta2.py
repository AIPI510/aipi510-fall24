''' 
Author:
Jesse Warren & Haochen Li
'''

import sqlite3 # 3.41.2
import csv # came with python package
import os

class sql_query():
    def __init__(self) -> None:
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
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
        
    '''Function to print the database'''
    def print_table(self):
        self.execute("SELECT * FROM tips")

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
        return
        query = '''
        
        '''
        self.execute(query)

    # Q3 Count the number of parties for each size
    def q3(self):
        return
        query = '''
        
        '''
        self.execute(query)
    
    # Q4 Retrieve the total bill and tip for parties of size 4 or more, where the tip percentage is greater than 15%
    def q4(self):
        return
        query = '''
        
        '''
        self.execute(query)
    
    # Q5 Retrieve the total bill, tip amount, and tip percentage for each combination of day and time, sorted by tip percentage in descending order
    def q5(self):
        return
        query = '''
        
        '''
        self.execute(query)

    # Q6 Find the average tip percentage for each combination of day, time, and smoker status
    def q6(self):
        return
        query = '''
        
        '''
        self.execute(query) 

    # Q7 Retrieve the total bill, tip amount, and tip percentage for each sex, sorted by total bill in descending order, and limit the results to the top 5 records
    def q7(self):
        return
        query = '''
        
        '''
        self.execute(query) 

    # Q8 Find the maximum and minimum tip percentage for each day and time combination, along with the corresponding total bill and tip amount
    def q8(self):
        return
        query = '''
        
        '''
        self.execute(query) 
    # Q9 Retrieve the total bill, tip amount, and tip percentage for parties of size 4 or more, where the tip percentage is greater than 15%, and the total bill is between $50 and $100
    def q9(self):
        return
        query = '''
        
        '''
        self.execute(query) 
    # Q10 Find the average tip percentage for each combination of day, time, and smoker status, but only include combinations with more than 5 records
    def q10(self):
        return
        query = '''
        
        '''
        self.execute(query) 
   
    

    

def main():
    query = sql_query()
    query.q1()

    query.finish()

if __name__ == '__main__':
    main()
