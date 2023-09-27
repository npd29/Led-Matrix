TIMEZONE = "America/New_York"  # http://worldtimeapi.org/timezones
LOGO_PATH = 'images/NDLogo-24.bmp'
WIDTH = 64
HEIGHT = 32

RED = 0xFF0000
ORANGE = 0xFF5504
YELLOW = 0xFFCA5A
GREEN = 0x00FF00
BLUE = 0x0000FF
INDIGO = 0x0800FF
VIOLET = 0x9400D3
BLACK = 0x000000
WHITE = 0xFFFFFF
GREY = 0x808080
BROWN = 0xA52A2A
PINK = 0xFF69B4
CYAN = 0x00FFFF
PALE_YELLOW = 0xFFCA5A
LILAC = 0x5A5AFF
SEA_GREEN = 0x00FF55
DK_GREY = 0x090909
LT_GREY = 0x404040
LT_BLUE = 0xCCCCFF

MONTHS = {
    1: "JAN",
    2: "FEB",
    3: "MAR",
    4: "APR",
    5: "MAY",
    6: "JUN",
    7: "JUL",
    8: "AUG",
    9: "SEP",
    10: "OCT",
    11: "NOV",
    12: "DEC"
}

DAY_OF_WEEK = {
    0: "SUN",
    1: "MON",
    2: "TUE",
    3: "WED",
    4: "THU",
    5: "FRI",
    6: "SAT"
}
def get_weather_icon(weather_code):
    if weather_code == 1000:
        return "sunny.bmp"
    if weather_code == 1003:
        return "partly_cloudy.bmp"
    elif weather_code in (1006, 1009, 1009):
        return "cloudy.bmp"
    elif weather_code in (1063, 1150, 1153, 1168, 1171):
        return "light_drizzle.bmp"
    elif weather_code in (1066, 1069, 1072, 1210, 1213, 1216, 1219):
        return "light_snow.bmp"
    elif weather_code in (1087, 1279, 1282):
        return "thunderstorms.bmp"
    elif weather_code in (1276, 1279):
        return "thundershowers.bmp"
    elif weather_code in (1114, 1117, 1222, 1225):
        return "blizzard.bmp"
    elif weather_code in (1135, 1147):
        return "fog.bmp"
    elif weather_code in (1180, 1183, 1186, 1189, 1192, 1195):
        return "rain_showers.bmp"
    elif weather_code in (1198, 1201, 1204, 1207, 1237):
        return "ice.bmp"
    else:
        return "unknown.bmp"  # Default icon for unknown weather codes

