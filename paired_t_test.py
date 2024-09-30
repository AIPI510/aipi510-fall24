import pandas as pd

from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO)

class DataAnalyzer:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path, encoding='latin1')
        self.t_data = None

    def preprocess_data(self):
        # Filter the data for 'F' and 'M' positions
        self.data = self.data[(self.data['Position'] == 'F') | (self.data['Position'] == 'M')]
        self.data = self.data[['Name', 'Year', 'Goals']]

        # Separate data for the two seasons
        data_2021 = self.data[self.data['Year'] == '20/21']
        data_1920 = self.data[self.data['Year'] == '19/20']

        # Merge the data
        self.t_data = pd.merge(data_1920, data_2021, on='Name', suffixes=('_19/20', '_20/21'))
        
        self.t_data = self.t_data.drop_duplicates(subset='Name', keep=False)

        # Create a column and store the difference between the two seasons' goals
        self.t_data['diff'] = self.t_data['Goals_19/20'] - self.t_data['Goals_20/21']

    #First assumption: The differences between samples are normally distributed
    def check_normality(self):
        differences = self.t_data['diff']
        
        #Histogram
        plt.figure(figsize=(8, 6))
        sns.histplot(differences, kde=True, bins=20)
        plt.title("Histogram of Differences Between Samples")
        plt.xlabel("Difference")
        plt.ylabel("Frequency")
        plt.show()

        # Q-Q plot
        stats.probplot(differences, dist="norm", plot=plt)
        plt.title("Q-Q Plot of Differences")
        plt.show()

    # Second assumption: No significant outliers in the difference between two samples
    def check_outliers(self):
        differences = self.t_data['diff']
        sns.boxplot(x=differences)
        plt.title("Boxplot of Differences")
        plt.show()

    # Clean outliers
    def handle_outliers(self):
        # Calculate Q1 (25th percentile) and Q3 (75th percentile)
        Q1 = self.t_data['diff'].quantile(0.25)
        Q3 = self.t_data['diff'].quantile(0.75)

        # Calculate the IQR
        IQR = Q3 - Q1

        # Define the lower and upper bounds
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Filter out outliers
        self.t_data = self.t_data[(self.t_data['diff'] >= lower_bound) & (self.t_data['diff'] <= upper_bound)]

        # Print shape after outlier removal
        print(f"Data shape after handling outliers: {self.t_data.shape}")

        

    # Perform paired t-test
    def t_test(self):
        score1 = self.t_data['Goals_19/20']
        score2 = self.t_data['Goals_20/21']

        # Paired t-test
        t_stat, p_value = stats.ttest_rel(score1, score2)

        # Output the results
        print(f"T-statistic: {t_stat}, P-value: {p_value}")

        return t_stat, p_value

    # Print the result
    def results(self, p_value):
        if p_value<0.05:
            logging.info("The means of the two samples are different")
            logging.info('''p value is less than .05, therefore there is a non-random difference 
              in the player goals between 19/20 and 20/21 for midfielders and forwards in the Premier League''')
        else:
            logging.info("The means of the two samples are equal.")
        #print(self.t_data.head())




if __name__ == "__main__":
    analyzer = DataAnalyzer('prem.csv')
    analyzer.preprocess_data()

    analyzer.check_normality()
    
    analyzer.check_outliers()
    
    analyzer.handle_outliers()  
    
    # Check if there are outliers again after handle_outliers()  
    analyzer.check_outliers()
    
    t_stat, p_value = analyzer.t_test()  
    analyzer.results(p_value)  

    
