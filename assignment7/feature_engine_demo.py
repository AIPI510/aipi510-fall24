import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Feature Engine
import feature_engine as fe
from feature_engine.pipeline import Pipeline as pipeline # https://feature-engine.trainindata.com/en/latest/api_doc/pipeline/Pipeline.html
# pipeline is similar to sklearn's pipeline, where you define each successive step of the data transformation
from feature_engine.outliers import Winsorizer as winsorizer # https://feature-engine.trainindata.com/en/latest/api_doc/outliers/Winsorizer.html#feature_engine.outliers.Winsorizer
from feature_engine.encoding import RareLabelEncoder as rare_encoder # https://feature-engine.trainindata.com/en/latest/api_doc/encoding/RareLabelEncoder.html
from feature_engine.encoding import MeanEncoder as target_encoder # https://feature-engine.trainindata.com/en/latest/api_doc/encoding/MeanEncoder.html
from feature_engine.imputation import MeanMedianImputer as median_imputer # https://feature-engine.trainindata.com/en/latest/api_doc/imputation/MeanMedianImputer.html
from feature_engine.imputation import CategoricalImputer as categorical_imputer # https://feature-engine.trainindata.com/en/latest/api_doc/imputation/CategoricalImputer.html


def discover_categorical_and_numerical(df):
  """_summary_
  This function returns a list of categorical, discrete, and  numerical features
  """
  categorical = df.select_dtypes(include=object).columns.to_list() # [c in df.columns if df[c].dtype == "O"]
  numerical = df.select_dtypes(include=np.number).columns.to_list() # df.columns.difference(categorical)

  # make a list of discrete variables
  discrete = [var for var in numerical if df[var].nunique() <= 15] # set the number of unique values does not exceed 15

  # categorical encoders work only with object type variables to treat numerical variables as categorical, we need to re-cast them
  df[discrete]= df[discrete].astype('object')

  # update numerical variables as continuous variables
  numerical = [var for var in numerical if var not in discrete]

  print(f"There are {len(categorical)} categorical, {len(discrete)} discrete numerical, and {len(numerical)} continuous numerical variables / features in the dataset")
  return categorical, discrete, numerical

def feature_engine(X, y, categorical, discrete, numerical):
    """
    This function does the feature engineering
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    processor = pipeline([
        # impute missing values with median value of the corresponding feature, applies to numerical features only
        ('median_imputation', median_imputer(imputation_method='median', variables=numerical)), 

        # winsorizer works by capping, instead of removing the outliers. This preserves the useful info from the data and keep the distribution relatively in tact.
        ('outlier_treatment', winsorizer(capping_method='iqr', variables=numerical)),
        
        
        # There are many ways to choose what calculation to winsorize, here 
        # we use "iqr" which stands for inter-quartile-range (above Q3 or below Q1), a fairly common way to identify outliers.

        # encode NA or missing values in categorical features with "missing".
        ('missing_val_encoding', categorical_imputer(variables=categorical, return_object=False, ignore_format=False)),

        # should there be rare values within a feature, encode with a label 'rare'
        ('rare_val_encoding', rare_encoder(variables=categorical,tol=0.05, n_categories=10)),

        # Encode with the avarage target value after grouping by each categorical feature. 
        ('target_encoder', target_encoder(variables=categorical))

    ])

    X_train_transformed = processor.fit_transform(X_train, y_train)
    return X_train_transformed


def main():
    # Load the dataset
    df = pd.read_csv("/Users/owner/Desktop/data_science/ml_course/aipi510/assignment7/data/customer_churn_data.csv")
    print(df.head(2))

    # drop useless variables
    df.drop(columns=['customer_id', 'Name', 'referral_id'], inplace=True)

    # Split the dataset into 3 distinct types
    categorical, discrete, numerical = discover_categorical_and_numerical(df)

    # Minor changes to the dataframe 
    numerical = numerical[1:]
    
    df['churn_risk_score'] = df['churn_risk_score'].astype(int)
    X, y = df.drop(columns="churn_risk_score"), df['churn_risk_score']

    # Feature engineering
    X_trained_transformed = feature_engine(X, y, categorical, discrete, numerical)

    print(f"\n\n The above warnings are normal as the process runs.\n")
    print(X_trained_transformed.head(2))

if __name__ == "__main__":
    main()
