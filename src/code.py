import gc
import time
import board
import displayio
import framebufferio as fb
import wifi

from displayManager import DisplayManager

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

# If you connected the pins to different ports then you will have to adjust these
matrix = RGBMatrix(
    width=width_value, height=height_value, bit_depth=bit_depth_value,
    rgb_pins=[board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5],
    addr_pins=[board.GP6, board.GP7, board.GP8, board.GP9],
    clock_pin=board.GP10, latch_pin=board.GP12, output_enable_pin=board.GP13,
    tile=tile_down, serpentine=serpentine_value,
    doublebuffer=True,
)

# Associate the RGB matrix with a Display so that we can use displayio features
display = fb.FramebufferDisplay(matrix, auto_refresh=True)

display_system = DisplayManager(display)  # show logo on startup

# Connect to Wi-Fi
while not wifi.radio.ipv4_address:
    try:
        wifi.radio.connect(secrets.SSID, secrets.PASSWORD)
    except ConnectionError as e:
        print("Connection Error:", e)
    time.sleep(10)

gc.collect()  # call garbage collector to free up memory

splash = displayio.Group(max_size=10)
display.show(splash)
color_bitmap = displayio.Bitmap(64, 32, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green
bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette,
                               x=0, y=0)
splash.append(bg_sprite)

while True:
    pass