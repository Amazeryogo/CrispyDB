#Here are the docker commands, mostly for my own reference.
docker build /home/suvid/Projects/CrispyDB -tag crispyDB:latest
docker run --publish 5000:5000 crispyDB:latest
