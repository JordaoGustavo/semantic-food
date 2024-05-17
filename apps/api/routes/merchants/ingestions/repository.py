from api.infrastructure.mongo_db_connection import MongoDBConnection

class MerchantIngestRepository:
    def __init__(self, db_connection: MongoDBConnection) -> None:
        self.db_connection = db_connection

    def ingest(self, merchant):
        merchant_collection = self.db_connection.get_collection("merchants")
        merchant_collection.insert_one(merchant)

    @staticmethod
    def create():
        return MerchantIngestRepository(MongoDBConnection.connect())
