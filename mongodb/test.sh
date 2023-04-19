#!/bin/bash
python3 ./generator/dummy_data_generator.py --generate 1 10 100 10 
./benchmark/benchmark.out 1 10 100 100000 >> ./results/0419/mongo_1app_10model_100record.log
python3 ./generator/dummy_data_generator.py --generate 1 10 1000 10 --drop 1
./benchmark/benchmark.out 1 10 1000 100000 >> ./results/0419/mongo_1app_10model_1000record.log
python3 ./generator/dummy_data_generator.py --generate 1 10 10000 10 --drop 1
./benchmark/benchmark.out 1 10 10000 100000 >> ./results/0419/mongo_1app_10model_10000record.log
python3 ./generator/dummy_data_generator.py --generate 10 10 100 10 --drop 1
./benchmark/benchmark.out 10 10 100 100000 >> ./results/0419/mongo_10app_10model_100record.log
python3 ./generator/dummy_data_generator.py --generate 100 10 100 10 --drop 10
./benchmark/benchmark.out 100 10 100 100000 >> ./results/0419/mongo_100app_10model_100record.log
python3 ./generator/dummy_data_generator.py --generate 1000 10 100 10 --drop 100
./benchmark/benchmark.out 1000 10 100 100000 >> ./results/0419/mongo_1000app_10model_100record.log
python3 ./generator/dummy_data_generator.py --drop 1000
