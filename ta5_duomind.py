import numpy as np
import math

# Paired sample data
before = np.array([50, 60, 55, 68, 52, 62, 58, 65])
after = np.array([54, 63, 60, 60, 54, 63, 55, 60])

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
from scipy.stats import norm
p_value = 2 * norm.cdf(z)  # Two-tailed test

# Output the results
print(f"Differences: {differences}")
print(f"Ranks: {ranks}")
print(f"Signed Ranks: {signed_ranks}")
print(f"Positive Ranks Sum: {positive_ranks_sum}")
print(f"Negative Ranks Sum: {negative_ranks_sum}")
print(f"Test Statistic (W): {W}")
print(f"Mean of W: {mu_W}")
print(f"Standard Deviation of W: {sigma_W}")
print(f"Z-score: {z}")
print(f"P-value: {p_value}")

# Step 9: Interpretation
alpha = 0.05  # significance level
if p_value < alpha:
    print("Reject the null hypothesis (significant difference).")
else:
    print("Fail to reject the null hypothesis (no significant difference).")