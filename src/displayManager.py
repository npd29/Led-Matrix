import ssl
from math import floor, log

import adafruit_imageload
import terminalio
from adafruit_bitmap_font import bitmap_font
import displayio
import secrets
from time import localtime, sleep, struct_time
from adafruit_display_text import label
from adafruit_display_text.scrolling_label import ScrollingLabel
from digitalio import DigitalInOut, Direction  # digital input/output for LED
import socketpool  # socket pool for Wi-Fi
import adafruit_ntp  # network time protocol for setting RTC
import rtc  # real time clock
import wifi  # wifi
import gc  # garbage collection
from board import LED  # board for LED
from utilities import convert_brightness
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
import adafruit_requests

brightness = 0.5


def connect_to_wifi(led):
    count = 0
    while not wifi.radio.ipv4_address and count < 1:
        try:
            wifi.radio.connect(secrets.SSID, secrets.PASSWORD)
            print("Connected to", secrets.SSID, "\nIP Address:", wifi.radio.ipv4_address)
        except ConnectionError as e:
            print("Conn Error:", e)
        sleep(1)
        print(count)
        count += 1
    # set RTC
    if wifi.radio.ipv4_address:
        try:
            pool = socketpool.SocketPool(wifi.radio)
            ntp = adafruit_ntp.NTP(pool, tz_offset=0)
            rtc.RTC().datetime = ntp.datetime
            led.value = True

        except OSError:
            print("OSError")
        except Exception as e:
            print("Unexpected error with syncing RTC")
            print(e)
    else:
        rtc.RTC().datetime = struct_time((2023, 9, 13, 19, 13, 15, 0, -1, -1))

    gc.collect()


def get_weather():
    pass
    # using Wi-Fi call weather api


def get_logo() -> displayio.Group:
    logo_bitmap, logo_palette = adafruit_imageload.load(secrets.LOGO_PATH,
                                                        bitmap=displayio.Bitmap,
                                                        palette=displayio.Palette)
    logo_palette[1] = convert_brightness("0xFFFFFF", brightness)

    logo_palette.make_transparent(0)

    return add_center(displayio.TileGrid(logo_bitmap, pixel_shader=logo_palette))


def test_text():
    text = "HELLO WORLD"
    font = terminalio.FONT
    color = convert_brightness("0xFFFFFF", brightness)
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


def get_current_time():
    scale = 1
    am = True
    # convert UTC hour to EST and from 24 to 12hr
    if rtc.RTC().datetime[3] > 12:
        am = False
    hour = (rtc.RTC().datetime[3] - 4) % 12
    if hour == 0:
        hour = 12
    formatted_time = str(hour) + ":" + str(rtc.RTC().datetime[4])
    font = bitmap_font.load_font("/Helvetica-Bold-16.bdf")
    # text_area.background_color = 0x000508
    layout = GridLayout(
        x=2,
        y=1,
        width=60,
        height=30,
        grid_size=(2, 3),
        cell_padding=0,
        divider_lines=False,  # divider lines around every cell
    )
    _labels = [label.Label(
        bitmap_font.load_font("/Helvetica-Bold-16.bdf"), scale=1, x=0, y=0, text=formatted_time, color=secrets.CYAN,
    )]

    layout.add_content(_labels[0], grid_position=(0, 0), cell_size=(1, 2), cell_anchor_point=(0.5, 0.5))
    # _labels.append(
    #     label.Label(
    #         terminalio.FONT, scale=1, x=0, y=0, text="", background_color=0x007700
    #     )
    # )
    # layout.add_content(_labels[1], grid_position=(1, 0), cell_size=(1, 1))
    # _labels.append(label.Label(terminalio.FONT, scale=1, x=0, y=0, text="DESMARAIS", color=secrets.PINK))
    # layout.add_content(_labels[2], grid_position=(0, 1), cell_size=(1, 1))
    # _labels.append(label.Label(terminalio.FONT, scale=1, x=0, y=0, text="", color=0xFF0000))
    # layout.add_content(_labels[3], grid_position=(1, 1), cell_size=(1, 1))
    group = displayio.Group()
    group.append(layout)
    return group


def add_center(item: displayio.Bitmap | displayio.TileGrid) -> displayio.Group:
    _group = displayio.Group()
    item.x = secrets.WIDTH // 2 - item.bitmap.width // 2
    item.y = secrets.HEIGHT // 2 - item.bitmap.height // 2
    _group.append(item)
    return _group


def create_layout():
    # weather = Weather(03110)
    # high = weather.high
    # low = weather.low
    layout = GridLayout(
        x=2,
        y=1,
        width=60,
        height=30,
        grid_size=(2, 3),
        cell_padding=0,
        divider_lines=False,  # divider lines around every cell
    )
    _labels = [label.Label(
        bitmap_font.load_font("/Helvetica-Bold-16.bdf"), scale=1, x=0, y=0, text="NOEL", color=secrets.CYAN,
        background_color=0x000000
    )]

    layout.add_content(_labels[0], grid_position=(0, 0), cell_size=(1, 2), cell_anchor_point=(0.5, 0.5))
    # _labels.append(
    #     label.Label(
    #         terminalio.FONT, scale=1, x=0, y=0, text="", background_color=0x007700
    #     )
    # )
    # layout.add_content(_labels[1], grid_position=(1, 0), cell_size=(1, 1))
    # _labels.append(label.Label(terminalio.FONT, scale=1, x=0, y=0, text="DESMARAIS", color=secrets.PINK))
    # layout.add_content(_labels[2], grid_position=(0, 1), cell_size=(1, 1))
    # _labels.append(label.Label(terminalio.FONT, scale=1, x=0, y=0, text="", color=0xFF0000))
    # layout.add_content(_labels[3], grid_position=(1, 1), cell_size=(1, 1))
    group = displayio.Group()
    group.append(layout)
    return group


class DisplayManager(displayio.Group):
    def __init__(self, display, led):
        self.is_setup = False
        super().__init__()
        global brightness
        display.rotation = 0
        self.display = display
        self.logo = get_logo()
        self.display.show(self.logo)
        self.current_time = None
        self.weather = None
        self.led = led

    def setup(self):
        self.current_time = get_current_time()
        connect_to_wifi(self.led)
        self.weather = create_layout()
        self.is_setup = True

    def add_text(self, text: str, x: int, y: int, color: int = 0xFFFFFF):
        font = terminalio.FONT
        text_area = label.Label(font, text=text, color=convert_brightness(color, self.brightness))
        text_area.x = x
        text_area.y = y
        self.group.append(text_area)

    def update(self):
        pass
        # self._scrolling_label.update()

    def show(self, group):
        self.display.show(group)

    def display_logo(self):
        self.logo.hidden = False
        self.current_time.hidden = True
        self.display.show(self.logo)

    def display_time(self):
        self.logo.hidden = True
        self.weather.hidden = True
        self.current_time.hidden = False
        # self.current_time = get_current_time()
        self.display.show(self.current_time)

    def display_weather(self):
        self.logo.hidden = True
        self.current_time.hidden = True
        self.weather.hidden = False
        self.display.show(self.weather)

    def update_time(self):
        self.current_time = get_current_time()


class Weather():
    def __init__(self):
        self.pool = socketpool.SocketPool(wifi.radio)
        self.requests = adafruit_requests.Session(self.pool, ssl.create_default_context())
        self.high = ""
        self.low = ""
#         self.source = (
#             "http://api.weatherapi.com/v1/forecast.json?key=c0902e1fe459436db2e224800230609&q=02837&days=3&aqi=yes&alerts=no
# "
#         )
#         self.tide_source = (
#             ""
#         )
