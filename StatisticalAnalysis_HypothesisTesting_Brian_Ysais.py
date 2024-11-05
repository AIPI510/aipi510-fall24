import numpy as np
import scipy.stats as stats
from statsmodels.stats.multitest import multipletests

# This is our script to perform the following:
# Hypothesis Testing
    # Type I and Type II errors
    # P-values and significance levels
    # Multiple hypothesis correction (Bonferroni)
#The calculations are simple but we will add verbose comments describing parameters, operations, and return values. 

def calculate_power(sample1, sample2, alpha, effect_size=None):
   
    # This method calculates the statistical power (probability of Type II error) of a two-sample t-test.
    #Let's describe some parameters used in this method:
    #- sample1: array-like, sample of data for group 1
    #- sample2: array-like, sample of data for group 2
    #- alpha: significance level
    #- effect_size: pre-calculated effect size (optional)

    # This method returns:
    # - power: estimated power of the test (1 - beta, where beta is the probability of Type II error)
    
    n1, n2 = len(sample1), len(sample2)
    std1, std2 = np.std(sample1, ddof=1), np.std(sample2, ddof=1)
    
    # Let's use an if statement to execute a block of code in case not effect_sized is met

    if not effect_size:
        pooled_std = np.sqrt(((n1 - 1) * std1**2 + (n2 - 1) * std2**2) / (n1 + n2 - 2))
        effect_size = (np.mean(sample1) - np.mean(sample2)) / pooled_std

    # Use scipy to calculate power
    # If running this script locally you may need to create a virtual environment and install the scipy and statsmodels libraries
    analysis = stats.norm()
    power = analysis.sf(stats.norm.ppf(alpha/2) - effect_size * np.sqrt(n1 + n2))
    return power

def hypothesis_test(sample1, sample2, alpha=0.05, correction_method='bonferroni', num_tests=1):
   
    # Perform a two-sample t-test for independent samples with Bonferroni multiple hypothesis correction.
    # Let's declare some parameters:
    # sample1: array-like, sample of data for group 1
    # sample2: array-like, sample of data for group 2
    # alpha: significance level (default is 0.05)
    # correction_method: method for multiple testing correction ('bonferroni' supported)
    # num_tests: number of tests being performed (for Bonferroni correction)

    # This method returns:
    # test_statistic: the t-test statistic value
    # p_value: the corrected p-value (if correction is applied)
    # conclusion: a string explaining if we reject or fail to reject the null hypothesis
    # type_i_error: the probability of a Type I error (false positive)
    # type_ii_error: the probability of a Type II error (false negative)
   #

    # Step 1: Perform the t-test and see what we obtain 
    test_statistic, p_value = stats.ttest_ind(sample1, sample2)

    # Step 2: Let's apply Bonferroni correction if applicable. This is the thid bullet point that we must complete in our hypothesis testing requirements from the assignment
    if correction_method == 'bonferroni':
        corrected_p_value = min(p_value * num_tests, 1.0)  # Adjust p-value by number of tests
    else:
        corrected_p_value = p_value

    # Step 3: We must now calculate Type I error (false positive) and Type II error (false negative)
    type_i_error = alpha
    power = calculate_power(sample1, sample2, alpha)
    type_ii_error = 1 - power  # Probability of failing to reject the null when it's false

    # Step 4: Let's determine if the null hypothesis is rejected
    if corrected_p_value < alpha:
        conclusion = "Reject the null hypothesis (significant difference)."
    else:
        conclusion = "Fail to reject the null hypothesis (no significant difference)."

    # Step 5: Let's define some return results
    return {
        'test_statistic': test_statistic,
        'corrected_p_value': corrected_p_value,
        'conclusion': conclusion,
        'type_i_error': type_i_error,
        'type_ii_error': type_ii_error
    }

def print_results(results):
    
   # Print the results of the hypothesis test in a human friendly way.
   # Let's declare some parameters:
   # - results: Dictionary containing test results including test statistic, p-value, and errors.
  
   print("T-test statistic: {:.4f}".format(results['test_statistic']))
   print("Corrected P-value: {:.4f}".format(results['corrected_p_value']))
   print("Conclusion: {}".format(results['conclusion']))
   print("Type I Error (α): {:.4f}".format(results['type_i_error']))
   print("Type II Error (β): {:.4f}".format(results['type_ii_error']))


# Below is an example of how to use this script and view the results.
if __name__ == "__main__":
    # The data below was arbitrarily added. You can add your own data sets.
    group1 = np.array([2.5, 3.1, 3.7, 4.0, 3.3])
    group2 = np.array([3.8, 4.1, 4.5, 3.9, 4.3])
    # Let's perform hypothesis test with Bonferroni correction
    num_tests = 3  # Number of hypothesis tests
    alpha = 0.05   # Given significance level
    #Call the hypothesis test method and pass the parameters
    results = hypothesis_test(group1, group2, alpha=alpha, correction_method='bonferroni', num_tests=num_tests)
    # Finally watch the results on your screen!
    print_results(results)
