
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
from bson.json_util import dumps, loads
from tester import Model
from copy import deepcopy
import time

mongo = MongoClient('localhost', 27017) # fixed mongo client


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




def single_bench(data_per_model, number_of_models):
    total_time = 0
    arr = {}
    ## create the Model array which stores prebuilt testing model
    for i in range(number_of_models):
        arr[i] = Model()

    ## for each model
    for j in range(number_of_models):
        model = arr[j]
        create_model("a",model.name, model.cols)
        ## generate bulk data
        for _ in range(data_per_model):
            start_time = time.time()
            create_data("a", model.name, deepcopy(model.data))
            stop_time = time.time()
            total_time +=  stop_time - start_time

    print("section elapsed time: " +str(total_time) + " secs" )
    mongo.drop_database("a")
    return total_time


def benchmark(n):
    elapsed = 0
    for _ in range(n):
        elapsed += single_bench(5000, 10)
    print("Total elapsed: "+ str(elapsed) + " secs")
    print("average: " + str(elapsed /  n ) + "secs")


benchmark(3)
