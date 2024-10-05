import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import matplotlib.pyplot as plt
import seaborn as sns

# Use the updated dataset from the previous results
updated_df = pd.DataFrame({
    'Substances': ['Garlic Powder']*11 + ['Silver']*11 + ['None']*14,
    'Religious_Iconography': ['Crosses']*6 + ['No Crosses']*5 + ['Crosses']*6 + ['No Crosses']*5 + ['Crosses']*6 + ['No Crosses']*8,
    'Noise_Level': [50.00, 52.48, 49.31, 53.24, 57.62, 48.83, 65.00, 63.83, 72.90, 68.84, 62.65,
                    55.00, 52.68, 52.67, 56.21, 45.43, 46.38, 70.00, 67.19, 64.94, 71.57, 65.46,
                    60.00, 67.33, 58.87, 60.34, 52.88, 57.28, 75.00, 75.55, 69.25, 76.88, 72.00, 73.54, 67.71, 68.49]
})

# Set random seed for reproducibility
np.random.seed(42)

# Function to generate new noise levels
def generate_noise_levels(mean, std_dev, size):
    return np.round(np.random.normal(loc=mean, scale=std_dev, size=size), 2)

# Generate additional data for each combination
new_data = []
for substance in ['Garlic Powder', 'Silver', 'None']:
    for iconography in ['Crosses', 'No Crosses']:
        subset = updated_df[(updated_df['Substances'] == substance) & (updated_df['Religious_Iconography'] == iconography)]
        mean_noise = subset['Noise_Level'].mean()
        new_noise = generate_noise_levels(mean_noise, 5, 20)  # Generate 20 new values for each combination
        new_data.extend([(substance, iconography, noise) for noise in new_noise])

# Create a new dataframe with the additional data
additional_df = pd.DataFrame(new_data, columns=['Substances', 'Religious_Iconography', 'Noise_Level'])

# Combine the original and new data
final_df = pd.concat([updated_df, additional_df], ignore_index=True)

# Display summary statistics of the final dataset
print(final_df.groupby(['Substances', 'Religious_Iconography'])['Noise_Level'].describe())

# Display the total number of samples
print(f"\nTotal number of samples: {len(final_df)}")

# Perform 2-way ANOVA
model = ols('Noise_Level ~ C(Substances) + C(Religious_Iconography) + C(Substances):C(Religious_Iconography)', data=final_df).fit()
anova_table = anova_lm(model, typ=2)

# Print ANOVA results
print("ANOVA Results:")
print(anova_table)
print("\n")

# Create interaction plot
plt.figure(figsize=(10, 6))
sns.boxplot(x='Substances', y='Noise_Level', hue='Religious_Iconography', data=final_df)
#sns.boxplot(x='Substances', y='Noise_Level', hue='Religious_Iconography', data=final_df, marker='o')
plt.title('Interaction Plot: Substances and Religious Iconography')
plt.ylabel('Noise Level (dB)')
plt.show()

# Print interpretations
print("Interpretations:")
print("1. Main effect of Substances:", "Significant" if anova_table.loc['C(Substances)', 'PR(>F)'] < 0.05 else "Not significant")
print("2. Main effect of Religious Iconography:", "Significant" if anova_table.loc['C(Religious_Iconography)', 'PR(>F)'] < 0.05 else "Not significant")
print("3. Interaction effect:", "Significant" if anova_table.loc['C(Substances):C(Religious_Iconography)', 'PR(>F)'] < 0.05 else "Not significant")

# Calculate the F Statistic

grand_mean = final_df['Noise_Level'].mean()

# Calculate SS for Substances
ss_substances = sum([(group['Noise_Level'].mean() - grand_mean)**2 * len(group) 
                     for name, group in final_df.groupby('Substances')])

# Calculate SS for Religious Iconography
ss_iconography = sum([(group['Noise_Level'].mean() - grand_mean)**2 * len(group) 
                      for name, group in final_df.groupby('Religious_Iconography')])

# Calculate SS for Interaction
ss_interaction = sum([(group['Noise_Level'].mean() - grand_mean)**2 * len(group) 
                      for name, group in final_df.groupby(['Substances', 'Religious_Iconography'])])
ss_interaction -= (ss_substances + ss_iconography)

# Calculate SS Total and SS Error
ss_total = sum((final_df['Noise_Level'] - grand_mean)**2)
ss_error = ss_total - (ss_substances + ss_iconography + ss_interaction)

# Calculate degrees of freedom
df_substances = 2  # 3 levels - 1
df_iconography = 1  # 2 levels - 1
df_interaction = 2  # (3-1) * (2-1)
df_error = len(final_df) - (3 * 2)  # total samples - (levels of A * levels of B)

# Calculate Mean Squares
ms_substances = ss_substances / df_substances
ms_iconography = ss_iconography / df_iconography
ms_interaction = ss_interaction / df_interaction
ms_error = ss_error / df_error

# Calculate F-statistics
f_substances = ms_substances / ms_error
f_iconography = ms_iconography / ms_error
f_interaction = ms_interaction / ms_error

print(f"F-statistic for Substances: {f_substances}")
print(f"F-statistic for Religious Iconography: {f_iconography}")
print(f"F-statistic for Interaction: {f_interaction}")


# Save the final dataset to a CSV file
final_df.to_csv('apocalypse_bunker_data.csv', index=False)
print("\nDataset saved as 'apocalypse_bunker_data.csv'")

