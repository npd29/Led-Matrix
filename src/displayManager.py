import time
from math import floor, log

import adafruit_imageload
import terminalio
import displayio
import secrets
from time import localtime
from adafruit_display_text import label
from adafruit_display_text.scrolling_label import ScrollingLabel


def get_logo()->displayio.Group:
    logo_bitmap, logo_palette = adafruit_imageload.load(secrets.LOGO_PATH,
                                                        bitmap=displayio.Bitmap,
                                                        palette=displayio.Palette)
    logo_palette[1] = 0x000000

    logo_palette.make_transparent(0)

    return add_center(displayio.TileGrid(logo_bitmap, pixel_shader=logo_palette))


def test_text():
    text = "HELLO WORLD"
    font = terminalio.FONT
    color = 0x0000FF
    text_area = label.Label(font, text=text, color=color)
    text_area.x = 10
    text_area.y = 10
    return text_area


def scroll(line, display):
    line.x = line.x - 1
    line_width = line.bounding_box[2]
    if line.x < -line_width:
        line.x = display.width


def reverse_scroll(line, display):
    line.x = line.x + 1
    line_width = line.bounding_box[2]
    if line.x >= display.width:
        line.x = -line_width


def get_current_time() -> displayio.Group:
    formatted_time = str(localtime()[3]) + ":" + str(localtime()[4])
    font = terminalio.FONT
    text_area = label.Label(font, text=formatted_time, color=0xFFFFFF)
    text_area.x = secrets.WIDTH // 2 - text_area.width // 2
    text_area.y = secrets.HEIGHT // 2 - text_area.height // 2
    _group = displayio.Group()
    _group.append(text_area)
    return _group


def add_center(item: displayio.Bitmap | displayio.TileGrid) -> displayio.Group:
    _group = displayio.Group()
    item.x = secrets.WIDTH // 2 - item.width // 2
    item.y = item.height // 2
    _group.append(item)
    return _group


class DisplayManager(displayio.Group):
    def __init__(self, display):
        super().__init__()
        display.rotation = 0
        self.display = display
        self.logo = get_logo()
        self.current_time = get_current_time()

    def add_text(self, text: str, x: int, y: int, color: int = 0xFFFFFF):
        font = terminalio.FONT
        text_area = label.Label(font, text=text, color=color)
        text_area.x = x
        text_area.y = y
        self.group.append(text_area)
        self.display.show(self.group)

    def update(self):
        pass
        # self._scrolling_label.update()

    def show(self, group):
        self.display.show(group)

    def display_logo(self):
        self.display.show(self.logo)

    def display_time(self):
        self.logo.hidden = True
        self.display.show(self.current_time)
