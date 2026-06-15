import os
import sys
import yaml
import pandas as pd

from scipy.stats import ks_2samp

from networksecurity.entity.artifact_entity import (
    DataValidationArtifact
)
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging



def read_yaml_file(file_path: str) -> dict:
        try:
            with open(file_path, "rb") as yaml_file:
                return yaml.safe_load(yaml_file)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    
def write_yaml_file(file_path: str, data: dict):
        try:
            dir_path = os.path.dirname(file_path)
            os.makedirs(dir_path, exist_ok=True)

            with open(file_path, "w") as yaml_file:
                yaml.dump(data, yaml_file)

        except Exception as e:
            raise NetworkSecurityException(e, sys)
    