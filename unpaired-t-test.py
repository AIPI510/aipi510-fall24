import numpy as np
import scipy.stats
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import pytest


def get_cli_argument():
    """ArgumentParser to accept inputs from user via command line: sample size, mean & variance for the two randomly generated samples"""
    parser = argparse.ArgumentParser(description="""Create two samples with random normal distribution based on specified mean, variance, and sample size, 
                                     then perform unpaired t-test to assess whether there is a significant difference in the mean of the two samples""")
    parser.add_argument("--n1", type=int, dest="n1", default = "100", help="Sample 1: Sample Size")
    parser.add_argument("--n2", type=int, dest="n2", default = "100", help="Sample 2: Sample Size")
    parser.add_argument("--m1", type=float, dest="m1", default = "10", help="Sample 1: Mean")
    parser.add_argument("--m2", type=float, dest="m2", default = "10", help="Sample 2: Mean")
    parser.add_argument("--v1", type=float, dest="v1", default = "1", help="Sample 1: Variance")
    parser.add_argument("--v2", type=float, dest="v2", default = "1", help="Sample 2: Variance")
    args = parser.parse_args()  
    return args


def create_random_samples(n,m,v):
    """Create normally-distributed random sample1, with mean m, variance v, and sample size n"""
    sample = np.random.normal(loc=m, scale=v, size=n)

    # Print sample size, and resulting mean/variance
    print("Sample Size = ", n) 
    print("Mean = ", "{:.4f}".format(np.mean(sample)))
    print("Variance = ", "{:.4f}".format(np.var(sample)))  
    return sample


def normality_test(sample, shapiro_alpha):
    """Perform Shapiro-Wilk Test of Normality"""
    shapiro_test_stat, shapiro_p_value = scipy.stats.shapiro(sample)
    if shapiro_p_value > shapiro_alpha:
        print("Fail to reject Null Hypothesis: Sample is from the normal distributions")
        sample_is_normal = True
    else:
        print("Reject Null Hypothesis: Sample is NOT from the normal distributions")
        sample_is_normal = False
    return sample_is_normal


def levene_test(sample1, sample2, levene_alpha):
    """Perform Levene's test for homogeneity of variances"""
    levene_w_stats, levene_p_value = scipy.stats.levene(sample1, sample2, center='mean')
    if levene_p_value > levene_alpha:
        print("Fail to reject Null Hypothesis: Homogeneity of Variances")
        variance_is_similar = True
    else:
        print("Reject Null Hypothesis: No Homogeneity of Variances")
        variance_is_similar = False
    return variance_is_similar


def unpaired_t_test(sample1, sample2, df, p_value_critical):
    """Perform Unpaired t-test"""
    # Calculate t-statistic using scipy
    t_statistic, p_value = scipy.stats.ttest_ind(a=sample1, b=sample2, equal_var=True)
    print("\nCalculation of t-value:")
    print("t-statistic = ", "{:.4f}".format(t_statistic))  

    # Calculate t-critial from given p-value and degrees of freedom
    # Two-tailed test
    t_critical = scipy.stats.t.ppf(q=1-p_value_critical/2,df=df)
    print("\nCalculation of critical t-value:")
    print("At p-value of ", "{:.2f}".format(p_value_critical))
    print("t-critical = ", "{:.4f}".format(t_critical))  

    # Interpretation
    print("\nInterpretation:")
    if t_statistic > t_critical:
        print("Reject H0: There is significant difference in the mean of the two samples")
        reject_h0 = True
    else:
        print("Fail to reject H0: There is NO significant difference in the mean of the two samples")
        reject_h0 = False

    return reject_h0


# Test Functions
def test_create_random_samples():
    """Test creating random normal samples, with sample size of 100, mean of 10.0, and variance of 1.0, then check if resulting random sample actually has 100 samples."""
    assert len(create_random_samples(100,10.0,1.0)) == 100

def test_normality_test():
    """Test creating random normal samples, with sample size of 1000, mean of 10.0, and variance of 1.0, then perform Normality Test. 
    As the sample size is large, we can expect that the resulting samples should approximately normally distributed"""
    assert normality_test(create_random_samples(1000,10.0,1.0), 0.05) == True

def test_levene_test():
    """Test creating two random normal samples, both with sample size of 1000, mean of 10.0, and variance of 1.0, then perform Levene's Test.
    As the sample size of the two samples are large, we can expect that the variance of the two random samples should be similar"""
    assert levene_test(create_random_samples(1000,10.0,1.0), create_random_samples(1000,10.0,1.0), 0.05) == True

def test_unpaired_t_test():
    """Test creating two random normal samples, both with sample size of 1000, mean of 10.0, and variance of 1.0, then perform Unpaired t-test.
    As the sample size of the two samples are large, we can expect that there is NO significant difference in the mean of the two samples (Fail to reject H0)"""
    assert unpaired_t_test(create_random_samples(1000,10.0,1.0), create_random_samples(1000,10.0,1.0), 10000-2, 0.05) == False


def main():
    """Get sample size, mean & variance, create two random samples, then perform unpaired t-test"""
    # Get all user's arguments
    args = get_cli_argument()
    n1 = args.n1
    n2 = args.n2
    m1 = args.m1
    m2 = args.m2
    v1 = args.v1
    v2 = args.v2
    
    # Create normally-distributed random sample1/sample2 based on given sample size, mean, and variance
    print("\nSample 1") 
    sample1 = create_random_samples(n1,m1,v1)
    print("\nSample 2") 
    sample2 = create_random_samples(n2,m2,v2)

    # Calculate degrees of freedom  
    df = min(n1,n2) - 2 

    # Plot histograms of the two samples to see if they are Gaussian-like
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    sns.histplot(data=sample1, bins = 20, ax=axes[0], color='blue') 
    axes[0].set_title('Sample 1 Histogram')

    sns.histplot(data=sample2, bins = 20, ax=axes[1], color='orange') 
    axes[1].set_title('Sample 2 Histogram')

    sns.histplot(data=sample1, bins = 20, ax=axes[2], color='blue') 
    sns.histplot(data=sample2, bins = 20, ax=axes[2], color='orange') 
    axes[2].set_title('Sample 1 (blue) and Sample 2 (orange)')

    fig.suptitle('Histograms of the two samples')
    plt.show()

    # Normality Test: Check Assumption of Normality using Shapiro-Wilk Test of Normality
    print("\nCheck Assumption of Normality:")
    shapiro_alpha = 0.05
    print("Sample 1") 
    sample_is_normal1 = normality_test(sample1, shapiro_alpha)
    print("Sample 2")
    sample_is_normal2 = normality_test(sample2, shapiro_alpha)

    # Levene's Test: Check Assumption of Homogeneity of Variances
    print("\nCheck Assumption of Homogeneity of Variances using Levene's Test:")
    levene_alpha = 0.05
    variance_is_similar = levene_test(sample1, sample2, levene_alpha)

    # Perform unpaired t-test if both samples are approximately normally distributed, and variance are similar
    print("\nUnpaired t-test")
    print("H0 (Null Hypotheses): There is NO significant difference in the mean of the two sample groups")
    print("H1 (Alternative Hypotheses): There is significant difference in the mean of the two sample groups")
    if sample_is_normal1 and sample_is_normal2 and variance_is_similar:
        print("\nBoth samples are approximately normally distributed, and variance are similar.")
        print("Unpaired t-test will then be performed")
        p_value_critical = 0.05
        reject_h0 = unpaired_t_test(sample1, sample2, df, p_value_critical)
    else:
        print("\nAssumptions for the unpaired t-test are not all satisfied.")
        print("Unpaired t-test will NOT be performed")
        if not sample_is_normal1:
            print("Sample 1 is not from the normal distributions")
        if not sample_is_normal2:
            print("Sample 2 is not from the normal distributions")
        if not variance_is_similar:
            print("No Homogeneity of Variances")


if __name__ == '__main__':
	main()






