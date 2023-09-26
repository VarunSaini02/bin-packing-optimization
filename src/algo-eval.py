import flask
from flask import jsonify
import requests

app = flask.Flask(__name__)

@app.route('/')
def home():
    return "hi from algo-eval"

@app.route('/compare/<num_runs>/<num_items>/<max_bin_size>', defaults={
    'endpt1': "alex",
    'endpt2': "carla",
})
@app.route('/compare/<endpt1>/<endpt2>/<num_runs>/<num_items>/<max_bin_size>')
def compare(endpt1, endpt2, num_runs, num_items, max_bin_size):
   
    default_port = 5000

    endpt1_id = requests.get(f"http://{endpt1}:{default_port}/newproblem/{max_bin_size}").json()["ID"]
    endpt2_id = requests.get(f"http://{endpt2}:{default_port}/newproblem/{max_bin_size}").json()["ID"]

    for i in range(int(num_runs)):
        items_json = requests.get(f"http://algo-eval-storage:{default_port}/get-test-items/{num_items}/{max_bin_size}").json()
        items = items_json["items"]
        
        for i in range(len(items)):
            requests.get(f"http://{endpt1}:{default_port}/placeitem/{endpt1_id}/{items[i]}")
            requests.get(f"http://{endpt2}:{default_port}/placeitem/{endpt2_id}/{items[i]}")

    endpt1_res = requests.get(f"http://{endpt1}:{default_port}/endproblem/{endpt1_id}").json()
    endpt2_res = requests.get(f"http://{endpt2}:{default_port}/endproblem/{endpt2_id}").json()
    
    endpt1_total_bins = int(endpt1_res["count"])
    endpt1_total_wasted_space = int(endpt1_res["wasted"])

    endpt2_total_bins = int(endpt2_res["count"])
    endpt2_total_wasted_space = int(endpt2_res["wasted"])

    return jsonify({
        "test_metadata": {
            "num_runs": num_runs,
            "num_items_per_run": num_items,
            "max_bin_size": max_bin_size,
        },
        endpt1: {
            "average_num_items_per_bin": (int(num_items) * int(num_runs)) / endpt1_total_bins,
            "average_percent_wasted_(%)": 100 * endpt1_total_wasted_space / (endpt1_total_bins * int(max_bin_size)),
            "average_amount_wasted_per_item": endpt1_total_wasted_space / (int(num_items) * int(num_runs)),
        },
        endpt2: {
            "average_num_items_per_bin": (int(num_items) * int(num_runs)) / endpt2_total_bins,
            "average_percent_wasted_(%)": 100 * endpt2_total_wasted_space / (endpt2_total_bins * int(max_bin_size)),
            "average_amount_wasted_per_item": endpt2_total_wasted_space / (int(num_items) * int(num_runs)),
        }
    })

@app.route('/ping/<hostname>')
def ping(hostname):
    return requests.get(f"http://{hostname}:{default_port}").text

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port, debug=True)

    