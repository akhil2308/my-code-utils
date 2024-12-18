import re
import os
import boto3
import urllib.parse
from datetime import datetime
from urllib.parse import urlparse

import logging
logger = logging.getLogger(__name__)


class S3Client:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, bucket_name):
        self.session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.s3 = self.session.client('s3')
        self.bucket_name = bucket_name

    def upload_file(self, file_path, object_key, metadata=None):
        """
        Uploads a file to the specified S3 bucket.

        Args:
            file_path (str): Path of the file to be uploaded.
            object_key (str): Key under which the file will be stored in the bucket.

        Returns:
            str or None: The URL of the uploaded file, or None if upload failed.
        """
        try:
            if metadata:
                filtered_dict = {key: value for key, value in metadata.items() if value is not None}
                extra_args = {'Metadata': filtered_dict}
            else:
                extra_args = {}
            
            self.s3.upload_file(file_path, self.bucket_name, object_key, ExtraArgs=extra_args)
            
            logger.info(f"File '{file_path}' uploaded successfully to S3 bucket '{self.bucket_name}' with key '{object_key}'.")
            return object_key
        except Exception as e:
            logger.error(f"Error uploading file to S3: {e}")
            return None
    
    def upload_fileobj(self, file_object, object_key, metadata=None):
        """
        Uploads a file to the specified S3 bucket.

        Args:
            file_object (File object): File object to be uploaded.
            folder_name (str): Name of the folder in the bucket.
            object_key (str): Key under which the file will be stored in the bucket.

        Returns:
            tuple: A tuple containing the URL of the uploaded file and the object key,
                   or None if upload failed.
        """
        try:
            if metadata:
                filtered_dict = {key: value for key, value in metadata.items() if value is not None}
                extra_args = {'Metadata': filtered_dict}
            else:
                extra_args = {}
            
            # Upload the file object to S3
            self.s3.upload_fileobj(file_object, self.bucket_name, object_key, ExtraArgs=extra_args)
            
            logger.info(f"File '{object_key}' uploaded successfully to S3 bucket '{self.bucket_name}'.")
            return object_key
        except Exception as e:
            logger.error(f"Error uploading file to S3: {e}")
            return None
        
    def get_presigned_url(self, object_key, expiration=3600):
        """
        Generates a pre-signed URL for accessing a file in the S3 bucket.

        Args:
            object_key (str): Key of the object in the bucket.
            expiration (int, optional): Expiration time of the URL in seconds. Defaults to 3600.

        Returns:
            str or None: The pre-signed URL, or None if an error occurred.
        """
        try:
            url = self.s3.generate_presigned_url( 
                ClientMethod='get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_key},
                ExpiresIn=expiration
                )
            return url
        except Exception as e:
            logger.error(f"Error generating pre-signed URL for object in S3: {e}")
            return None
    
    def delete_object(self, object_key):
        """
        Deletes an object from the S3 bucket.

        Args:
            object_key (str): Key of the object to be deleted.

        Returns:
            None
        """
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=object_key)
            logger.info(f"Object with key '{object_key}' deleted successfully from bucket '{self.bucket_name}'.")
        except Exception as e:
            logger.error(f"Error deleting object from S3: {e}")

    def download_file(self, object_key, local_file_path):
        """
        Downloads a file from the specified S3 bucket.

        Args:
            object_key (str): Key of the object to be downloaded.
            local_file_path (str): Local file path where the downloaded file will be saved.

        Returns:
            bool: True if download successful, False otherwise.
        """
        try:
            self.s3.download_file(self.bucket_name, object_key, local_file_path)
            logger.info(f"File with key '{object_key}' downloaded successfully from S3 bucket '{self.bucket_name}' to '{local_file_path}'.")
            return True
        except Exception as e:
            logger.error(f"Error downloading file from S3: {e}")
            return False
    
    def list_objects(self):
        """
        Lists all objects in the S3 bucket.

        Returns:
            list or None: A list of object keys, or None if an error occurred.
        """
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            objects = [obj['Key'] for obj in response.get('Contents', [])]
            return objects
        except Exception as e:
            print(f"Error listing objects in S3 bucket: {e}")
            return None