import streamlit as st
import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.formula.api import ols
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns


# Tukey's test
def perform_tukey_hsd(data):
    df = pd.DataFrame(data)
    model = ols('sleep_hours ~ C(group)', data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    tukey = pairwise_tukeyhsd(endog=df['sleep_hours'], groups=df['group'], alpha=0.05)
    tukey_result_df = pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0])
    return tukey_result_df

# Streamlit UI
st.title("Tukey's HSD Sleep Hours Analysis")

# Number of groups
num_groups = st.number_input("Enter number of groups:", min_value=2, max_value=10, step=1)

# Create inputs for each group
group_data = {}

for i in range(1, num_groups + 1):
    group_name = f"Group {i}"
    num_members = st.number_input(f"Enter number of members for {group_name}:", min_value=1, max_value=20, step=1)
    
    # get sleeping hours for each group as a list 
    sleep_hours = []
    for j in range(num_members):
        sleep_hours.append(st.number_input(f"Hours of sleep for member {j+1} of {group_name}:", min_value=0.0, max_value=24.0, step=0.1))
    
    # make the dictionary for group i 
    group_data[group_name] = sleep_hours

# Submit button click
if st.button("Submit"):
    # Prepare the data for Tukey's HSD
    data = {
        'group': [],
        'sleep_hours': []
    }
    
    for group, hours in group_data.items():
        data['group'].extend([group] * len(hours))
        data['sleep_hours'].extend(hours)
    
    # Tukey's HSD test
    result = perform_tukey_hsd(data)
    
    # Display Tukey's HSD results
    st.write("### Tukey's HSD Results (p-values)")
    st.dataframe(result)
    
    df = pd.DataFrame(data)
    
    # Plot overall distribution of sleep hours for all groups 
    st.write("### Distribution of Hours of Sleep")
    fig, ax = plt.subplots()
    sns.histplot(df['sleep_hours'], kde=True, ax=ax)
    ax.set_xlabel("Hours of Sleep")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
    
    # Plot boxplots for each group
    st.write("### Boxplots of Hours of Sleep for Each Group")
    fig, ax = plt.subplots()
    sns.boxplot(x='group', y='sleep_hours', data=df, ax=ax)
    ax.set_xlabel("Group")
    ax.set_ylabel("Hours of Sleep")
    st.pyplot(fig)
