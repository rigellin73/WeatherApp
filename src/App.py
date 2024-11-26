from __future__ import print_function
import weatherapi
from weatherapi.rest import ApiException
from pprint import pprint
import yaml
import tkinter as tk
from tkinter import ttk

import requests


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


def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def get_location_city():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    return response.get("city")


def create_weather_entries(content_frame, weather_info_dict):
    # create result as a table
    for index, key in enumerate(weather_info_dict):
        key_entry = tk.Entry(content_frame, width=20, fg='blue', font=('Arial', 16, 'bold'))
        value_entry = tk.Entry(content_frame, width=20, fg='blue', font=('Arial', 16, 'bold'))
        key_entry.grid(row=index, column=0)
        value_entry.grid(row=index, column=1)
        key_entry.insert(tk.END, key)
        value_entry.insert(tk.END, weather_info_dict[key])


def create_window_content(window, api_response):

    # Step 3: Create a Frame for Grid Layout
    frame = ttk.Frame(window)
    frame.grid(row=0, column=0, sticky="nsew")

    # Step 4: Create a Canvas and Scrollbar
    canvas = tk.Canvas(frame)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Step 5: Create a Frame for Scrollable Content
    content_frame = ttk.Frame(canvas)

    # Step 6: Configure the Canvas and Scrollable Content Frame
    content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    create_weather_entries(content_frame, api_response)

    # Step 8: Create Window Resizing Configuration
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    # Step 9: Pack Widgets onto the Window
    canvas.create_window((0, 0), window=content_frame, anchor="nw")
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Step 10: Bind the Canvas to Mousewheel Events
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)


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
