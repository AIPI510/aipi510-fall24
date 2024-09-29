# PPT: https://docs.google.com/presentation/d/1-gd7BSLd3pqxKH5wceoWW7dzh5YfwOMHIsVri8Qaa0c/edit?usp=sharing

# https://storage.googleapis.com/aipi_datasets/Auto.csv
import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
path = Path()

# Sidebar
st.sidebar.title("Normality Test Explorer")
st.sidebar.markdown("""
This app allows you to upload or link to a dataset and perform various tests of normality.
### Tests Included:
- **Shapiro-Wilk**: Best for small datasets.
- **Anderson-Darling**: More sensitive to tails.
- **Kolmogorov-Smirnov**: Compares data to the normal distribution.

#### Instructions:
1. Upload a dataset (CSV/XLSX) or paste a link (Github/Google APIs)
2. Tune parameters like significance level.
3. Select which test(s) to run.
4. View the results and visualize data with plots.
""")

st.title("Normality Test Application")
st.markdown("Upload a dataset or paste a link to a dataset (Github/Google APIs).")

# Option to upload file or input URL
file_upload = st.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])
url_input = st.text_input("Or paste a URL to a CSV/XLSX")


def load_data(filename, url):
    if filename:
        if filename.name.endswith(".csv"):
            data = pd.read_csv(filename)
        elif filename.name.endswith(".xlsx"):
            data = pd.read_excel(filename)
        else:
            st.error("Please upload a valid CSV or Excel file.")
            return pd.DataFrame()

    # If URL is provided
    elif url:
        try:
            # Handle GitHub raw links
            if "github.com" in url:
                url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            
            # Handle Google Cloud Storage links or other direct CSV/XLSX URLs
            if url.startswith("https://storage.googleapis.com") or url.endswith((".csv", ".xlsx")):
                if url.endswith(".csv"):
                    data = pd.read_csv(url)
                elif url.endswith(".xlsx"):
                    data = pd.read_excel(url)
                else:
                    st.error("URL must point to a CSV or Excel file.")
                    return pd.DataFrame()
            else:
                st.error("Unsupported URL. Please provide a valid CSV or Excel file URL.")
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Error loading data from URL: {e}")
            return pd.DataFrame()
    else:
        data = pd.DataFrame()

    return data

# Load data
data = load_data(file_upload, url_input)

if not data.empty:
    with st.expander("Dataset Preview"):
        st.table(data.head())
        st.write(f"Number of Data Samples: {data.shape[0]}")

    # basic cleaning
    data = data.dropna()
    
    if 'horsepower' in data.columns:
        data['horsepower'] = data['horsepower'].apply(pd.to_numeric, errors='coerce')


    st.subheader("Set Testing Parameters")
    numeric_columns = data.select_dtypes(include=np.number).columns
    selected_column = st.selectbox("Select a numeric column to test", numeric_columns)

    if selected_column:
        st.write(f"Selected column: {selected_column}")
        column_data = data[selected_column].dropna()

        # Parameter for significance level (alpha)
        alpha = st.slider("Select significance level (alpha)", 0.01, 0.10, 0.05)
        
        with st.expander("Understanding Significance Level (Alpha)"):
            st.write(f"The significance level (alpha) represents the threshold for rejecting the null hypothesis of normality. If the p-value is less than alpha ({alpha}), we reject the null hypothesis, suggesting the data is not normally distributed. Here's how varying alpha affects your decisions:")
            st.write("- A smaller alpha (e.g., 0.01) requires stronger evidence to reject the null hypothesis.")
            st.write("- A larger alpha (e.g., 0.10) makes it easier to reject the null hypothesis, potentially leading to more false positives.")


        st.subheader("Select Tests to Run")
        st.write("Null Hypothesis H(0): The data column chosen follows a normal distribution.")
        shapiro_test = st.checkbox("Shapiro-Wilk Test", True)
        ad_test = st.checkbox("Anderson-Darling Test", True)
        ks_test = st.checkbox("Kolmogorov-Smirnov Test", True)

        # Running selected tests
        results = {}

        button = st.button("Run Selected Tests")

        if button:
            if shapiro_test:
                stat, p_value = stats.shapiro(column_data)
                results["Shapiro-Wilk"] = {"statistic": stat, "p-value": p_value}

            if ad_test:
                stat, critical_values, sig_level = stats.anderson(column_data, dist='norm')
                results["Anderson-Darling"] = {
                    "statistic": stat, 
                    "critical_values": critical_values,
                    "significance_levels": sig_level
                }

            if ks_test:
                stat, p_value = stats.kstest(column_data, 'norm')
                results["Kolmogorov-Smirnov"] = {"statistic": stat, "p-value": p_value}

            # Display results
            result_data = []

            if "Shapiro-Wilk" in results:
                shapiro_result = results["Shapiro-Wilk"]
                shapiro_decision = "Reject" if shapiro_result["p-value"] < alpha else "Fail to Reject"
                result_data.append({
                    "Test": "Shapiro-Wilk",
                    "Statistic": shapiro_result["statistic"],
                    "p-value": shapiro_result["p-value"],
                    "Decision": shapiro_decision
                })


            if "Anderson-Darling" in results:
                ad_result = results["Anderson-Darling"]
                ad_decision = "Reject" if ad_result["statistic"] > ad_result["critical_values"][2] else "Fail to Reject"  # Using 0.05 level
                result_data.append({
                    "Test": "Anderson-Darling",
                    "Statistic": ad_result["statistic"],
                    "Critical Values": ad_result["critical_values"],
                    "Decision": ad_decision
                })

            if "Kolmogorov-Smirnov" in results:
                ks_result = results["Kolmogorov-Smirnov"]
                ks_decision = "Reject" if ks_result["p-value"] < alpha else "Fail to Reject"
                result_data.append({
                    "Test": "Kolmogorov-Smirnov",
                    "Statistic": ks_result["statistic"],
                    "p-value": ks_result["p-value"],
                    "Decision": ks_decision
                })

            # Show results in a table
            st.subheader("Normality Test Results")
            st.table(pd.DataFrame(result_data))

            st.write("p-value is the proportion of values in the null distribution less than or equal to the observed value of the statistic.")

            # Plot visualization
            st.subheader("Data Visualization")
            fig, ax = plt.subplots(1, 2, figsize=(12, 5))

            # Histogram
            sns.histplot(column_data, kde=True, ax=ax[0])
            ax[0].set_title(f"{selected_column} Distribution")

            # Q-Q plot
            stats.probplot(column_data, dist="norm", plot=ax[1])
            ax[1].set_title(f"{selected_column} Q-Q Plot")

            st.pyplot(fig)
        
            col1, col2 = st.columns(2)

            with col1:
                st.write("A bell-shaped curve suggests normality.")
            with col2:
                st.write("Compares the quantiles of the sample data against the quantiles of a normal distribution. If the points fall along a straight line, the data is likely normally distributed.")
            

else:
    st.write("Please upload a dataset or provide a valid URL.")
