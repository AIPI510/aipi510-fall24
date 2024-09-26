import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.request
from pathlib import Path
import os
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
1. Upload a dataset (CSV) or paste a link.
2. Tune parameters like significance level.
3. Select which test(s) to run.
4. View the results and visualize data with plots.
""")

st.title("Normality Test Application")
st.markdown("Upload a dataset or paste a link to a dataset.")

# Option to upload file or input URL
file_upload = st.file_uploader("Upload CSV", type=["csv"])
url_input = st.text_input("Or paste a URL to a CSV")


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
    st.write("Dataset Preview:")
    st.write(data.head())

    # Select column for normality testing
    numeric_columns = data.select_dtypes(include=np.number).columns
    selected_column = st.selectbox("Select a numeric column to test", numeric_columns)

    if selected_column:
        st.write(f"Selected column: {selected_column}")
        column_data = data[selected_column].dropna()

        # Parameter for significance level (alpha)
        alpha = st.slider("Select significance level (alpha)", 0.01, 0.10, 0.05)

        # Test options
        shapiro_test = st.checkbox("Shapiro-Wilk Test", True)
        ad_test = st.checkbox("Anderson-Darling Test", True)
        ks_test = st.checkbox("Kolmogorov-Smirnov Test", True)

        # Running selected tests
        results = {}

        if shapiro_test:
            stat, p_value = stats.shapiro(column_data)
            results["Shapiro-Wilk"] = {"statistic": stat, "p-value": p_value}

        if ad_test:
            stat, critical_values, sig_level = stats.anderson(column_data, dist='norm')
            results["Anderson-Darling"] = {"statistic": stat, "critical_values": critical_values, "significance_levels": sig_level}

        if ks_test:
            stat, p_value = stats.kstest(column_data, 'norm')
            results["Kolmogorov-Smirnov"] = {"statistic": stat, "p-value": p_value}

        # Display results
        st.subheader("Normality Test Results")
        for test_name, result in results.items():
            st.write(f"**{test_name}**")
            for key, value in result.items():
                st.write(f"{key}: {value}")

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

else:
    st.write("Please upload a dataset or provide a valid URL.")
