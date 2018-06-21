from pymongo import *

client = MongoClient()
db = client['test']  # db = client.test
collection = db['test_collection']  # collection = db.test_collection

test_dict = {'name': 'tongxyu', 'age': 20, 'height': '184cm'}
test_dict1 = {'name': 'wewqe', 'age': 45, 'height': 'wew'}
test_dict2 = {'name': 'rng', 'age': 43, 'height': '184cm'}
test_dict3 = {'name': 'skt', 'age': 76, 'height': 'edsa3'}

# collection.insert([test_dict, test_dict1, test_dict2, test_dict3])
# result = collection.insert(test_dict)
# for i in collection.find().sort('age', DESCENDING):
collection.update({'name': 'skt'}, {'$set': {'height': '55', 'insert': 'test'}})
#     print(i)
collection.delete_many({'height': {'$gte': '5555'}})
for i in collection.find():
    print(i)