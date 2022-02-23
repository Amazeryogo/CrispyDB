TOKEN="1e533624-1ea6-4106-9f61-a557cc917632"

#import requests as rq
 #
 #token = "1e533624-1ea6-4106-9f61-a557cc917632"
 #
 #print(rq.get('http://0.0.0.0:5000/').text)
 #print(rq.get('http://0.0.0.0:5000/create/collection?token=' + token).text)
 #print(rq.get('http://0.0.0.0:5000/getdata/collection?token=' + token).text)
 #print(rq.post('http://0.0.0.0:5000/add/collection?token=' + token,json={'name':'test','data':'test'}).text)
 #print(rq.get('http://0.0.0.0:5000/getdata/collection?token=' + token).text)
 #print(rq.post('http://0.0.0.0:5000/removefrom/collection?token=' + token,json={'name':'test','_crispy-id':1}).text)
 #print(rq.get('http://0.0.0.0:5000/getdata/collection?token=' + token).text)
 #print(rq.post('http://0.0.0.0:5000/delete/collection?token=' + token).text)


curl http://0.0.0.0:5000/
echo " "
curl http://0.0.0.0:5000/create/collection?token=$TOKEN
echo " "
curl http://0.0.0.0:5000/getdata/collection?token=$TOKEN
echo " "
curl http://0.0.0.0:5000/add/collection?token=$TOKEN  --header "Content-Type: application/json" --request POST --data '{"name":"test","_crispy-id":1}'
echo " "
curl http://0.0.0.0:5000/getdata/collection?token=$TOKEN
echo " "
curl http://0.0.0.0:5000/removefrom/collection?token=$TOKEN  --header "Content-Type: application/json" --request POST --data '{"name":"test","_crispy-id":1}'
echo " "
curl http://0.0.0.0:5000/getdata/collection?token=$TOKEN
echo " "
curl http://0.0.0.0:5000/delete/collection?token=$TOKEN
echo " "