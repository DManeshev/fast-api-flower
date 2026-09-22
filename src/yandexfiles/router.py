from boto3 import session
from config import settings

from fastapi import APIRouter

bucket_name = "flower-storage"

# yandex_session = boto3.Session()

ENDPOINT = "https://storage.yandexcloud.net"

router = APIRouter()

def get_s3_instance():
    yandex_session = session.Session()

    yandex_session = session.Session(
        aws_access_key_id=(settings.YANDEX_ACCESS_KEY),
        aws_secret_access_key=(settings.YANDEX_SECRET_KEY),
        region_name="ru-central1",
    )

    return yandex_session.client(
        "s3", endpoint_url=ENDPOINT
    )

# TODO: ALL METHOD AUTH
@router.get("")
async def getListImage():
    list_buckets= get_s3_instance().list_buckets()

    return list_buckets
    # for key in s3.list_objects(Bucket=bucket_name)['Content']:
    #     print(key)
    #     return key
