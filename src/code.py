import gc
import time
import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import wifi
from adafruit_imageload import load
import secrets
from displayManager import DisplayManager
from digitalio import DigitalInOut, Direction
import socketpool
import adafruit_ntp
import rtc

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=6, rgb_pins=[board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5],
    addr_pins=[board.GP6, board.GP7, board.GP8, board.GP9],
    clock_pin=board.GP10, latch_pin=board.GP12, output_enable_pin=board.GP13)

# Associate the RGB matrix with a Display so that we can use displayio features
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False, rotation=0)

#
# scroll_text = adafruit_display_text.label.Label(
#     terminalio.FONT,
#     color=0x0080ff,
#     text="Testing scrolling text")
# scroll_text.x = display.width
# scroll_text.y = 24

# Put each line of text into a Group, then show that group.
# g = displayio.Group()
# g.append(scroll_text)
# display.show(g)

gc.collect()
manager = DisplayManager(display)
manager.display_logo()
gc.collect()

# logo_bitmap, logo_palette = load(secrets.LOGO_PATH,
#                                  bitmap=displayio.Bitmap,
#                                  palette=displayio.Palette)
# logo_palette[1] = 0x000000
#
# TILEGRID = displayio.TileGrid(bitmap=logo_bitmap,
#                               pixel_shader=logo_palette,
#                               x=32-logo_bitmap.width//2,
#                               y=16-logo_bitmap.height//2)
# for optimization?
# BITMAP = displayio.OnDiskBitmap(FILENAME)
# PALETTE = BITMAP.pixel_shader
# TILEGRID = displayio.TileGrid(
#     BITMAP,
#     pixel_shader=PALETTE,
#     tile_width=BITMAP.width,
#     tile_height=BITMAP.height)

# GROUP = displayio.Group(scale=1)
# GROUP.append(TILEGRID)
#
# display.show(GROUP)
display.refresh()

while not wifi.radio.ipv4_address:
    try:
        wifi.radio.connect(secrets.SSID, secrets.PASSWORD)
    except ConnectionError as e:
        print("Conn Error:", e)
    print("Connected to", secrets.SSID, "\nIP Address:", wifi.radio.ipv4_address)
    time.sleep(10)
# set RTC
pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=0)
rtc.RTC().datetime = ntp.datetime
gc.collect()
display.refresh()
manager.display_time()
display.refresh()



# frame = Rect(0,0,64,32, fill=0x00FF00)  # Green color (0x00FF00)
# connected = displayio.Group(scale=1)
# connected.append(frame)
# # connected.append(TILEGRID)
# display.show(connected)
# display.refresh()


gc.collect()


# display.show(None)
# scroll(line2)
# display.refresh(target_frames_per_second=10, minimum_frames_per_second=0)

while True:
    # set brightness

    # indicate wifi connection
    if wifi.radio.ipv4_address:
        led.value = True
    else:
        led.value = False

    pass
