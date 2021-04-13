# from gpiozero import RGBLED, PWMLED
import time
import traceback
import yaml
import schedule
from datetime import datetime as dt, timedelta

# RGB_LED = RGBLED(red=17, green=22, blue=27)  # TODO Move pin numbers to config and also move to separate Class
# LED = PWMLED()

from sun import SunriseSunet
from lights import LightsControl


def get_conf_data(data: str):
    with open('config.yaml', 'r') as stream:
        d = yaml.load(stream, Loader=yaml.Loader)
    result = d.get(data)
    return result

color_list = get_conf_data('light_color_list')
lights = LightsControl(color_list)

geocode_data = get_conf_data('geocode')
geocode = {}
for gc in geocode_data:
    for k, v in gc.items():
        geocode[k] = v
s = SunriseSunet(longitude=geocode['longitude'], latitude=geocode['latitude'])
sunrise_start = s.sunrise_start(dt.now())
sunset_start = s.sunset_start(dt.now())
current_time = dt.now().strftime('%H:%M:%S')
if sunrise_start < current_time < sunset_start:
    lights.main_light()
    duration = s.sunset_duration(dt.now())
    schedule.every().day.at(sunset_start).do(lights.dawn_emulator, 'sunset', duration)
elif sunset_start < current_time or current_time < sunrise_start:
    date = dt.now()+timedelta(days=1)
    sunrise_start = s.sunrise_start(date)
    duration = s.sunrise_duration(date)
    schedule.every().day.at(sunrise_start).do(lights.dawn_emulator, 'sunrise', duration)
    print('Hold on until sunrise')


# duration = s.sunrise_duration(dt.now())
# schedule.every().day.at(sunrise_start).do(dawn_emulator, 'sunrise')
# schedule.every(5).seconds.do(lights.dawn_emulator, 'sunrise', duration)
print('Start script')
while True:
    schedule.run_pending()
    time.sleep(1)
