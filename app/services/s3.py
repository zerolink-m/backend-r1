# app/services/s3.py — async-функции для S3 через aioboto3
from typing import TYPE_CHECKING

import aioboto3
from botocore.config import Config
from config import settings

if TYPE_CHECKING:
    from app.models import FileFormat


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


# --- Multipart upload (стриминговая загрузка больших файлов) ---

MULTIPART_MIN_PART_SIZE = 5 * 1024 * 1024  # S3: каждая часть (кроме последней) >= 5MB


async def multipart_create(key: str, content_type: str = "application/octet-stream") -> str:
    """Начать multipart-загрузку. Возвращает upload_id."""
    async with make_client() as s3:
        resp = await s3.create_multipart_upload(
            Bucket=settings.s3_bucket,
            Key=key,
            ContentType=content_type,
        )
    return resp["UploadId"]


async def multipart_upload_part(key: str, upload_id: str, part_number: int, data: bytes) -> dict:
    """Загрузить одну часть (нумерация с 1). Возвращает {"PartNumber", "ETag"} для complete."""
    async with make_client() as s3:
        resp = await s3.upload_part(
            Bucket=settings.s3_bucket,
            Key=key,
            UploadId=upload_id,
            PartNumber=part_number,
            Body=data,
        )
    return {"PartNumber": part_number, "ETag": resp["ETag"].strip('"')}


async def multipart_complete(key: str, upload_id: str, parts: list[dict]) -> None:
    """Завершить загрузку. parts — список, возвращённый multipart_upload_part (по возрастанию PartNumber)."""
    async with make_client() as s3:
        await s3.complete_multipart_upload(
            Bucket=settings.s3_bucket,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts},
        )


async def multipart_abort(key: str, upload_id: str) -> None:
    """Отменить загрузку (например, клиент оборвал соединение). S3 удалит уже загруженные части."""
    async with make_client() as s3:
        await s3.abort_multipart_upload(
            Bucket=settings.s3_bucket,
            Key=key,
            UploadId=upload_id,
        )


async def multipart_stream(
    key: str,
    stream,
    content_type: str = "application/octet-stream",
    max_size: int | None = None,
    min_size: int | None = None,
) -> tuple[int, "FileFormat"]:
    """
    Стриминговая multipart-загрузка из async-итератора байтов (например request.stream()).
    Файл никогда не лежит в памяти целиком.

    Возвращает (size, format): размер в БАЙТАХ и распознанный формат
    (app.models.FileFormat) по magic bytes первых чанков (fallback — расширение из filename).

    Лимиты (в байтах):
    - max_size / min_size — опционально; дефолт settings.file_max_size / settings.file_min_size (KB).
    - Content-Length из заголовка проверяется ДО создания multipart upload.
    - Если по факту пришло меньше min_size или больше max_size — abort + CursedException.
    """
    from app.utils import CursedException, codes, detect_format

    if max_size is None:
        max_size = settings.file_max_size * 1024
    if min_size is None:
        min_size = settings.file_min_size * 1024

    upload_id: str | None = None
    parts: list[dict] = []
    buffer = b""
    head = b""  # первые байты для распознавания формата
    total = 0
    part_number = 1
    try:
        # 0. Предварительная проверка по Content-Length (без создания multipart upload)
        declared = None
        header = getattr(stream, "headers", None)
        if header is not None:
            raw = header.get("content-length")
            if raw is not None:
                try:
                    declared = int(raw)
                except ValueError:
                    raise CursedException(
                        code=codes.BAD_REQUEST,
                        error="Content-Length header is not a valid integer.",
                    )
        if declared is not None:
            if declared < min_size:
                raise CursedException(
                    code=codes.TOO_LARGE,
                    error=f"File size {declared} bytes is less than minimum {min_size} bytes.",
                )
            if declared > max_size:
                raise CursedException(
                    code=codes.TOO_SMALL,
                    error=f"File size {declared} bytes exceeds maximum {max_size} bytes.",
                )

        upload_id = await multipart_create(key, content_type)
        async for chunk in stream:
            total += len(chunk)
            # 2. Превышен максимум по факту — отмена
            if total > max_size:
                raise CursedException(
                    code=codes.TOO_LARGE,
                    error=f"Uploaded size {total} bytes exceeds maximum {max_size} bytes.",
                )
            if len(head) < 32:
                head += chunk[:32 - len(head)]
            buffer += chunk
            while len(buffer) >= MULTIPART_MIN_PART_SIZE:
                part, buffer = buffer[:MULTIPART_MIN_PART_SIZE], buffer[MULTIPART_MIN_PART_SIZE:]
                parts.append(await multipart_upload_part(key, upload_id, part_number, part))
                part_number += 1
        # 1. Загрузка закончилась, не достигнув минимума — отмена
        if total < min_size:
            raise CursedException(
                code=codes.TOO_LARGE,
                error=f"Uploaded size {total} bytes is less than minimum {min_size} bytes.",
            )
        if buffer:
            parts.append(await multipart_upload_part(key, upload_id, part_number, buffer))
        await multipart_complete(key, upload_id, parts)
    except Exception:
        if upload_id is not None:
            try:
                await multipart_abort(key, upload_id)
            except Exception:
                pass
        raise
    return total, detect_format(head, key)