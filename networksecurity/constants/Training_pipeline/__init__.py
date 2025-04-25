# networksecurity/constants/Training_pipeline/__init__.py

import os
import sys
import numpy as np
import pandas as pd

"""
defining common constant variable for training pipeline
"""
TARGET_COLUMN = "target"
PIPELINE_NAME: str = "networksecurity"
ARTIFACT_DIR: str = os.path.join(os.getcwd(), "artifact")
FILE_NAME: str = "cyber_threat_intelligence_train.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

SAVED_MODEL_DIR = os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "network_data"
DATA_INGESTION_DATABASE_NAME: str = "AUSTINAI"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
Data Validation related constant start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

# Adding the missing constants
DATA_VALIDATION_TRAIN_FILE_NAME: str = "train.csv"
DATA_VALIDATION_TEST_FILE_NAME: str = "test.csv"

"""
Data Transformation related constant start with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed_data"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR_NAME: str = "transformed_object"
PREPROCSSING_OBJECT_DIR_NAME: str = "preprocessing_object"  # Added constant
PREPROCESSING_TRANSFORMED_OBJECT_FILE_NAME: str = "transformed_object.pkl"  # Added constant

# knn  to replace nan values
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "n_neighbors": 3,
    "weights": "uniform"
}

DATA_VALIDATION_TRAIN_FILE_PATH: str = "train.npz"
DATA_VALIDATION_TEST_FILE_PATH: str = "test.npz"

"""
Model Trainer related constant start with MODEL_TRAINER VAR NAME for XGboost
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD: float = 0.05

"""
Model Evaluation related constant start with MODEL_EVALUATION VAR NAME
"""