
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
from sys import argv
from copy import deepcopy

FIELD_TYPES = ['int', 'str', 'bool', 'datetime', 'ObjectId']
DEFAULT_VALUES = [1586479000, 'Lorem ipsum dolor sit amet, consectetur adipisicing elit',
                  True, datetime.now(), ObjectId('6419e750a0a8c985a6afac16')]
MONGO_URL = "mongodb://foo:bar@localhost"
MONGO_PORT = 27017


mongo = MongoClient(MONGO_URL, MONGO_PORT)


# field number not used since fixed data has applied.
def gen_data(apps_num, model_num, record_num, field_num):
    arr = {}
    field = {}
    for l in range(field_num):  # Field
        field[f"field_{l}"] = DEFAULT_VALUES[l % len(DEFAULT_VALUES)]
    # create the Model array which stores prebuilt testing model
    for i in range(apps_num):  # App
        for j in range(model_num):  # Model
            for k in range(record_num):  # Record
                field['index'] = k
                # mongoDB will push the oid to the object and cannot be uploaded again.
                mongo[f"app_{i}"][f"model_{j}"].insert_one(deepcopy(field))


def drop_databases(database_count):
    for i in range(database_count):
        mongo.drop_database(f"app_{i}")


def main():
    if "--drop" in argv:
        drop_databases(int(argv[argv.index("--drop")+1]))
    if "--generate" in argv:
        index = argv.index("--generate")
        if not argv[index + 4]:
            print("--generate <app_num> <model_num> <record_num> <field_num>")
        else:
            gen_data(int(argv[index+1]), int(argv[index+2]),
                     int(argv[index+3]), int(argv[index+4]))


if __name__ == "__main__":
    main()
