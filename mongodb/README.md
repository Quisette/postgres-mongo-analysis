# MongoDB Implementation

## File Structure

```text
mongodb (this folder)
├── benchmark
│   ├── benchmark.c  : random read access benchmark program using C
│   └── compile.sh   : shell script to quick compile
├── generator
│   └── dummy_data_generator.py : script for generating bulk dummy data
├── README.md : this documentation
└── results
    └── *.md : result analysis document
```



## Prerequisites

### Data Generator

pip package `pymongo` should be installed to link the python script to MongoDB file.

```bash
pip install pymongo
```

### Benchmark Program

This program uses `libmongoc-dev` to make MongoDB access available in C.
[install manual page](https://mongoc.org/libmongoc/current/installing.html)
```bash
apt-get install libmongoc-1.0-0
```


## Usage

please refer to documentation of two folders respectively:

* [benchmark.c Documentation](./benchmark/README.md)
* [dummy_data_generator.py` Documentation](./generator/README.md)

