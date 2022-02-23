# CrispyDB
CrispyDB is a simple database for storing and retrieving data designed to be used in applications that don't require a huge and feature-rich database.

## Features
* Uses Json to store data
* Uses GET and POST requests to store and retrieve data instead of queries
* Has a fancy GUI web interface called WebUI



### It uses the following libraries:
* Flask
* OS
* JSON
* Jinja
* Bootstrap
* Requests
* Flask limiter
* Flask WTF forms



## How to run the database
```shell
$ git clone https://github.com/Amazeryogo/CrispyDB
$ cd CrispyDB
$ nano config/.config.json # change the settings
# for installing the requirements
$ bash run.sh install
# now for the web server
$ bash run.sh
# for the cli
$ bash run.sh cli
```



## Here is a simple example of how to use CrispyDB
```python
import requests
print(requests.post('http://127.0.0.1:5000/create/hmmm',auth=('admin','admin')).text)
# creates a collection called hmmm
print(requests.get('http://127.0.0.1:5000/getdata/hmmm',auth=('admin','admin')).text)
# returns the data in the collection hmmm (which should be [])
print(requests.post('http://127.0.0.1:5000/add/hmmm',json={'a':1,'b':2},auth=('admin','admin')).text)
# adds the data to the collection hmmm
print(requests.get('http://127.0.0.1:5000/getdata/hmmm',auth=('admin','admin')).text)
# returns the data in the collection hmmm (which should be [{'a':1,'b':2}])
print(requests.post('http://127.0.0.1:5000/remove/hmmm',json={'a':1,'b':2},auth=('admin','admin')).text)
# removes the data from the collection hmmm
print(requests.get('http://127.0.0.1:5000/getdata/hmmm',auth=('admin','admin')).text)
# returns the data in the collection hmmm (which should be [])
print(requests.post('http://127.0.0.1:5000/delete/hmmm',auth=('admin','admin')).text)
# deletes the collection hmmm

# Usually, we have a list to keep all your json in memory, if you want to save your data, you must send a request to /save
print(requests.post('http://127.0.0.1:5000/save',auth=('admin','admin')).text)
```
### The License
```
MIT License

Copyright (c) 2021 Suvid Datta

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
