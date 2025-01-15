import os
import sys
import json

from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Get MongoDB URI from environment variable
uri = os.getenv('MONGODB_URI')

print("MongoDB URI:", uri)

import certifi #root certificate for http connection and store in ca(certificate authority)
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(uri, tlsCAFile=ca)
            self.db = self.client['network_security']
            self.collection = self.db['network_data']
            logging.info("MongoDB connection established successfully")
        except Exception as e:
            logging.error("Error while connecting to MongoDB")
            raise NetworkSecurityException(e, sys) from e
        
    def csv_to_json_converter(self, file_path):
        try:
            df = pd.read_csv(file_path)
            if df.empty:
                raise ValueError("CSV file is empty.")
            df.reset_index(drop=True, inplace=True)
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

        
    def insert_data_mongodb(self, records, database, collection):
        try:
            # Initialize MongoDB client and access specified database and collection
            mongo_client = pymongo.MongoClient(uri, tlsCAFile=ca)
            db = mongo_client[database]
            collection = db[collection]
            
            # Insert records into the collection
            collection.insert_many(records)
            return len(records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

        
if __name__ == "__main__":
    file_path = "Network_Data/cyber_threat_intelligence_train.csv"
    database = "AUSTINAI"
    collection = "network_data"

    network_data_extract = NetworkDataExtract()
    records = network_data_extract.csv_to_json_converter(file_path)
    num_records = network_data_extract.insert_data_mongodb(records, database, collection)
    print(f"Inserted {num_records} records into MongoDB")

        