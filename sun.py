import yaml
from pysolar.solar import *
import datetime
from datetime import datetime as dt
from datetime import timedelta
from pysolar.util2 import get_sunrise_sunset_transit
import pytz
import time

SUN_ZENITH_SUNRISE_SUNSET = 0  # Sunrise sunset
SUN_ZENITH_CIVIL_TWILIGHT = 1  # Civil twilight's
SUN_ZENITH_NAUTICAL_TWILIGHT = 2  # Nautical twilight's
SUN_ZENITH_ASTRO_TWILIGHT = 3  # Astronomical twilight's


class SunriseSunet:
    def __init__(self):
        # "https://api.sunrise-sunset.org/json?lat=" + config['lat'] + "&lng=" + config[
        #                 'lng'] + "&date=" + today + "&formatted=0"
        self.url = 'https://api.sunrise-sunset.org/json?'

    def __get_geocode(self):
        result = {}
        with open('config.yaml', 'r') as stream:
            config = yaml.load(stream, Loader=yaml.Loader)
        gc = config.get('geocode')
        for key in gc:
            for k, v in key.items():
                result[k] = v
        return result

    #
    # def get_sun_data(self):
    #     result = {}
    #     today = datetime.datetime.today().strftime('%Y-%m-%d')
    #     geocode = self.__get_geocode()
    #     url = '{0}lat={1}&lng={2}&date={3}&formatted=0'.format(self.url, geocode.get('lat'), geocode.get('lng'), today)
    #     try:
    #         r = requests.get(url).json()
    #         for k, v in r.items():
    #             if k == 'results':
    #                 for desc, data in v.items():
    #                     try:
    #                         '''
    #                         Меняю двоеточие у таймзоны, так как иначе питон не даёт преобразовать в timestamp
    #                         '''
    #                         d = data.replace('+00:00', '+0000')
    #                     except AttributeError:
    #                         d = data
    #                     result[desc] = d
    #         return result
    #
    #     except ConnectionError:
    #         return False
    def sunrise_duration(self):
        geocode = self.__get_geocode()
        longitude = geocode['longitude']
        latitude = geocode['latitude']
        date = dt.now()
        tz = pytz.timezone('UTC')
        date = date.replace(tzinfo=tz)
        sunrise, sunset, transit = get_sunrise_sunset_transit(latitude, longitude, date, SUN_ZENITH_ASTRO_TWILIGHT)
        astro_sunrise_timestamp = int(time.mktime(sunrise.timetuple()))

        sunrise, sunset, transit = get_sunrise_sunset_transit(latitude, longitude, date, SUN_ZENITH_CIVIL_TWILIGHT)
        civil_sunrise_timestamp = int(time.mktime(sunrise.timetuple()))
        sec = civil_sunrise_timestamp - astro_sunrise_timestamp
        return sec

    def sunset_duration(self):
        geocode = self.__get_geocode()
        longitude = geocode['longitude']
        latitude = geocode['latitude']
        date = dt.now()
        tz = pytz.timezone('UTC')
        date = date.replace(tzinfo=tz)
        sunrise, sunset, transit = get_sunrise_sunset_transit(latitude, longitude, date, SUN_ZENITH_ASTRO_TWILIGHT)
        astro_sunset_timestamp = int(time.mktime(sunrise.timetuple()))

        sunrise, sunset, transit = get_sunrise_sunset_transit(latitude, longitude, date, SUN_ZENITH_CIVIL_TWILIGHT)
        civil_sunset_timestamp = int(time.mktime(sunrise.timetuple()))
        sec = civil_sunset_timestamp - astro_sunset_timestamp
        return sec

    def sunrise_start(self):
        geocode = self.__get_geocode()
        longitude = geocode['longitude']
        latitude = geocode['latitude']
        date = dt.now()
        tz = pytz.timezone('UTC')
        date = date.replace(tzinfo=tz)
        sunrise, sunset, transit = get_sunrise_sunset_transit(latitude, longitude, date, SUN_ZENITH_ASTRO_TWILIGHT)
        result = sunrise.strftime('%H:%M:%S')
        return result

    def sunset_start(self):
        geocode = self.__get_geocode()
        longitude = geocode['longitude']
        latitude = geocode['latitude']
        date = dt.now()
        tz = pytz.timezone('UTC')
        date = date.replace(tzinfo=tz)
        sunrise, sunset, transit = get_sunrise_sunset_transit(latitude, longitude, date, SUN_ZENITH_CIVIL_TWILIGHT)
        result = sunset.strftime('%H:%M:%S')
        return result

    def sun_altitude(self):
        geocode = self.__get_geocode()
        date = dt.now()
        tz = pytz.timezone('UTC')
        date = date.replace(tzinfo=tz)
        a = get_altitude(longitude_deg=geocode['lng'], latitude_deg=geocode['lat'], when=date, elevation=18)
        print(a)
