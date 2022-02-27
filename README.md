# CrispyDB
CrispyDB is a simple database for storing and retrieving data designed to be used in applications that don't require a huge and feature-rich database.

## Features
* Uses Json to store data
* Uses GET and POST requests to store and retrieve data instead of queries
* Has a fancy GUI web interface called WebUI
* Has a cli written in bash to make it an executable script to be used anywhere



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
```bash
TOKEN="1e533624-1ea6-4106-9f61-a557cc917632"

# to make sure it is running
curl http://0.0.0.0:5000/
# create a new collection called collection
curl http://0.0.0.0:5000/create/collection?token=$TOKEN
# get the data from the collection (should be empty)
curl http://0.0.0.0:5000/getdata/collection?token=$TOKEN
# add some data to the collection
curl http://0.0.0.0:5000/add/collection?token=$TOKEN  --header "Content-Type: application/json" --request POST --data '{"name":"test","_crispy-id":1}'
# get data again
curl http://0.0.0.0:5000/getdata/collection?token=$TOKEN
# remove the data from the collection
curl http://0.0.0.0:5000/removefrom/collection?token=$TOKEN  --header "Content-Type: application/json" --request POST --data '{"name":"test","_crispy-id":1}'
# get data again which should be empty again
curl http://0.0.0.0:5000/getdata/collection?token=$TOKEN
# delete the collection
curl http://0.0.0.0:5000/delete/collection?token=$TOKEN
```
or in python
```python3
import requests
TOKEN="1e533624-1ea6-4106-9f61-a557cc917632"

requests.get("http://0.0.0.0:5000/")
requests.get("http://0.0.0.0:5000/create/collection?token={}".format(TOKEN))
requests.get("http://0.0.0.0:5000/getdata/collection?token={}".format(TOKEN))
requests.post("http://0.0.0.0:5000/add/collection?token={}".format(TOKEN), json={"name":"test","_crispy-id":1})
requests.post("http://0.0.0.0:5000/getdata/collection?token={}".format(TOKEN))
requests.post("http://0.0.0.0:removefrom/collection?token={}".format(TOKEN), json={"name":"test","_crispy-id":1})
requests.post("http://0.0.0.0:5000/getdata/collection?token={}".format(TOKEN))
requests.post("http://0.0.0.0:5000/delete/collection?token={}".format(TOKEN))
```
#### NOTE: YOU NEED TO MAKE A TOKEN USING /create/token endpoint

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
