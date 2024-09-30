import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt


"""
Coin Flip P-Value Analysis:

This script contains code for simulating coin flips, calculating p-values using different statistical tests, and visualizing the results. 
The analysis focuses on determining whether a coin is fair based on the results of multiple flips.

"""

# Simulating coin flips
def simulate_coin_flips(n_flips=100, prob_head=0.5, seed=42): ## using a random seed of 42, feel free to change this and the accompanying tests.
    np.random.seed(seed)
    flips = np.random.binomial(1, prob_head, n_flips)
    return flips

# Performing statistical tests
def calculate_p_values(n_heads, n_flips, prob_head=0.5):
    # 1. Binomial test
    binom_p_value = stats.binomtest(n_heads, n_flips, prob_head, alternative='two-sided').pvalue

    # 2. Z-test for proportions
    expected_heads = n_flips * prob_head
    standard_error = np.sqrt(n_flips * prob_head * (1 - prob_head))
    z_stat = (n_heads - expected_heads) / standard_error
    z_p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))  # Two-tailed test

    # 3. Chi-square test
    n_tails = n_flips - n_heads
    observed = np.array([n_heads, n_tails])
    expected = np.array([n_flips * prob_head, n_flips * (1 - prob_head)])
    chi2_stat, chi2_p_value = stats.chisquare(observed, expected)

    return binom_p_value, z_p_value, chi2_p_value, z_stat

# Printing the results
def print_p_values(n_heads, n_flips, prob_head, binom_p_value, z_p_value, chi2_p_value):
    observed_proportion_heads = n_heads / n_flips
    print(f"Number of heads: {n_heads}")
    print(f"Observed proportion of heads: {observed_proportion_heads:.2f}")
    print("\n--- P-values from different tests ---")
    print(f"Binomial Test P-value: {binom_p_value:.4f}")
    print(f"Z-Test P-value: {z_p_value:.4f}")
    print(f"Chi-Square Test P-value: {chi2_p_value:.4f}")

# Checking hypothesis rejection
def check_hypothesis(binom_p_value, alpha=0.05):
    if binom_p_value < alpha:
        return "Reject H₀, coin may not be fair."
    else:
        return "Fail to reject H₀, coin is likely fair."

# Plotting results of coin flips
def plot_flips(flips, n_heads, n_tails):
    sns.histplot(flips, discrete=True, binwidth=1, kde=False)
    plt.xticks([0, 1], ["Tails", "Heads"])
    plt.title(f"Coin Flip Results: {n_heads} Heads, {n_tails} Tails")
    plt.xlabel("Outcome")
    plt.ylabel("Count")
    plt.show()

# Plotting p-value visualization for Z-Test
def plot_p_value_ztest(z_stat):
    x = np.linspace(-3, 3, 1000)
    y = stats.norm.pdf(x, 0, 1)

    plt.plot(x, y, label="Standard Normal Distribution")
    plt.fill_between(x, 0, y, where=(x >= abs(z_stat)), color='red', alpha=0.3, label="Rejection Region")
    plt.fill_between(x, 0, y, where=(x <= -abs(z_stat)), color='red', alpha=0.3)
    plt.axvline(x=z_stat, color='blue', linestyle='--', label=f"Observed Z = {z_stat:.2f}")
    plt.title("P-value Visualization (Z-Test)")
    plt.legend()
    plt.show()

# Main function
def main():
    n_flips = 100
    prob_head = 0.5

    # Simulating coin flips
    flips = simulate_coin_flips(n_flips, prob_head)
    n_heads = np.sum(flips)
    n_tails = n_flips - n_heads

    # Calculating p-values
    binom_p_value, z_p_value, chi2_p_value, z_stat = calculate_p_values(n_heads, n_flips, prob_head)

    # Printing results
    print_p_values(n_heads, n_flips, prob_head, binom_p_value, z_p_value, chi2_p_value)

    # Checking hypothesis
    hypothesis_result = check_hypothesis(binom_p_value)
    print(f"\nBinomial Test: {hypothesis_result}")

    # Ploting flips and p-value visualizations
    plot_flips(flips, n_heads, n_tails)
    plot_p_value_ztest(z_stat)

if __name__ == "__main__":
    main()
