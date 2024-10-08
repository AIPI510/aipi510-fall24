import numpy as np
from retry_requests import retry
import requests_cache
import openmeteo_requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
from sklearn.linear_model import LinearRegression

def setup_record_responses():
    """
    Sets up a cache session and pulls responses from the API link.

    Args: None

    Returns:
        response (WeatherAPIResponse): A WeatherAPIResponse variable that houses the hourly weather data at the specified coords 
            which is used in our script.
    """
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 35.994,
        "longitude": -78.8986,
        "hourly": "temperature_2m",
        "start_date": "2024-07-01",
        "end_date": "2024-10-01"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Processes only the first location.
    response = responses[0]
    return response

def process_hourly_data(response):
    """
    Processes hourly data from the WeatherAPI response.

    Args:
        response (WeatherAPIResponse): A WeatherAPIResponse variable that houses the hourly weather data at the specified coords 
            which is used in our script.

    Returns:
        hourly_dataframe (df): A dataframe variable that houses the data and hour of associated temperatures.
    """
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    print(hourly_dataframe.head())

    return hourly_dataframe

def compute_stats(df, num_bootstrap_samples=1000):
    """
    Computes numerous statistics regarding the CI

    Args:
        df (df): A dataframe variable that houses the data and hour of associated temperatures.

    Returns:
        lower_bound (float): The lower bound of the calculated CI (Confidence Interval)
        upper_bound (float): The upper bound of the calculated CI (Confidence Interval)
        lower_bootstrap (float): The lower bound of the calculated BCI (Bootstrap Confidence Interval)
        upper_bootstrap (float): The upper bound of the calculated BCI (Bootstrap Confidence Interval)
    """
    sample_size = df.shape[0]
    sample_mean = df['temperature_2m'].mean()
    std_dev = df['temperature_2m'].std()
    z = 1.96

    print('Sample Size:', sample_size)
    print('Sample Mean:', sample_mean)
    print('Standard Deviation:', std_dev)

    # Calculate confidence interval using normal distribution
    upper_bound = sample_mean + z * (std_dev / math.sqrt(sample_size))
    lower_bound = sample_mean - z * (std_dev / math.sqrt(sample_size))
    
    print('Upper and Lower Bounds', (lower_bound, upper_bound))
    
    bootstrap_means = []
    for _ in range(num_bootstrap_samples):
        bootstrap_sample = df['temperature_2m'].sample(n=sample_size, replace=True)
        bootstrap_means.append(bootstrap_sample.mean())
    
    # Calculate bootstrap confidence interval (in this case, 95% CI)
    lower_bootstrap = np.percentile(bootstrap_means, 2.5)
    upper_bootstrap = np.percentile(bootstrap_means, 97.5)
    
    print('Bootstrap 95% Confidence Interval:', (lower_bootstrap, upper_bootstrap))

    # Predict p-value (two-tailed test) for hypothesis that mean is equal to some value
    hypothetical_mean = 0
    more_extreme = [mean for mean in bootstrap_means if abs(mean - hypothetical_mean) >= abs(sample_mean - hypothetical_mean)]
    p_value = len(more_extreme) / num_bootstrap_samples
    
    print('P-value for mean being equal to 0:', p_value)

    return lower_bound, upper_bound, lower_bootstrap, upper_bootstrap

def linear_regression_analysis(df, X0):
    """
    Performs a linear regression analysis based on time and weather data.

    Args:
        df (df): A dataframe variable that houses the data and hour of associated temperatures.
        X0 (Coefficient that is multiplied into the beta in y_hat = Beta0_hat + Beta1_hat * X0)

    Returns:
        Y_hat (float): The predicted fit of temperatures generated from the X0 (Specific date)
        ci_lower (float): The lower bound of the calculated CI (Confidence Interval)
        ci_upper (float): The upper bound of the calculated CI (Bootstrap Confidence Interval)
    """
    # Perform linear regression on temperature over time
    df['time_ordinal'] = pd.to_datetime(df['date']).map(pd.Timestamp.toordinal)
    X = df[['time_ordinal']]
    y = df['temperature_2m']

    model = LinearRegression()
    model.fit(X, y)

    # Prediction for X0
    X0_ordinal = pd.Timestamp(X0).toordinal()
    X0_reshaped = np.array([[X0_ordinal]])  # Reshape X0 to deal with labeling issue
    Yhat = model.predict(pd.DataFrame(X0_reshaped, columns=['time_ordinal']))[0]

    # Calculate SSxx, MSE, and SE for prediction
    Xbar = df['time_ordinal'].mean()
    SSxx = sum((df['time_ordinal'] - Xbar) ** 2)
    residuals = y - model.predict(X)
    MSE = (residuals ** 2).sum() / (len(df) - 2)
    SEYhat = math.sqrt(MSE * (1 / len(df) + ((X0_ordinal - Xbar) ** 2) / SSxx))

    t_value = 1.96 
    ci_lower = Yhat - t_value * SEYhat
    ci_upper = Yhat + t_value * SEYhat

    print(f'fit: {Yhat:.4f}')
    print(f'lwr: {ci_lower:.4f}')
    print(f'upr: {ci_upper:.4f}')

    plot_regression_line(df, model, X0, Yhat, ci_lower, ci_upper)

    return Yhat, ci_lower, ci_upper

def plot_regression_line(df, model, X0, Yhat, ci_lower, ci_upper):
    """
    Visualizes the linear regression analysis based on time and weather data.

    Args:
        df (df): A dataframe variable that houses the data and hour of associated temperatures.
        model (LinearRegression): The linear regression model that is fit on ordinal time and weather data.
        X0 (Coefficient that is multiplied into the beta in y_hat = Beta0_hat + Beta1_hat * X0)
        Y_hat (float): The predicted fit of temperatures generated from the X0 (Specific date)
        ci_lower (float): The lower bound of the calculated CI (Confidence Interval)
        ci_upper (float): The upper bound of the calculated CI (Bootstrap Confidence Interval)

    Returns: None
    """
    plt.figure(figsize=(10, 6))

    plt.scatter(df['date'], df['temperature_2m'], label='Observed Data', alpha=0.6)

    # Regression line
    df_sorted = df.sort_values('time_ordinal')
    plt.plot(df_sorted['date'], model.predict(df_sorted[['time_ordinal']]), color='blue', label='Regression Line')

    # Predicted value for X0 with confidence interval
    X0_date = pd.Timestamp(X0)
    plt.errorbar(X0_date, Yhat, yerr=[[Yhat - ci_lower], [ci_upper - Yhat]], fmt='o', color='red', ecolor='orange', elinewidth=2, capsize=4, label='Prediction with CI')

    plt.xlabel('Date')
    plt.ylabel('Temperature (Celsius)')
    plt.title('Linear Regression of Temperature vs. Time with Prediction CI')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    plt.show()

def line_plot(df, lb, ub):
    """
    Visualizes a line plot based on the dataframe and lower and upper bounds.

    Args:
        df (df): A dataframe variable that houses the data and hour of associated temperatures.
        lb (float): The lower bound of the calculated CI (Confidence Interval)
        ub (float): The upper bound of the calculated CI (Confidence Interval)

    Returns: None
    """
    sns.lineplot(x=df['date'], y=df['temperature_2m'])
    plt.axhline(y=lb, color='red', linestyle='--', label=str(lb))
    plt.axhline(y=ub, color='red', linestyle='--', label=str(ub))
    plt.xticks(rotation=45)
    plt.title("Temperature Change by date in Durham")
    plt.ylabel('Temperature (Celsius)')
    plt.xlabel('Date')
    plt.tight_layout()
    plt.show()

def hist_plot(df, lb, ub):
    """
    Visualizes a histogram plot based on the dataframe and lower and upper bounds.

    Args:
        df (df): A dataframe variable that houses the data and hour of associated temperatures.
        lb (float): The lower bound of the calculated CI (Confidence Interval)
        ub (float): The upper bound of the calculated CI (Confidence Interval)

    Returns: None
    """
    sns.histplot(df['temperature_2m'], bins=10, kde=True)
    plt.axvline(x=lb, color='red', linestyle='--', label=f'{lb}')
    plt.axvline(x=ub, color='red', linestyle='--', label=f'{ub}')
    plt.title("Distribution of Temperature in Durham")
    plt.xlabel('Temperature (Celsius)')
    plt.ylabel('Count of Temperature Values')
    plt.show()

if __name__ == '__main__':
    response = setup_record_responses()
    hourly_dataframe = process_hourly_data(response)
    lower_bound, upper_bound, lower_bootstrap, upper_bootstrap = compute_stats(hourly_dataframe)

    # Specify a date for prediction
    X0 = "2024-08-15"
    Yhat, ci_lower, ci_upper = linear_regression_analysis(hourly_dataframe, X0)

    line_plot(hourly_dataframe, lower_bound, upper_bound)
    line_plot(hourly_dataframe, lower_bootstrap, upper_bootstrap)

    hist_plot(hourly_dataframe, lower_bound, upper_bound)
    hist_plot(hourly_dataframe, lower_bootstrap, upper_bootstrap)