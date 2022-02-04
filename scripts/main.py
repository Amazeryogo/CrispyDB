import requests as rq

exampletoken = "1e533624-1ea6-4106-9f61-a557cc917632"

print(rq.get('http://0.0.0.0:5000/').text)
print(rq.get('http://0.0.0.0:5000/create/collection?exampletoken=' + exampletoken).text)
print(rq.get('http://0.0.0.0:5000/getdata/collection?exampletoken=' + exampletoken).text)
print(rq.post('http://0.0.0.0:5000/add/collection?exampletoken=' + exampletoken,json={'name':'test','data':'test'}).text)
print(rq.get('http://0.0.0.0:5000/getdata/collection?exampletoken=' + exampletoken).text)
print(rq.post('http://0.0.0.0:5000/removefrom/collection?exampletoken=' + exampletoken,json={'name':'test','_crispy-id':1}).text)
print(rq.get('http://0.0.0.0:5000/getdata/collection?exampletoken=' + exampletoken).text)
print(rq.post('http://0.0.0.0:5000/delete/collection?exampletoken=' + exampletoken).text)
