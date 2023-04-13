echo "100"
python sql-generator.py 1 10 100 10
./benchmark.out 100 1 1 >> "1_100"

echo "1000"
python sql-generator.py 1 10 1000 10
./benchmark.out 100 1 1 >> "1_1000"
echo "10000"
python sql-generator.py 1 10 10000 10
./benchmark.out 100 1 1 >> "1_10000"

echo "task 2 10 "
python sql-generator.py 10 10 100 10
./benchmark.out 100 1 1 >> "2_10"

echo "100"
python sql-generator.py 100 10  100 10
./benchmark.out 100 1 1 >> "2_100"
echo "1000"
python sql-generator.py 1000 10 100 10
./benchmark.out 100 1 1 >> "2_1000"
