import requests

print(requests.post('http://127.0.0.1:5000/create/hmmm'))
print(requests.post('http://127.0.0.1:5000/load/hmmm'))
print(requests.post('http://127.0.0.1:5000/add/hmmm',json="{'a':1,'b':2}"))
print(requests.post('http://127.0.0.1:5000/load/hmmm'))
print(requests.post('http://127.0.0.1:5000/remove/hmmm',json="{'a':1,'b':2}"))
print(requests.post('http://127.0.0.1:5000/load/hmmm'))
print(requests.post('http://127.0.0.1:5000/delete/hmmm',))