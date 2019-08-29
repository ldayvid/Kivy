import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import glob
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

raw_files = glob.glob("C:/Users/Davacho/PycharmProjects/MusicPlayer/*.mp3")

files = []

length = len(raw_files)

for i in range(length):
    base = os.path.basename(raw_files[i])
    files.append(os.path.splitext(base)[0])

print(files)


class grid(GridLayout):
    def __init__(self, **kwargs):
        super(grid, self).__init__(**kwargs)
        self.cols = 1
        self.size_hint_y = None
        self.bind(minimum_height = self.setter('height'))


class scroll(ScrollView):
    def __init__(self, **kwargs):
        super(scroll, self).__init__(**kwargs)
        self.g = grid()
        self.size_hint = (1, None)
        self.size = (Window.width, Window.height)


class interface(FloatLayout):
    def __init__(self, **kwargs):
        super(interface, self).__init__(**kwargs)

        self.cur_song = SoundLoader.load(files[0] + '.mp3')
        self.playing = False
        self.cur_id = 0
        self.btns = []
        self.song_len = self.cur_song.length

        self.choice = GridLayout(cols = 3)

        self.play_b = Button(text = "Play", size_hint_y = None, height = Window.height / 10)
        self.play_b.bind(on_press = self.press_play)

        self.prev = Button(text = "Previous", size_hint_y = None, height = Window.height / 10)
        self.prev.bind(on_press = self.press_prev)

        self.next = Button(text = "Next", size_hint_y = None, height = Window.height / 10)
        self.next.bind(on_press = self.press_next)

        self.choice.add_widget(self.prev)
        self.choice.add_widget(self.play_b)
        self.choice.add_widget(self.next)

        self.s = scroll()
        self.s.size_hint = (1.0, 0.9)

        self.g = grid()

        for i in range(length):
            btn = Button(text = files[i], id = str(i), size_hint_y = None, height = 40)
            btn.bind(on_press = self.press_song)
            self.btns.append(btn)
            self.g.add_widget(btn)

        self.s.add_widget(self.g)
        self.add_widget(self.s)
        self.add_widget(self.choice)


    def update(self, var):

        if self.playing and self.cur_song.state == "stop":
            self.cur_id = (self.cur_id + 1) % length
            self.cur_song = SoundLoader.load(files[self.cur_id] + '.mp3')


    def press_play(self, instance):

        if self.playing:
            self.play_b.text = "Play"
            self.playing = False
            (self.cur_song).stop()

        else:
            self.play_b.text = "Stop"
            self.playing = True
            (self.cur_song).play()


    def press_prev(self, instance):

        if self.playing:
            (self.cur_song).stop()

        self.play_b.text = "Stop"
        self.cur_id = (self.cur_id - 1 + length) % length
        self.cur_song = SoundLoader.load(files[self.cur_id] + '.mp3')
        self.playing = True
        (self.cur_song).play()


    def press_next(self, instance):

        if self.playing:
            (self.cur_song).stop()

        self.play_b.text = "Stop"
        self.cur_id = (self.cur_id + 1) % length
        self.cur_song = SoundLoader.load(files[self.cur_id] + '.mp3')
        self.playing = True
        (self.cur_song).play()


    def press_song(self, instance):

        self.play_b.text = "Stop"

        if self.playing:
            (self.cur_song).stop()

        sound = files[int(instance.id)] + '.mp3'

        if sound:
            self.cur_id = int(instance.id)
            self.cur_song = SoundLoader.load(sound)
            self.playing = True
            (self.cur_song).play()


class MusicPlayer(App):
    def build(self):
        i = interface()
        Clock.schedule_interval(i.update, 1.0 / 60.0)
        return i


if __name__ == "__main__":
    MusicPlayer().run()