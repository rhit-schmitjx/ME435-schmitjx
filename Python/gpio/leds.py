import gpiozero as gz
import time
import signal

def basic_on_off():
    print("Basic On / Off")
    green_led = gz.DigitalOutputDevice(18)
    green_led.on()
    time.sleep(3)
    green_led.off()

def fancy_leds():
    print("Fancy LEDs")
    red_led = gz.LED(14)
    blue_led = gz.LED(15)
    green_led = gz.LED(18)

    # green_led.on()
    # time.sleep(3)
    # green_led.off()

    # blue_led.blink(on_time=0.1, off_time=0.1, n=40, background=False)
    red_led.blink(on_time=0.3, off_time=0.3)
    time.sleep(0.1)
    blue_led.blink(on_time=0.3, off_time=0.3)
    time.sleep(0.1)
    green_led.blink(on_time=0.3, off_time=0.3)

    signal.pause()

def led_board():
    print("LED Board")
    
    # TODO: FIgure out how to use a LEDBoard for pins 14,15,18

    # Construct is
    #Make a loop that runs 5 times.
    # Turn on all the LEDs
    # Wait 1 second
    # Turn off all the LEDs
    # Wait 1 second
    # Turn on just red and green
    # Wait 1 second

    led_board = gz.LEDBoard(14,15,18, pwm=True)
    for i in range(5):
        led_board.on()
        time.sleep(1)
        led_board.off()
        time.sleep(1)
        led_board.value = (1,0,1)
        time.sleep(1)
        led_board.value = (0,0.001,0)
        time.sleep(1)

    # (extra challenge) Turn on just yellow at 0.5 brightness
    # Wait 1 second

def main():
    print("Leds")
    # basic_on_off()
    led_board()

main()
