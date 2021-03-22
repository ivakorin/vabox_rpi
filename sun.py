import yaml
import datetime
import requests
import json


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

    def get_sun_data(self):
        result = {}
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        geocode = self.__get_geocode()
        url = '{0}lat={1}&lng={2}&date={3}&formatted=0'.format(self.url, geocode.get('lat'), geocode.get('lng'), today)
        try:
            r = requests.get(url).json()
            for k, v in r.items():
                if k == 'results':
                    for desc, data in v.items():
                        try:
                            '''
                            Меняю двоеточие у таймзоны, так как иначе питон не даёт преобразовать в timestamp 
                            '''
                            d = data.replace('+00:00', '+0000')
                        except AttributeError:
                            d = data
                        result[desc] = d
            return result

        except ConnectionError:
            return False
