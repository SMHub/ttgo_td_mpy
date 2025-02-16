
import random #for random number generation (like random color)
import st7789 #for display
import time #mostly fro sleep
from machine import Pin, SPI # for display and buttons
import math #math for pi value
from sysfont import sysfont #sysfont for drawing text


BL_Pin = 4     #backlight pin
SCLK_Pin = 18  #clock pin
MOSI_Pin = 19  #mosi pin
MISO_Pin = 2   #miso pin
RESET_Pin = 23 #reset pin
DC_Pin = 16    #data/command pin
CS_Pin = 5     #chip select pin

Button1_Pin = 35; #right button
Button2_Pin = 0;  #left button
button1 = Pin(Button1_Pin, Pin.IN, Pin.PULL_UP)
button2 = Pin(Button2_Pin, Pin.IN, Pin.PULL_UP)

rotation=6

def callback_b1(p):
    clear_screen()

def callback_b2(p):
    fill_random_color()

button1.irq(trigger=Pin.IRQ_FALLING, handler=callback_b1) #interrupt for right button (button 2)
button2.irq(trigger=Pin.IRQ_FALLING, handler=callback_b2) #interrupt for left button (button 1)

BLK = Pin(BL_Pin, Pin.OUT)
spi = SPI(baudrate=40000000, miso=Pin(MISO_Pin), mosi=Pin(MOSI_Pin, Pin.OUT), sck=Pin(SCLK_Pin, Pin.OUT))
display = st7789.ST7789(spi, 135, 240, cs=Pin(CS_Pin), dc=Pin(DC_Pin), rst=None)

def clear_screen():
    display._set_mem_access_mode(rotation, False, False, False)
    display.fill(0) #filling the display with black

def fill_random_color():
    fill_hline()
    fill_vline()
    display.fill(random_color())
    display._set_mem_access_mode(rotation, False, False, False)

def fill_hline():
    display._set_mem_access_mode(rotation, False, False, False)
    for i in range(0,240):
      display.hline(0, i, 65, st7789.color565(random.getrandbits(8),random.getrandbits(8),random.getrandbits(8)))

    display._set_mem_access_mode(1, False, False, False)
    for i in range(0,240):
      display.hline(0, i, 65, st7789.color565(random.getrandbits(8),random.getrandbits(8),random.getrandbits(8)))

    clear_screen()


def fill_vline():
    display._set_mem_access_mode(rotation, False, False, False)
    for i in range(0,135):
      display.vline(i, 0, 110, st7789.color565(random.getrandbits(8),random.getrandbits(8),random.getrandbits(8)))

    display._set_mem_access_mode(rotation, False, False, False)
    for i in range(0,135):
      display.vline(i, 0, 110, st7789.color565(random.getrandbits(8),random.getrandbits(8),random.getrandbits(8)))

    clear_screen()

def random_color():
    return st7789.color565(random.getrandbits(8),random.getrandbits(8),random.getrandbits(8))

start_time = time.time()  # Record the start time

def format_elapsed_time(seconds):
    hours = int(seconds // 3600)  # Integer division and convert to int
    minutes = int((seconds % 3600) // 60)  # Integer division and convert to int
    remaining_seconds = int(seconds % 60)  # Modulo and convert to int

    # Use string formatting to ensure leading zeros and correct types
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, remaining_seconds)


def main():
    time_sec = 0
    clear_screen() #clear screen by filling black rectangle (slow)
    BLK.value(1) #turn backlight on
    display._set_mem_access_mode(rotation, False, False, True) #setting screen orientation (rotation (0-7), vertical mirror, horizonatal mirror, is bgr)

    while True:
      clear_screen()
      BLK.value(1)
      display.fill(0);
      v = 20
      display.text((0, v), "Time", random_color(), sysfont, 3, nowrap=True)
      
      elapsed_seconds = time.time() - start_time
      elapsed_time_str = format_elapsed_time(elapsed_seconds)
      display.text((80, v), elapsed_time_str, random_color(), sysfont, 3, nowrap=True)
      
      v += sysfont["Height"]+20
      display.text((0, v), "Prog.", random_color(), sysfont, 3, nowrap=True)
      v += sysfont["Height"] * 2+10
      display.text((0, v), "CC", random_color(), sysfont, 3, nowrap=True)
      v += sysfont["Height"] * 3+10
      display.text((0, v), str(1234), random_color(), sysfont, 4, nowrap=True)
      time.sleep_ms(1000)
      display.fill(0);
      time.sleep(2)
      BLK.value(0)
      time_sec=time_sec+3

main() #execute the main() function so that we don't have to execute manually in repl

