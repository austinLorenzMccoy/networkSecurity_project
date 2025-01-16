from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import Training_pipeline_config
import sys

if __name__ == "__main__":
    try:
       training_pipeline_config=Training_pipeline_config()
       dataingestionconfig=DataIngestionConfig(training_pipeline_config)
       data_ingestion=DataIngestion(data_ingestion_config=dataingestionconfig)
       logging.info("starting data ingestion")
       dataingestionartifact=data_ingestion.initiate_data_ingestion()
       print(dataingestionartifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys) 