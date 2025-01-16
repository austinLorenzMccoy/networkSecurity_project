from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import os
import pandas as pd
import sys
from networksecurity.utils.main_utils import read_yaml_file, write_yaml_file

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self.schema_config["columns"])
            logging.info(f"Number of columns in dataframe: {len(dataframe.columns)}")
            logging.info(f"Required number of columns as per schema: {number_of_columns}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def detect_drift_in_data(self, base_df, current_df, threshold=0.5) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column: {
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": is_found
                }})
            
            drift_report_file_path = os.path.join(
                self.data_validation_config.drift_report_file_path,
                "drift_report.json"
            )

            # Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report, replace=True)
            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            error_message = ""
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Read data from train and test file location
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            # Validate number of columns
            status = self.validate_number_of_columns(dataframe=train_df)
            if not status:
                error_message = f"{error_message}Train dataframe does not contain all columns."
                logging.info(f"{error_message}Train dataframe does not contain all columns.")
            status = self.validate_number_of_columns(dataframe=test_df)
            if not status:
                error_message = f"{error_message}Test dataframe does not contain all columns."
                logging.info(f"{error_message}Test dataframe does not contain all columns.")

            # Check data drift
            status = self.detect_drift_in_data(base_df=train_df, current_df=test_df)
            
            # Create directory for valid data
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)