# networksecurity/utils/ml_utils/model/estimator.py

from networksecurity.constants.Training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME
import os
import pickle

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkModel:
    def __init__(self, preprocessor, model):
        """
        :param preprocessor: preprocessing object that will transform the input data
        :param model: trained model object
        """
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise e
    
    def predict(self, x):
        """
        :param x: input features
        :return: predictions
        """
        try:
            x_transform = self.preprocessor.transform(x)
            return self.model.predict(x_transform)
        except Exception as e:
            raise e

    def save(self, file_path):
        """
        Save the model to the specified file path
        """
        try:
            dir_path = os.path.dirname(file_path)
            os.makedirs(dir_path, exist_ok=True)
            with open(file_path, 'wb') as f:
                pickle.dump(self, f)
        except Exception as e:
            raise e

    @staticmethod
    def load(file_path):
        """
        Load the model from the specified file path
        """
        try:
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            raise e