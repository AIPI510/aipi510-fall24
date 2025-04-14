import pandas as pd
from scipy.stats import mannwhitneyu

def perform_mann_whitney_test(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Separate the data into two groups
    remote_group = data[data['Employment_Type'] == 'Remote']['Productivity_Score']
    in_office_group = data[data['Employment_Type'] == 'In-Office']['Productivity_Score']

    if remote_group.empty or in_office_group.empty:
        print("Error: One of the groups is empty. Ensure that both 'Remote' and 'In-Office' groups have data.")
        return

    # Perform the Mann-Whitney U test
    stat, p_value = mannwhitneyu(remote_group, in_office_group, alternative='two-sided')

    # Print the results
    print(f'Mann-Whitney U Test Statistic: {stat}')
    print(f'P-value: {p_value}')

# Example usage
file_path = 'remote_work_productivity.csv'
perform_mann_whitney_test(file_path)