# SQL Benchmark

## Prerequisites

The following packages are required:

- libpq-dev (via apt)

## Step 1: Edit environment variables

Copy the file `env-example` to `.env`. Open it and fill in the required variables.

## Step 2: Edit and run the generator

Data is generated via the `generator.py` script. First, open it and edit the parameters.

Once the parameters have been set, execute the command:

```bash
python3 generator.py {APPS} {MODEL_PER_APP} {RECORDS_PER_MODEL} {FIELDS_PERO_MODEL}
```

### Step 3: Compile the benchmark program

```bash
gcc -o benchmark.out db-bench-c.c -lpq -lm dotenv.c -lm
```

### Step 4: Execute the benchmark

Three arguments are needed.

```bash
./benchmark.out {EPOCH_COUNT} {QUERIES_PER_EPOCH} {RECORDS PER QUERY}
```
