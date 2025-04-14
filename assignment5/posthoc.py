# import packages used for Ad-hoc testing

from scipy.stats import f_oneway
import scikit_posthocs as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import KNNImputer
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.subplots as sp
import statsmodels.api as sm
import scipy.stats as stats

# load data
df = pd.read_csv('./ev_charging_patterns.csv')
df.head()

# change the column names to be easier for use
df.columns = ['user_id', 'model', 'battery_capacity_kwh',
       'charging_station_id', 'charging_station_location',
       'charging_start_time', 'charging_end_time', 'energy_consumed_kwh',
       'charging_duration_hours', 'charging_rate_kw',
       'charging_cost_usd', 'time_of_day', 'day_of_week',
       'start%', 'end %',
       'distance_driven_km', 'temperature',
       'vehicle_age_years', 'charger_type', 'user_type']

# define a function to cate the lists of categorical_and_numerical variables

def discover_categorical_and_numerical(df):
  categorical = df.select_dtypes(include=object).columns.to_list() # [c in df.columns if df[c].dtype == "O"]
  numerical = df.select_dtypes(include=np.number).columns.to_list() # df.columns.difference(categorical)

  # make a list of discrete variables
  discrete = [var for var in numerical if len(df[var].unique()) < 20]

  # categorical encoders work only with object type variables to treat numerical variables as categorical, we need to re-cast them
  df[discrete]= df[discrete].astype('O')

  # update numerical variables as continuous variables
  numerical = [var for var in numerical if var not in discrete]

  print(f"There are {len(categorical)} categorical, {len(discrete)} discrete numerical, and {len(numerical)} continuous numerical variables / features in the dataset")
  return categorical, numerical

categorical, numerical = discover_categorical_and_numerical(df)

# impute missing values 
def knn_imputation(data):
  knn_imputer = KNNImputer(n_neighbors=5, weights="distance").set_output(transform='pandas')
  data_transformed = knn_imputer.fit_transform(data)
  return data_transformed

# remove outliers 
def remove_outliers_iqr(data):
  for column in df.select_dtypes(include=[np.number]).columns:
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    # define bounds 
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
  return data[(data >= lower_bound) & (data <= upper_bound)]

# only numerical columns need outlier removal and missing vlaue imputation.
df[numerical] = knn_imputation(df[numerical])
df[numerical] = remove_outliers_iqr(df[numerical])

# create a melted table for compatible use with the Python Ad-hoc test packages.
df_melt = pd.melt(df, id_vars=['charger_type'], value_vars=['charging_cost_usd'])

# Scheffe
string = """\
The Scheffé test determines if the average of one group of means differs from that of another group of means.
The downside is a relatively low statistical power.\n\n
"""
print(string)
print(sp.posthoc_scheffe(df_melt, val_col='value', group_col='charger_type'))

string = """From the above, we can see that the group means of DC Fast Charger vs Level 1 and DC Fast Charger vs Level 2 are significantly different, since the corresponding p-values < 0.05. \
However, Level 1 and level 2 do not appear to have statisitcally different means according to Scheffe's test.\n\n"""

print(string)

# Duncan's test

string = """Dunn’s test is to identify which groups differ from others if the statistically significant differences between groups are detected in the omnibus test.\n
Dunn’s test is non-parametric, not relying on assumptions about data distributions."""

print(string)

dunn_p_values = sp.posthoc_dunn(df_melt, val_col='value', group_col='charger_type', p_adjust='holm')
print(dunn_p_values)
print("The results are noticeably similar.")

# Tukey

from scipy.stats import tukey_hsd

fast_charger = df[df["charger_type"] == "DC Fast Charger"]
level_1_charger = df[df["charger_type"] == "Level 1"]
level_2_charger = df[df["charger_type"] == "Level 2"]

print(tukey_hsd(fast_charger['charging_cost_usd'], 
                level_1_charger['charging_cost_usd'], 
                level_2_charger['charging_cost_usd']))

print("HSD Pairwise test gives confidence intervals as well. Interestingly, the test shows that no significant differences can be found across the board")