import random, string
from datetime import datetime
from random import randint
from bson.objectid import ObjectId
def generate_name(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


FIELD_TYPES     = ['int', 'str', 'bool', 'datetime', 'ObjectId']
DEFAULT_VALUES  = [1586479000, 'Lorem ipsum dolor sit amet, consectetur adipisicing elit', True, datetime.now(), ObjectId('6419e750a0a8c985a6afac16')]

class Model:

    def __init__(self, num):
        self.name = f"model_{num}"
        self.fields = []
        self.cols = {}
        self.data = {}
        for i in range(9):
            rand_index = i % 4
            self.field = {
                'type': FIELD_TYPES[rand_index],
                'name': f"field_{i}",
                'default_value': DEFAULT_VALUES[rand_index],
            }
            self.fields.append(self.field)
        self.fields.append( {
                'type': 'int',
                'name': 'index',
                'default_value': DEFAULT_VALUES[0],
            })
        self.generate_cols()
        self.generate_data()
    def generate_cols(self):
        self.cols = {}
        for item in self.fields:
            self.cols[item["name"]]  =  item["type"]
    def generate_data(self):
        self.data = {}
        for item in self.fields:
            self.data[item["name"]]  =  item["default_value"]







