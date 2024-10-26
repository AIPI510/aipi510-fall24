"""A Python script that demonstrates feature engineering and selection using scikit-learn.

Usage: python scikit-learn-demo-mwilliams.py
"""

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.preprocessing import OneHotEncoder, StandardScaler


print("For this demonstration, we'll use scikit-learn's feature engineering and selection capabilities",
      "to prepare the iris dataset for modeling.\n")
print("Importing the iris dataset...\n")

# Load the iris dataset into a pandas dataframe
iris = load_iris()
iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
iris_df['species'] = iris.target

print("Here are 5 random rows o the imported dataset:\n")
print(iris_df.sample(5))

print("\nFirst we'll use scikit-learn's StandardScaler to standardize the feature columns.")
print("StandardScaler will transform the feature columns to have a mean of 0 and a standard deviation of 1.")
print("This is a common requirement for models that may function poorly if the features do not", 
      "have a standard normal distribution.")
print("Standardizing the feature columns...\n")

# Standardize the feature columns
scaler = StandardScaler()
iris_scaled = scaler.fit_transform(iris.data)

# Merge the standardized feature columns with the species column
iris_scaled_df = pd.concat([pd.DataFrame(iris_scaled, columns=iris_df.columns[:-1]),
                            iris_df[['species']]],
                           axis=1)
                         
print("Here are 5 random rows of the dataset to show the results of standardization:\n")
print(iris_scaled_df.sample(5))

print("\n" + "*" * 135)

print("Next, we'll transform the species column using one-hot encoding to prepare it for modeling.")

print("""
The iris dataset already uses label encoding for the species column. Specifically, setosa=0, versicolor=1, and 
virginica=2. To avoid models assuming these numerical values in the species column have an ordinal relationship, 
we can use one-hot encoding to create a binary column for each species. Before doing so, we'll convert 
the species column to a string datatype to illustrate converting string-based categorical data.
""")

print("Converting the species column to a string datatype...\n")

iris_scaled_df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)

print("Here are 5 random rows of the dataset to show the species column converted to a string datatype:\n")
print(iris_scaled_df.sample(5))

print("\nNow, we'll use one-hot encoding to create a binary column for each species.")
print("One-hot encoding the species column...\n")

# One-hot encode the species column
encoder = OneHotEncoder(sparse_output=False)
species_encoded = encoder.fit_transform(iris_scaled_df[['species']])

print("Here are the new one-hot representations for each species:\n")
print(f"Setosa:\n\t{species_encoded[0]}\n")
print(f"Versicolor:\n\t{species_encoded[50]}\n")
print(f"Virginica:\n\t{species_encoded[100]}\n")

print("Now we'll update the dataset to use the one-hot encoded species columns.")
print("Creating a new dataframe with the one-hot encoded species columns...\n")

# Create a new dataframe with the one-hot encoded species columns
encoded_df = pd.concat([iris_scaled_df.drop(columns=['species']), 
                             pd.DataFrame(species_encoded, 
                                          columns=encoder.get_feature_names_out())],
                                          axis=1)

print("Here are 5 random rows of the new dataframe with the one-hot encoded species columns:\n")
print(encoded_df.sample(5))
print("\n" + "*" * 135)

print("Finally, we'll use scikit-learn to perform feature selection on the dataset.\n")
print("For this demonstration, we'll use scikit-learn's SelectKBest to select the top 3 of the 4 features.")
print("To determine the top features, we'll use ANOVA F-value (f_classif) as the scoring function.")
print("The ANOVA F-value measures the difference in means between different classes for each feature.\n")
print("Here are the computed F-values for each feature:\n")

# Perform feature selection using SelectKBest with ANOVA F-value (f_classif)
selector = SelectKBest(score_func=f_classif, k=3)

# Print the F-values for each feature
selector.fit(iris_scaled_df.drop(columns=['species']), iris_scaled_df['species'])
f_values = selector.scores_
for i, feature in enumerate(iris.feature_names):
    print(f"{feature}: {f_values[i]}")

print("\nAs you can see, sepal width has the lowest F-value, indicating it may not be as important for classification.")
print("The other three features have a stronger relationship to the target variable.\n")
print("Now we'll produce a new dataset using only the top 3 features.\n")

# Produce the new dataset with the top 3 features
new_iris_array = selector.transform(iris_scaled_df.drop(columns=['species']))
new_iris_df = pd.DataFrame(new_iris_array, columns=[iris.feature_names[i] for i in selector.get_support(indices=True)])

# Concatenate the one-hot encoded species columns
final_df = pd.concat([new_iris_df, encoded_df.iloc[:, -3:]], axis=1)

print("Here are 10 random rows of the new dataset with the top 3 features:\n")
print(final_df.sample(10))

print("\nThis concludes the demonstration of feature engineering and selection using scikit-learn.")
print("Our final dataset is now ready for modeling with the top 3 standardized features and one-hot encoded species columns.")
print("Thank you for following along!\n")