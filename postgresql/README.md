## PostgreSQL

There are a two essential scripts for benchmarking PostgreSQL:

| File Name | Language | Description |
| - | - | - |
| sql-generator.py | Python | Data generation |
| db-bench-c.c | C | Query benchmark |

### Prerequisites

**SQLAlchemy**

The `sqlalchemy` Python package is required for the generator script to run.

```bash
pip install SQLAlchemy
```

**libpq**

The official `libpq` C library is used in `db-bench-c.c` for performing SQL operations to a local PostgreSQL server.

The package can be installed via `apt`:

```bash
sudo apt install libpq-dev
```

**dotenv**

The `dotenv` library is included to provide support for loading environment variables. The two required files, `dotenv.c` and `dotenv.h`, have already been included.

## Compiling

The `db-bench-c.c` script should be compiled via `gcc`:

```bash
gcc -o benchmark.out db-bench-c.c -lpq -lm dotenv.c -lm
```

note that the `-lpq` option is required.

If the compiler fails to locate the `libpq` package, you could modify the following path in `db-bench-c.c`:
```c
#include "/usr/include/postgresql/libpq-fe.h"
```

## Creating the `.env` file

The `.env` file is required for running the benchmark script. It contains connection info of the PostgreSQL server.

The following copies the `env-example` template to a new file called `.env` :

```bash
cp env-example .env
vim .env
```

**Environment Variables**

| Variable | Description |
| - | - |
| db_host | The host address of the PostgreSQL server, such as `localhost` |
| db_port | The port of the server, usually `5432` |
| db_name | The target database name |
| db_username | The login username for the server |
| db_password | The login password for the server |

## Generating Data

To populate the database, run `sql-generator.py`:

```bash
python sql-generator.py {APP_COUNT} {MODEL_COUNT_PER_APP} {RECORD_COUNT_PER_APP} {FIELD_COUNT_PER_APP}
```

For example, this command generates `5` apps with `10` models per app. Each model contains `10000` records and `20` fields.

```bash
python sql-generator.py 5 10 10000 20
```

The script will drop all the existing tables in the database prior to data generation, which may take some time.

## Running the benchmark

The following command executes the `benchmark.out` script:

```bash
./benchmark.out {BENCHMARK_COUNT} {QUERIES_PER_BENCHMARK} {RECORDS_PER_QUERY} {DATASIZE_APP_COUNT} {DATASIZE_MODELS_PER_MODEL} {DATASIZE_RECORDS_PER_MODEL}
```

where `RECORDS_PER_QUERY` will be put into the SQL query strings.

The last three parameters tell the system the datasize in the database. These should match the arguments passed during data generation. They tell the benchmark script the range of random id selection.


For example, the following runs repeats `100,000` times, with `10` queries per benchmark and queries `1` record per query.
It specifies there are 1 app, 10 models per app, and 100 records per model.

```bash
./benchmark.out 100000 10 1 1 10 100
```
