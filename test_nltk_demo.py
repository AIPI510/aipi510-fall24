import pytest
from unittest.mock import patch
import pandas as pd
from io import StringIO
import sys
from nltk_demo import find_sentiment

# Providing mock data for the test
@pytest.fixture
def mock_data():
    return pd.DataFrame({
        'author_id': [1, 2, 3, 4, 5],
        'content': ['I love this!', 'This is terrible.', 'Just okay.', 'Absolutely fantastic!', 'It was an average day']
    })

@patch('nltk_demo.pd.read_csv')
def test_find_sentiment(mock_read_csv, mock_data):

    # Mocking the read_csv function to reference the mock data
    mock_read_csv.return_value = mock_data

    # Redirect stdout to capture print statements
    captured_output = StringIO()
    sys.stdout = captured_output

    # Run the file_sentiment function with a random csv path
    find_sentiment('random_path.csv')

    # Reset to return to its original state
    sys.stdout = sys.__stdout__

    # Check the output contains the sentiment values
    output = captured_output.getvalue()
    assert 'positive' in output
    assert 'negative' in output
    assert 'neutral' in output