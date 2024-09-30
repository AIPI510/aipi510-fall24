import pytest
import seaborn as sns
import numpy as np
from p_values import perform_t_test, perform_anova, perform_chi_square, perform_logistic_regression

# Fixture for loading the Titanic dataset
@pytest.fixture
def titanic_df():
    return sns.load_dataset("titanic").dropna(subset=['age', 'fare'])

def test_t_test(titanic_df):
    t_stat, p_value = perform_t_test(titanic_df)
    # Check if p-value and t-stat are floats
    assert isinstance(t_stat, float)
    assert isinstance(p_value, float)
    # p-value should be between 0 and 1
    assert 0 <= p_value <= 1

def test_anova(titanic_df):
    f_stat, p_value = perform_anova(titanic_df)
    # Check if F-statistic and p-value are floats
    assert isinstance(f_stat, float)
    assert isinstance(p_value, float)
    # p-value should be between 0 and 1
    assert 0 <= p_value <= 1

def test_chi_square(titanic_df):
    chi2_stat, p_value = perform_chi_square(titanic_df)
    # Check if chi-square statistic and p-value are floats
    assert isinstance(chi2_stat, float)
    assert isinstance(p_value, float)
    # p-value should be between 0 and 1
    assert 0 <= p_value <= 1

def test_logistic_regression(titanic_df):
    fpr, tpr, roc_auc = perform_logistic_regression(titanic_df)
    # Check if ROC AUC score is a float
    assert isinstance(roc_auc, float)
    # Check if false positive rate and true positive rate are numpy arrays
    assert isinstance(fpr, np.ndarray)
    assert isinstance(tpr, np.ndarray)
    # ROC AUC should be between 0 and 1
    assert 0 <= roc_auc <= 1
