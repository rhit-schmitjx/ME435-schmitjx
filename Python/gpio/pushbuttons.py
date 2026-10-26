import gpiozero as gz
import time
import signal

def buttons_state():
    button = gz.Button(25)

    while True:
        if button.is_pressed:
            print("Button is pressed")
        else:
            print("Button is NOT pressed")
        time.sleep(0.5)

def function_using_def():
    print("This is a function using the keyword def")
    print("It can have many lines")

function_using_lambda = lambda: print("This is a func object using the keyword lambda")

def some_helper_function(led_board, brightness):
    print("Some helper function")
    led_board.value = (brightness, 0, brightness)
    time.sleep(1)
    led_board.off()
    time.sleep(1)

def button_events():
    print("Button Events")
    button = gz.Button(25)
    led_board = gz.LEDBoard(14,15,18)

    button.when_pressed = function_using_def
    button.when_released = function_using_lambda
    button.when_held = lambda: some_helper_function(led_board, 0.3)
    
    signal.pause()

def main():
    print("Pushbuttons")
    # buttons_state()
    button_events()


main()