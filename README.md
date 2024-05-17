# Semantic-food

Semantic-food is a project that combines traditional text search with advanced semantic search to create a hybrid search and recommendation system using vector search. This approach enhances the search experience by leveraging both keyword-based and context-aware searches, providing more accurate and relevant results for users.

This guide will help you set up and initialize a Python API with a connection to MongoDB

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.7 or later
- pip (Python package installer)
- MongoDB server (local or cloud-based, such as MongoDB Atlas)

## Project Setup

Follow these steps to set up the project:

1. **Venv** 

   ```bash
      python -m venv venv
      source venv/bin/activate   # On Windows use `venv\Scripts\activate`

2. **Install Dependencies**

   ```bash 
      make requirements

3. **Create a .env File**

    ```bash 
      Your mongo atlas srv
      mongo_srv=''

4. **Running**

   ```bash  
      make server

5. **Ingestion**

    ```bash
        change to your location https://github.com/JordaoGustavo/semantic-food/blob/main/apps/api/routes/merchants/ingestions/endpoint.py#L97
        and then
        curl --location --request POST 'http://localhost:8080/merchants/'
        After ingest your data you need to create an index in your atlas mongo db
        With name NameFullTextSearch and mappings like:
        {
          "mappings": {
            "dynamic": true,
            "fields": {
              "content_description_embedding": {
                "dimensions": 384,
                "similarity": "cosine",
                "type": "knnVector"
              }
            }
          }
        }