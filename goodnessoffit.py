# Assignment 5 - Goodness of a fit measures (R-squared, AIC, BIC) - Evan Moh

'''
Student Performance Factors data
https://www.kaggle.com/datasets/lainguyn123/student-performance-factors <br>
Description: "This dataset provides a comprehensive overview of various factors affecting student performance in exams. It includes information on study habits, 
attendance, parental involvement, and other aspects influencing academic success."
'''

# Import all the libraries
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

#Import csv file downloaded from Kaggle.
data = pd.read_csv('StudentPerformanceFactors.csv')

#Response variable is the variable that is being predicted. Also known as outcome variable.
response = 'Exam_Score'

#Predictor variable is the variable used to predict the response variable. Also known as independent variable.
predictor = ['Hours_Studied','Attendance','Sleep_Hours','Previous_Scores','Tutoring_Sessions','Physical_Activity']

#Seeing dimensions, data types,and missing values in StudentPerformanceFactors dataset.
def structure(input_Data):
    print("Data Structure")
    print("---------------")
    print(f"Dimensions: {input_Data.shape}")
    print(f"Data Types:\n{input_Data.dtypes}")
    print(f"Missing Values:\n{input_Data.isnull().sum()}")

structure(data)
'''
Interpretation
There are 6607 rows and 20 different variables.
There are missing values from teacher quality, parental education level, and distance from home columns. 
Since we will focus more on the numeric values, we will skip the steps like dropping the rows or filling in the gaps.
'''


#Before starting any analysis or transforming the data, look at the descriptive statistics.
def descr(input_Data):
    print("\nDescriptive Statistics")
    print("----------------------")
    numeric_columns = input_Data.select_dtypes(include=[np.number]).columns
    print("Central Tendency Measures:")
    print(input_Data[numeric_columns].describe().loc[['mean', '50%']])
    print("\nDispersion Measures:")
    print(input_Data[numeric_columns].describe().loc[['std', 'min', 'max']])

    # Check for distribution normality (skewness and kurtosis)
    print("\nDistribution Measures:")
    print("------------------------")
    print(input_Data[numeric_columns].skew())
    print(input_Data[numeric_columns].kurt())

descr(data)

'''
Interpretation

Exam score, the response variable, has a range from 55 to 101. The mean of this variable is 67.23, and the median is 67. 
The data is positively skewed (right-skewed). 
The skewness of 1.64 indicates a right-skewed distribution, while the kurtosis of 10.57 indicates heavier tails.
Columns such as hours studied, attendance, sleep hours, previous scores, and physical activity are close to a normal distribution.
'''

def standardize(input_Data):
    numeric_columns = input_Data.select_dtypes(include=[np.number]).columns
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(input_Data[numeric_columns])

#Back to DF for readibility and using pandas features
    scaled_df = pd.DataFrame(scaled_data, columns=numeric_columns)
    return scaled_df

def Linear(input_Data,response_input,predictor_input):
    #Define response variable
    y= input_Data[response_input]
    
    #Define predictor variables
    x= input_Data[predictor_input]
    x= sm.add_constant(x)

    #fit regression model
    model1 = sm.OLS(y, x).fit()
    return model1
'''
Data Transformation

Determining between Min-Max scaling and Z score standardization for this type of dataset requires careful consideration. 
Min Max scaling makes no distribution assumptions and is sensitive to outliers. 
It is often used for binary/categorical data which has bounded data. 
Z score standardization assumes data is normally distributed. It needs to handle outliers beforehand. 
As we removed all the outliers from previous steps, we will go with Z score standardization.
'''

#Standardize data
inputdata = standardize(data)
fitted_model1 = Linear(inputdata, response, predictor)


# View r squared, AIC, BIC models.
def r2(model):
    print(f"r^2 of the linear model: {model.rsquared}")

def AIC(model):
    print(f"AIC of the linear model: {model.aic}")

def BIC(model):
    print(f"BIC of the linear model: {model.bic}")

r2(fitted_model1)
AIC(fitted_model1)
BIC(fitted_model1)
'''
r^2 of the linear model: 0.598249632840968
AIC of the linear model: 12738.769528169923
BIC of the linear model: 12786.340722974133

### Interpretation
#### R Squared
R squared (coefficient of determination) measures the proportion of variance in the response variable that can be explained by the predictor variables in the model.
R^2 value of 0.598 indicates 59.8% of the variance in the response variable is explained by the model. This has a moderate level of explanatory power.

#### AIC (Akaike Information Criterion)
AIC is used to compare different models based on their goodness of fit and complexity. 
It penalizes models with more parameters to ovoid overfitting. 
Lower AIC value is a better model in terms of the trade-off between fit and complexity.

#### BIC (Bayesian Information Criterion)
BIC is similar to AIC but applies a stricter penalty for model complexity. BIC value of 12786 suggests this model (when adjusted for complexity), fits the data fairly well. 
It is best used for model comparison.
'''