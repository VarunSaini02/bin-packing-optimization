import flask
from flask import jsonify

app = flask.Flask(__name__)

binsList = []
binsSizeList = []

@app.route('/')
def home():
    return "hi from alex"

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
    bins = problem[2:-2].split('#')
    added = False
    for i in range(len(bins)):
        sizeList = bins[i].split('!')
        if sizeList[0] == '':
            bins[i] = size
            loc = i + 1
            added = True
            break
        spaceTaken = 0
        for item in sizeList:
            spaceTaken += int(item)
        if spaceTaken + size <= binsSizeList[problemID]:
            bins[i] += '!' + str(size)
            loc = i + 1
            added = True
            break
    if not added:
        bins.append(size)
        loc = len(bins)
    final = '##'
    for bin in bins:
        final += str(bin) + '#'
    final += '' if len(bins) == 0 else '#'
    binsList[problemID] = final

    return {
        'ID': problemID,
        'size': size,
        'loc': loc,
        'bins': final,
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