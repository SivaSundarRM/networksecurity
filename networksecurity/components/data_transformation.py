import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (DataValidationArtifact,DataTransformationArtifact)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object,load_object

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def get_data_transformer_object(self)->Pipeline:
        logging.info("Entering the get_data_transformer_object method of Data_Transformation class")
        try:
            imputer_params=DATA_TRANSFORMATION_IMPUTER_PARAMS
            knn_imputer=KNNImputer(**imputer_params)
            pipeline=Pipeline(steps=[
                ("KNNImputer",knn_imputer)
            ])
            return pipeline
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    
    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Initiating data transformation")
        try:
            logging.info("Reading the train and test file")
            train_df=pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            test_df=pd.read_csv(self.data_validation_artifact.valid_test_file_path)

            logging.info("Splitting input and target feature from train and test dataframe")
            x_train=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            y_train=train_df[TARGET_COLUMN]
            y_train = y_train.replace(-1, 0)

            x_test=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            y_test=test_df[TARGET_COLUMN]
            y_test = y_test.replace(-1, 0 )

            logging.info("Applying KNN Imputer to impute missing values in train and test data")
            knn_imputer=self.get_data_transformer_object()
            x_train=knn_imputer.fit_transform(x_train)
            x_test=knn_imputer.transform(x_test)

            train_arr=np.c_[x_train,y_train]
            test_arr=np.c_[x_test,y_test]   
            
    

            # transformed_train_dir=os.path.dirname(self.data_transformation_config.transformed_train_file_path)
            # transformed_test_dir=os.path.dirname(self.data_transformation_config.transformed_test_file_path)

            # os.makedirs(transformed_train_dir,exist_ok=True)
            # os.makedirs(transformed_test_dir,exist_ok=True)
            logging.info("Saving transformed train and test array")
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path,obj=knn_imputer)
             
            save_object("final_model/knn_imputer.pkl",knn_imputer)
            data_transformation_artifact=DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    