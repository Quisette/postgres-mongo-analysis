
gcc -o benchmark.out benchmark.c $(pkg-config --libs --cflags libmongoc-1.0) -g
# ./benchmark.out #1 #2 #3 #4

