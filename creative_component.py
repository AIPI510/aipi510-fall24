import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Function to calculate statistics
def calculate_stats(data):
    '''
    Given the data, calculate the measures of central tendency (mean, median, mode)
    
    Inputs:
        data (ndarray): data for which the mean, median, and mode will be calculated
    
    Outputs:
        mean: float64
        median: float64
        mode: float64
    '''
    mean = np.mean(data)
    median = np.median(data)
    rounded_data = np.round(data, 1)
    mode = stats.mode(rounded_data, keepdims=False).mode
    return mean, median, mode

# Function to generate datasets
def generate_dataset(distribution_type, size=100):
    '''
    Generate a small dataset with the given distribution_type and size
    
    Inputs:
        size (int): size of the generated dataset
        distribtion_type (object): string representing the distribution type [Normal, Left-Skewed, Right-skewed]

    Outputs:
        data (ndarray): dataset to be used
    '''
    if distribution_type == 'Normal':
        # Create an array of random elements with a normal distribution
        return np.random.normal(loc=0, scale=1, size=size)
    elif distribution_type == 'Left-skewed':
        # Using scipy, create an array of random elements with a left-skewed distribution
        data = stats.skewnorm.rvs(a=-5, size=size)
        return data
    elif distribution_type == 'Right-skewed':
        # Using scipy, create an array of random elements with a right-skewed distribution
        data = stats.skewnorm.rvs(a=5, size=size)
        return data

# Function to plot distribution
def plot_distribution(data, mean, median, mode):
    '''
    Create a histogram plot to visualize the data distribution.
    Includes mean, median, and mode as vertical lines for visualization purposes.
    
    Inputs:
        data (ndarray): dataset whose distribution will be plotted
        mean (float64): mean of the dataset
        median (float64): median of the dataset
        mode (float64): mode of the dataset

    Outputs:
        fig (pyplot.figure): histogram plot of the data passed as input
    '''
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data, kde=True, ax=ax)
    #Including the measures of central tendencies in the plot as vertical lines
    ax.axvline(mean, color='r', linestyle='--', label=f'Mean: {mean:.2f}')
    ax.axvline(median, color='g', linestyle='--', label=f'Median: {median:.2f}')
    ax.axvline(mode, color='b', linestyle='--', label=f'Mode: {mode:.2f}')
    ax.legend()
    return fig

# Main function that creates the streamlit web app
def main():
    #Setting the web page's title 
    st.title('Deftones Stats Visualizer')

    # Initialize session state, which allows us data to persist in the session
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'last_added_point' not in st.session_state:
        st.session_state.last_added_point = None
    if 'distribution_type' not in st.session_state:
        st.session_state.distribution_type = 'Normal'

    # Create a sidebar to select the pre-built dataset to plot or file upload
    st.sidebar.header('Data Source')
    data_source = st.sidebar.radio('Select Data Source', ['Pre-defined Distributions', 'Upload CSV'])

    #If pre-defined distributions was selected, intialize the appropriate data that will be persisted
    if data_source == 'Pre-defined Distributions':
        distribution_type = st.sidebar.selectbox('Select Distribution', ['Normal', 'Left-skewed', 'Right-skewed'], key='distribution_select')
        if distribution_type != st.session_state.distribution_type or st.session_state.data is None:
            st.session_state.data = generate_dataset(distribution_type)
            st.session_state.distribution_type = distribution_type
    else:
        #If file upload was selected
        uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            # Create a df from the uploaded csv
            df = pd.read_csv(uploaded_file)
            # Filter out categorical features and only keep numeric ones to avoid any bugs 
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            column = st.sidebar.selectbox('Select Numeric Columns to Visualize (dtype int or float)', numeric_columns)
            #Set the session data to the chosen column so that it persists
            st.session_state.data = df[column].values
        else:
            st.sidebar.warning('Please upload a CSV file')
            return
    
    # Calculate Initial Statistics
    mean, median, mode = calculate_stats(st.session_state.data)

    # Display Initial plot
    st.subheader('Distribution Visualization')
    fig = plot_distribution(st.session_state.data, mean, median, mode)
    plot_placeholder = st.pyplot(fig)

    # Add data point section
    st.subheader('Add Data Point')
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button('Add Random Data Point'):
            new_point = np.random.uniform(min(st.session_state.data), max(st.session_state.data))
            st.session_state.data = np.append(st.session_state.data, new_point)
            st.session_state.last_added_point = new_point

    with col2:
        specific_point = st.number_input('Enter a specific value:', value=0.0, step=0.1)
        if st.button('Add Specific Data Point'):
            st.session_state.data = np.append(st.session_state.data, specific_point)
            st.session_state.last_added_point = specific_point

    # Calculate new statistics
    mean, median, mode = calculate_stats(st.session_state.data)

    # Update plot since we recalculated the stats and changed the persisted data with the new added point
    fig = plot_distribution(st.session_state.data, mean, median, mode)
    plot_placeholder.pyplot(fig)

    #Create separate columns to display different info (cleaner visualization)
    stat_col1, stat_col2, stat_col3 = st.columns(3)

    #Display the measures of central tendency
    stat_col1.subheader('Statistics')
    stat_col1.write(f'Mean: {mean:.2f}')
    stat_col1.write(f'Median: {median:.2f}')
    stat_col1.write(f'Mode: {mode:.2f}')

    # Display last added point
    if st.session_state.last_added_point is not None:
        stat_col2.subheader('Last Added Point')
        stat_col2.write(f'Value: {st.session_state.last_added_point:.2f}')

    # Display total number of data points
    stat_col3.subheader('Total Data Points')
    stat_col3.write(f'Count: {len(st.session_state.data)}')

    # Added section with notable observations and questions users should keep in mind while using the web app
    st.subheader('Observations')
    st.write('Look at the difference in value between mean, median, and mode. What does that tell us about the data skewness?')
    st.write('Does the relationship between relationship between mean, median,and mode hold for distributions with multiple peaks?')
    st.write('Notice the change in mean value when adding extreme values')
    st.write('Notice how the degree of skewness changes as the difference between mean and median changes')
    
if __name__ == '__main__':
    main()