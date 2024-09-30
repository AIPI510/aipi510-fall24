import pytest
from p_values import simulate_coin_flips, calculate_p_values, check_hypothesis

"""
    Since I'm using a specific example simulation, I can logically only test for those exact values. 
    Feel free to change this when you work with a different random seed.
"""

def test_simulate_coin_flips():
    flips = simulate_coin_flips(n_flips=100, prob_head=0.5, seed=42)
    assert len(flips) == 100, "Number of flips should be 100"
    assert sum(flips) == 47, "Number of heads should be 47 (with seed 42)"
    assert sum(flips == 0) == 53, "Number of tails should be 53"

def test_calculate_p_values():
    n_heads = 47
    n_flips = 100
    prob_head = 0.5
    binom_p_value, z_p_value, chi2_p_value, z_stat = calculate_p_values(n_heads, n_flips, prob_head)

    # Checking binomial test p-value
    assert pytest.approx(binom_p_value, 0.0001) == 0.6173, "Binomial test p-value is incorrect"
    
    # Checking z-test p-value
    assert pytest.approx(z_p_value, 0.0001) == 0.5485, "Z-test p-value is incorrect"
    
    # Checking chi-square test p-value
    assert pytest.approx(chi2_p_value, 0.0001) == 0.5485, "Chi-square test p-value is incorrect"

def test_check_hypothesis():
    """
    I'm using just the binomial test for this 
    """
    # Failing to reject null hypothesis (coin likely fair)
    binom_p_value = 0.6173
    result = check_hypothesis(binom_p_value)
    assert result == "Fail to reject H₀, coin is likely fair."

    # Rejecting null hypothesis (coin may not be fair)
    binom_p_value = 0.03
    result = check_hypothesis(binom_p_value)
    assert result == "Reject H₀, coin may not be fair."
