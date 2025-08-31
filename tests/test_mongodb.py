from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment variable
uri = os.getenv('MONGODB_URI')

# Check if URI is loaded correctly
if not uri:
    raise ValueError("MONGODB_URI is not set in the .env file or not loaded properly.")

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
