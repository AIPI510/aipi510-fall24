import requests
import unittest
from unittest.mock import patch

def fetch_league_info(league_id):
    """
    Fetch league information from Sleeper API.
    
    Args:
        league_id (str): The unique identifier for the Sleeper league.
    
    Returns:
        dict: League data returned from the API, or None if the request fails.
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for 4XX/5XX responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching league data: {e}")
        return None

def display_league_info(league_data):
    """
    Display basic league information.
    
    Args:
        league_data (dict): League data obtained from the Sleeper API.
    """
    if league_data:
        print(f"League Name: {league_data.get('name')}")
        print(f"Number of Teams: {league_data.get('total_rosters')}")
        print(f"Draft Status: {league_data.get('status')}")
    else:
        print("No league data to display.")

class TestSleeperAPI(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_league_info_success(self, mock_get):
        """Test successful API call to fetch league info."""
        mock_response = {
            "name": "Test League",
            "total_rosters": 10,
            "status": "drafting"
        }
        mock_get.return_value.json.return_value = mock_response

        league_id = '12345'
        league_data = fetch_league_info(league_id)

        self.assertIsNotNone(league_data)
        self.assertEqual(league_data['name'], 'Test League')
        self.assertEqual(league_data['total_rosters'], 10)
        self.assertEqual(league_data['status'], 'drafting')

    @patch('requests.get')
    def test_fetch_league_info_failure(self, mock_get):
        """Test API call failure due to network error."""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        league_id = '12345'
        league_data = fetch_league_info(league_id)

        self.assertIsNone(league_data)

    def test_display_league_info(self):
        """Test display_league_info function output."""
        league_data = {
            "name": "Test League",
            "total_rosters": 10,
            "status": "drafting"
        }

        with patch('builtins.print') as mock_print:
            display_league_info(league_data)

            mock_print.assert_any_call("League Name: Test League")
            mock_print.assert_any_call("Number of Teams: 10")
            mock_print.assert_any_call("Draft Status: drafting")

    def test_display_league_info_no_data(self):
        """Test display_league_info function when no data is passed."""
        with patch('builtins.print') as mock_print:
            display_league_info(None)

            mock_print.assert_called_once_with("No league data to display.")

if __name__ == "__main__":
    league_id = 28964632850438553
    league_data = fetch_league_info(league_id)
    display_league_info(league_data)

    # Run unit tests
    unittest.main(argv=[''], exit=False)
