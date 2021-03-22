import time
import traceback
import yaml
from EmulatorGUI import GPIO as GPIO
# import RPi.GPIO as GPIO
import dateutil.parser as dp

from sun import SunriseSunet

s = SunriseSunet()
d = s.get_sun_data()
import datetime
parsed_t = dp.parse(d['sunrise'])
t_in_seconds = parsed_t.strftime('%s')
print(t_in_seconds)