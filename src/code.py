import gc  # garbage collection
from time import monotonic, localtime

import board  # board for LED
import displayio
from framebufferio import FramebufferDisplay
from rgbmatrix import RGBMatrix
from wifi import radio
from digitalio import DigitalInOut, Direction, Pull  # digital input/output for LED
from rtc import RTC

from displayManager import DisplayManager  # manage display

# set up display
displayio.release_displays()
matrix = RGBMatrix(
    width=64, height=32, bit_depth=6, rgb_pins=[board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5],
    addr_pins=[board.GP6, board.GP7, board.GP8, board.GP9],
    clock_pin=board.GP10, latch_pin=board.GP12, output_enable_pin=board.GP13)

# Associate the RGB matrix with a Display so that we can use displayio features
display = FramebufferDisplay(matrix, auto_refresh=False, rotation=0)

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

print("SETUP COMPLETE")
displayScreen = 0
prev_time = monotonic()
pause = .5
NUM_SCREENS = 3
display_settings = False
holding = False
settings_time = 5
prev_settings_time = monotonic()
while True:
    if button.value:  # button is pushed switch screens
        if not holding:
            prev_settings_time = monotonic()
            holding = True

        if monotonic() - prev_time >= pause:
            displayScreen += 1
            displayScreen %= NUM_SCREENS
            prev_time = monotonic()

        if holding and monotonic() - prev_settings_time >= settings_time:
            display_settings = True
            displayScreen = -1
    else:
        holding = False
    # loop through screens when button is pushed
    if displayScreen == 0:
        manager.display_weather()
    elif displayScreen == 1:
        manager.display_time()
    elif displayScreen == 2:
        manager.display_sun_times()
    elif displayScreen == -1:
        manager.display_settings()

    # indicate wifi connection
    if radio.ipv4_address:
        led.value = True
    else:
        led.value = False

    if (displayScreen == 1 or displayScreen == 0) and localtime()[5] == 0:
        try:
            manager.update_time()
            if localtime()[3] == 0 and localtime()[4] == 0:
                manager.update_weather()  # if its a new day get the new weather
        except MemoryError as e:
            manager.settings = None # free up memory by removing settings screen
            print(e)
            gc.collect()

    display.refresh(target_frames_per_second=10, minimum_frames_per_second=0)
