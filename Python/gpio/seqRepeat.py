import gpiozero as gz
import time
import signal

def main():
    print("Reverse Simon Game Starting...")

    red_led = gz.LED(14)
    yellow_led = gz.LED(15)
    green_led = gz.LED(18)

    red_button = gz.Button(22)
    yellow_button = gz.Button(23)
    green_button = gz.Button(24)
    play_button = gz.Button(25)

    pattern = []


    red_button.when_pressed = lambda: (red_led.on(), pattern.append(red_led))
    red_button.when_released = lambda: red_led.off()
    yellow_button.when_pressed = lambda: (yellow_led.on(), pattern.append(yellow_led))
    yellow_button.when_released = lambda: yellow_led.off()
    green_button.when_pressed = lambda: (green_led.on(), pattern.append(green_led))
    green_button.when_released = lambda: green_led.off()

    def play():
        
        red_led.off()
        yellow_led.off()
        green_led.off()
        time.sleep(0.1)

        for led in pattern:
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.1)

        pattern.clear()

    play_button.when_pressed = play
    signal.pause()

if __name__ == "__main__":
    main()