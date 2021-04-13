from pysolar.util2 import get_sunrise_sunset_transit
import pytz
import time

SUN_ZENITH_SUNRISE_SUNSET = 0  # Sunrise sunset
SUN_ZENITH_CIVIL_TWILIGHT = 1  # Civil twilight's
SUN_ZENITH_NAUTICAL_TWILIGHT = 2  # Nautical twilight's
SUN_ZENITH_ASTRO_TWILIGHT = 3  # Astronomical twilight's


class SunriseSunet:
    def __init__(self, longitude, latitude, tz='UTC'):
        """

        :param longitude: Долгота
        :param latitude: Широта
        :param tz: Временная зона для которой происходит расчёт по умолчанию UTC
        """
        self.longitude = longitude
        self.latitude = latitude
        self.tz = pytz.timezone(tz)

    def sunrise_duration(self, date):
        """
        :return: Возвращает длительность рассвета от астронамического рассвета до гражданского рассвета в секундах
        :param date: Дата для расчёта
        """
        date = date.replace(tzinfo=self.tz)
        sunrise, sunset, transit = get_sunrise_sunset_transit(self.latitude, self.longitude, date,
                                                              SUN_ZENITH_ASTRO_TWILIGHT)
        astro_sunrise_timestamp = int(time.mktime(sunrise.timetuple()))
        sunrise, sunset, transit = get_sunrise_sunset_transit(self.latitude, self.longitude, date,
                                                              SUN_ZENITH_CIVIL_TWILIGHT)
        civil_sunrise_timestamp = int(time.mktime(sunrise.timetuple()))
        sec = civil_sunrise_timestamp - astro_sunrise_timestamp
        return sec

    def sunset_duration(self, date):
        """
        :return: Возвращает длительность заката от гражданского заката до астронамического заката в секундах
        :param date: Дата для расчёта
        """
        date = date.replace(tzinfo=self.tz)
        sunrise, sunset, transit = get_sunrise_sunset_transit(self.latitude, self.longitude, date,
                                                              SUN_ZENITH_ASTRO_TWILIGHT)
        astro_sunset_timestamp = int(time.mktime(sunrise.timetuple()))
        sunrise, sunset, transit = get_sunrise_sunset_transit(self.latitude, self.longitude, date,
                                                              SUN_ZENITH_CIVIL_TWILIGHT)
        civil_sunset_timestamp = int(time.mktime(sunrise.timetuple()))
        sec = civil_sunset_timestamp - astro_sunset_timestamp
        return sec

    def sunrise_start(self, date):
        """
        :return: Возвращает время начала астрономического рассвета в формате H:M:S
        :param date: Дата для расчёта
        """
        date = date.replace(tzinfo=self.tz)
        sunrise, sunset, transit = get_sunrise_sunset_transit(self.latitude, self.longitude, date,
                                                              SUN_ZENITH_ASTRO_TWILIGHT)
        result = sunrise.strftime('%H:%M:%S')
        return result

    def sunset_start(self, date):
        """
        :return: Возвращает время начала гражданского заката в формате H:M:S
        :param date: Дата для расчёта
        """
        date = date.replace(tzinfo=self.tz)
        sunrise, sunset, transit = get_sunrise_sunset_transit(self.latitude, self.longitude, date,
                                                              SUN_ZENITH_CIVIL_TWILIGHT)
        result = sunset.strftime('%H:%M:%S')
        return result
