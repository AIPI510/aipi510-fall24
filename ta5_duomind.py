import numpy as np
import math
from scipy.stats import norm

# Paired sample data
before = np.array([15, 20, 10, 25, 12, 18, 22, 30, 17, 40])
after = np.array([12, 16, 11, 27, 17, 24, 29, 38, 26, 50])

# Step 1: Calculate the differences
differences = after - before

# Step 2: Rank the absolute differences, ignore zero differences
non_zero_diff = differences[differences != 0]  # ignore zero differences
ranks = np.argsort(np.abs(non_zero_diff)) + 1  # Get ranks for absolute differences

# Step 3: Assign ranks their original signs
signed_ranks = np.sign(non_zero_diff) * ranks

# Step 4: Sum the positive and negative ranks
positive_ranks_sum = np.sum(signed_ranks[signed_ranks > 0])
negative_ranks_sum = np.sum(np.abs(signed_ranks[signed_ranks < 0]))

# Step 5: Compute the test statistic W (the smaller of the positive and negative sums)
W = min(positive_ranks_sum, negative_ranks_sum)

# Step 6: Calculate the mean and standard deviation for the test statistic W
n = len(non_zero_diff)
mu_W = n * (n + 1) / 4  # Mean of the W distribution
sigma_W = math.sqrt(n * (n + 1) * (2 * n + 1) / 24)  # Standard deviation of the W distribution

# Step 7: Calculate the z-score
z = (W - mu_W) / sigma_W

# Step 8: Calculate p-value from z-score
p_value = 2 * norm.cdf(z)  # Two-tailed test

# Output the results
print(f"Differences: {differences}\n")
print(f"Ranks: {ranks}\n")
print(f"Signed Ranks: {signed_ranks}\n")
print(f"Positive Ranks Sum: {positive_ranks_sum}\n")
print(f"Negative Ranks Sum: {negative_ranks_sum}\n")
print(f"Test Statistic (W): {W}\n")
print(f"Mean of W: {mu_W}\n")
print(f"Standard Deviation of W: {sigma_W}\n")
print(f"Z-score: {z}\n")
print(f"P-value: {p_value}\n")

# Step 9: Interpretation
alpha = 0.05  # significance level
if p_value < alpha:
    print("Reject the null hypothesis (significant difference).")
else:
    print("Fail to reject the null hypothesis (no significant difference).")