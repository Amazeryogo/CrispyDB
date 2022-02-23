while true
do
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
done