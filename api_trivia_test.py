import pytest
import unittest
import pandas as pd

# Parameterized test can only have one test case
# Repeated API calls within a period of 5 seconds will reject the API call
#   due to restrictions
@pytest.mark.parametrize('args, expected_number_of_questions', [
                        (['-n', '20'], 20)])
def test_results_format_correct(args, expected_number_of_questions):
    """
    Tests that the api calls correctly,
    """
    from api_trivia import call_api, parse_args
    arguments = parse_args(args)
    results = call_api(arguments)

    assert( len(results) == expected_number_of_questions )


@pytest.mark.parametrize('args, expected_number_of_questions', [
                        (['-n', '25'], 25)])
def test_results_downloaded_correctly(args, expected_number_of_questions):
    """
    Tests that the api calls correctly,
    """
    # To delay the request, so that the next request is valid
    import time
    time.sleep(5.1)
    
    from api_trivia import call_api, parse_args, save_df_to_csv, make_dataframe
    arguments = parse_args(args)
    results = call_api(arguments)
    save_df_to_csv(make_dataframe(results), "test_questions.csv")

    df = pd.read_csv("test_questions.csv")
    assert(df.shape[0] == expected_number_of_questions)

    assert( len(results) == expected_number_of_questions )