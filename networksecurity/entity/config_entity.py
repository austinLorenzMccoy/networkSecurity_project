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

class DataValidationConfig:
    def __init__(self, training_pipeline_config):
        self.data_validation_dir:str=os.path.join(
            training_pipeline_config.artifact_dir, Training_pipeline.DATA_VALIDATION_DIR_NAME
        )
        self.valid_data_dir:str=os.path.join(self.data_validation_dir, Training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir:str=os.path.join(self.data_validation_dir, Training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path:str=os.path.join(self.valid_data_dir, Training_pipeline.DATA_VALIDATION_TRAIN_FILE_NAME)
        self.valid_test_file_path:str=os.path.join(self.valid_data_dir, Training_pipeline.DATA_VALIDATION_TEST_FILE_NAME)
        self.invalid_train_file_path:str=os.path.join(self.invalid_data_dir, Training_pipeline.DATA_VALIDATION_TRAIN_FILE_NAME)
        self.invalid_test_file_path:str=os.path.join(self.invalid_data_dir, Training_pipeline.DATA_VALIDATION_TEST_FILE_NAME)
        self.drift_report_file_path:str=os.path.join(self.data_validation_dir, Training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
        Training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)

class DataTransformationConfig:
    def __init__(self, training_pipeline_config):
        self.data_transformation_dir:str=os.path.join(
            training_pipeline_config.artifact_dir, Training_pipeline.DATA_TRANSFORMATION_DIR_NAME
        )
        self.transformed_train_file_path:str=os.path.join(
            self.data_transformation_dir, Training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            Training_pipeline.TRAIN_FILE_NAME.replace("csv", "npz")
        )
        self.transformed_test_file_path:str=os.path.join(
            self.data_transformation_dir, Training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            Training_pipeline.TEST_FILE_NAME.replace("csv", "npz")
        )
        self.transformed_object_file_path:str=os.path.join(
            self.data_transformation_dir, Training_pipeline.PREPROCSSING_OBJECT_DIR_NAME,
            Training_pipeline.PREPROCESSING_TRANSFORMED_OBJECT_FILE_NAME
        )