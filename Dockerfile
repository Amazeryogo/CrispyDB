FROM ubuntu:latest
WORKDIR /app
RUN mkdir db && chmod 777 db
COPY . .
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt
RUN bash run.sh setpath db/
EXPOSE 5000
CMD ["bash", "run.sh"]
