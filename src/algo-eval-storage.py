import flask
from flask import jsonify
from random import randint

app = flask.Flask(__name__)

@app.route('/')
def home():
    return "hi from algo-eval-storage"

@app.route('/get-test-items/<num_items>/<max_bin_size>')
def get_test_items(num_items, max_bin_size):
    return jsonify({
        "items": [randint(1, int(max_bin_size)) for _ in range(int(num_items))]
    })

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port, debug=True)