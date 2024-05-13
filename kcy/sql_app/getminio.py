from minio import Minio
from minio.error import S3Error
from io import BytesIO


def get_minio_client():
    client = Minio(
        "127.0.0.1:9000",
        access_key="RISIOIC1JGUrr2mxCQ1U",
        secret_key="L4jHoulLDdio9dKl6ScaanCfhjNJzoUIdi3GSmRF",
        secure=False  # 如果你的 MinIO 使用了 HTTPS，这里设置为 True
    )
    return client
