import flask
import requests

app = flask.Flask(__name__)

@app.route('/')
def home():
    return "hi from algo-eval"

@app.route('/ping/<hostname>')
def ping(hostname):
    return requests.get(f"http://{hostname}:5000").text

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port, debug=True)

    