import pytest
from unittest.mock import patch
import io
from ta5_code_demo import simpsons_paradox_demo

# Helper function to capture printed output
def run_demo_with_inputs(inputs):
    with patch('builtins.input', side_effect=inputs):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            simpsons_paradox_demo()
            return fake_out.getvalue()

# Test cases for different user inputs
def test_demo_user_thinks_drug_effective_from_start():
    inputs = ['yes', 'yes', 'no']  # User thinks drug is effective from the start
    output = run_demo_with_inputs(inputs)
    
    # Check for expected output at various steps
    assert "You seem confident about the drug's effectiveness" in output
    assert "The aggregated data suggests that the drug is 10% more effective" in output
    assert "Surprising, right?" in output
    assert "changed your mind after seeing the disaggregated data" in output

def test_demo_user_skeptical_from_start():
    inputs = ['no', 'no', 'no']  # User is skeptical from the start
    output = run_demo_with_inputs(inputs)
    
    # Check for expected output at various steps
    assert "You're skeptical about the drug." in output
    assert "You still don't believe in the drug's effectiveness" in output
    assert "It looks like your skepticism was justified!" in output

def test_demo_user_unsure_from_start():
    inputs = ['', '', 'yes']  # User is unsure, then changes opinion
    output = run_demo_with_inputs(inputs)
    
    # Check for expected output at various steps
    assert "I'll assume you are unsure. Let's analyze the data together." in output
    assert "It seems like you're still unsure." in output
    assert "Interesting! Despite the subgroup analysis, you still believe the drug is effective." in output

def test_demo_user_changes_mind():
    inputs = ['yes', 'yes', 'no']  # User initially believes drug is effective, then changes mind
    output = run_demo_with_inputs(inputs)
    
    # Check for expected output at various steps
    assert "You seem confident about the drug's effectiveness" in output
    assert "Despite initially thinking the drug was effective based on the aggregated data" in output
    assert "It seems you've changed your mind after seeing the disaggregated data." in output
