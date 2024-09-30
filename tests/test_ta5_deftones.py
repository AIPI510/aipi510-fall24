from collections import Counter
import numpy as np
import pytest
from scipy import stats
import sys
import os

# Add the parent directory to sys.path to import the required module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import the functions to test
from ta5_deftones import get_mean, get_median, get_mode

def test_mean_symmetric():
    '''
    tests the get_mean function for a symmetric normal distribution by calculating the mean manually, comparing it 
    to the way in which the mean is calculated in get_mean (np.mean()) and asserts that the two are equivalent up to 5 decimal places
    '''

    data = np.random.normal(loc=0, scale=1, size=1000000)
    mean = get_mean(data)
    check_mean = sum(data) / len(data)

    assert round(mean, 5) == round(check_mean, 5)

def test_mean_skewed_right():
    '''
    tests the get_mean function for a distribution skewed to the right by calculating the mean manually, comparing it 
    to the way in which the mean is calculated in get_mean (np.mean()) and asserts that the two are equivalent up to 5 decimal places
    '''

    data = stats.skewnorm.rvs(a=5, size=100000)
    mean = get_mean(data)
    check_mean = sum(data) / len(data)

    assert round(mean, 5) == round(check_mean, 5)

def test_mean_skewed_left():
    '''
    tests the get_mean function for a distribution skewed to the left by calculating the mean manually, comparing it 
    to the way in which the mean is calculated in get_mean (np.mean()) and asserts that the two are equivalent up to 5 decimal places
    '''
        
    data = stats.skewnorm.rvs(a=-5, size=100000)
    mean = get_mean(data)
    check_mean = sum(data) / len(data)

    assert round(mean, 5) == round(check_mean, 5)

def test_median_symmetric():
    '''
    tests the get_median function for a symmetric normal distribution by getting the median manually (using the size
    passed in in the main function), comparing it to the way in which the median is calculated in get_mean (np.median()) and 
    asserts that the two are equivalent
    '''

    data = np.random.normal(loc=0, scale=1, size=1000000)
    median = get_median(data)
    
    # Sort the data
    sorted_data = sorted(data)
    mid = 500000

    check_median = (sorted_data[mid -1] + sorted_data[mid]) / 2

    assert median == check_median

def test_median_skewed_right():
    '''
    tests the get_median function for a distribution skewed to the right by getting the median manually (using the size
    passed in in the main function), comparing it to the way in which the median is calculated in get_mean (np.median()) and 
    asserts that the two are equivalent
    '''

    data = stats.skewnorm.rvs(a=5, size=100000)
    median = get_median(data)
    
    # Sort the data
    sorted_data = sorted(data)
    mid = 50000

    check_median = (sorted_data[mid -1] + sorted_data[mid]) / 2

    assert median == check_median

def test_median_skewed_left():
    '''
    tests the get_median function for a distribution skewed to the left by getting the median manually (using the size
    passed in in the main function), comparing it to the way in which the median is calculated in get_mean (np.median()) and 
    asserts that the two are equivalent
    '''
        
    data = stats.skewnorm.rvs(a=-5, size=100000)
    median = get_median(data)
    
    # Sort the data
    sorted_data = sorted(data)
    mid = 50000

    check_median = (sorted_data[mid -1] + sorted_data[mid]) / 2

    assert median == check_median

def test_mode_symmetric():
    '''
    tests the get_mode function for a symmetric normal distribution by using Counter from collections to get the most common value in the array,
    comparing it to the way in which the mode is calculated in get_mode (stats.mode(data).mode) and asserts that the two are equivalent
    '''
        
    data = np.random.normal(loc=0, scale=1, size=1000000)
    data = np.round(data)
    mode = get_mode(data)

    count = Counter(data)
    
    # Find the element(s) with the maximum frequency
    check_mode = count.most_common(1)[0][0]

    assert mode == check_mode

def test_mode_skewed_right():
    '''
    tests the get_mode function for a distribution skewed to the right by using Counter from collections to get the most common value in the 
    array, comparing it to the way in which the mode is calculated in get_mode (stats.mode(data).mode) and asserts that the two are equivalent
    '''

    data = stats.skewnorm.rvs(a=5, size=100000)
    data = np.round(data,1)
    mode = get_mode(data)

    count = Counter(data)
    
    # Find the element(s) with the maximum frequency
    check_mode = count.most_common(1)[0][0]

    assert mode == check_mode

def test_mode_skewed_left():
    '''
    tests the get_mode function for a distribution skewed to the left by using Counter from collections to get the most common value in the 
    array, comparing it to the way in which the mode is calculated in get_mode (stats.mode(data).mode) and asserts that the two are equivalent
    '''

    data = stats.skewnorm.rvs(a=-5, size=100000)
    data = np.round(data,1)
    mode = get_mode(data)

    count = Counter(data)
    
    # Find the element(s) with the maximum frequency
    check_mode = count.most_common(1)[0][0]

    assert mode == check_mode