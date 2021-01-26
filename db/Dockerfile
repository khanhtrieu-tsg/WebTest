#FROM mongo:4.0.0
# Parent Dockerfile https://github.com/docker-library/mongo/blob/982328582c74dd2f0a9c8c77b84006f291f974c3/3.0/Dockerfile
FROM mongo:latest

# custom label for the docker image
LABEL version="0.1" maintainer="ObjectRocket"

# use 'RUN' to execute commands in the container's bash terminal
RUN apt-get update -y
RUN apt-get remove mongodb-org -y
RUN apt-get install mongodb -y
RUN mkdir -p ./data/db
RUN service mongodb start -y

# expose MongoDB's default port of 27017
EXPOSE 27017
