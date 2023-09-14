import gc  # garbage collection
import time

import board  # board for LED
import displayio
import framebufferio
import rgbmatrix
import wifi
from digitalio import DigitalInOut, Direction, Pull  # digital input/output for LED
from rtc import RTC

from displayManager import DisplayManager  # manage display

# set up display
displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=6, rgb_pins=[board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5],
    addr_pins=[board.GP6, board.GP7, board.GP8, board.GP9],
    clock_pin=board.GP10, latch_pin=board.GP12, output_enable_pin=board.GP13)

# Associate the RGB matrix with a Display so that we can use displayio features
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False, rotation=0)

# set up LED for wifi connection indicator
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

button = DigitalInOut(board.GP14)
button.direction = Direction.INPUT
button.pull = Pull.DOWN

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

# set up display manager and display logo
manager = DisplayManager(display, led)
display.refresh(target_frames_per_second=10, minimum_frames_per_second=0)
manager.setup()
# manager.display_weather()
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

# frame = Rect(0,0,64,32, fill=0x00FF00)  # Green color (0x00FF00)
# connected = displayio.Group(scale=1)
# connected.append(frame)
# # connected.append(TILEGRID)
# display.show(connected)
# display.refresh()

# display.show(None)
# scroll(line2)
# display.refresh(target_frames_per_second=10, minimum_frames_per_second=0)

print("entering loop!")
displayScreen = 0
prev_time = time.monotonic()
pause = .5
while True:

    # manager.display_time()
    if time.monotonic() - prev_time >= pause and button.value:
        displayScreen += 1
        displayScreen %= 3
        prev_time = time.monotonic()

    # loop through screens when button is pushed
    if displayScreen == 0:
        manager.display_weather()
    elif displayScreen == 1:
        manager.display_time()
    else:
        manager.display_animation()

    # indicate wifi connection
    if wifi.radio.ipv4_address:
        led.value = True
    else:
        led.value = False

    if time.localtime()[5] == 0:
        manager.update_time()

    # time.monotonic()
    # if not manager.current_time.hidden:
    #     manager.update_time()
    display.refresh(target_frames_per_second=10, minimum_frames_per_second=0)
