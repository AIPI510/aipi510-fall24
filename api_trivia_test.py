import pytest
import unittest

def test_results_format_correct():
    """
    Tests that the api calls correctly,
    """
    from api_trivia import call_api
    results = call_api()

    assert( len(results) >= 10 )