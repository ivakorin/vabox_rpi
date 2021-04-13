import time
import schedule


class LightsControl:
    def __init__(self, colors):
        self.colors = colors

    def dawn_emulator(self, scene: str, duration):
        """
        :param duration: Продолжителдьность заката или рассвета
        :param scene: Закат или рассвет
        :return:
        """
        color_list = self.colors
        try:
            if scene == 'sunrise':

                period_for_each_color = duration / len(color_list) / 200 #TODO Must be removed
                for count, value in enumerate(color_list):
                    red = value['R']
                    green = value['G']
                    blue = value['B']
                    print('Red value is {0}\nGreen value is {1}\nBlue value is {2}'.format(red, green, blue))
                    time.sleep(period_for_each_color)
                #  Разжигаем светодиод на 6000к и гасим RGB
                print('Finished')
            elif scene == 'sunset':
                period_for_each_color = duration / len(color_list)
                for count, value in enumerate(reversed(color_list)):
                    print(count, '>', value)
                    print('sleep for:', period_for_each_color)
                    time.sleep(period_for_each_color)
            return schedule.CancelJob
        except:
            raise SystemExit('Scene must be "sunrise" or "sunset"!')

    def main_light(self):
        return True

