import os
import sys
import argparse
import json
import mlflow
import mlflow.sklearn
from dagshub import dagshub_logger

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

def start_data_ingestion(config=TrainingPipelineConfig()):
    try:
        data_ingestion_config = DataIngestionConfig(config)
        data_ingestion = DataIngestion(data_ingestion_config)
        return data_ingestion.initiate_data_ingestion()
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def start_data_validation(data_ingestion_artifact, config=TrainingPipelineConfig()):
    try:
        data_validation_config = DataValidationConfig(config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        return data_validation.initiate_data_validation()
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def start_data_transformation(data_validation_artifact, config=TrainingPipelineConfig()):
    try:
        data_transformation_config = DataTransformationConfig(config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        return data_transformation.initiate_data_transformation()
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def start_model_trainer(data_transformation_artifact, config=TrainingPipelineConfig()):
    try:
        model_trainer_config = ModelTrainerConfig(config)
        model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        
        # Log metrics to MLflow
        mlflow.log_metric("train_accuracy", model_trainer_artifact.train_metric_artifact.accuracy)
        mlflow.log_metric("test_accuracy", model_trainer_artifact.test_metric_artifact.accuracy)
        mlflow.log_metric("train_f1", model_trainer_artifact.train_metric_artifact.f1Score)
        mlflow.log_metric("test_f1", model_trainer_artifact.test_metric_artifact.f1Score)
        mlflow.log_metric("train_precision", model_trainer_artifact.train_metric_artifact.precision)
        mlflow.log_metric("test_precision", model_trainer_artifact.test_metric_artifact.precision)
        mlflow.log_metric("train_recall", model_trainer_artifact.train_metric_artifact.recall)
        mlflow.log_metric("test_recall", model_trainer_artifact.test_metric_artifact.recall)
        
        # Log model
        mlflow.sklearn.log_model(
            model_trainer_artifact.model, 
            "model",
            registered_model_name="NetworkSecurityModel"
        )
        
        # Save metrics to JSON for DVC
        os.makedirs("reports", exist_ok=True)
        metrics = {
            "train_accuracy": float(model_trainer_artifact.train_metric_artifact.accuracy),
            "test_accuracy": float(model_trainer_artifact.test_metric_artifact.accuracy),
            "train_f1": float(model_trainer_artifact.train_metric_artifact.f1Score),
            "test_f1": float(model_trainer_artifact.test_metric_artifact.f1Score),
            "train_precision": float(model_trainer_artifact.train_metric_artifact.precision),
            "test_precision": float(model_trainer_artifact.test_metric_artifact.precision),
            "train_recall": float(model_trainer_artifact.train_metric_artifact.recall),
            "test_recall": float(model_trainer_artifact.test_metric_artifact.recall)
        }
        
        with open("reports/metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)
            
        return model_trainer_artifact
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def run_pipeline(stage=None):
    try:
        # Initialize MLflow
        mlflow.set_tracking_uri("https://dagshub.com/austinLorenzMccoy/networkSecurity_project.mlflow")
        mlflow.set_experiment("network_security_classification")
        
        # Initialize DAGsHub logger
        dagshub_logger(
            metrics_path="reports/metrics.json",
            hparams_path="reports/params.json"
        )
        
        with mlflow.start_run():
            # Create pipeline config
            config = TrainingPipelineConfig()
            
            if stage is None or stage == "data_ingestion":
                data_ingestion_artifact = start_data_ingestion(config)
                if stage == "data_ingestion":
                    return
                
            if stage is None or stage == "data_validation":
                data_validation_artifact = start_data_validation(data_ingestion_artifact, config)
                if stage == "data_validation":
                    return
                
            if stage is None or stage == "data_transformation":
                data_transformation_artifact = start_data_transformation(data_validation_artifact, config)
                if stage == "data_transformation":
                    return
                
            if stage is None or stage == "model_trainer":
                model_trainer_artifact = start_model_trainer(data_transformation_artifact, config)
                
    except Exception as e:
        raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", type=str, help="Stage of the pipeline to run", 
                        choices=["data_ingestion", "data_validation", "data_transformation", "model_trainer"])
    args = parser.parse_args()
    
    run_pipeline(args.stage)
