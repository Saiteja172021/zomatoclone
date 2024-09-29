from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json


uri = "mongodb://localhost:27017"


client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
db = client.zomatoDB
restaurant = db.restaurant


file1_path = './file1.json'
file2_path = './file2.json'

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

data_file1 = load_json_data(file1_path)
data_file2 = load_json_data(file2_path)

def convert_and_insert(data):
    restaurant.insert_many(data)
    print("Data inserted successfully!")
convert_and_insert(data_file1)
convert_and_insert(data_file2)
