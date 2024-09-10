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
    def execute(self, query, question_num):
        try:
            self.cursor.execute(query)

            # print retrived data if needed
            if isinstance(question_num, int):
                rows = self.cursor.fetchall()
                title = []
                for description in self.cursor.description:
                    title.append(description[0])
                print("Question"+ str(question_num) +"-"*20)
                print(tuple(title))   
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
        self.execute(query,1)

    # Q2 Find the maximum and minimum total bull amounts
    def q2(self):
        query = '''
        SELECT MAX(total_bill) AS max_bill, MIN(total_bill) AS min_bill
        FROM tips;
        '''
        self.execute(query,2)

    # Q3 Count the number of parties for each size
    def q3(self):
        query = '''
        SELECT size, count(size) AS number_of_parties
        FROM tips
        GROUP BY size;
        '''
        self.execute(query,3)
    
    # Q4 Retrieve the total bill and tip for parties of size 4 or more, where the tip percentage is greater than 15%
    def q4(self):
        query = '''
        SELECT total_bill, tip
        FROM tips
        WHERE size >=4 and tip > (total_bill * 0.15)
        '''
        self.execute(query,4)
    
    # Q5 Retrieve the total bill, tip amount, and tip percentage for each combination of day and time, sorted by tip percentage in descending order
    def q5(self):
        query = '''
        SELECT day, time, total_bill, tip, tip/total_bill AS tip_percent
        FROM tips
        GROUP BY day, time
        ORDER BY tip_percent DESC
        '''
        self.execute(query,5)

    # Q6 Find the average tip percentage for each combination of day, time, and smoker status
    def q6(self):
        
        query = '''
        SELECT day, time, AVG(tip/total_bill) AS tip_percent
        FROM tips
        GROUP BY day, time, smoker
        '''
        self.execute(query,6) 

    # Q7 Retrieve the total bill, tip amount, and tip percentage for each sex, sorted by total bill in descending order, and limit the results to the top 5 records
    def q7(self):
        query = '''
        WITH MaleTop5 AS(
            SELECT sex, total_bill, tip, tip/total_bill AS tip_percent
            FROM tips
            WHERE sex = 'Male'
            ORDER BY total_bill DESC
            LIMIT 5
        ),
        FemaleTop5 AS(
            SELECT sex, total_bill, tip, tip/total_bill AS tip_percent
            FROM tips
            WHERE sex = 'Female'
            ORDER BY total_bill DESC
            LIMIT 5
        )
        SELECT * FROM MaleTop5
        UNION ALL
        SELECT * FROM FemaleTop5
        '''
        self.execute(query,7) 

    # Q8 Find the maximum and minimum tip percentage for each day and time combination, along with the corresponding total bill and tip amount
    def q8(self):
        query = '''
        SELECT day, time, MAX(tip/total_bill) AS max_tip_percent, MIN(tip/total_bill) AS max_tip_percent, total_bill, tip
        FROM tips
        GROUP BY day, time
        '''
        self.execute(query,8) 
    

    # Q9 Retrieve the total bill, tip amount, and tip percentage for parties of size 4 or more, where the tip percentage is greater than 15%, and the total bill is between $50 and $100
    def q9(self):
        
        query = '''
        SELECT total_bill, tip, tip/total_bill AS tip_percent
        FROM tips
        WHERE size >= 4 AND tip_percent > 0.15 AND total_bill >= 50 AND total_bill <= 100
        '''
        self.execute(query,9) # the result should return an empty table 
    
    # Q10 Find the average tip percentage for each combination of day, time, and smoker status, but only include combinations with more than 5 records
    def q10(self):
        
        query = '''
        SELECT day, time, smoker, AVG(tip/total_bill) as avg_tip_percent
        FROM tips
        GROUP BY day, time, smoker
        HAVING count(*) > 5 
        '''
        self.execute(query,10) 

    # Q11 Count the record for each combination of day, time, smoker status, then sort the records by descending order
    def q11(self):
        query = '''
        SELECT day, time, COUNT(*) AS count
        FROM tips
        GROUP BY day, time, smoker
        ORDER BY count DESC
        '''
        self.execute(query,11)

    # Q12 Find the average tip percentage for smokers and non smokers
    def q12(self):
        query = '''
        SELECT smoker, AVG(tip/total_bill) AS avg_tip_percent
        FROM tips
        GROUP BY smoker
        '''
        self.execute(query,12)
    
    # Q13 Find the average bill per person for each combination of day and time, then sort by descending order
    def q13(self):
        query = '''
        SELECT day, time, total_bill/size AS avg_bill
        FROM tips
        GROUP BY day, time
        ORDER BY avg_bill DESC
        '''
        self.execute(query,13)

    # Q14 Find the TOP 3 popular day and time combinations of the week and display by descending order in count
    def q14(self):
        query = '''
        SELECT day, time, count(*) as count
        FROM tips
        GROUP BY day, time
        ORDER BY count(*) DESC
        LIMIT 3
        '''
        self.execute(query,14)

    # Q15 Find the smoker number and tip percentage group by size, order smoker count in descending order
    def q15(self):
        query = '''
        SELECT size, count(smoker) AS smoker_num, tip/total_bill AS tip_percent
        FROM tips
        GROUP BY size
        ORDER BY count(smoker) DESC
        '''
        self.execute(query,15)

    ## UPDATE
    def update(self):
        query='''
        UPDATE tips
        SET smoker = 'Yes'
        WHERE ROWID=10
        '''
        self.execute(query,"Update")

    ## DELETE
    def delete(self):
        query = '''
        DELETE FROM tips WHERE total_bill < 10
        '''
        self.execute(query,"Delete")

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
