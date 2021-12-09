import requests

while True:
    print(requests.post('http://127.0.0.1:5000/create/hmmm',auth=('sus','sus')).text)
    print(requests.post('http://127.0.0.1:5000/load/hmmm',auth=('sus','sus')).text)
    print(requests.post('http://127.0.0.1:5000/add/hmmm',json={'a':1,'b':2},auth=('sus','sus')).text)
    print(requests.post('http://127.0.0.1:5000/load/hmmm',auth=('sus','sus')).text)
    print(requests.post('http://127.0.0.1:5000/remove/hmmm',json="{'a':1,'b':2}",auth=('sus','sus')).text)
    print(requests.post('http://127.0.0.1:5000/load/hmmm',auth=('sus','sus')).text)
    print(requests.post('http://127.0.0.1:5000/delete/hmmm',auth=('sus','sus')).text)