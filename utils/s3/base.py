from fastapi import UploadFile
from minio import Minio


class S3Storage:

    def __init__(self, endpoint, access_key, secret_key, bucket_name):
        self.endpoint = endpoint
        self.client = Minio(endpoint=endpoint,
                            access_key=access_key, secret_key=secret_key,
                            cert_check=False)
        self.bucket_name = bucket_name

    def upload_file(self, path, file: UploadFile):
        self.client.put_object(
            self.bucket_name, path, file.file, file.size, content_type=file.content_type
        )

    def get_file_url(self, path):
        return f'http://{self.endpoint}/{self.bucket_name}{path}'

