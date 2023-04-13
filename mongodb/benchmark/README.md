
# Prerequisites



This program uses `libmongoc-dev` to make MongoDB access available in C language.
[install manual page](https://mongoc.org/libmongoc/current/installing.html)
```bash
apt-get install libmongoc-1.0-0
```

# `.env` File
Note that it is necessary to copy `.env.example` to `.env` and modify the file to fit your settings.
```bash
cp .env.example .env
```

The keys are listed below:
| key | meaning|
| --- | --- |
|`mongodb_host` | IP of MongoDB|
|`mongodb_port` | port of MongoDB|
|`mongodb_user` | user name of MongoDB|
|`mongodb_password` | password of MongoDB|

# Compiling



```bash
gcc -o benchmark.out benchmark.c $(pkg-config --libs --cflags libmongoc-1.0) dotenv.c -lm -g
```


# Usage

```bash
./benchmark.out <apps_num> <model_num> <record_num> <query_times>
```

for example, `./benchmark.out 1 10 100 10000` will randomly access `10000` records (one at a time), where the records are stored within `1` app and `10` models.


# Code Reference

[Mongo C Driver Quick Start](https://mongoc.org/libmongoc/current/tutorial.html#starting-mongodb)
