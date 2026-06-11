import os
import sys

from dotenv import load_dotenv
load_dotenv()

import certifi
import pymongo
import pandas as pd

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger


MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ca = certifi.where()


class NetworkDataExtract:

    def __init__(self):
        try:
            self.client = pymongo.MongoClient(
                MONGO_DB_URL,
                tlsCAFile=ca
            )
            logger.info("MongoDB client created successfully")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convert(self, file_path):
        try:
            df = pd.read_csv(file_path)

            df.reset_index(drop=True, inplace=True)

            # Preserve column names
            records = df.to_dict(orient="records")

            logger.info(
                f"CSV converted to JSON records successfully. Total records: {len(records)}"
            )

            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongodb(self, records, database_name, collection_name):
        try:
            db = self.client[database_name]

            collection = db[collection_name]

            result = collection.insert_many(records)

            logger.info(
                f"{len(result.inserted_ids)} documents inserted successfully"
            )

            return len(result.inserted_ids)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":

    FILE_PATH = r"C:\Users\sivar\Desktop\NetworkSecurity\Network_Data\phisingData.csv"

    DATABASE_NAME = "Siva"
    COLLECTION_NAME = "NetworkSecurity"

    network_data_extract = NetworkDataExtract()

    records = network_data_extract.csv_to_json_convert(FILE_PATH)

    print("Sample Record:")
    print(records[0])

    inserted_count = network_data_extract.insert_data_to_mongodb(
        records,
        DATABASE_NAME,
        COLLECTION_NAME
    )

    print(f"{inserted_count} records inserted successfully into MongoDB")