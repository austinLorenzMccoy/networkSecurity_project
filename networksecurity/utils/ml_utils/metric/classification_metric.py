## NETWORKSECURITY/networksecurity/utils/ml_utils/metric/classification_metric.py

from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import precision_score, recall_score, f1_score
import sys

def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        model_precision = precision_score(y_true, y_pred)
        model_recall = recall_score(y_true, y_pred)
        model_f1 = f1_score(y_true, y_pred)

        classification_metric = ClassificationMetricArtifact(f1Score=model_f1, precisionScore=model_precision, recallScore=model_recall)
        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e, sys)
        