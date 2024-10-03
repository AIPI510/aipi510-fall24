'''
Initial version generated by Perplexity AI
'''

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Create sample data with multiple observations per condition
data = {
    'Substances': ['Garlic', 'Garlic', 'Silver', 'Silver', 'None', 'None'] * 5,
    'Iconography': ['Crosses', 'No Crosses', 'Crosses', 'No Crosses', 'Crosses', 'No Crosses'] * 5,
    'Noise_Level': [
        50, 65, 55, 70, 60, 75,
        52, 63, 57, 68, 62, 73,
        49, 66, 54, 71, 59, 76,
        51, 64, 56, 69, 61, 74,
        48, 67, 53, 72, 58, 77
    ]
}

df = pd.DataFrame(data)

# Perform two-way ANOVA
substances = df['Substances']
iconography = df['Iconography']
noise_level = df['Noise_Level']

f_value, p_value = stats.f_oneway(
    noise_level[substances == 'Garlic'],
    noise_level[substances == 'Silver'],
    noise_level[substances == 'None']
)

print("Effect of Substances:")
print(f"F-value: {f_value}, p-value: {p_value}")

f_value, p_value = stats.f_oneway(
    noise_level[iconography == 'Crosses'],
    noise_level[iconography == 'No Crosses']
)

print("\nEffect of Iconography:")
print(f"F-value: {f_value}, p-value: {p_value}")

# Visualize the data
plt.figure(figsize=(10, 6))
sns.boxplot(x='Substances', y='Noise_Level', hue='Iconography', data=df)
plt.title('Effect of Substances and Iconography on Monster Noise Levels')
plt.show()