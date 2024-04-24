from pymongo import MongoClient
import os

db_pass = os.environ["MDB"]

# db_client = MongoClient().local

db_client = MongoClient(f"mongodb+srv://jmfaliaga:{db_pass}@cluster0.wllrqzs.mongodb.net/?retryWrites=true&w=majority").Cluster0
