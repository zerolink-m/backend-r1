# Успех
SUCCESS = 0
CREATED = 1
EDITED = 2
PARTIALLY_EDITED = 3
DELETED = 4
ACCEPTED_FOR_WORK = 5
NOT_CHANGED = 6
TEMPORARY_REDIRECTED = 7
AUTHORIZED = 8
REDIRECTED = 9
STREAMING_RESPONSE = 10
PARTIALLY_SUCCESS = 11

# Ошибка
VALIDATION_ERROR = 50
TOKEN_ERROR = 51
TOKEN_EXPIRED = 52
TOKEN_SIGN_INCORRECT_KEY = 53
TOKEN_HAS_INCORRECT_ALGORITHM = 54
FORBIDDEN = 55
FORBIDDEN_ROLE = 56
FORBIDDEN_RESOURCE = 57
BAD_REQUEST = 58
METHOD_NOT_ALLOWED = 59
CONFLICT = 60
OBJECT_FIELD_EXISTS = 61
TOO_LARGE = 62
BAD_GATEWAY = 63
DB_ERROR = 64
RATE_LIMITED = 65
SERVICE_UNAVAILABLE = 66
SERVICE_OVERLOADED = 67
FIELDS_INCORRECT_AUTHORIZATION_ERROR = 68
FIELD_NOT_EDITABLE = 69
FILE_NOT_FOUND = 70
FILE_BAD_FORMAT = 71
S3_DISABLED = 72
YOU_ARE_BLOCKED = 73
S3_ERROR = 74
DATACENTER_NOT_FOUND = 75
REMNAWAVE_ERROR = 76
WGDASHBOARD_ERROR = 77
FUNCTION_NOT_IMPLEMENTED = 78
OBJECT_HAS_CHILDS = 79
TOO_SMALL = 80

OBJECT_NOT_FOUND = 96
AVATAR_NOT_FOUND = 97
NOT_FOUND = 98
INTERNAL_SERVER_ERROR = 99

HTTP_MAP = {
    SUCCESS: 200,
    CREATED: 201,
    EDITED: 200,
    PARTIALLY_EDITED: 200,
    DELETED: 200,
    ACCEPTED_FOR_WORK: 202,
    NOT_CHANGED: 304,
    TEMPORARY_REDIRECTED: 307,
    AUTHORIZED: 200,
    REDIRECTED: 301,
    STREAMING_RESPONSE: 200,
    PARTIALLY_SUCCESS: 200,

    VALIDATION_ERROR: 422,
    TOKEN_ERROR: 401,
    TOKEN_EXPIRED: 401,
    TOKEN_SIGN_INCORRECT_KEY: 401,
    TOKEN_HAS_INCORRECT_ALGORITHM: 401,
    FORBIDDEN: 403,
    FORBIDDEN_ROLE: 403,
    FORBIDDEN_RESOURCE: 403,
    BAD_REQUEST: 400,
    METHOD_NOT_ALLOWED: 405,
    CONFLICT: 409,
    OBJECT_FIELD_EXISTS: 409,
    TOO_LARGE: 413,
    BAD_GATEWAY: 502,
    DB_ERROR: 500,
    RATE_LIMITED: 429,
    SERVICE_UNAVAILABLE: 503,
    SERVICE_OVERLOADED: 503,
    FIELDS_INCORRECT_AUTHORIZATION_ERROR: 401,
    FIELD_NOT_EDITABLE: 403,
    FILE_NOT_FOUND: 404,
    FILE_BAD_FORMAT: 406,
    S3_DISABLED: 503,
    YOU_ARE_BLOCKED: 403,
    S3_ERROR: 500,
    DATACENTER_NOT_FOUND: 404,
    REMNAWAVE_ERROR: 502,
    WGDASHBOARD_ERROR: 502,
    FUNCTION_NOT_IMPLEMENTED: 501,
    OBJECT_HAS_CHILDS: 409,
    TOO_SMALL: 400,

    OBJECT_NOT_FOUND: 404,
    AVATAR_NOT_FOUND: 404,
    NOT_FOUND: 404,
    INTERNAL_SERVER_ERROR: 500
}

DETAILS_MAP = {
    SUCCESS: "Success",
    CREATED: "Created succesfully",
    EDITED: "Edited succesfully",
    PARTIALLY_EDITED: "Partially edited succesfully",
    DELETED: "Deleted succesfully",
    ACCEPTED_FOR_WORK: "Accepted for work",
    NOT_CHANGED: "Not changed",
    TEMPORARY_REDIRECTED: "Temporary redirected",
    AUTHORIZED: "Authorized succesfully",
    REDIRECTED: "Redirected",
    STREAMING_RESPONSE: "Streaming response.",
    PARTIALLY_SUCCESS: "Partially success.",

    VALIDATION_ERROR: "Validation error.",
    TOKEN_ERROR: "Token error.",
    TOKEN_EXPIRED: "The token has expired.",
    TOKEN_SIGN_INCORRECT_KEY: "The token is signed with an incorrect key.",
    TOKEN_HAS_INCORRECT_ALGORITHM: "The token has an invalid algorithm.",
    FORBIDDEN: "The resource is not permitted for one or more objects.",
    FORBIDDEN_ROLE: "Forbidden due to an incorrect role.",
    FORBIDDEN_RESOURCE: "Access to this resource is denied for this object.",
    BAD_REQUEST: "Invalid request.",
    METHOD_NOT_ALLOWED: "The method is not permitted for one or more objects.",
    CONFLICT: "General conflict.",
    OBJECT_FIELD_EXISTS: "The field already exists for this object or one of the objects.",
    TOO_LARGE: "The request field contains extra elements, or the total request size has been exceeded.",
    BAD_GATEWAY: "The external API is unavailable for one reason or another.",
    DB_ERROR: "The external database is unavailable for one reason or another.",
    RATE_LIMITED: "Request limit exceeded for one or more objects.",
    SERVICE_UNAVAILABLE: "The service is unavailable for one reason or another.",
    SERVICE_OVERLOADED: "The service is under heavy load.",
    FIELDS_INCORRECT_AUTHORIZATION_ERROR: "One or more fields are incorrect. Authorization is not possible.",
    FIELD_NOT_EDITABLE: "This fields cannot edit for one or more objects.",
    FILE_NOT_FOUND: "File not found.",
    FILE_BAD_FORMAT: "The file format is not suitable.",
    S3_DISABLED: "File storage is temporarily unavailable.",
    YOU_ARE_BLOCKED: "You are blocked.",
    S3_ERROR: "External object storage error.",
    DATACENTER_NOT_FOUND: "Datacenter not found.",
    REMNAWAVE_ERROR: "The remnawave API is unavailable for one reason or another.",
    WGDASHBOARD_ERROR: "The wgdashboard API is unavailable for one reason or another.",
    FUNCTION_NOT_IMPLEMENTED: "This function is not currently implemented.",
    OBJECT_HAS_CHILDS: "The object has child objects.",
    TOO_SMALL: "The request field is missing elements, or the total request size is below the minimum allowed limit.",

    OBJECT_NOT_FOUND: "Object not found.",
    AVATAR_NOT_FOUND: "Avatar file not found.",
    NOT_FOUND: "Resource not found.",
    INTERNAL_SERVER_ERROR: "Server error.",
}

import logging

# Функция делает мапу на HTTP код с курседа
# В случае если кода нет возвращает 500
def http_map(code: int) -> int:
    result = int(HTTP_MAP.get(code, 500))
    logging.debug(f"http_map({code}) -> {result}")
    return result

# Функция делет мапу на детаилс код с курседа
# В случае если нету то Server error.!!!!!!!!!!!!!!!!
def detail_map(code: int) -> str:
    result = str(DETAILS_MAP.get(code, "Server error."))
    logging.debug(f"detail_map({code}) -> {result}")
    return result
