import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from anova import myANOVA  # Import the ANOVA function
from scipy.stats import f

# Setting the page title and layout
st.set_page_config(page_title="One-way ANOVA Dashboard", layout="wide")

# App title
st.title("📊 One-way ANOVA Test with SQL Integration 📊")

st.write("""
### Welcome to the One-way ANOVA Dashboard! 
This interactive app allows you to:
- Upload a CSV file
- Store and query the data using an SQLite database
- Perform One-way ANOVA to determine if there's a significant difference between groups.
""")

# Sidebar section for explanations
st.sidebar.header("Understanding One-way ANOVA")
st.sidebar.write("""
**One-way ANOVA** (Analysis of Variance) is a statistical method used to compare means of three or more samples. 
It tests the null hypothesis that all groups have the same population mean. The test produces an F-statistic 
and a corresponding p-value to determine statistical significance.

- **F-statistic**: A ratio of the variance between group means to the variance within the groups.
- **p-value**: If the p-value is below the chosen significance level (alpha), you reject the null hypothesis, indicating a significant difference between the groups.
""")

# File upload section
uploaded_file = st.file_uploader("Upload your CSV file for analysis", type=["csv"])

if uploaded_file:
    try:
        conn = sqlite3.connect("anova_test_db.db")  # open the connection to an SQL database named anova_test_db
        st.success("🔌 Connected to the SQLite Database!")

        # Read the uploaded CSV file and display it
        data = pd.read_csv(uploaded_file)

        # Check if the first column is non-numeric and may represent labels (group names)
        if not np.issubdtype(data.iloc[:, 0].dtype, np.number):
            labels = data.iloc[:, 0]  # Save group labels for display
            data_numeric = data.iloc[:, 1:]  # Exclude the first column (non-numeric)
        else:
            labels = None
            data_numeric = data  # If first column is numeric, use all data
        
        st.write("**Uploaded CSV Data:**", data)

        # Save CSV data to SQL table
        try:
            data.to_sql('table1', conn, index=False, if_exists='replace')  
            st.success("✅ Data successfully uploaded to the SQL database!")
        except Exception as e:
            st.error(f"❌ Data upload error: {e}")

        # Select columns instead of rows for ANOVA
        st.write("#### Select the columns representing your groups for the ANOVA test:")
        all_columns = data_numeric.columns.tolist()
        select_all = st.checkbox("Select all columns")

        # If "Select all" is checked, select all columns
        if select_all:
            column_indices = all_columns
        else:
            column_indices = st.multiselect("Choose columns for analysis:", all_columns)

        if column_indices:
            # Query only the selected columns
            selected_columns = data_numeric[column_indices]  # Use selected columns for ANOVA
            st.write("**Selected Data for ANOVA (columns as groups):**", selected_columns)

            # Ensure that we have enough columns for ANOVA
            if len(column_indices) < 2:
                st.error("❌ You need to select at least two columns (groups) for the ANOVA test.")
            else:
                # Allow user to set the significance level (alpha)
                alpha = st.number_input("Set the significance level (alpha)", min_value=0.01, max_value=0.10, value=0.05, step=0.01)

                # Button to run the ANOVA test
                if st.button("Run One-way ANOVA"):
                    try:
                        myGrid = selected_columns.to_numpy().T  # Transpose to treat columns as groups
                        result, myF, Fstat = myANOVA(myGrid, alpha)
                        
                        # Calculate the degrees of freedom
                        DFBG = len(myGrid) - 1  # Degrees of freedom between groups
                        DFWG = myGrid.size - len(myGrid)  # Degrees of freedom within groups
                        
                        # Calculate the p-value using the F-distribution survival function
                        p_value = f.sf(myF, DFBG, DFWG)  # Survival function (1 - CDF)

                        # Display results
                        st.write(f"**F-statistic**: {myF}")
                        st.write(f"**Critical F-value**: {Fstat}")
                        st.write(f"**P-value**: {p_value:.8f}")

                        # Provide contextual interpretation
                        if p_value < alpha:
                            st.success(f"Result: There is a statistically significant difference between the groups (p-value = {p_value:.5f}).")
                        else:
                            st.warning(f"Result: There is no evidence for a significant difference between the groups (p-value = {p_value:.5f}).")
                    except Exception as e:
                        st.error(f"❌ Error during ANOVA computation: {e}")

    except sqlite3.Error as e:
        st.error(f"❌ Database connection error: {e}")

    finally:
        if conn:
            conn.close()  # close the connection to the SQL database
            st.success("🔒 Your database connection has been closed.")
else:
    st.info("📂 Please upload a CSV file to begin.")
