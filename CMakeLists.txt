cmake_minimum_required(VERSION 3.13)

# initialize the SDK based on PICO_SDK_PATH
# note: this must happen before project()
include(pico_sdk_import.cmake)
# set(PICO_BOARD pico_w)

project(picow_blink)

pico_sdk_init()

# initialize the Raspberry Pi Pico SDK

add_executable(picow_blink
    main.cpp
    picow_blink.c
)

# Add the required libraries
target_link_libraries(picow_blink
    pico_stdlib
    pico_cyw43_arch_none
)

# create map/bin/hex/uf2 file in addition to ELF.
pico_add_extra_outputs(picow_blink)