
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
from bson.json_util import dumps, loads
from tester import Model
from copy import deepcopy
import time

mongo = MongoClient('mongodb://foo:bar@localhost', 27017) # fixed mongo client


# create a model using column template
def create_model(app_name, model_name: str, col_template):
    if list(mongo[app_name]["_internal"].find({"model_name": model_name})) != []:
        print("The model " + model_name + " has been defined previously.")
        return
    if list(mongo[app_name]["_internal"].find()) == []:
        mongo[app_name]["_internal"].insert_one({"created_time": datetime.now()})
    mongo[app_name]["_internal"].insert_one(
        {"model_name": model_name, "col_template": col_template,"created_time": datetime.now()})


# get all models' template by app
def get_all_models(app):
    foo = mongo[app]["_internal"].find()
    for obj in foo:
        if("model_name") in obj:
            return dumps(obj)

# create a set of data based on app, model and data column.
def create_data(app_name, model_name, data):
    model_blueprint = mongo[app_name]["_internal"].find_one({"model_name" : model_name})["col_template"]
    if len(data)!= len(model_blueprint):
        print("comparison failed, no data was inserted. ")
        return
    for key in data:
        if(type(data.get(key)).__name__ != str(model_blueprint.get(key))):
            raise TypeError(type(data.get(key)).__name__ + "!="+ str(model_blueprint.get(key)) )
    mongo[app_name][model_name].insert_one(data)
    return True



def modify_data():
    return


def delete_data():
    return


FIELD_TYPES     = ['int', 'str', 'bool', 'datetime', 'ObjectId']
DEFAULT_VALUES  = [1586479000, 'Lorem ipsum dolor sit amet, consectetur adipisicing elit', True, datetime.now(), ObjectId('6419e750a0a8c985a6afac16')]


def gen_data(apps_num, model_num, record_num , field_num):
    total_time = 0
    arr = {}
    field = {}

    ## create the Model array which stores prebuilt testing model
    for i in range(model_num):
        arr[i] = Model(i)

    ## for each model

    for i in range(apps_num):
        for j in range(model_num):
            for k in range(record_num):
                # for l in range(field_num):
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




    # for j in range(model_num):
    #     model = arr[j]
    #     for k in range(apps_num):
    #         # create_model(f"app_{k}",model.name, model.cols)
    #         ## generate bulk data
    #         for num in range(record_num):
    #             start_time = time.time()
    #             # for i in range(field_num - 1):
    #             #     field[f"field_{i}"] = DEFAULT_VALUES[i % 5]
    #             #     field["index"] = num
    #             # mongo[f"app_{k}"][f"model_{j}"].insert_one(field)

    #             mongo[f"app_{k}"][model.name].insert_one({
    #                 "field_0": 1586479000,
    #                 "field_1": "Lorem ipsum dolor sit amet, consectetur adipisicing elit",
    #                 "field_2": True,
    #                 "field_3": datetime.now(),
    #                 "field_4": ObjectId('6419e750a0a8c985a6afac16'),
    #                 "field_5": 1586479000,
    #                 "field_6": "Lorem ipsum dolor sit amet, consectetur adipisicing elit",
    #                 "field_7": True,
    #                 "field_8": datetime.now(),
    #                 "field_9": datetime.now(),
    #                 "index": num
    #             })
    #             stop_time = time.time()
    #             total_time +=  stop_time - start_time
    print("section elapsed time: " +str(total_time) + " secs" )
    # mongo.drop_database("a")
    return total_time


# def benchmark(n):
#     elapsed = 0
#     for _ in range(n):
#         elapsed +=
#     # print("Total elapsed: "+ str(elapsed) + " secs")
#     # print("average: " + str(elapsed /  n ) + "secs")


# benchmark(1)



def drop(n):
    for i in range(n):
        mongo.drop_database(f"app_{i}")
drop(1)
gen_data(100, 10, 100, 10)
