# Semantic-food

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
      mongo_srv=''

4. **Running**
   ```bash  
      make server