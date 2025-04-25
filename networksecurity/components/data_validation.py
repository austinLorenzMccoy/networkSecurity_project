# networksecurity.components.data_validation.py

import os
import sys
import pandas as pd
import numpy as np
from typing import Dict, Any
from scipy.stats import ks_2samp
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.utils.main_utils import read_yaml_file, write_yaml_file

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self.schema_config = read_yaml_file(self.data_validation_config.schema_file_path)

    def validate_schema(self, df: pd.DataFrame) -> Dict[str, Any]:
        try:
            validation_report = {
                "columns_match": True,
                "missing_columns": [],
                "extra_columns": [],
                "dtype_match": True
            }

            # Validate column presence
            expected_columns = set(self.schema_config["columns"].keys())
            actual_columns = set(df.columns)
            
            validation_report["missing_columns"] = list(expected_columns - actual_columns)
            validation_report["extra_columns"] = list(actual_columns - expected_columns)
            
            if validation_report["missing_columns"] or validation_report["extra_columns"]:
                validation_report["columns_match"] = False
                return validation_report

            # Validate data types
            for column, dtype in self.schema_config["columns"].items():
                if str(df[column].dtype) != dtype:
                    validation_report["dtype_match"] = False
                    break

            return validation_report
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold: float = 0.05) -> Dict[str, Any]:
        try:
            drift_report = {}
            for column in base_df.columns:
                if base_df[column].dtype in [np.float64, np.int64]:
                    statistic, p_value = ks_2samp(base_df[column], current_df[column])
                    drift_report[column] = {
                        "drift_detected": p_value < threshold,
                        "p_value": float(p_value)
                    }
            return drift_report
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("Starting data validation")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # Validate schema
            train_schema_report = self.validate_schema(train_df)
            test_schema_report = self.validate_schema(test_df)

            logging.info(f"Train schema validation report: {train_schema_report}")
            logging.info(f"Test schema validation report: {test_schema_report}")

            if not (train_schema_report["columns_match"] and train_schema_report["dtype_match"] and
                   test_schema_report["columns_match"] and test_schema_report["dtype_match"]):
                logging.error("Schema validation failed")
                
                # Save invalid datasets
                os.makedirs(os.path.dirname(self.data_validation_config.invalid_train_file_path), exist_ok=True)
                train_df.to_csv(self.data_validation_config.invalid_train_file_path, index=False)
                test_df.to_csv(self.data_validation_config.invalid_test_file_path, index=False)
                
                raise ValueError("Schema validation failed")

            # Detect data drift
            drift_report = self.detect_data_drift(train_df, test_df)
            write_yaml_file(self.data_validation_config.drift_report_file_path, drift_report)

            # Save valid datasets
            os.makedirs(os.path.dirname(self.data_validation_config.valid_train_file_path), exist_ok=True)
            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False)

            artifact = DataValidationArtifact(
                validation_status=True,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            logging.info("Data validation completed successfully")
            return artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)