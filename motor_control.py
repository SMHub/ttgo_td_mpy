from machine import Pin
import time

# Motor control pins
motor_pin1 = Pin(32, Pin.OUT)
motor_pin2 = Pin(33, Pin.OUT)

# Hall sensor pin
hall_pin = Pin(39, Pin.IN)

# Button pin (using pull-up resistor)
button_pin = Pin(35, Pin.IN, Pin.PULL_UP)

# Step counter
step_count = 0

def motor_forward():
    motor_pin1.value(1)
    motor_pin2.value(0)
    print("Motor forward")

def motor_backward():
    motor_pin1.value(0)
    motor_pin2.value(1)
    print("Motor backward")

def motor_stop():
    motor_pin1.value(0)
    motor_pin2.value(0)
    print("Motor stopped")

# Hall sensor interrupt handler
def hall_interrupt_handler(pin):
    global step_count
    step_count += 1
    print("Step:", step_count)

# Set up hall sensor interrupt
hall_pin.irq(trigger=Pin.IRQ_RISING, handler=hall_interrupt_handler)

# Button interrupt handler
def button_interrupt_handler(pin):
    global step_count
    step_count = 0
    print("Step counter reset!")

# Set up button interrupt (falling edge, because of pull-up)
button_pin.irq(trigger=Pin.IRQ_FALLING, handler=button_interrupt_handler)

while True:
    motor_forward()
    time.sleep(5)

    motor_stop()
    time.sleep(2)

    motor_backward()
    time.sleep(5)

    motor_stop()
    time.sleep(2)

    # Optional: Print total steps (uncomment if needed)
    # print("Total steps:", step_count)
    # time.sleep(1)
