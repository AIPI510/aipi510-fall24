import weather

def test_resolve_location(): 
    geo = weather.IPGeo()
    assert(geo.data['status'] == 'success')

def test_get_forecast(): 
    geo = weather.IPGeo()
    forecast = weather.Forecast()
    forecast.resolve_location(geo.lat, geo.lon) 
    assert(type(forecast.forecast_url) is str)
    assert(type(forecast.station) is str)
    assert(type(forecast.location) is str)
    
    forecast.update_forecast()
    assert(type(forecast.forecast) is list)

def test_get_precipitation(): 
    p = weather.Precipitation()
    p.update_precipitation('27603', 2)

    assert(type(p.precip) is list)