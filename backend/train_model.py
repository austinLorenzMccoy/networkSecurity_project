#!/usr/bin/env python
"""
This script patches the pymongo compatibility issue with Python 3.12
and runs the model training pipeline.
"""
import sys
import os

# Add compatibility patch for pymongo with Python 3.12
import collections
import collections.abc

# Python 3.10+ moved these classes to collections.abc
if not hasattr(collections, 'MutableMapping'):
    collections.MutableMapping = collections.abc.MutableMapping
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping
if not hasattr(collections, 'MutableSet'):
    collections.MutableSet = collections.abc.MutableSet
if not hasattr(collections, 'Iterable'):
    collections.Iterable = collections.abc.Iterable

# Now import and run the main training pipeline
try:
    from networksecurity.components.data_ingestion import DataIngestion
    from networksecurity.components.data_validation import DataValidation
    from networksecurity.components.data_transformation import DataTransformation
    from networksecurity.components.model_trainer import ModelTrainer
    from networksecurity.entity.config_entity import (
        DataIngestionConfig, 
        DataValidationConfig, 
        DataTransformationConfig, 
        ModelTrainerConfig, 
        TrainingPipelineConfig
    )
    from networksecurity.exception.exception import NetworkSecurityException
    from networksecurity.logging.logger import logging

    if __name__ == "__main__":
        try:
            print("Starting the training pipeline...")
            # Initialize configurations
            training_pipeline_config = TrainingPipelineConfig()
            data_ingestion_config = DataIngestionConfig(training_pipeline_config)
            data_validation_config = DataValidationConfig(training_pipeline_config)
            data_transformation_config = DataTransformationConfig(training_pipeline_config)
            model_trainer_config = ModelTrainerConfig(training_pipeline_config)

            # Run pipeline
            print("Starting data ingestion...")
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            print("Data ingestion completed.")

            print("Starting data validation...")
            data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            print("Data validation completed.")

            print("Starting data transformation...")
            data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            print("Data transformation completed.")

            print("Starting model training...")
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            print("Model training completed.")
            
            print("Training pipeline completed successfully!")

        except Exception as e:
            print(f"Error in training pipeline: {e}")
            raise NetworkSecurityException(e, sys)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
