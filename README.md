## Testing Environment
```
Model: 2019 MacBook Pro
OS: macOS 13.2.1
CPU: 2.4 GHz Quad-Core Intel Core i5
RAM: 8 GB 2133 MHz LPDDR3
```
```
Python3 Version:      3.9.6
MongoDB Version:      6.0.3
PostgresSQL Version:  ?
```

## Setup environment
Please copy & paste the `.env.example` then rename the file as `.env`.

Modify the desired value of the services.


## Start the environment
```
$ docker-compose up -d
```
```
$ python3 -m venv venv
$ source ./venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```