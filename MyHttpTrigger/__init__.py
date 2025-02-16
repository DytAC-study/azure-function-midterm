import azure.functions as func
import json
import logging
import os
from azure.cosmos import CosmosClient

# Cosmos DB connection details
COSMOS_DB_URI = os.environ.get("COSMOS_DB_URI")
COSMOS_DB_KEY = os.environ.get("COSMOS_DB_KEY")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "default-db")
CONTAINER_NAME = os.environ.get("CONTAINER_NAME", "default-container")

if not COSMOS_DB_URI or not COSMOS_DB_KEY:
    logging.error("❌ ERROR: Missing required environment variables!")
    raise ValueError("Missing required environment variables!")

# Initialize CosmosDB Client
client = CosmosClient(COSMOS_DB_URI, credential=COSMOS_DB_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Function HTTP Trigger Handler"""
    logging.info("✅ Function MyHttpTrigger received a request.")

    method = req.method

    if method == "GET":
        logging.info("GET request received")
        query = "SELECT * FROM c"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        return func.HttpResponse(json.dumps(items, indent=2), mimetype="application/json")

    elif method == "POST":
        logging.info("POST request received")
        try:
            data = req.get_json()
            container.create_item(body=data)
            return func.HttpResponse("✅ Item added successfully!", status_code=201)
        except Exception as e:
            logging.error(f"❌ ERROR: {str(e)}")
            return func.HttpResponse(f"❌ ERROR: {str(e)}", status_code=500)

    return func.HttpResponse("⚠️ Invalid request", status_code=400)
