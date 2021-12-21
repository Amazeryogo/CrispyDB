# CrispyDB
A database for my projects.

In a nutshell, its an API that uses the json library to write an read data in json files.
<br/>
*It does have a webUI currently under development*

It uses the following libraries:
```
flask
os
json
requests
jinja
flask limiter
flask WTF forms
```

The WebUI is really janky and still in development.
<br/>
*Also dont expect the WebUI to be very fancy like the dashboard for kubernetes*

Here is a sample script to test the DB
```python
#python
print(requests.post('http://127.0.0.1:5000/create/hmmm',auth=('admin','admin')).text)
print(requests.post('http://127.0.0.1:5000/load/hmmm',auth=('admin','admin')).text)    
print(requests.post('http://127.0.0.1:5000/add/hmmm',json={'a':1,'b':2},auth=('admin','admin')).text)
print(requests.post('http://127.0.0.1:5000/load/hmmm',auth=('admin','admin')).text)
print(requests.post('http://127.0.0.1:5000/remove/hmmm',json={'a':1,'b':2},auth=('admin','admin')).text)
print(requests.post('http://127.0.0.1:5000/load/hmmm',auth=('admin','admin')).text)
print(requests.post('http://127.0.0.1:5000/delete/hmmm',auth=('admin','admin')).text)
```


**I might make a python library for it, if anyone uses it....**

### For some tweaking or changes, try seeing config/config.json

## I hope this project is helpful, if it isnt..... well you should use MongoDB instead.
