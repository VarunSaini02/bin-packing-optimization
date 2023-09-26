import flask
from flask import jsonify

app = flask.Flask(__name__)

binsList = []
binsSizeList = []

@app.route('/')
def home():
    return "hi from carla"

@app.route('/newproblem/', defaults={'bin_size': 100})
@app.route('/newproblem/<bin_size>')
def newproblem(bin_size):
    id = len(binsList)
    binEncoding = "##"
    binsList.append(binEncoding)
    binsSizeList.append(int(bin_size))
    newproblem = {'ID': id, 'bins': binEncoding}
    return newproblem

@app.route('/placeitem/<problemID>/<size>/')
def placeitem(problemID, size):
    problemID = int(problemID)
    size = int(size)
    if binsList[problemID][-1] == 'c':
        return "This list is closed. You can no longer add to it."
    problem = binsList[problemID]
    if size > binsSizeList[problemID] :
        return f"Failed to add to bin. Item is sized greater than {binsSizeList[problemID]}."

    bins = []
    if len(problem[2:-2]) != 0:
        bins = problem[2:-2].split('#')
    bins.append(size)

    binsList[problemID] = '##' + "#".join(str(i) for i in bins)
    if len(bins) != 0:
        binsList[problemID] += '##'

    return {
        'ID': problemID,
        'size': size,
        'loc': len(bins),
        'bins': binsList[problemID],
    }

@app.route('/endproblem/<problemID>/')
def endProblem(problemID):
    problemID = int(problemID)
    data = {'ID': problemID}
    if len(binsList[problemID]) == 2:
        return {'ID': problemID, 'size': 0, 'items': 0, 'count': 0, 'wasted': 0, 'bins': '##'}
    if binsList[problemID][-1] == 'c':
        binsList[problemID] = binsList[problemID][:-1]
    binData = binsList[problemID][2:-2]
    bins = binData.split("#")
    totalSize = 0
    numItems = 0
    for bin in bins:
        items = bin.split("!")
        for item in items:
            numItems += 1
            totalSize += int(item)
    data['size'] = totalSize
    data['items'] = numItems
    data['count'] = len(bins)
    data['wasted'] = data['count'] * binsSizeList[problemID] - totalSize
    data['bins'] = binsList[problemID]
    binsList[problemID] += 'c'
    return jsonify(data)


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port, debug=True)