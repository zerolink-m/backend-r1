# app/utils/fileformat.py — распознавание формата файла по magic bytes + расширению
from app.models import FileFormat


# Расширения -> FileFormat
EXTENSION_MAP: dict[str, FileFormat] = {
    # image
    "png": FileFormat.image,
    "jpg": FileFormat.image,
    "jpeg": FileFormat.image,
    "gif": FileFormat.image,
    "webp": FileFormat.image,
    "bmp": FileFormat.image,
    "ico": FileFormat.image,
    "svg": FileFormat.image,
    "tiff": FileFormat.image,
    "heic": FileFormat.image,
    # video
    "mp4": FileFormat.video,
    "mkv": FileFormat.video,
    "webm": FileFormat.video,
    "avi": FileFormat.video,
    "mov": FileFormat.video,
    "flv": FileFormat.video,
    "wmv": FileFormat.video,
    "m4v": FileFormat.video,
    # music
    "mp3": FileFormat.music,
    "wav": FileFormat.music,
    "flac": FileFormat.music,
    "ogg": FileFormat.music,
    "m4a": FileFormat.music,
    "aac": FileFormat.music,
    "opus": FileFormat.music,
    # text
    "txt": FileFormat.text,
    "md": FileFormat.text,
    "log": FileFormat.text,
    "csv": FileFormat.text,
    "json": FileFormat.text,
    "xml": FileFormat.text,
    "yml": FileFormat.text,
    "yaml": FileFormat.text,
    "ini": FileFormat.text,
    "conf": FileFormat.text,
    # document
    "pdf": FileFormat.document,
    "doc": FileFormat.document,
    "docx": FileFormat.document,
    "xls": FileFormat.document,
    "xlsx": FileFormat.document,
    "ppt": FileFormat.document,
    "pptx": FileFormat.document,
    "odt": FileFormat.document,
    "rtf": FileFormat.document,
}

# Magic bytes -> FileFormat (префиксы, порядок важен — более специфичные выше)
MAGIC_MAP: list[tuple[bytes, FileFormat]] = [
    # image
    (b"\x89PNG\r\n\x1a\n", FileFormat.image),          # PNG
    (b"\xff\xd8\xff", FileFormat.image),                 # JPEG
    (b"GIF87a", FileFormat.image),
    (b"GIF89a", FileFormat.image),
    (b"BM", FileFormat.image),                           # BMP (слабый, но ок после специфичных)
    (b"II*\x00", FileFormat.image),                      # TIFF LE
    (b"MM\x00*", FileFormat.image),                      # TIFF BE
    # video
    (b"\x1a\x45\xdf\xa3", FileFormat.video),             # MKV / WebM
    (b"FLV\x01", FileFormat.video),
    (b"\x30\x26\xb2\x75\x8e\x66\xcf\x11", FileFormat.video),  # AVI / WMV (RIFF-ASF)
    # music
    (b"ID3", FileFormat.music),                          # MP3 с ID3-тегом
    (b"\xff\xfb", FileFormat.music),                     # MP3 frame
    (b"\xff\xf3", FileFormat.music),                     # MP3 frame
    (b"\xff\xf2", FileFormat.music),                     # MP3 frame
    (b"fLaC", FileFormat.music),
    (b"OggS", FileFormat.music),                         # OGG (аудио/видео, чаще аудио)
    (b"RIFF", FileFormat.video),                         # AVI/WAV — уточняется ниже по RIFF-типу
    # document
    (b"%PDF", FileFormat.document),
    (b"\xd0\xcf\x11\xe0", FileFormat.document),          # старый MS Office (doc/xls/ppt)
    # архивы и прочее -> file
    (b"\x1f\x8b", FileFormat.file),                      # gzip
    (b"PK\x03\x04", FileFormat.file),                    # zip / docx / xlsx (уточняется по расширению)
    (b"7z\xbc\xaf\x27\x1c", FileFormat.file),
    (b"Rar!\x1a\x07", FileFormat.file),
]


def detect_format(head: bytes, filename: str = "") -> FileFormat:
    """
    Определить формат файла.
    head — первые байты файла (достаточно 16-32 байт).
    filename — оригинальное имя (fallback по расширению, если magic не распознан).

    Возвращает FileFormat (никогда не None; неизвестное -> FileFormat.file).
    """
    # 1. RIFF-контейнер: смотрим тип на смещении 8 (WAV = музыка, AVI = видео)
    if head.startswith(b"RIFF") and len(head) >= 12:
        riff_type = head[8:12]
        if riff_type == b"WAVE":
            return FileFormat.music
        if riff_type == b"AVI ":
            return FileFormat.video
        if riff_type == b"WEBP":
            return FileFormat.image

    # 2. MP4: ftyp-бокс на смещении 4 (видео/аудио/картинка — считаем видео)
    if len(head) >= 12 and head[4:8] == b"ftyp":
        brand = head[8:12]
        if brand in (b"M4A ", b"M4B "):
            return FileFormat.music
        if brand == b"heic":
            return FileFormat.image
        return FileFormat.video

    # 3. Общий проход по magic-префиксам
    for magic, fmt in MAGIC_MAP:
        if head.startswith(magic):
            # zip-контейнер: docx/xlsx/pptx — это документы, если расширение говорит об этом
            if magic == b"PK\x03\x04":
                ext = _extension(filename)
                if ext in ("docx", "xlsx", "pptx", "odt"):
                    return FileFormat.document
            return fmt

    # 4. Fallback по расширению
    ext_fmt = EXTENSION_MAP.get(_extension(filename))
    if ext_fmt is not None:
        return ext_fmt

    # 5. Fallback: похоже на текст (все байты печатаемые/переносы) -> text
    if head and all(b == 0x09 or b == 0x0a or b == 0x0d or 0x20 <= b < 0x7f for b in head):
        return FileFormat.text

    return FileFormat.file


def _extension(filename: str) -> str:
    """Расширение без точки, lowercase. Пустая строка, если нет."""
    name = filename.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    if "." not in name or name.startswith(".") and name.count(".") == 1:
        return ""
    return name.rsplit(".", 1)[-1].lower()
