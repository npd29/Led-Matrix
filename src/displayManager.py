from math import floor, log

import adafruit_imageload
import terminalio
import displayio
import secrets
from time import localtime, strftime
from adafruit_display_text import label
from adafruit_display_text.scrolling_label import ScrollingLabel



def get_logo(x, y):
    logo_bitmap, logo_palette = adafruit_imageload.load(secrets.LOGO_PATH,
                                                        bitmap=displayio.Bitmap,
                                                        palette=displayio.Palette)
    logo_palette[1] = 0x0000FF
    logo_palette.make_transparent(0)

    return displayio.TileGrid(logo_bitmap, pixel_shader=logo_palette, x=x, y=y)

def get_time():
    font = terminalio.FONT
    group = displayio.Group()
    time_label = label.Label(font, text="", color=0xFFFFFF)
    time_label.x = 10
    time_label.y = 10

    group.append(time_label)
    current_time = localtime()
    formatted_time = strftime("%H:%M:%S", current_time)

def test_text():
    text = "HELLO WORLD"
    font = terminalio.FONT
    color = 0x0000FF
    text_area = label.Label(font, text=text, color=color)
    text_area.x = 10
    text_area.y = 10
    return text_area

class DisplayManager(displayio.Group):
    def __init__(self, display):
        super().__init__()
        display.rotation = 0
        self.display = display
        self._first_enter_page = True
        self.my_logo = get_logo(0, 0)
        # self.loading_group = displayio.Group()
        # self._scrolling_label = ScrollingLabel(terminalio.FONT, text="subscribers", max_characters=11, animate_time=0.3,
        #                                        color=0x00FFFF)
        #
        # self._scrolling_label.x = 0
        # self._scrolling_label.y = 25
        # line1 = adafruit_display_text.label.Label(terminalio.FONT, color=0x0000CC)

        # self._line1 = line1
        # self._line1.text = " "

        self.loading_screen = displayio.Group()
        self.loading_screen.append(self.my_logo)
        # self._line_group.append(self)
        self.append(self.loading_screen)
        # self.append(self._scrolling_label)

        display.show(self.loading_screen)

    def update(self):
        pass
        # self._scrolling_label.update()

    def display_logo(self):
        tile_grid = get_logo(1, 2)
        # youtube_tile_grid = get_youtube_logo(51, 9)
        group = displayio.Group()

        # self._line1.x = 19
        # self._line1.y = 12

        group.append(tile_grid)
        # group.append(youtube_tile_grid)

        self.loading_screen.append(group)

        self.display.show(self.loading_screen)

    def display_time(self):
        self.display.show(get_time())

    def show(self, group):
        self.display.show(group)

