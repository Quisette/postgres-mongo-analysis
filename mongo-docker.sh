docker rm mongodb
export MONGODB_VERSION=6.0-ubi8
sudo docker run --name mongodb -p 27017:27017 -v $(pwd):/data/db mongodb/mongodb-community-server:$MONGODB_VERSION

