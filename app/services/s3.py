# app/services/s3.py — async-функции для S3 через aioboto3
import aioboto3
from botocore.config import Config
from config import settings


_session = aioboto3.Session(
    aws_access_key_id=settings.s3_access,
    aws_secret_access_key=settings.s3_secret,
    region_name=settings.s3_region,
)


def make_client():
    """Новый S3-клиент. Стиль адресации из конфига (path = бакет в пути URL)."""
    style = settings.s3_style
    return _session.client(
        "s3",
        endpoint_url=settings.s3_url,
        config=Config(s3={"addressing_style": style}),
    )


async def upload_file(key: str, data: bytes, content_type: str = "application/octet-stream") -> int:
    """1. Загрузка файла в бакет. Возвращает размер."""
    async with make_client() as s3:
        await s3.put_object(Bucket=settings.s3_bucket, Key=key, Body=data, ContentType=content_type)
    return len(data)


async def delete_file(key: str) -> None:
    """2. Удаление файла. Если файла нет — просто ничего не делает."""
    async with make_client() as s3:
        await s3.delete_object(Bucket=settings.s3_bucket, Key=key)


async def download_file(key: str) -> bytes:
    """Скачать файл целиком в память."""
    async with make_client() as s3:
        resp = await s3.get_object(Bucket=settings.s3_bucket, Key=key)
        async with resp["Body"] as stream:
            return await stream.read()


async def file_exists(key: str) -> bool:
    """Проверить наличие файла."""
    async with make_client() as s3:
        try:
            await s3.head_object(Bucket=settings.s3_bucket, Key=key)
            return True
        except s3.exceptions.ClientError:
            return False


async def file_info(key: str) -> dict | None:
    """Метаданные файла (размер, etag, content_type). None, если файла нет."""
    async with make_client() as s3:
        try:
            head = await s3.head_object(Bucket=settings.s3_bucket, Key=key)
        except s3.exceptions.ClientError:
            return None
    return {
        "size": head["ContentLength"],
        "etag": head["ETag"].strip('"'),
        "content_type": head["ContentType"],
        "last_modified": int(head["LastModified"].timestamp()),
    }


async def presigned_url(key: str, expires: int = 900, upload: bool = False) -> str:
    """Временная ссылка. upload=True -> для ЗАГРУЗКИ клиентом (PUT), иначе для скачивания."""
    params: dict = {"Bucket": settings.s3_bucket, "Key": key}
    if upload:
        params["ContentType"] = "application/octet-stream"
    async with make_client() as s3:
        return await s3.generate_presigned_url(
            "put_object" if upload else "get_object",
            Params=params,
            ExpiresIn=expires,
        )