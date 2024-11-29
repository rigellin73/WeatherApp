from __future__ import print_function
import weatherapi
from weatherapi.rest import ApiException
from pprint import pprint
import yaml
import tkinter as tk
from ui.weather_app_ui import create_window_content
from api.weather_app_api import get_location_city


test_response = {'cloud': 75,
 'condition': {'code': 1003,
               'icon': '//cdn.weatherapi.com/weather/64x64/night/116.png',
               'text': 'Partly cloudy'},
 'dewpoint_c': 5.6,
 'dewpoint_f': 42.1,
 'feelslike_c': 3.9,
 'feelslike_f': 39.0,
 'gust_kph': 49.9,
 'gust_mph': 31.0,
 'heatindex_c': 7.7,
 'heatindex_f': 45.9,
 'humidity': 81,
 'is_day': 0,
 'last_updated': '2024-11-26 17:15',
 'last_updated_epoch': 1732637700,
 'precip_in': 0.0,
 'precip_mm': 0.01,
 'pressure_in': 29.91,
 'pressure_mb': 1013.0,
 'temp_c': 8.1,
 'temp_f': 46.6,
 'uv': 0.0,
 'vis_km': 10.0,
 'vis_miles': 6.0,
 'wind_degree': 232,
 'wind_dir': 'SW',
 'wind_kph': 32.8,
 'wind_mph': 20.4,
 'windchill_c': 3.4,
 'windchill_f': 38.1}


def get_weather_info_from_response(api_response):
    response_fields_dict = {
        'temp_c': 'Temperature',
        'feelslike_c': 'Feels like',
        'humidity': 'Humidity',
        'wind_dir': 'Wind direction',
        'wind_kph': 'Wind speed'
    }
    weather_info = dict()
    weather_info['Condition'] = api_response['condition']['text']
    for key, value in response_fields_dict.items():
        weather_info[value] = api_response[key]
    return weather_info


# Read config file
config = yaml.safe_load(open("../config/config.yml"))

# Configure API key authorization: ApiKeyAuth
configuration = weatherapi.Configuration()
configuration.api_key['key'] = config['key']
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'

# create an instance of the API class
api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))

# get location

#ip_location_city = get_location_city() # str | Pass US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude (decimal degree) or city name.
ip_location_city = "Malmo"

try:
    #api_realtime_response = api_instance.realtime_weather(ip_location_city)
    #pprint(api_realtime_response['current'])
    #weather_info_dict = get_weather_info_from_response(api_realtime_response["current"])
    weather_info_dict = get_weather_info_from_response(test_response)

    # create a root window.
    main_window = tk.Tk()
    main_window.title("Current weather")
    # Define the size of the window.
    main_window.geometry("500x750")
    create_window_content(main_window, weather_info_dict)
    main_window.mainloop()

except ApiException as e:
    print("Exception when calling APIsApi->realtime_weather: %s\n" % e)
