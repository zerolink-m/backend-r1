from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict


# Trust IP - специальная система для универсального определния айпи.
# IP = Это значит что например от tcp-айпи 127.0.0.1 он будет брать айпи из X-Real-Ip иначе - будет брать из tcp-айпи
# STRING = Это значит в не зависимости от tcp-айпи он будет смотреть хеадер Proxy-Pass-Ip и проверять если он имеет нужое значение то будет брать от X-Real-Ip иначе - tcp-айпи
# NO = берёт из tcp-айпи
class TrustIpMethodEnum(str, Enum):
    IP = "IP"
    STRING = "STRING"
    NO = "NO"

class LoggingEnum(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class Level(str, Enum):
    PROD = "PROD"
    TEST = "TEST"

class DatabaseTypeEnum(str, Enum):
    MYSQL = "MYSQL"

class JWTAlgorithmEnum(str, Enum):
    HS256 = "HS256"

class YesNo(str, Enum):
    YES = "YES"
    NO = "NO"

class S3_Addressing(str, Enum):
    PATH = "PATH"
    VIRTUAL = "VIRTUAL"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Настройки ДБ
    db_type: DatabaseTypeEnum = DatabaseTypeEnum.MYSQL
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "sqluser"
    db_password: str = ""
    db_name: str = "zerolink"

    # JWT
    jwt_access_secret: str = ""
    jwt_refresh_secret: str = ""
    jwt_algorithm: JWTAlgorithmEnum = JWTAlgorithmEnum.HS256
    jwt_access_expire: int = 900
    jwt_refresh_expire: int =  345600

    # Logging
    log_level: LoggingEnum = LoggingEnum.WARNING
    log_format: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    log_date_format: str = "%Y-%m-%d %H:%M:%S"
    log_file_enabled: YesNo = YesNo.NO
    log_file: str = "app.log"
    # MB
    log_file_max_size: int = 3
    log_file_backup_count: int = 5

    # SMTP
    smtp_enabled: YesNo = YesNo.NO
    smtp_host: str = "localhost"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = ""

    # S3
    s3_enabled: YesNo = YesNo.NO
    s3_bucket_in_path: YesNo = YesNo.NO
    s3_bucket: str = "0baef724-631e54-f68f30f"
    s3_url: str = "https://s3.storage.ru"
    s3_style: S3_Addressing = S3_Addressing.PATH
    s3_access: str = "abc"
    s3_secret: str = "abc"
    s3_region: str = "ru-1"
    s3_multipart_min_part_size: int = 5

    s3_cdn_enabled: YesNo = YesNo.NO
    s3_cdn_url: str = "https://s3.private.com"
    s3_cdn_key: str = "abc123"
    s3_cdn_token_live: int = 900

    # File, kb
    file_max_size: int = 10000
    file_min_size: int = 0

    # Настройки сервера
    level: Level = Level.TEST
    version: str = "v1.0.0R0-Alpha"
    host: str = "127.0.0.1"
    port: int = 8080

    # Система траста
    trust_ip_method: TrustIpMethodEnum = TrustIpMethodEnum.NO
    trust_ip_value: str = "127.0.0.1"

settings = Settings()
