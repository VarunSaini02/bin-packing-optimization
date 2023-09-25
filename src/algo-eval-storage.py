import flask

app = flask.Flask(__name__)

@app.route('/')
def home():
    return "hi from algo-eval-storage"

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port, debug=True)