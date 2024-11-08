import sqlite3
import pandas as pd
import numpy as np
from scipy.stats import f
import matplotlib.pyplot as plt

def myANOVA(grid, alpha):
    
    # Calculate the grand mean (GM)
    GM = np.mean(grid)

    # Calculate group means
    groupMeans = np.zeros(len(grid))
    for i in range(len(grid)):
        groupMeans[i] = np.mean(grid[i])
        
    # Initialize sum of squares
    SStotal = 0
    SSWG = 0
    SSBG = 0

    # Calculate sum of squares
    for i in range(len(grid)):
        SSBG += len(grid[i]) * (groupMeans[i] - GM)**2
        for j in range(len(grid[i])):
            SStotal += (grid[i, j] - GM)**2
            SSWG += (grid[i, j] - groupMeans[i])**2

    # Degrees of freedom
    DFtotal = grid.size - 1
    DFBG = len(grid) - 1
    DFWG = grid.size - len(grid)

    # Variance between groups and within groups
    varBG = SSBG / DFBG
    varWG = SSWG / DFWG

    # Calculate the F-statistic
    myF = varBG / varWG

    # Get the critical F-value using the F-distribution CDF (f.ppf)
    Fstat = f.ppf(1 - alpha, DFBG, DFWG)
    
    # Get the PDF of the F-distribution for plotting
    
    pdfAxis = np.linspace(0,6,1000)
    
    Fdist = f.pdf(pdfAxis, DFBG, DFWG)

    # Compare F-statistic with the critical F-value to make the decision
    if myF > Fstat:
        result = "There is a statistically significant difference between the groups!"
    else:
        result = "There is no evidence for a significant difference between the groups."
    
    # Return three values: result, F-statistic, and critical F-value
    return result, myF, Fstat, groupMeans, pdfAxis, Fdist


# define the sqlquery function to execute a given SQL query on a given SQL database connection

def sqlquery(connection,prompt):
    try:
        cur = connection.cursor() # try to create a cursor for an SQL query
        cur.execute(prompt) # prompt parameter is fed in as SQL query
        results = cur.fetchall() # store all results from the query in a variable
        if len(results) > 0: # if the query returned a nonzero number of results
            return results # return the results
        else:
            return "No results found." # return the message that no data entry matched the query
        
    except sqlite3.Error as e:
        print(f"SQL query execution error: {e}") # print error message if the SQL query cannot be performed

fileName = "/Users/rajivraman/Downloads/anovatest.csv" # replace with your csv file path - make sure groups are in columns with titles

try: 
    conn = sqlite3.connect("test1") # open the connection to an SQL database named test1
    print("Connected to the SQL Database! Executing all queries...\n")
    
    data = pd.read_csv(fileName) # store the data in this variable
    
    try:
        data.to_sql('table1',conn,index=False,if_exists='replace') # forms the SQL database
    except Exception as e:
        print(f"Data upload error: {e}") # print error message if data cannot be uploaded to the SQL database
    
    sql1 = sqlquery(conn,"SELECT * FROM table1")
    
except sqlite3.Error as e:
    print(f"Database connection error: {e}") # print error message if we cannot connect to the database
    
finally: # if everything in the "try" block is finished
    if conn: # and if the SQL connection still exists
        conn.close() # close the connection to the SQL database
        print("\nYour database connection has been closed.\n")

myGrid = (np.transpose(sql1)[1:,:]).astype(float)

# Run the ANOVA test and display the results
result, myF, Fstat, groupMeans, Faxis, Fdist = myANOVA(myGrid, 0.05)

# Print the ANOVA results

print(f"F-statistic: {myF}")
print(f"Critical F-value: {Fstat}")
print(result)

fig, axs = plt.subplots(1,3,figsize=(20,6))

dist = myGrid.flatten()

axs[0].hist(dist,bins=10,color='mediumpurple',edgecolor='black')
axs[0].set_title("Distribution of Data")
axs[0].set_xlabel("IQ Score")
axs[0].set_ylabel("Number of Tests")


x = ["3 hours","5 hours","7 hours","9 hours","11 hours"]  # x positions for the bars (one for each group)
axs[1].bar(x, groupMeans, color='deepskyblue', edgecolor='black',width=0.5, label='Group Mean')

# Plot the dots around each bar
for i in range(len(groupMeans)):
    y = myGrid[i]  # IQ scores for group i
    axs[1].scatter([i] * len(y), y, color='red', zorder=2, label='Individual Scores' if i == 0 else "")  # Plot data points

# Add labels and title
axs[1].set_xlabel('Hours of Sleep')
axs[1].set_ylabel('IQ Score')
axs[1].set_title('Group Mean Data')
axs[1].legend()

axs[2].plot(Faxis,Fdist,color='blue')
axs[2].set_xlabel("F-ratio")
axs[2].set_ylabel("Density")
axs[2].set_title("F-Distribution")
axs[2].fill_between(Faxis, Fdist, where=(Faxis >= Fstat), color='red', alpha=0.5, label=f'Indicates Significance (α = 0.05)')
axs[2].legend()
axs[2].grid(True)

# Show the plot
plt.tight_layout()
plt.show()




