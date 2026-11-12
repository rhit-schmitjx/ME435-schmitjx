import flask
import threading
from blinds_control import App

app = flask.Flask(__name__, static_url_path="", static_folder="public")

# Create a lock for thread-safe hardware control (preventing simultaneous stepper steps)
serial_lock = threading.Lock()
stepper = App()
open_deg = 360.0*6

@app.route("/")
def hello_naked_domain():
    return flask.redirect("/index.html")
    
@app.get("/api/blinds/<command>")
def handle_blinds_command(command):
    with serial_lock:
        if command == "open":
            stepper.rotate(open_deg)
            return "Blinds Opened"
        elif command == "close":
            stepper.rotate(-open_deg)
            return "Blinds Closed"
        else:
            return "Unknown command", 400

@app.get("/api/rotate/<degrees>")
def handle_rotate_command(degrees):
    with serial_lock:
        try:
            deg = float(degrees)
            stepper.rotate(deg)
            return f"Rotated {deg} degrees"
        except ValueError:
            return "Invalid degree value", 400

@app.get("/api/alarm/<hour>/<minute>")
def handle_alarm_command(hour, minute):
    with serial_lock:
        try:
            h = int(hour)
            m = int(minute)
            stepper.set_alarm(h, m)
            return f"Alarm successfully set to {h:02d}:{m:02d}"
        except ValueError:
            return "Invalid time format", 400

if __name__ == "__main__":
    print("Running Flask Blinds Server!")
    app.run(host='0.0.0.0', port=5000, use_reloader=False)