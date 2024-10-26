import pandas as pd
from tsfresh import extract_features

# pip install tsfresh
# pip install setuptools

def main():
    try:
        # Read the csv file and put it into pandas dataframe
        df = pd.read_csv('data/thailand-air-quality.csv', usecols=["city", "date", "pm25", "pm10"], skipinitialspace = True)
        df.dropna(subset=["pm25", "pm10"], inplace=True)
        print(df)
        # df = df.drop(["o3", "no2", "so2", "co"], axis=1, inplace=True)
        
    except Exception as err:
        print(f'Error occurred: {err}')

    extracted_features = extract_features(df, column_id='city', column_sort='date')
    print(extracted_features.head())

if __name__ == '__main__':
	main()