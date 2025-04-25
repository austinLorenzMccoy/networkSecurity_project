## NETWORKSECURITY/networksecurity/utils/main_utils/utils.py

import os
import sys
import numpy as np
import joblib
import yaml
from typing import Any, Dict

def read_yaml_file(file_path: str) -> Dict:
    """Read a YAML configuration file."""
    try:
        with open(file_path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise ValueError(f"Error reading YAML file: {e}")

def write_yaml_file(file_path: str, content: Dict, replace: bool = False):
    """Write data to a YAML configuration file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # If replace is False and file exists, load existing content and update
        if not replace and os.path.exists(file_path):
            with open(file_path, 'r') as existing_file:
                existing_content = yaml.safe_load(existing_file) or {}
            existing_content.update(content)
            content = existing_content

        with open(file_path, 'w') as yaml_file:
            yaml.dump(content, yaml_file, default_flow_style=False)
    except Exception as e:
        raise ValueError(f"Error writing YAML file: {e}")

def save_numpy_array_data(file_path: str, array: np.ndarray):
    """Save NumPy array to a file."""
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Ensure the file has .npz extension
        if not file_path.endswith('.npz'):
            file_path = file_path + '.npz'
        
        # Save the array with a key
        np.savez_compressed(file_path, data=array)
    except Exception as e:
        raise ValueError(f"Error saving NumPy array: {e}")

def load_numpy_array_data(file_path: str) -> np.ndarray:
    """Load NumPy array from a file."""
    try:
        # Ensure the file has .npz extension
        if not file_path.endswith('.npz'):
            file_path = file_path + '.npz'
        
        # Load the array with pickle enabled for object arrays
        with np.load(file_path, allow_pickle=True) as data:
            # Check if 'data' exists, otherwise return first available array
            return data['data'] if 'data' in data else data[list(data.keys())[0]]
    except FileNotFoundError:
        raise FileNotFoundError(f"File does not exist: {file_path}")
    except Exception as e:
        raise ValueError(f"Error loading NumPy array: {e}")


def save_object(file_path: str, obj: Any):
    """Save Python object using joblib."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        joblib.dump(obj, file_path)
    except Exception as e:
        raise ValueError(f"Error saving object: {e}")

def load_object(file_path: str) -> Any:
    """Load Python object using joblib."""
    try:
        return joblib.load(file_path)
    except Exception as e:
        raise ValueError(f"Error loading object: {e}")

def evaluate_models(x_train, y_train, x_test, y_test, models, params):
    """Evaluate multiple machine learning models."""
    try:
        model_report = {}
        for name, model in models.items():
            model.fit(x_train, y_train)
            y_pred = model.predict(x_test)
            model_report[name] = np.mean(y_pred == y_test)
        return model_report
    except Exception as e:
        raise ValueError(f"Error evaluating models: {e}")