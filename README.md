# Tidbyt-Inspired LED Matrix
Inspired by a very targeted ad promoting the [Tidbyt](https://tidbyt.com), I created my own using an LED Matrix and a Raspberry Pi Pico W.
I had a difficult time finding a proper tutorial explaining aspects of this project like the HUB75 transfer protocol or how to connect the jumpers so I'm putting it all in one place here.

I tried it in C++ to have a bit more control over everything as well as improve refresh rate but ran into a few issues (mostly because a lot of the tutorials were in C which I haven't yet learned). I'm planning on coming back to the C/C++ version but for now it's just CircuitPython.

Future features I'm planning to add soon:
- DHT22 Temperature/Humidity Sensor
- On/Off Button

# Setup

## Supplies
- [ ] [64x32 LED Matrix](https://www.amazon.com/Full-Color-Raspberry-Displaying-Adjustable-Brightness/dp/B0B3W1PFY6?th=1)
- [ ] [Barrel Jack Connector](https://www.amazon.com/DAYKIT-Female-2-1x5-5MM-Adapter-Connector/dp/B01J1WZENK/ref=sr_1_1_sspa?crid=1MW115A6TV7YY&keywords=barrel+jack+connector&qid=1693456075&s=electronics&sprefix=barrel+jack%2Celectronics%2C117&sr=1-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1)
- [ ] Raspberry Pi Pico W
- [ ] Data Transfer Micro USB
- [ ] 5V Power Supply (I used 5V/2A)
- [ ] Jumper Wires

## Install CircuitPython
1. Go to the [CircuitPython download page](https://circuitpython.org/board/raspberry_pi_pico_w/) and download the latest CircuitPython firmware for the Raspberry Pi Pico.
2. Connect your Pico to your computer using a USB cable.
3. Press and hold the BOOTSEL button on your Pico, then plug the USB cable into your computer. Continue to hold the BOOTSEL button until the drive named RPI-RP2 appears on your computer.
4. Drag and drop the CircuitPython firmware file onto the RPI-RP2 drive.
5. Wait for the file transfer to complete, then eject the RPI-RP2 drive.
6. The Raspberry Pi Pico will reboot and CircuitPython should be installed.

## Wiring

### Pico to LED Matrix

I strongly suggest soldering the wires directly to the Pico because it will be extremely difficult to troubleshoot wiring issues while debugging code.

Using this diagram connect the wires as follows:
![](<Additional Resources/HUB75 Ribbon Pinout.jpg> "HUB75 Ribbion Wiring")

| Number | Input              | Pico GPIO Pin |
|--------|--------------------|---------------|
| 1      | Ground (GND)       | GND           |
| 2      | Output Enable (OE) | GP13          |
| 3      | Latch (LAT)        | GP12          |
| 4      | Clock (CLK)        | GP10          |
| 5      | D                  | GP9           |
| 6      | C                  | GP8           |
| 7      | B                  | GP7           |
| 8      | A                  | GP6           |
| 9      | E                  | _NONE_        |
| 10     | B2                 | GP5           |
| 11     | G2                 | GP4           |
| 12     | R2                 | GP3           |
| 13     | Ground (GND)       | GND           |
| 14     | B1                 | GP2           |
| 15     | G1                 | GP1           |
| 16     | R1                 | GP0           |
You don't use the E input so I just capped off the wire.
### LED Matrix to Power Supply
Connect the power cable to a barrel jack adapter (Red to + & Black to -) and then to a power supply (or directly to the power supply if you're fancy like that).


