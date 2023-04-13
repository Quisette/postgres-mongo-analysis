#bin/bash
gcc -o benchmark.out benchmark.c $(pkg-config --libs --cflags libmongoc-1.0) dotenv.c -lm -g

