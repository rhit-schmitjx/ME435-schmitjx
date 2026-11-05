import flask

app = flask.Flask(__name__)

@app.route("/")
def hello_route():
    return "Hello, World!! Joey - computer"
    


if __name__ == "__main__":
    print("Running Flask!")
    app.run(host='0.0.0.0', port=8080, debug=True) # use_reloader=False

