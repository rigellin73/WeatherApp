from __future__ import print_function
import weatherapi
from weatherapi.rest import ApiException
from pprint import pprint
import yaml
from datetime import date

import requests

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def get_location_city():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    return response.get("city")

# Read config file
config = yaml.safe_load(open("../config.yml"))

# Configure API key authorization: ApiKeyAuth
configuration = weatherapi.Configuration()
configuration.api_key['key'] = config['key']
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'

# create an instance of the API class
api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))

# get location

q = get_location_city() # str | Pass US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude (decimal degree) or city name. Visit [request parameter section](https://www.weatherapi.com/docs/#intro-request) to learn more.

# get current date
dt = date.today().strftime("%y-%m-%d") # date | Date on or after 1st Jan, 2015 in yyyy-MM-dd format

try:
    # Astronomy API
    api_response = api_instance.astronomy(q, dt)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling APIsApi->astronomy: %s\n" % e)
