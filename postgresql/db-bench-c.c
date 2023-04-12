// gcc db-bench-c.c -lm -lpq

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dotenv.h"
#include <time.h>

#include "/usr/include/postgresql/libpq-fe.h"

// #define EPOCH_COUNT 1
// #define QUERIES_PER_EPOCH 1
// #define RECORDS_PER_QUERY 100


int query(PGconn* const db, const int records_per_query, const char* str_records_per_query) {
    PGresult* res1 = (PGresult*)PQexec(db, "SELECT id FROM apps WHERE name = 'app_0';");
    char* app_id = PQgetvalue(res1, 0, 0);

    char model_query[512] = "SELECT id FROM models WHERE name = 'model_0' and app_id = '";
    strcat(model_query, app_id);
    strcat(model_query, "';");

    PGresult* res2 = (PGresult*)PQexec(db, model_query);
    char* model_id = PQgetvalue(res2, 0, 0);

    char record_query[512] = "SELECT id FROM records WHERE model_id = '";
    strcat(record_query, model_id);
    strcat(record_query, "' LIMIT ");
    strcat(record_query, str_records_per_query);
    strcat(record_query, ";");
    // printf("%s\n", record_query);

    PGresult* res3 = (PGresult*)PQexec(db, record_query);
    const int record_count = PQntuples(res3);

    for (int i = 0; i < records_per_query; ++i) {
        char* const record_id = PQgetvalue(res3, i, 0);

        char data_query[512] = "SELECT value FROM data WHERE record_id = '";
        strcat(data_query, record_id);
        strcat(data_query, "';");
        PGresult* res4 = (PGresult*)PQexec(db, data_query);
        char* data_id = PQgetvalue(res4, 0, 0);
    }
}

int main(int* argc, char** argv) {

    // printf("%d\t%d\t%d\n", atoi(argv[1]), atoi(argv[2]), atoi(argv[3]));

    const int epoch_count = atoi(argv[1]);
    const int queries_per_epoch = atoi(argv[2]);
    const int records_per_query = atoi(argv[3]);

    char str_records_per_query[16];
    sprintf(str_records_per_query, "%d", records_per_query);

    env_load(".env", false);

    printf("Benchmarking PostgreSQL database with %d epochs, %d queries per epoch, and %d records per query.\n", epoch_count, queries_per_epoch, records_per_query);

    PGconn* db = (PGconn*)PQsetdbLogin((char*)getenv("db_host"), (char*)getenv("db_port"), NULL, NULL, (char*)getenv("db_name"), (char*)getenv("db_username"), (char*)getenv("db_password"));

    double benchsum = 0.0;
    double benchmin = 99999.0;
    double benchmax = 0.0;

    for (int n = 0; n < epoch_count; ++n) {
        clock_t start = clock();

        //do stuff
        for (int i = 0; i < queries_per_epoch; ++i)
            query(db, records_per_query, str_records_per_query);

        clock_t end = clock();

        // const unsigned long timediff = (((double)stop.tv_sec - (double)start.tv_sec) * (double)1000000 + (double)stop.tv_usec - (double)start.tv_usec) / (double)1000;
        const double timediff = (double)(end-start) / CLOCKS_PER_SEC * 1000;

        if (timediff < benchmin) benchmin = timediff;
        if (timediff > benchmax) benchmax = timediff;

        // printf("Start #%-3d ==> %.5lf ms\n", n+1, (double)start / CLOCKS_PER_SEC * 1000);
        // printf("End #%-3d ==> %.5lf ms\n", n+1, (double)end / CLOCKS_PER_SEC * 1000);
        printf("Epoch #%-3d ==> %.5lf ms\n", n+1, timediff);
        benchsum += timediff;
    }

    printf("Minimum: %.5lf ms\n", benchmin);
    printf("Maximum: %.5lf ms\n", benchmax);
    printf("Average: %.5lf ms\n", (benchsum / epoch_count));

    return 0;
}
