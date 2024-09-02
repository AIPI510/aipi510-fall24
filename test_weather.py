import nws_api

def test_resolve_location(): 
    geo = nws_api.IPGeo()
    assert(geo.data['status'] == 'success')

def test_get_forecast(): 
    geo = nws_api.IPGeo()
    forecast = nws_api.Forecast()
    forecast.resolve_location(geo.lat, geo.lon) 
    assert(type(forecast.forecast_url) is str)
    assert(type(forecast.office) is str)
    assert(type(forecast.location) is str)
    
    forecast.update_forecast()
    assert(type(forecast.forecast) is list)