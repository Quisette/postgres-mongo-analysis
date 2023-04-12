# SQL Benchmark

## Prerequisites

The following packages are required:

- libpq-dev (via apt)

## Step 1: Edit environment variables

There is a file `.env` in this directory. Open it and fill in the required variables.

## Step 2: Edit and run the generator

Data is generated via the `generator.py` script. First, open it and edit the parameters.

Once the parameters have been set, execute the command:

```bash
python3 generator.py
```

### Step 3: Compile the benchmark program

```bash
gcc -O benchmark.out db-bench-c.c -leq -lm dotenv.c -lm
``` 

### Step 4: Execute the benchmark

Three arguments are needed.

```bash
./benchmark.out {EPOCH_COUNT} {QUERIES_PER_EPOCH} {RECORDS PER QUERY}
```
