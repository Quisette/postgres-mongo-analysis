
# Prerequisites



This program uses `libmongoc-dev` to make MongoDB access available in C language.
[install manual page](https://mongoc.org/libmongoc/current/installing.html)
```bash
apt-get install libmongoc-1.0-0
```



# Compiling Argument


Before compiling, it is required to modify `MONGO_URL` on `benchmark.c ` to the url that fit your settings.
```bash
gcc -o benchmark.out benchmark.c $(pkg-config --libs --cflags libmongoc-1.0) -g
```


# Usage

```bash
./benchmark.out <apps_to_access> <model_num> <record_num> <query_times>
```
# Code Reference

[Mongo C Driver Quick Start](https://mongoc.org/libmongoc/current/tutorial.html#starting-mongodb)
