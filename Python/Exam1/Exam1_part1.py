import flask
import threading
import LEDOnOff

app = flask.Flask(__name__, static_url_path="", static_folder="public")

serial_lock = threading.Lock()
LED = LEDOnOff.LEDOnOff() 
LED.connect()         

@app.route("/")
def hello_naked_domain():
    return flask.redirect("/index.html")
    
@app.get("/api/led/<command>")
def handle_LED_commands(command):
    with serial_lock:
        response = LED.onOff("LED " + command)
    return response

@app.get("/api/flash/<numFlashes>/<timeDelay>")
def handle_Flash_commands(numFlashes, timeDelay):
    with serial_lock:
        # response = LED.flash("Flash " + numFlashes + " " + timeDelay)
        response = LED.flash(numFlashes, timeDelay)
    return response

if __name__ == "__main__":
    print("Running Flask!")
    app.run(host='0.0.0.0', port=5000, use_reloader=False) # use_reloader=False
    print("Hi")

