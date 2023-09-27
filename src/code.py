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

# OPTIONAL: set up button for screen switching
button = DigitalInOut(board.GP14)
button.direction = Direction.INPUT
button.pull = Pull.DOWN


# set up display manager and display logo
manager = DisplayManager(display, led)
display.refresh(target_frames_per_second=10, minimum_frames_per_second=0)
manager.setup()

gc.collect()
print("SETUP COMPLETE")
displayScreen = 0
prev_time = time.monotonic()
pause = .5
NUM_SCREENS = 3
while True:
    if time.monotonic() - prev_time >= pause and button.value: # button is pushed switch screens
        displayScreen += 1
        displayScreen %= NUM_SCREENS
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

    display.refresh(target_frames_per_second=10, minimum_frames_per_second=0)
