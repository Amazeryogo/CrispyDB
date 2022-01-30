import requests
import time

print(requests.post('http://0.0.0.0:5000/create/hmmm',auth=('admin','admin')).text)

while True:
    print(requests.get('http://0.0.0.0:5000/getdata/hmmm',auth=('admin','admin')).text)
    print(requests.post('http://0.0.0.0:5000/add/hmmm',json={'a':1,'b':2},auth=('admin','admin')).text)
    print(requests.get('http://0.0.0.0:5000/getdata/hmmm',auth=('admin','admin')).text)
    print(requests.post('http://0.0.0.0:5000/remove/hmmm',json={'a':1,'b':2},auth=('admin','admin')).text)
    print(requests.get('http://0.0.0.0:5000/getdata/hmmm',auth=('admin','admin')).text)
    print(requests.post('http://0.0.0.0:5000/save',auth=('admin','admin')).text)
    time.sleep(1)