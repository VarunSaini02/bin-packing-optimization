import requests

# new problem
api_command = 'newproblem'

# test new problem
print(requests.get('http://localhost:5001/' + api_command + '/').text)
print(requests.get('http://localhost:5001/' + api_command + '/').text)

print(requests.get('http://localhost:5001/placeitem/0/60').text)
# test that item that doesn't fit goes to new bin
print(requests.get('http://localhost:5001/placeitem/0/60').text)
# test that code will retroactively add to old bin
print(requests.get('http://localhost:5001/placeitem/0/20').text)
# test that you cannot place object bigger than 100
print(requests.get('http://localhost:5001/placeitem/0/101').text)

print(requests.get('http://localhost:5001/endproblem/0/').text)
# test that you cannot add to closed problem
print(requests.get('http://localhost:5001/placeitem/0/20').text)



