
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
from sys import argv


FIELD_TYPES     = ['int', 'str', 'bool', 'datetime', 'ObjectId']
DEFAULT_VALUES  = [1586479000, 'Lorem ipsum dolor sit amet, consectetur adipisicing elit', True, datetime.now(), ObjectId('6419e750a0a8c985a6afac16')]
MONGO_URL = "mongodb://foo:bar@localhost"
MONGO_PORT = 27017


mongo = MongoClient(MONGO_URL, MONGO_PORT)


def gen_data(apps_num, model_num, record_num , field_num): # field number not used since fixed data has applied.
    arr = {}
    field = {}

    # create the Model array which stores prebuilt testing model
    for i in range(apps_num): # App
        for j in range(model_num): # Model
            for k in range(record_num): # Record
                # for l in range(field_num): # Field
                mongo[f"app_{i}"][f"model_{j}"].insert_one({
                    "field_0": 1586479000,
                    "field_1": "Lorem ipsum dolor sit amet, consectetur adipisicing elit",
                    "field_2": True,
                    "field_3": datetime.now(),
                    "field_4": ObjectId('6419e750a0a8c985a6afac16'),
                    "field_5": 1586479000,
                    "field_6": "Lorem ipsum dolor sit amet, consectetur adipisicing elit",
                    "field_7": True,
                    "field_8": datetime.now(),
                    "field_9": datetime.now(),
                    "index": k
                })


def drop_databases(database_count):
    for i in range(database_count):
        mongo.drop_database(f"app_{i}")




def main():
    if "--drop" in argv:
        drop_databases(int(argv[argv.index("--drop")+1]))
    if "--generate" in argv:
        index = argv.index("--generate")
        if not argv[index + 4]:
            print("--generate <app> <model> <record> <field>")
        else:
            gen_data(int(argv[index+1]),int(argv[index+2]), int(argv[index+3]),int(argv[index+4]))





if __name__ == "__main__":
    main()
