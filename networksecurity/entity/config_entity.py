#all configuration details
from datetime import datetime
import os
from networksecurity.constants import Training_pipeline

print(Training_pipeline.PIPELINE_NAME)
print(Training_pipeline.ARTIFACT_DIR)

class Training_pipeline_config:
    def __init__(self):
        timestamp=datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name=Training_pipeline.PIPELINE_NAME
        self.artifact_name=Training_pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name, timestamp)
        self.timestamp=timestamp

class DataIngestionConfig:
    def __init__(self,training_pipeline_config):
        self.data_ingestion_dir:str=os.path.join(
            training_pipeline_config.artifact_dir, Training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path:str=os.path.join(
            self.data_ingestion_dir, Training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, Training_pipeline.FILE_NAME
        )
        self.training_file_path:str=os.path.join(
            self.data_ingestion_dir, Training_pipeline.DATA_INGESTION_INGESTED_DIR, Training_pipeline.TRAIN_FILE_NAME
        )
        self.test_file_path:str=os.path.join(
            self.data_ingestion_dir, Training_pipeline.DATA_INGESTION_INGESTED_DIR, Training_pipeline.TEST_FILE_NAME
        )
        self.train_test_split_ratio:float=Training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name:str=Training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name:str=Training_pipeline.DATA_INGESTION_DATABASE_NAME