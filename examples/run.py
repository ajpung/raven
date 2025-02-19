import datetime

import azure.cosmos.cosmos_client as cosmos_client
from azure.cosmos.partition_key import PartitionKey

from raven.core.api_base import collect_keys
from raven.modules.weather.collection import collect_weather

# Read configuration from docs/api_keys.json
keys = collect_keys()

HOST = keys["CosmosDB"]["host"]
MASTER_KEY = keys["CosmosDB"]["master_key"]
DATABASE_ID = keys["CosmosDB"]["database_id"]
CONTAINER_ID = keys["CosmosDB"]["container_id"]


def get_container(HOST, MASTER_KEY, DATABASE_ID, CONTAINER_ID):
    # Initialize the Cosmos DB client - fix the credential format
    client = cosmos_client.CosmosClient(
        url=HOST,
        credential=MASTER_KEY,  # Just pass the key directly
    )

    # Get or create the database
    database_name = DATABASE_ID
    try:
        database = client.get_database_client(database_name)
    except:
        database = client.create_database(database_name)

    # Get or create the container with appropriate partitioning
    container_name = CONTAINER_ID
    try:
        container = database.get_container_client(container_name)
    except:
        # Create with partition key on date for efficient time-based queries
        container = database.create_container(
            id=container_name,
            partition_key=PartitionKey(
                path="/location/lat"
            ),  # Use latitude as partition key
            offer_throughput=400,
        )

    return container


def store_weather_readings(wx_id, container):
    # Create document for weather source
    dtnow = datetime.datetime.now(datetime.UTC)
    tstmp = dtnow.strftime("%y%m%dT%H%M%S")  # Removed colons which might cause issues
    raw_doc = collect_weather(site=wx_id, lat=38.422508, lon=-85.797633)
    weather_doc = raw_doc["data"]

    # Add required 'id' field to the document
    weather_doc["id"] = f"{wx_id}_{tstmp}"

    # Store the document
    response = container.create_item(body=weather_doc)
    print(f"Document created with id: {response['id']}")
    return response


# Collect / store weather data
container = get_container(HOST, MASTER_KEY, DATABASE_ID, CONTAINER_ID)
store_weather_readings("tmrwio", container)
