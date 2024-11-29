import requests
import logging
import weatherapi
import yaml

logger = logging.getLogger(__name__)


def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def get_location_city():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    return response.get("city")


def get_weather_api_instance():
    # TODO: read key from env, do not store it in config file
    # Read WeatherAPI key from config file
    weather_api_key_path = "../config/weather_api_key.yml"
    logger.info(f"Reading config file {weather_api_key_path}")
    weather_api_key = yaml.safe_load(open(weather_api_key_path))

    # Configure API key authorization: ApiKeyAuth
    weather_api_config = weatherapi.Configuration()
    weather_api_config.api_key['key'] = weather_api_key['key']

    # create an instance of the API class
    return weatherapi.APIsApi(weatherapi.ApiClient(weather_api_config))


def get_realtime_weather(weather_api_instance, location):
    return weather_api_instance.realtime_weather(location)