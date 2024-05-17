from pymongo import MongoClient
import os

class MongoDBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Create a connection to MongoDB
            cls._instance.client = MongoClient(os.getenv('mongo_srv'))
            cls._instance.db = cls._instance.client.VectorSearch
        return cls._instance

    def get_connection(self):
        return self.db
    
    def get_collection(self, collection):
        return self.db[collection]
    
    @staticmethod
    def connect():
        return MongoDBConnection()