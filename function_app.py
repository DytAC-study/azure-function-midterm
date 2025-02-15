import azure.functions as func
import json
import logging
import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient

load_dotenv()

# Create Azure Function App instance
app = func.FunctionApp()


# Cosmos DB connection details (Replace with your values)

COSMOS_DB_URI = os.getenv("COSMOS_DB_URI")
COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY")
DATABASE_NAME = os.getenv("DATABASE_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

# Initialize Cosmos DB client
client = CosmosClient(COSMOS_DB_URI, credential=COSMOS_DB_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.FUNCTION)
def my_http_trigger(req: func.HttpRequest) -> func.HttpResponse:
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
            return func.HttpResponse("Item added successfully", status_code=201)
        except Exception as e:
            return func.HttpResponse(f"Error: {str(e)}", status_code=500)

    return func.HttpResponse("Invalid request", status_code=400)
