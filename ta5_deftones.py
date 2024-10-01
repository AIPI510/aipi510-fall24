import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set a seed for reproducibility
np.random.seed(0)

def get_mean(data):
    '''
    gets the mean from a numpy array
    
    Inputs:
        data(np.ndarray): input data

    Returns:
        the mean of data
    '''

    return np.mean(data)

def get_median(data):
    '''
    gets the median from a numpy array
    
    Inputs:
        data(np.ndarray): input data

    Returns:
        the median of data
    '''

    return np.median(data)

def get_mode(data):
    '''
    gets the mode from a numpy array
    
    Inputs:
        data(np.ndarray): input data

    Returns:
        the mode of data
    '''

    return stats.mode(data).mode

def plot_symmetric_dist(loc, scale, size):
    '''
    creates and shows a plot for a symmetric normal distribution
    
    Inputs:
        loc(float): the mean for which to center the distribution
        scale(float): the standard deviation of the distribution
        size(int): the number of datapoints for the distribution

    '''

    # Generate a large normally distributed dataset
    data = np.random.normal(loc=loc, scale=scale, size=size)

    # Calculate mean, median, and mode
    mean = get_mean(data)
    median = get_median(data)
    mode = get_mode(np.round(data))

    # Plot the distribution with mean, median, and mode
    plt.figure(figsize=(10, 6))
    hist = sns.histplot(data, kde=True, color='skyblue', bins=30)
    hist.lines[0].set_color('blue')

    # Add vertical lines for mean, median, and mode
    plt.axvline(mean, color='red', linestyle='--', label=f'Mean: {mean:.2f}')
    plt.axvline(median, color='green', linestyle='--', label=f'Median: {median:.2f}')
    plt.axvline(mode, color='blue', linestyle='--', label=f'Mode: {mode:.2f}')

    # title the plot, give it a legend and show the plot
    plt.title('Perfectly Symmetric Normal Distribution')
    plt.legend()
    plt.show()

def plot_skewed_dist(a, size, plot_title):
    '''
    creates and shows a plot for a skewed distribution
    
    Inputs:
        a(float): the skewness of the distribution
        size(int): the number of datapoints for the distribution
        plot_title(str): what to title the plot
    '''

    # Generate a large skewed dataset
    data = stats.skewnorm.rvs(a=a, size=size)

    # Calculate mean, median, and mode
    mean = get_mean(data)
    median = get_median(data)
    mode = get_mode(np.round(data, 1))

    # Plot the distribution with mean, median, and mode
    plt.figure(figsize=(10, 6))
    hist = sns.histplot(data, kde=True, color='skyblue', bins=30)
    hist.lines[0].set_color('blue')

    # Add vertical lines for mean, median, and mode
    plt.axvline(mean, color='red', linestyle='--', label=f'Mean: {mean:.2f}')
    plt.axvline(median, color='green', linestyle='--', label=f'Median: {median:.2f}')
    plt.axvline(mode, color='blue', linestyle='--', label=f'Mode: {mode:.2f}')

    # title the plot, give it a legend and show the plot
    plt.title(plot_title)
    plt.legend()
    plt.show()

def main():
    plot_symmetric_dist(0, 1, 1000000)
    plot_skewed_dist(5, 100000, 'Distribution Skewed to the Right')
    plot_skewed_dist(-5, 100000, 'Distribution Skewed to the Left')

if __name__ == "__main__":
    main()