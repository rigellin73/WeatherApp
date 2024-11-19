from __future__ import print_function
import weatherapi
from weatherapi.rest import ApiException
from pprint import pprint
import yaml
import tkinter as tk

import requests

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def get_location_city():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    return response.get("city")

def show_weather(window, api_response):
    pprint(api_response)

    # create result as a table
    for index, key in enumerate(api_response):
        key_entry = tk.Entry(window, width=20, fg='blue', font=('Arial', 16, 'bold'))
        value_entry = tk.Entry(window, width=20, fg='blue', font=('Arial', 16, 'bold'))
        key_entry.grid(row=index, column=0)
        value_entry.grid(row=index, column=1)
        key_entry.insert(tk.END, key)
        value_entry.insert(tk.END, api_response[key])


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
    api_realtime_response = api_instance.realtime_weather(ip_location_city)

    # create a root window.
    main_window = tk.Tk()
    main_window.title("Current weather")
    # Define the size of the window.
    main_window.geometry("500x750")
    show_weather(main_window, api_realtime_response["current"])
    main_window.mainloop()

except ApiException as e:
    print("Exception when calling APIsApi->realtime_weather: %s\n" % e)
