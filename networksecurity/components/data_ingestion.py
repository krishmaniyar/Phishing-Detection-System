from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

## Configuration of Data Ingestion
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os, sys
import pymongo
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        """
        Export a MongoDB collection as a Pandas DataFrame.

        Args:
            collection_name (str): The name of the MongoDB collection to export.

        Returns:
            pd.DataFrame: A DataFrame containing the data from the specified collection.
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            logging.info(f"Connected to MongoDB database: {database_name}, collection: {collection_name}")
            df = pd.DataFrame(list(collection.find()))
            logging.info(f"Exported {len(df)} records from collection: {collection_name}")
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace(to_replace='na', value=pd.NA, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> str:
        try:
            feature_store_dir = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_dir)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Exporting data to feature store at: {self.data_ingestion_config.feature_store_file_path}")
            dataframe.to_csv(feature_store_dir, index=False, header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )
            logging.info("Successfully split data into training and testing sets")
            
            dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            train_set.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            
            logging.info(f"Exported training data to: {self.data_ingestion_config.train_file_path}")
            logging.info(f"Exported testing data to: {self.data_ingestion_config.test_file_path}")
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        """
        Initiates the data ingestion process by exporting data from MongoDB,
        splitting it into training and testing sets, and saving them to CSV files.

        Returns:
            tuple: Paths to the training and testing CSV files.
        """
        try:
            logging.info("Starting data ingestion process")
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifacts = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )
            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifacts}")
            return data_ingestion_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)