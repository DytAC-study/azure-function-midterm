# CST8911-midterm

1️⃣ **Login to Azure (With Your Student Account)**

```bash
az login
```

- This will open a **browser** for authentication.If your school blocks normal login, use:

  ```bash
  az login --use-device-code
  ```

2️⃣ **Initialize a New Azure Function Project**

```bash
mkdir azure-function-midterm
cd azure-function-midterm
func init --worker-runtime python
func new --name MyHttpTrigger --template "HTTP trigger" --authlevel "function"

#run in venv
python3.11 -m venv venv
source venv/bin/activate
```

3️⃣ **Modify `function_app.py` to Connect to Cosmos DB**

```python
import azure.functions as func
import json
from azure.cosmos import CosmosClient

# Cosmos DB configuration
COSMOS_DB_URI = "https://<your-cosmosdb-name>.documents.azure.com:443/"
COSMOS_DB_KEY = "<your-primary-key>"
DATABASE_NAME = "MyDatabase"
CONTAINER_NAME = "MyCollection"

client = CosmosClient(COSMOS_DB_URI, credential=COSMOS_DB_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def main(req: func.HttpRequest) -> func.HttpResponse:
    method = req.method

    if method == "GET":
        query = "SELECT * FROM c"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        return func.HttpResponse(json.dumps(items, indent=2), mimetype="application/json")

    elif method == "POST":
        try:
            data = req.get_json()
            container.create_item(body=data)
            return func.HttpResponse("Item added successfully", status_code=201)
        except Exception as e:
            return func.HttpResponse(f"Error: {str(e)}", status_code=500)

    return func.HttpResponse("Invalid request", status_code=400)

```

4️⃣ **Install Required Python Dependencies**

```bash
pip3 install azure-functions azure-cosmos
```

5️⃣ **Generate `requirements.txt`**

```bash
pip3 freeze > requirements.txt
```

------

## **🔹 Step 3: Deploy Function to Azure from Ubuntu**

### **1️⃣ Login to Azure**

```bash
az login
```

If you're **using a school-managed account**, use:

```bash
az login --use-device-code
```

### **2️⃣ Create a Function App in Azure**

```bash
az functionapp create --resource-group <your-resource-group> --consumption-plan-location eastus \
--runtime python --runtime-version 3.9 --functions-version 4 \
--name midtermtest01 --storage-account <your-storage-account>
```

### **3️⃣ Deploy the Function from Ubuntu**

```bash
func azure functionapp publish midtermtest01
```

