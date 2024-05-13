from kcy.sql_app import getminio
from io import BytesIO
from kcy.sql_app import crud
import  requests
if __name__ == '__main__':
    image_path = "2024-05-08/30f692afce29d4f8958013cc3f6e27b8.jpg"
    file_name = image_path.split('/')[1]
    print(file_name)
    bucket_name = "images"
    client = getminio.get_minio_client()
    response = client.fget_object(bucket_name,image_path,file_name)
    print(response)

