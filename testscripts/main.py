import requests
print(requests.post('http://127.0.0.1:5000/create/hmmm',auth=('admin','admin')).text)
print(requests.get('http://127.0.0.1:5000/getdata/hmmm',auth=('admin','admin')).text)
print(requests.post('http://127.0.0.1:5000/add/hmmm',json={'a':1,'b':2},auth=('admin','admin')).text)
print(requests.get('http://127.0.0.1:5000/getdata/hmmm',auth=('admin','admin')).text)
print(requests.post('http://127.0.0.1:5000/remove/hmmm',json={'a':1,'b':2},auth=('admin','admin')).text)
print(requests.get('http://127.0.0.1:5000/getdata/hmmm',auth=('admin','admin')).text)
print(requests.post('http://127.0.0.1:5000/delete/hmmm',auth=('admin','admin')).text)
# Usually, we have a list to keep all your json in memory, if you want to save your data, you must send a request to /save
print(requests.post('http://127.0.0.1:5000/save',auth=('admin','admin')).text)