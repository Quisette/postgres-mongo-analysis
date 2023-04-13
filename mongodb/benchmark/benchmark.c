#include <mongoc/mongoc.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include "dotenv.h"
#define MONGO_URL "mongodb://foo:bar@localhost:27017"

mongoc_client_t *client;
mongoc_database_t *database;
mongoc_collection_t *collection;

void random_query(mongoc_client_t *client, int app_num, int model_num, int record_num, int times) {
    const bson_t *doc;
    bson_error_t error;
    time_t t;
    double time_spent = 0, sum = 0, max = 0, min = 99999;
    // initialize random seed
    srand((unsigned)time(&t));
    for (int it = 0; it < times; it++) {
        // randomize number
        int rand_app_num = rand() % app_num;
        int rand_model_num = rand() % model_num;
        int rand_record_num = rand() % record_num;

        // create app name and model name
        char * app_name = malloc(20), * model_name = malloc(20);
        sprintf(app_name, "app_%d", rand_app_num);

        sprintf(model_name, "model_%d", rand_model_num);

        // clock start
        clock_t begin = clock();

        // generate query string cursor
        database = mongoc_client_get_database(client, app_name);
        collection = mongoc_client_get_collection(client, app_name, model_name);
        bson_t *query = BCON_NEW("index", BCON_INT32(rand_record_num));

        // main query function
        mongoc_cursor_t *cursor = mongoc_collection_find_with_opts(collection, query, NULL, NULL);

        // clock end
        clock_t end = clock();

        // calculate time spent
        time_spent = (double)(end - begin) / CLOCKS_PER_SEC;

        sum += time_spent;
        if (time_spent > max) {
            max = time_spent;
        }
        if (time_spent < min) {
            min = time_spent;
        }
        free(app_name);
        free(model_name);

        // printf("query time spent (single): %f\n", time_spent * 1000);
    }

    printf("query time spent (avg): %f ms\n", sum * 1000 / times);
    printf("query time spent (total): %f ms\n", sum * 1000);
    printf("query time spent (max): %f ms\n", max * 1000);
    printf("query time spent (min): %f ms\n", min * 1000);
}

int main(int argc, char *argv[]) {
    env_load(".env", false);
    char *uri_string = malloc(100);
    sprintf(uri_string, "mongodb://%s:%s@%s:%s", getenv("mongodb_user"), getenv("mongodb_password"), getenv("mongodb_host"), getenv("mongodb_port"));
    mongoc_uri_t *uri;
    mongoc_client_t *client;
    mongoc_database_t *database;
    mongoc_collection_t *collection;
    bson_t *command, *insert;
    bson_error_t error;
    char *str;
    bool retval;

    // initialize libmongoc's internals
    mongoc_init();

    /*
     * Optionally get MongoDB URI from command line
     */
    // if (argc > 1) {
    //     uri_string = argv[1];
    // }

    // mongoDB uri error handling
    uri = mongoc_uri_new_with_error(uri_string, &error);
    if (!uri) {
        fprintf(stderr,
                "failed to parse URI: %s\n"
                "error message:       %s\n",
                uri_string,
                error.message);
        return EXIT_FAILURE;
    }

    // new instance
    client = mongoc_client_new_from_uri(uri);
    if (!client) {
        return EXIT_FAILURE;
    }
    if (argc != 5) {
        printf("Usage: ./benchmark.out [app_num] [model_num] [record_num] [times]\n");
        return EXIT_FAILURE;
    }

    /*
     * Register the application name so we can track it in the profile logs
     * on the server. This can also be done from the URI (see other examples).
     */
    mongoc_client_set_appname(client, "connect-example");

    // main program starts
    random_query(client, atoi(argv[1]), atoi(argv[2]), atoi(argv[3]), atoi(argv[4]));

    // release memory
    mongoc_uri_destroy(uri);
    mongoc_client_destroy(client);
    mongoc_cleanup();
    free(uri_string);

    return EXIT_SUCCESS;
}
