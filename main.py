import time
import traceback
import yaml
# from EmulatorGUI import GPIO as GPIO
# import RPi.GPIO as GPIO
import dateutil.parser as dp
import schedule

from sun import SunriseSunet

s = SunriseSunet()
sunrise_start = s.sunrise_start()


def get_light_color():
    with open('config.yaml', 'r') as stream:
        color_list = yaml.load(stream, Loader=yaml.Loader)
    color_list = color_list.get('light_color_list')
    result = color_list
    return result


def dawn_emulator(scene: str):
    """
    :param scene:
    :return:
    """
    if scene == 'sunrise':
        sunrise_duration = s.sunrise_duration()
        color_list = get_light_color()
        period_for_each_color = sunrise_duration / len(color_list)
        for count, value in enumerate(color_list):
            print(value)
            print('sleep for:', period_for_each_color)
            time.sleep(period_for_each_color)
        sunset_start = s.sunset_start()
        schedule.every().day.at(sunset_start).do(dawn_emulator, 'sunset')
        return schedule.CancelJob
    elif scene == 'sunset':
        sunset_duration = s.sunset_duration()
        color_list = get_light_color()
        period_for_each_color = sunset_duration / len(color_list)
        for count, value in enumerate(reversed(color_list)):
            print(count, '>', value)
            print('sleep for:', period_for_each_color)
            time.sleep(period_for_each_color)
        return schedule.CancelJob
    else:
        raise SystemExit('Scene must be "sunrise" or "sunset"!')


schedule.every().day.at(sunrise_start).do(dawn_emulator, 'sunrise')
while True:
    schedule.run_pending()
    time.sleep(1)
