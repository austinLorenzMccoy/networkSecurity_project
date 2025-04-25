import os
import sys
import pytest
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.pipeline.training_pipeline import start_data_ingestion

class TestPipeline:
    def test_data_ingestion_creates_artifact(self):
        """Test that data ingestion creates the expected artifact directory"""
        # Run data ingestion
        data_ingestion_artifact = start_data_ingestion(TrainingPipelineConfig())
        
        # Check if the artifact paths exist
        assert os.path.exists(data_ingestion_artifact.feature_store_file_path)
        assert os.path.exists(data_ingestion_artifact.train_file_path)
        assert os.path.exists(data_ingestion_artifact.test_file_path)
        
    def test_config_creation(self):
        """Test that the pipeline configuration is created correctly"""
        config = TrainingPipelineConfig()
        assert config is not None
        assert os.path.exists(config.artifact_dir)
