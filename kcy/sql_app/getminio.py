from minio import Minio
from minio.error import S3Error
from io import  BytesIO


client = Minio(
    "192.168.3.249:9000",
    access_key="6tXe3Z03SuBIPhqjaapd",
    secret_key="ACFa48Hc2yK2o3uIlsb6iDDhvDIsm3jWXDL4OsmM",
    secure=False  # 如果你的 MinIO 使用了 HTTPS，这里设置为 True
)



if __name__ == '__main__':
    buckets = client.list_buckets()
    for bucket in buckets:
        print(bucket.name, bucket.creation_date)