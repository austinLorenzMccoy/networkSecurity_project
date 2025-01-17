import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from networksecurity.constants.Training_pipeline import TARGET_COLUMN
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def get_data_transformer_object(self) -> Pipeline:
        """
        Creates a preprocessing pipeline that combines numerical and categorical transformations
        
        Returns:
            Pipeline object
        """
        logging.info(
            "Entered get_data_transformer_Object method of Transformation class"
            )
        try:
            # Read sample data to determine column types
            sample_df = self.read_data(self.data_validation_artifact.valid_train_file_path)
            sample_df = sample_df.drop(columns=[TARGET_COLUMN], axis=1)
            
            # Identify numeric and categorical columns
            numeric_features = sample_df.select_dtypes(include=['int64', 'float64']).columns
            categorical_features = sample_df.select_dtypes(include=['object']).columns
            
            logging.info(f"Numerical columns: {numeric_features}")
            logging.info(f"Categorical columns: {categorical_features}")
            
            # Numeric pipeline
            numeric_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', StandardScaler())
            ])
            
            # Categorical pipeline - Updated OneHotEncoder parameters
            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
                ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
            ])
            
            # Combine transformers
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', numeric_transformer, numeric_features),
                    ('cat', categorical_transformer, categorical_features)
                ],
                remainder='passthrough'
            )
            
            logging.info("Created preprocessing pipeline")
            return preprocessor
            
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Initiating data transformation")
        try:
            logging.info("Starting data transformation")
            train_df = pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            test_df = pd.read_csv(self.data_validation_artifact.valid_test_file_path)
           
            # training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            # testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)                

            logging.info("Got preprocessor object")
            preprocessor = self.get_data_transformer_object()
            
            logging.info("Fitting preprocessor on training data")
            transformed_input_train_feature = preprocessor.fit_transform(input_feature_train_df)
            
            logging.info("Transforming test data")
            transformed_input_test_feature = preprocessor.transform(input_feature_test_df)

            logging.info("Creating final numpy arrays")
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            logging.info("Saving transformed data and preprocessor object")
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)

            # preparing artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )
            
            logging.info("Data transformation completed successfully")
            return data_transformation_artifact
        
        except Exception as e:
            logging.error("Error in data transformation")
            raise NetworkSecurityException(e, sys)