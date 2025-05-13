import os
import sys
import numpy as np
import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

load_dotenv()
uri = os.getenv('MONGODB_URI')

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config

    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """
        Export MongoDB collection to a DataFrame.
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            logging.info(f"Connecting to MongoDB: {database_name}.{collection_name}")
            
            client = pymongo.MongoClient(uri)
            collection = client[database_name][collection_name]
            cursor = collection.find({})
            
            df = pd.DataFrame(list(cursor))
            if "_id" in df.columns:
                df.drop(columns=["_id"], axis=1, inplace=True)
            
            df.replace("", np.nan, inplace=True)
            logging.info(f"DataFrame shape: {df.shape}")
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, df: pd.DataFrame) -> None:
        """
        Split data into train and test sets.
        """
        try:
            train_set, test_set = train_test_split(
                df, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42
            )
            logging.info(f"Train set shape: {train_set.shape}, Test set shape: {test_set.shape}")
            
            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Main method to initiate data ingestion.
        """
        try:
            logging.info("Starting data ingestion")
            df = self.export_collection_as_dataframe()
            self.split_data_as_train_test(df)
            
            artifact = DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )
            logging.info("Data ingestion completed successfully")
            return artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)