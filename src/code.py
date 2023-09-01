import time
import board
import displayio
import framebufferio
import wifi


from displayManager import DisplayManager
from analytics import YouTubeAnalytics

from rgbmatrix import RGBMatrix

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

bit_depth_value = 1
base_width = 64
base_height = 32
chain_across = 1
tile_down = 1
serpentine_value = True

width_value = base_width * chain_across
height_value = base_height * tile_down

displayio.release_displays()

matrix = RGBMatrix(
    width=width_value, height=height_value, bit_depth=bit_depth_value,
    rgb_pins=[board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5],
    addr_pins=[board.GP6, board.GP7, board.GP8, board.GP9],
    clock_pin=board.GP10, latch_pin=board.GP12, output_enable_pin=board.GP13,
    tile=tile_down, serpentine=serpentine_value,
    doublebuffer=True,
)

# Associate the RGB matrix with a Display so that we can use displayio features
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)

display_system = DisplayManager(display)
# youtubeAnalytics = YouTubeAnalytics(secrets)

display_system.display_logo()

recheck_delay = 600
last_recheck = 0


matrix.fill(0)



while True:

    wifi_ssid = secrets['ssid']
    wifi_pass = secrets['password']

    # Connect to Wi-Fi
    while not wifi.radio.ipv4_address:
        try:
            wifi.radio.connect(self._wifi_ssid, self._wifi_pass)
        except ConnectionError as e:
            print("Connection Error:", e)
        time.sleep(10)
        gc.collect()
    if time.time() - last_recheck > recheck_delay:
        # Blocking call which returns when the get_analytics() http request is done
        # Tried async, but not enough room on pico
        sub_count = youtubeAnalytics.get_analytics()
        display_system.update_sub_count(sub_count)
        last_recheck = time.time()

    display_system.update()