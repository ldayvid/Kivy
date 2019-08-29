import pandas as pd
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Line
from kivy.core.window import Window


df = pd.read_csv("AMZN.csv")
df = df[['Date', 'Open']]

length = len(df.index)

data = []

for i in range(1, length):
    data.append(float(df.iloc[i, 1]))

length -= 1

training_input = []
training_output = []

testing_input = []
testing_output = []


for i in range(0, length, 2):
    training_input.append(i)
    training_output.append(data[i])

for i in range(1, length, 2):
    testing_input.append(i)
    testing_output.append(data[i])


class interface(FloatLayout):
    def __init__(self, **kwargs):
        super(interface, self).__init__(**kwargs)


    def populate(self):

        with self.canvas:

            Color(1, 1, 1)
            Line(points = [50, 50, Window.width, 50], width = 5)
            Line(points = [50, 50, 50, Window.height], width = 5)


            for i in range(1, length):
                Line(points = [50 + (i - 1) / 10.0, 60 + data[i - 1] / 5.0,
                                50 + i / 10.0, 60 + data[i] / 5.0],
                        width = 1)


class StockForecaster(App):
    def build(self):
        i = interface()
        i.populate()
        return i


if __name__ == "__main__":
    StockForecaster().run()