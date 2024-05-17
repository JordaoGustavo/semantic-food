from api.infrastructure.mongo_db_connection import MongoDBConnection

class MongoRagSearchRepository:
    def __init__(self, merchants) -> None:
        self.merchants = merchants

    def get_random(self): 
        return self.merchants.aggregate([
            { '$sample': { 'size': 10 },  }, { "$project": {'_id': 0, 'content_description_embedding': 0 } }
        ])

    def hybrid_search(self, query):
        text_search = self.merchants.aggregate([
            {
                "$search": {
                    "index": "NameFullTextSearch",
                    "text": {
                        "query": query["text_search"],
                        "path":{
                            "wildcard": "*"
                        }
                    }
                }
            }, { "$project": {'_id': 0, 'content_description_embedding': 0,  "score": {"$meta": "searchScore"}} }
        ])

        semantic_search_results = self.semantic_search(query['embedding'])

        merchants = list(text_search)
        merchant_ids = [merchant['id'] for merchant in merchants]
        results = {
            "text_search": merchants,
            "recommendation": sorted((x for x in semantic_search_results if x['id'] not in merchant_ids), key=lambda x: x['score'], reverse=True)[:5]
        }

        return results
    
    def semantic_search(self, embedding):
        return self.merchants.aggregate([
            {"$vectorSearch": {
                "queryVector": embedding,
                "path": "content_description_embedding",
                "numCandidates": 100,
                "limit": 10,
                "index": "ContentDescriptionSemanticSearch",
                }},
                {
                "$project": {'_id': 0, 'content_description_embedding': 0,  "score": { "$meta": "vectorSearchScore" }}
            }
        ])

    def get(self, id): 
        return self.merchants.find_one({'id': id})

    @staticmethod
    def create():
        db_connection = MongoDBConnection.connect()
        return MongoRagSearchRepository(db_connection.get_collection("merchants")) 