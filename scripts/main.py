import requests
print(requests.post('http://0.0.0.0:5000/create/hmmm',auth=('admin','admin')).text)
print(requests.post('http://0.0.0.0:5000/changeauth?newpassword=cringe',auth=('admin','admin')).text)
# creates a collection called hmmm
print(requests.get('http://0.0.0.0:5000/getdata/hmmm',auth=('admin','admin')).text)
# returns the data in the collection hmmm (which should be [])
print(requests.post('http://0.0.0.0:5000/add/hmmm',json={'a':1,'b':2},auth=('admin','admin')).text)
# adds the data to the collection hmmm
print(requests.get('http://0.0.0.0:5000/getdata/hmmm',auth=('admin','admin')).text)
# returns the data in the collection hmmm (which should be [{'a':1,'b':2}])
#print(requests.post('http://0.0.0.0:5000/remove/hmmm',json={'a':1,'b':2},auth=('admin','admin')).text)
# removes the data from the collection hmmm
print(requests.get('http://0.0.0.0:5000/getdata/hmmm',auth=('admin','admin')).text)
# returns the data in the collection hmmm (which should be [])
#print(requests.post('http://0.0.0.0:5000/delete/hmmm',auth=('admin','admin')).text)
# deletes the collection hmmm

# Usually, we have a list to keep all your json in memory, if you want to save your data, you must send a request to
# /save
print(requests.post('http://0.0.0.0:5000/save',auth=('admin','admin')).text)