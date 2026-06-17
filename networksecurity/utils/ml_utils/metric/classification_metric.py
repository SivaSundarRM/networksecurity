from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from sklearn.metrics import f1_score, precision_score, recall_score
from networksecurity.exception.exception import NetworkSecurityException
import sys
def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        f1=f1_score(y_true, y_pred,average='weighted',zero_division=0)
        precision=precision_score(y_true, y_pred,average='weighted',zero_division=0)
        recall=recall_score(y_true, y_pred,average='weighted',zero_division=0)
        classification_metric_artifact=ClassificationMetricArtifact(f1_score=f1,
                                                                    precision_score=precision,
                                                                    recall_score=recall)
        return classification_metric_artifact
    except Exception as e:
        raise NetworkSecurityException(e, sys)