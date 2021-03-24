from gpiozero import RGBLED  # TODO Change to RGBLED
import time
import traceback
import yaml
# from EmulatorGUI import GPIO as GPIO
import dateutil.parser as dp
import schedule
# from gpiozero.pins.mock import MockFactory # This line necessary only for PC
import os

# os.environ['GPIOZERO_PIN_FACTORY'] = os.environ.get('GPIOZERO_PIN_FACTORY', 'mock') # This line necessary only for PC

RGB_LED = RGBLED(red=17, green=22, blue=27)  # TODO Move pin numbers to config and also move to separate Class

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
        period_for_each_color = sunrise_duration / len(color_list) / 50  # TODO Remove that before realise.
        for count, value in enumerate(color_list):
            red, green, blue = [round(x / 255, 2) for x in value]
            # RGBLED.value(red, green, blue)  #TODO Uncomment it before RPI upload
            print('red > {0}\ngreen > {1}\nblue > {2}'.format(R_LED, G_LED, B_LED))
            time.sleep(period_for_each_color)
        print('Finished')

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


# schedule.every().day.at(sunrise_start).do(dawn_emulator, 'sunrise')
schedule.every(5).seconds.do(dawn_emulator, 'sunrise')
print('Start script')
while True:
    schedule.run_pending()
    time.sleep(1)
