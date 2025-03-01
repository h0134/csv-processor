from PIL import Image
from minio import Minio
from minio.error import S3Error
from datetime import timedelta
import io

class MinioUtil:
    def __init__(self, minio_url, access_key, secret_key, bucket_name):
        self.minio_client = Minio(
            minio_url, 
            access_key=access_key, 
            secret_key=secret_key, 
            secure=False  
        )
        self.bucket_name = bucket_name
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            if not self.minio_client.bucket_exists(self.bucket_name):
                self.minio_client.make_bucket(self.bucket_name)
                print(f"Bucket '{self.bucket_name}' created.")
            else:
                print(f"Bucket '{self.bucket_name}' already exists.")
        except S3Error as e:
            print(f"Error checking or creating bucket: {str(e)}")
    
    def upload_image(self, img: Image, file_name: str):
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0) 
        
        try:
            print("hello filename")
            print(file_name)
            self.minio_client.put_object(self.bucket_name, file_name, img_byte_arr, len(img_byte_arr.getvalue()))
            print(f"Image '{file_name}' uploaded successfully.")

            # Generate the presigned URL
            presigned_url = self.generate_presigned_url(file_name)
            return presigned_url

        except S3Error as e:
            print(f"Error uploading image: {str(e)}")
            return None

    def generate_presigned_url(self, file_name, expiration_seconds=3600):
        expiration = timedelta(seconds=expiration_seconds)

        try:
            url = self.minio_client.presigned_get_object(self.bucket_name, file_name, expires=expiration)
            print(f"Presigned URL generated: {url}")
            return url
        except S3Error as e:
            print(f"Error generating presigned URL: {str(e)}")
            return None
