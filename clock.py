from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.graphics import Color, Line
import time
import math

class interface(FloatLayout):
    def __init__(self, **kwargs):
        super(interface, self).__init__(**kwargs)

        self.sec_hand_len = 100
        self.min_hand_len = 100
        self.hour_hand_len = 50
        self.seconds = time.time() % 60
        self.minutes = (time.time() / 60) % 60
        self.hours = (time.time() / 3600) % 24

        self.sec_hand_width = 1.5
        self.min_hand_width = 3
        self.hour_hand_width = 6

        with self.canvas:
            self.clock_face = Image(source = 'clock_face.jpg')
            self.add_widget(self.clock_face)


    def update(self, var):

        self.seconds = int(time.time() % 60)
        self.minutes = int((time.time() / 60) % 60)
        self.hours = int(((time.time() / 3600) + 8) % 24)
        sec_angle = (math.pi / 2.0) - ((math.pi * self.seconds) / 30.0)
        min_angle = (math.pi / 2.0) - ((math.pi * self.minutes) / 30.0) - ((math.pi * self.seconds) / 1800.0)
        hour_angle = (math.pi / 2.0) - ((math.pi * (self.hours % 12)) / 6.0) - ((math.pi / 360.0) * self.minutes)


        with self.canvas:

            self.canvas.clear()

            Color(0, 0, 0)

            Line(points = [self.center_x, self.center_y,
                                         self.center_x + self.sec_hand_len * math.cos(sec_angle),
                                         self.center_y + self.sec_hand_len * math.sin(sec_angle)],
                                 width = self.sec_hand_width)

            Line(points = [self.center_x, self.center_y,
                                         self.center_x + self.min_hand_len * math.cos(min_angle),
                                         self.center_y + self.min_hand_len * math.sin(min_angle)],
                                 width = self.min_hand_width)

            Line(points = [self.center_x, self.center_y,
                                          self.center_x + self.hour_hand_len * math.cos(hour_angle),
                                          self.center_y + self.hour_hand_len * math.sin(hour_angle)],
                                  width = self.hour_hand_width)


class Time(App):
    def build(self):
        i = interface()
        Clock.schedule_interval(i.update, 1.0 / 60.0)
        return i


if __name__ == "__main__":
    Time().run()