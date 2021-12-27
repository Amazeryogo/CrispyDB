# CrispyDB
A database for my projects.

In a nutshell, its an API that uses the json library to read and write data in json files.
<br/>
*It does have a webUI currently under development*

The WebUI is really janky and still in development.
<br/>
*Also dont expect the WebUI to be very fancy like the dashboard for kubernetes*

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

[For some tweaking or changes, try seeing config/config.json]('https://github.com/Amazeryogo/CrispyDB/blob/main/config/config.json)

To run it... just run the bash script
```shell
$ bash run.sh
```




## I hope this project is helpful, if it isnt..... well you should use MongoDB instead.


The LICENSE
```MIT License

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
