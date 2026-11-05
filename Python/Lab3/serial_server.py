import flask
import plateLoader
import threading

app = flask.Flask(__name__, static_url_path="", static_folder="public")

serial_lock = threading.Lock()
loader = plateLoader.PlateLoader() # TODO: Set the port if needed.

@app.route("/")
def hello_naked_domain():
    return flask.redirect("/index.html")
    
@app.get("/api/<command>")
def handle_plateloader_commands(command):
    with serial_lock:
        response = loader.send_command(command)
    return response

if __name__ == "__main__":
    print("Running Flask!")
    loader.connect()
    app.run(host='0.0.0.0', port=8080, use_reloader=False) # use_reloader=False

