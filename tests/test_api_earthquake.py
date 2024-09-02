import argparse
import requests
from api_earthquake import get_earthquake_data, get_latlong_from_zipcode, is_validate_date, distill_earthquake_data

def test_version_response():
    resp = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/version")
    assert resp.status_code == 200

def test_get_latlong_from_zipcode():
    lat, long = get_latlong_from_zipcode("29401")
    assert lat == 32.7795
    assert long == -79.9371

def test_is_valid_date():
    assert is_validate_date("2024-01-01")
    assert not is_validate_date("2024-13-01")
    assert not is_validate_date("2024-01-32")
    assert not is_validate_date("2024/02/30")

def test_get_earthquake_data():
    args = argparse.Namespace(zipcode=29401,
                              radius=200,
                              startdate="2024-01-01",
                              enddate="2024-06-01",
                              minmagnitude=2,
                              maxmagnitude=2.2)

    earthquake_json = get_earthquake_data(args)
    assert len(earthquake_json["features"]) == 2
    assert earthquake_json["features"][0]["properties"]["mag"] == 2.16

def test_distill_earthquake_data():
    args = argparse.Namespace(zipcode=29401,
                              radius=200,
                              startdate="2024-01-01",
                              enddate="2024-06-01",
                              minmagnitude=2,
                              maxmagnitude=2.2)

    earthquake_json = get_earthquake_data(args)
    earthquakes = distill_earthquake_data(earthquake_json)
    assert len(earthquakes) == 2
    assert earthquakes[0].magnitude == 2.16
    assert earthquakes[1].magnitude == 2.19
