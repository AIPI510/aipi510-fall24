# Team Assignment #2
## Data Storage and Access

## Instructions
### CREATE
You have been provided with a sample .csv file. Create a SQLite database in Python using the data in this sample .csv file.

### READ
Answer the following questions (must show your work via SQL queries):
1. Retrieve the average tip percentage for each day of the week 
2. Find the maximum and minimum total bull amounts
3. Count the number of parties for each size
4. Retrieve the total bill and tip for parties of size 4 or more, where the tip percentage is greater than 15%
5. Retrieve the total bill, tip amount, and tip percentage for each combination of day and time, sorted by tip percentage in descending order
6. Find the average tip percentage for each combination of day, time, and smoker status
7. Retrieve the total bill, tip amount, and tip percentage for each sex, sorted by total bill in descending order, and limit the results to the top 5 records
8. Find the maximum and minimum tip percentage for each day and time combination, along with the corresponding total bill and tip amount
9. Retrieve the total bill, tip amount, and tip percentage for parties of size 4 or more, where the tip percentage is greater than 15%, and the total bill is between $50 and $100
10. Find the average tip percentage for each combination of day, time, and smoker status, but only include combinations with more than 5 records

Come up with your own SQL queries for the table. You must show 5 additional queries beyond the 10 outlined above. 

**After you have performed the above queries:**

### UPDATE
It was determined that there was an error in the database. Please update the record that corresponds to id=10 and set smoker to Yes. 

### DELETE
Delete records from the database that have a total bill that is less than $10. 

### Follow best practices:
* Use Context Managers to ensure proper resource handling and automatic closing of connections
* Use Parameterized Queries- named parameters offer better readability and maintainability
* Use Error Handling - wrap database operations within try-except blocks to handle errors

## Submission
To submit your code, make a PR into the sql-ta2 branch and add me and the TA as reviewers. Your code can be in the form of scripts or a notebook. Follow the naming convention teamname-sql-ta2.ipynb / teamname-sql-ta2.py. 

Note: For this assignment, I recommend turning off any autocomplete or copilot code services you are using. SQL queries are a task LLMs are pretty good at. (So, Dr. Bent, why are we learning it? 1. So you know how things work and 2. Because SQL queries are a beloved interview question. You won’t have an LLM helping you during your interview, so I recommend doing this one on your own)

## Rubric
### Code (45 points)
* Code is clean and well organized
* Code is documented with docstrings and comments 
* Code is free of commented out code (ie debug print statements)
* Script has a clear name
* Branching and PRs were done appropriately
* Requirements are included in the text of the PR and are correct and versioned
* The code runs as documented
* The appropriate steps were taken for CREATE
* The appropriate steps were taken for READ
* 5 additional unique queries were added to the READ step
* The appropriate steps were taken for UPDATE
* The appropriate steps were taken for DELETE
* SQL-python best practices were followed (Context Managers used, parameterized queries, and error handling)
