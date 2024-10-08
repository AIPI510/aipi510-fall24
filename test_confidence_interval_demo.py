import pytest
from confidence_interval_demo import pd, np, LinearRegression, compute_stats, linear_regression_analysis

'''Sample data to be used for testing'''
@pytest.fixture
def sample_dataframe():
    dates = pd.date_range(start="2024-07-01", periods=10, freq='D')
    temperatures = [25.0, 26.1, 24.5, 25.5, 27.3, 28.0, 26.5, 25.0, 24.8, 27.0]
    return pd.DataFrame({'date': dates, 'temperature_2m': temperatures})

'''Test 1: Test the shape of the dataframe returned by compute_stats'''
def test_compute_stats_shape(sample_dataframe):
    lower_bound, upper_bound, lower_bootstrap, upper_bootstrap = compute_stats(sample_dataframe)
    assert isinstance(lower_bound, float)
    assert isinstance(upper_bound, float)

'''Test 2: Test if the computed confidence intervals are in the correct order'''
def test_compute_stats_interval_order(sample_dataframe):
    lower_bound, upper_bound, lower_bootstrap, upper_bootstrap = compute_stats(sample_dataframe)
    assert lower_bound <= upper_bound
    assert lower_bootstrap <= upper_bootstrap

'''Test 3: Test if the MSE is calculated correctly (positive value)'''
def test_positive_mse(sample_dataframe):
    df = sample_dataframe.copy()
    df['time_ordinal'] = pd.to_datetime(df['date']).map(pd.Timestamp.toordinal)
    X = df[['time_ordinal']]
    y = df['temperature_2m']
    model = LinearRegression().fit(X, y)
    residuals = y - model.predict(X)
    MSE = (residuals ** 2).sum() / (len(df) - 2)
    assert MSE > 0

'''Test 4: Test regression line prediction at an existing point'''
def test_prediction_at_existing_point(sample_dataframe):
    df = sample_dataframe.copy()
    df['time_ordinal'] = pd.to_datetime(df['date']).map(pd.Timestamp.toordinal)
    X = df[['time_ordinal']]
    y = df['temperature_2m']
    model = LinearRegression().fit(X, y)
    existing_date = df['date'].iloc[0]
    existing_ordinal = pd.Timestamp(existing_date).toordinal()
    Yhat = model.predict([[existing_ordinal]])[0]
    assert isinstance(Yhat, float)

'''Test 5: Test that bootstrap confidence intervals are not equal to the normal intervals'''
def test_bootstrap_vs_normal_intervals(sample_dataframe):
    lower_bound, upper_bound, lower_bootstrap, upper_bootstrap = compute_stats(sample_dataframe)
    assert (lower_bound != lower_bootstrap) or (upper_bound != upper_bootstrap)