docker build /home/suvid/Projects/CrispyDB -tag crispydb:latest
docker run --publish 5000:5000 crispydb:latest
