import azure.cosmos.documents as documents
import azure.cosmos.exceptions as exceptions
from raven.core.api_base import collect_keys
from raven.modules.weather.collection import collect_weather
import azure.cosmos.cosmos_client as cosmos_client
from azure.cosmos.partition_key import PartitionKey
import datetime

# Read configuration from docs/api_keys.json
keys = collect_keys()

HOST = keys["CosmosDB"]["host"]
MASTER_KEY = keys["CosmosDB"]["master_key"]
DATABASE_ID = keys["CosmosDB"]["database_id"]
CONTAINER_ID = keys["CosmosDB"]["container_id"]


def get_container(HOST, MASTER_KEY, DATABASE_ID, CONTAINER_ID):
    # Initialize the Cosmos DB client
    client = cosmos_client.CosmosClient(
        url=HOST,
        credential={"masterKey": MASTER_KEY},
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
            partition_key=PartitionKey(path="/date"),
            offer_throughput=400,  # Minimum throughput, adjust as needed
        )

    return container


def store_weather_readings(CONTAINER_ID):
    # Create document for first source (Tomorrow.io)
    dtnow = datetime.datetime.now(datetime.UTC)
    tstmp = dtnow.strftime("%y%m%dT%H:%M:%S")
    tomorrow_doc = {
        "id": f"tmrw_{tstmp}",
        "source": "tomorrow_io",
        "type": "weather_reading",
        "timestamp": dtnow.isoformat(),
        "date": dtnow.strftime("%Y-%m-%d"),
        "location": "toronto",
        #'temperature': tomorrow_data['data']['temperature'],
        #'humidity': tomorrow_data['data']['humidity'],
        # Other Tomorrow.io specific fields
    }

    # Store both documents
    container.create_item(body=tomorrow_doc)


container = get_container(HOST, MASTER_KEY, DATABASE_ID, CONTAINER_ID)

# Now you can use this container in your store_weather_readings function
store_weather_readings(container)
