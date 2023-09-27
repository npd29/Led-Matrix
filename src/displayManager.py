from ssl import create_default_context
from math import floor, log, sin

from adafruit_bitmap_font import bitmap_font  # for displaying fonts
import displayio  # for displaying things on the screen
import secrets  # secrets.py file for passwords
from time import localtime, sleep, struct_time
from adafruit_display_text import label  # for displaying text
from adafruit_display_text.scrolling_label import ScrollingLabel  # for scrolling text
from digitalio import DigitalInOut, Direction  # digital input/output for LED
from socketpool import SocketPool  # socket pool for Wi-Fi
import adafruit_ntp  # network time protocol for setting RTC
from rtc import RTC  # real time clock
from wifi import radio  # wifi
from gc import collect, mem_free  # garbage collection
from board import LED  # board for LED
from utilities import convert_brightness  # i made this but you don't really need it
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_displayio_layout.widgets.icon_widget import IconWidget  # for displaying images
from adafruit_requests import Session  # for getting data from API
import constants as c  # constants.py file
from rect import \
    Rect  # rect.py file for making rectangles originally from adafruit_display_shapes but the full library was too large
import json  # for parsing json

brightness = 0.5


def connect_to_wifi(led):
    count = 0
    chances_to_connect = 5
    while not radio.ipv4_address and count < chances_to_connect:  # try to connect to wifi 5 times
        try:
            radio.connect(secrets.SSID, secrets.PASSWORD)
            print("Connected to", secrets.SSID, "\nIP Address:", radio.ipv4_address)
        except ConnectionError as e:
            if count == 0:
                print("\nConnection Error:", e)
            if chances_to_connect == chances_to_connect - 1:
                print("UNABLE TO CONNECT - CONTINUING OFFLINE")
            else:
                print("Retry -", count)

        count += 1
    # if connected to wifi set the real time clock onboard the pi
    if radio.ipv4_address:
        try:
            pool = SocketPool(radio)
            ntp = adafruit_ntp.NTP(pool, tz_offset=0)
            RTC().datetime = ntp.datetime
            led.value = True  # indicate wifi connection by turning on the onboard LED
            print("RTC set")

        except Exception as e:
            print("Unexpected error with syncing RTC")
            print(e)
    else:  # this is for testing purposes
        # if there is no wifi connection it will set the time to 6/14/2023 2:57pm UTC
        RTC().datetime = struct_time((2023, 4, 20, 8, 4, 0, 0, -1, -1))

    collect()


# Displays the logo on the screen
def get_logo() -> displayio.Group:
    logo_bitmap = displayio.OnDiskBitmap(c.LOGO_PATH)

    return add_center(displayio.TileGrid(logo_bitmap, pixel_shader=logo_bitmap.pixel_shader))


# this is one way to add text
# def test_text():
#     text = "HELLO WORLD"
#     font = bitmap_font.load_font("/fonts/nond-5.bdf")
#     color = convert_brightness("0xFFFFFF", brightness)
#     text_area = label.Label(font, text=text, color=color)
#     text_area.x = 10
#     text_area.y = 10
#     return text_area


# I don't use this but if you wanted scrolling text
# def scroll(line, display):
#     line.x = line.x - 1
#     line_width = line.bounding_box[2]
#     if line.x < -line_width:
#         line.x = display.width


# I don't use this but if you wanted reverse scrolling text
# def reverse_scroll(line, display):
#     line.x = line.x + 1
#     line_width = line.bounding_box[2]
#     if line.x >= display.width:
#         line.x = -line_width


# gets the current time and date and converts it to EST
def get_current_time():
    date = c.MONTHS[localtime()[1]] + " " + str(localtime()[2])
    square = Rect(x=0, y=0, width=64, height=7, fill=c.INDIGO)  # makes a rectangle to go at the bottom of screen
    am_pm = "AM"
    # convert UTC hour to EST and from 24 to 12hr
    if localtime()[3] > 12:
        am_pm = "PM"
    hour = (localtime()[3] - 4) % 12
    if hour == 0:
        hour = 12
    if localtime()[4] < 10:
        minute = "0" + str(localtime()[4])
    else:
        minute = localtime()[4]
    formatted_time = str(hour) + ":" + str(minute)

    '''
        How this works is you create a grid and create some content then attach the content to the grid
        For this I am creating 2 grids and nesting them inside each other
        |--------------------------------------------| Big grid is called layout
        |                                            |  - _time gets added to layout
        |                                            |
        |                  2:57                      |
        |                                            |
        |                                            |
        |--------------------------------------------|
        | |----------------------------------------| |This little nested grid is called bottom
        | |PM             |                  SEP 19| |  - _bottom_labels get added to bottom
        | |----------------------------------------| |      - _bottom_labels[0] is AM/PM and _bottom_labels[1] is date
        |--------------------------------------------|  - bottom gets added to layout   
    '''
    layout = GridLayout(
        x=0,
        y=0,
        width=64,  # uses full dimensions of the screen and puts the time in the top 2/3 and the date in the bottom 1/3
        height=32,
        grid_size=(1, 3),
        cell_padding=0,
        divider_lines=False,  # divider lines around every cell
    )

    _time = label.Label(
        bitmap_font.load_font("/fonts/BarlowCondensed-Medium-28.bdf"), scale=1, x=0, y=0, text=formatted_time,
        color=c.GREY
    )

    layout.add_content(_time, grid_position=(0, 0), cell_size=(1, 2), cell_anchor_point=(0.5, 1))
    bottom = GridLayout(
        x=0,
        y=0,
        width=64,
        height=10,
        grid_size=(2, 1),  # makes a 2x1 grid for the date and AM/PM to go on the bottom
        cell_padding=0,
        divider_lines=False  # divider lines around every cell
    )
    _bottom_labels = [
        label.Label(
            bitmap_font.load_font("/fonts/nond-5.bdf"), scale=1, x=0, y=0, text=am_pm, color=c.BLACK
        ),
        label.Label(
            bitmap_font.load_font("/fonts/nond-5.bdf"), scale=1, x=0, y=0, text=date,
            color=c.BLACK
        )
    ]
    bottom.add_content(_bottom_labels[0], grid_position=(0, 0), cell_size=(1, 1), cell_anchor_point=(0.1, 1))
    bottom.add_content(_bottom_labels[1], grid_position=(1, 0), cell_size=(1, 1), cell_anchor_point=(.9, 1))
    layout.add_content(square, grid_position=(0, 2), cell_size=(1, 1), cell_anchor_point=(0, 1))
    layout.add_content(bottom, grid_position=(0, 2), cell_size=(1, 1), cell_anchor_point=(0, 0))

    group = displayio.Group()
    group.append(layout)
    return group


def add_center(item: displayio.Bitmap | displayio.TileGrid) -> displayio.Group:
    _group = displayio.Group()
    item.x = c.WIDTH // 2 - item.bitmap.width // 2
    item.y = c.HEIGHT // 2 - item.bitmap.height // 2
    _group.append(item)
    return _group

def get_default_layout():
    date = c.MONTHS[localtime()[1]] + " " + str(localtime()[2])
    square = Rect(x=0, y=0, width=64, height=7, fill=c.INDIGO)  # makes a rectangle to go at the bottom of screen
    am_pm = "AM"
    # convert UTC hour to EST and from 24 to 12hr
    if localtime()[3] > 12:
        am_pm = "PM"
    hour = (localtime()[3] - 4) % 12
    if hour == 0:
        hour = 12
    if localtime()[4] < 10:
        minute = "0" + str(localtime()[4])
    else:
        minute = localtime()[4]
    formatted_time = str(hour) + ":" + str(minute)
    layout = GridLayout(
        x=0,
        y=0,
        width=64,  # uses full dimensions of the screen and puts the time in the top 2/3 and the date in the bottom 1/3
        height=32,
        grid_size=(1, 3),
        cell_padding=0,
        divider_lines=False,  # divider lines around every cell
    )

    _time = label.Label(
        bitmap_font.load_font("/fonts/BarlowCondensed-Medium-28.bdf"), scale=1, x=0, y=0, text=formatted_time,
        color=c.GREY
    )

    layout.add_content(_time, grid_position=(0, 0), cell_size=(1, 2), cell_anchor_point=(0.5, 1))
    bottom = GridLayout(
        x=0,
        y=0,
        width=64,
        height=10,
        grid_size=(2, 1),  # makes a 2x1 grid for the date and AM/PM to go on the bottom
        cell_padding=0,
        divider_lines=False  # divider lines around every cell
    )
    _bottom_labels = [
        label.Label(
            bitmap_font.load_font("/fonts/nond-5.bdf"), scale=1, x=0, y=0, text=am_pm, color=c.BLACK
        ),
        label.Label(
            bitmap_font.load_font("/fonts/nond-5.bdf"), scale=1, x=0, y=0, text=date,
            color=c.BLACK
        )
    ]
    bottom.add_content(_bottom_labels[0], grid_position=(0, 0), cell_size=(1, 1), cell_anchor_point=(0.1, 1))
    bottom.add_content(_bottom_labels[1], grid_position=(1, 0), cell_size=(1, 1), cell_anchor_point=(.9, 1))
    layout.add_content(square, grid_position=(0, 2), cell_size=(1, 1), cell_anchor_point=(0, 1))
    layout.add_content(bottom, grid_position=(0, 2), cell_size=(1, 1), cell_anchor_point=(0, 0))

    group = displayio.Group()
    group.append(layout)
    return group

def get_settings(location="NONE"):
    layout = GridLayout(
        x=0,
        y=0,
        width=64,
        height=32,
        grid_size=(3, 3),
        cell_padding=0,
        divider_lines=False,  # divider lines around every cell
    )
    if radio.ipv4_address:
        wifi_color = c.GREEN
        ip = radio.ipv4_address
        icon = IconWidget(
            "",
            "images/wifi_connected.bmp",
            on_disk=True,
            transparent_index=c.BLACK
        )
    else:
        wifi_color = c.RED
        ip = "No wifi"
        icon = IconWidget(
            "",
            "images/wifi_not_connected.bmp",
            on_disk=True,
            transparent_index=c.WHITE
        )
    collect()
    info = [
        label.Label(
            bitmap_font.load_font("/fonts/nond-mono-5.bdf"), scale=1, x=0, y=0, text=ip, color=wifi_color,
        ),
        label.Label(
            bitmap_font.load_font("/fonts/nond-mono-5.bdf"), scale=1, x=0, y=0, text="FREE: " + str(mem_free()),
            color=c.GREY,
        ),
        label.Label(
            bitmap_font.load_font("/fonts/nond-mono-5.bdf"), scale=1, x=0, y=0, text=location, color=c.GREY,
        )]

    layout.add_content(icon, grid_position=(0, 0), cell_size=(1, 1), cell_anchor_point=(0.5, 0.5))
    layout.add_content(info[0], grid_position=(1, 0), cell_size=(2, 1), cell_anchor_point=(0, 0.5))
    layout.add_content(info[1], grid_position=(0, 1), cell_size=(3, 1), cell_anchor_point=(0.5, 0.5))
    layout.add_content(info[2], grid_position=(0, 2), cell_size=(3, 1), cell_anchor_point=(0.5, 0.5))

    group = displayio.Group()
    group.append(layout)
    return group


def get_sun_times(today: Weather):
    layout = GridLayout(
        x=0,
        y=0,
        width=64,
        height=32,
        grid_size=(2, 2),
        cell_padding=0,
        divider_lines=False,  # divider lines around every cell
    )
    print(today.sunrise)
    today.sunrise = today.sunrise.lstrip("0").rstrip(" AM")
    today.sunset = today.sunset.lstrip("0").rstrip(" PM")
    _times = [
        label.Label(
            bitmap_font.load_font("/fonts/Helvetica-Bold-16.bdf"), scale=1, x=0, y=0, text=today.sunrise, color=c.GREY,
        ), label.Label(
            bitmap_font.load_font("/fonts/Helvetica-Bold-16.bdf"), scale=1, x=0, y=0, text=today.sunset, color=c.GREY,
        )]
    icons = [IconWidget(
        "",
        "images/sunrise.bmp",
        on_disk=True,
        transparent_index=c.BLACK
    ),
        IconWidget(
            "",
            "images/sunset.bmp",
            on_disk=True,
            transparent_index=c.BLACK
        )]

    layout.add_content(icons[0], grid_position=(0, 0), cell_size=(1, 1), cell_anchor_point=(0, 0.5))
    layout.add_content(icons[1], grid_position=(1, 1), cell_size=(1, 1), cell_anchor_point=(1, 0.5))
    layout.add_content(_times[0], grid_position=(1, 0), cell_size=(1, 1), cell_anchor_point=(0, 0.5))
    layout.add_content(_times[1], grid_position=(0, 1), cell_size=(1, 1), cell_anchor_point=(1, 0.5))

    group = displayio.Group()
    group.append(layout)
    return group


# If you want to use this you will need to get an API key from weatherapi.com
def get_weather(zip="auto:ip") -> [displayio.Group, []]:
    try:
        pool = SocketPool(radio)
        requests = Session(pool, create_default_context())
        source = (
                "http://api.weatherapi.com/v1/forecast.json?key=" + secrets.WEATHER_API_KEY + "&q=" + zip + "&days=3&aqi=no&alerts=no")

        collect()

        temp = dict()

        response = requests.get(source, stream=True, json=temp)
        response = response.json()
        forecast = []
        location = response["location"]["name"]

        for day in response["forecast"]["forecastday"]:
            forecast.append(
                Weather(
                    day["date"],
                    day["date_epoch"],
                    day["day"]["maxtemp_f"],
                    day["day"]["mintemp_f"],
                    day["day"]["avgtemp_f"],
                    day["day"]["condition"]["code"],
                    day["day"]["totalsnow_cm"],
                    day["day"]["daily_chance_of_rain"],
                    day["astro"]["sunrise"],
                    day["astro"]["sunset"],
                    location
                )
            )
    except KeyError:
        print("Unable to Retrieve weather data using default data")
        forecast = [Weather(date_epoch=0, code=1003), Weather(date_epoch=86400, code=1279), Weather(date_epoch=2*86400)]
    except Exception as e:
        print("Unexpected error with weather data using default data")
        forecast = [Weather(date_epoch=0, code=1003), Weather(date_epoch=86400, code=1279), Weather(date_epoch=2*86400)]
        print(e)
    collect()

    layout = GridLayout(
        x=0,
        y=0,
        width=64,
        height=32,
        grid_size=(3, 5),
        cell_padding=0,
        divider_lines=False,  # divider lines around every cell
        v_divider_line_cols=[1, 2],  # vertical divider lines between columns 1 and 2
        divider_line_color=c.DK_GREY
    )
    _labels = [
        # next 3 days
        label.Label(
            bitmap_font.load_font("/fonts/nond-5.bdf"), scale=1, x=0, y=0, text=forecast[0].day_of_week, color=c.WHITE,
        ), label.Label(
            bitmap_font.load_font("/fonts/nond-5.bdf"), scale=1, x=0, y=0, text=forecast[1].day_of_week, color=c.WHITE,
        ), label.Label(
            bitmap_font.load_font("/fonts/nond-5.bdf"), scale=1, x=0, y=0, text=forecast[2].day_of_week, color=c.WHITE,
        ),
        # high temps
        label.Label(
            bitmap_font.load_font("/fonts/nond-5.bdf"), scale=1, x=0, y=0, text=str(forecast[0].high), color=c.YELLOW,
        ), label.Label(
            bitmap_font.load_font("/fonts/nond-5.bdf"), scale=1, x=0, y=0, text=str(forecast[1].high), color=c.YELLOW,
        ), label.Label(
            bitmap_font.load_font("/fonts/nond-5.bdf"), scale=1, x=0, y=0, text=str(forecast[2].high), color=c.YELLOW,
        ),
        # low temps
        label.Label(
            bitmap_font.load_font("/fonts/nond-5.bdf"), scale=1, x=0, y=0, text=str(forecast[0].low), color=c.LT_GREY,
        ), label.Label(
            bitmap_font.load_font("/fonts/nond-5.bdf"), scale=1, x=0, y=0, text=str(forecast[1].low), color=c.LT_GREY,
        ), label.Label(
            bitmap_font.load_font("/fonts/nond-5.bdf"), scale=1, x=0, y=0, text=str(forecast[2].low), color=c.LT_GREY,
        )
    ]
    weather_icons = [IconWidget(
        "",
        forecast[0].icon,
        on_disk=True,
        transparent_index=c.BLACK
    ),
        IconWidget(
            "",
            forecast[1].icon,
            on_disk=True,
            transparent_index=c.BLACK
        ),
        IconWidget(
            "",
            forecast[2].icon,
            on_disk=True,
            transparent_index=c.BLACK
        )]

    layout.add_content(weather_icons[0], grid_position=(0, 0), cell_size=(1, 2), cell_anchor_point=(0.5, 0.5))
    layout.add_content(weather_icons[1], grid_position=(1, 0), cell_size=(1, 2), cell_anchor_point=(0.5, 0.5))
    layout.add_content(weather_icons[2], grid_position=(2, 0), cell_size=(1, 2), cell_anchor_point=(0.5, 0.5))

    # next 3 days

    layout.add_content(_labels[0], grid_position=(0, 2), cell_size=(1, 1), cell_anchor_point=(0.5, 0))
    layout.add_content(_labels[1], grid_position=(1, 2), cell_size=(1, 1), cell_anchor_point=(0.5, 0))
    layout.add_content(_labels[2], grid_position=(2, 2), cell_size=(1, 1), cell_anchor_point=(0.5, 0))
    # high temps
    layout.add_content(_labels[3], grid_position=(0, 3), cell_size=(1, 1), cell_anchor_point=(0.5, 0.5))
    layout.add_content(_labels[4], grid_position=(1, 3), cell_size=(1, 1), cell_anchor_point=(0.5, 0.5))
    layout.add_content(_labels[5], grid_position=(2, 3), cell_size=(1, 1), cell_anchor_point=(0.5, 0.5))
    # low temps
    layout.add_content(_labels[6], grid_position=(0, 4), cell_size=(1, 1), cell_anchor_point=(0.5, 0.5))
    layout.add_content(_labels[7], grid_position=(1, 4), cell_size=(1, 1), cell_anchor_point=(0.5, 0.5))
    layout.add_content(_labels[8], grid_position=(2, 4), cell_size=(1, 1), cell_anchor_point=(0.5, 0.5))

    group = displayio.Group()
    group.append(layout)
    return [group, forecast]


class DisplayManager(displayio.Group):
    # initialize the display manager
    def __init__(self, display, led):
        self.is_setup = False
        super().__init__()
        self.display = display
        self.logo = get_logo()
        self.display.show(self.logo)
        self.current_time = None
        self.weather = None
        self.sun_times = None
        self.led = led
        self.forecast = None
        self.settings = None

    # set up the display
    def setup(self):
        connect_to_wifi(self.led)
        self.current_time = get_current_time()
        self.update_weather()
        self.is_setup = True
        self.logo = None # free up memory
        collect()


    def update_weather(self):
        _temp = get_weather()
        self.weather = _temp[0]
        self.forecast = _temp[1]
        self.sun_times = get_sun_times(self.forecast[0])

    def add_text(self, text: str, x: int, y: int, color: int = 0xFFFFFF):
        font = bitmap_font.load_font("/fonts/nond-5.bdf")
        text_area = label.Label(font, text=text, color=convert_brightness(color, self.brightness))
        text_area.x = x
        text_area.y = y
        self.group.append(text_area)

    def show(self, group):
        self.display.show(group)

    # for these next 3 functions I am just hiding the other 2 screens and showing the one I want
    def display_logo(self):
        self.hide_all()
        self.display.show(self.logo)

    def display_time(self):
        self.hide_all()
        # self.current_time = get_current_time()
        self.display.show(self.current_time)

    def display_weather(self):
        self.hide_all()
        self.display.show(self.weather)

    def display_sun_times(self):
        self.hide_all()
        self.display.show(self.sun_times)

    def display_animation(self):
        pass
        # tile_grid = displayio.TileGrid(self.bitmap, pixel_shader=self.palette)
        # group = displayio.Group()
        # group.append(tile_grid)
        # self.display.show(group)
        #
        # self.animation_col = (self.animation_col + 1) % c.WIDTH
        # self.animation_color = (self.animation_color + 1) % (len(self.palette) - 1)
        # # for row in range(c.HEIGHT):
        # #     self.bitmap[self.animation_col, row] = self.animation_color
        # for col in range(c.WIDTH):
        #     for row in range(c.HEIGHT):
        #         self.bitmap[col, row] = 2

    def display_settings(self):
        self.hide_all()
        if self.settings is None:
            self.settings = get_settings(self.forecast[0].location)
        self.display.show(self.settings)

    def update_time(self):
        self.current_time = get_current_time()

    def reset_time(self):
        self.current_time = None
        collect()
        self.current_time = get_current_time()

    def hide_all(self):
        for item in self:
            try:
                item.hidden = True
            except AttributeError:
                pass


class Weather:
    def __init__(self, date="N/A", date_epoch=0, high=100, low=0, average=50, code=1180, total_snow=0, chance_rain=0,
                 sunrise="N/A", sunset="N/A", location="N/A"):
        self.date = date
        self.high = int(high)
        self.low = int(low)
        self.average = int(average)
        self.total_snow = total_snow
        self.chance_rain = chance_rain
        self.sunrise = sunrise
        self.sunset = sunset
        self.day_of_week = c.DAY_OF_WEEK[(date_epoch / 86400 + 4) % 7]  # convert epoch to day of week 0=SUN
        self.icon = self.get_icon(code)
        self.location = location

    def get_icon(self, code):
        return "images/" + c.get_weather_icon(code)
