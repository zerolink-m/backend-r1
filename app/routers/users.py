# app/routers/users.py
from app.utils import (
    require_authorization,
    check_resource_access,
    ResourceOperation,
    CursedResponser,
    CursedException,
    CursedStreamingResponser,
    codes,
    model_to_dict,
    models_to_dict,
    check_fields,
    now,
    hash_password,
    verify_password,
    apply_query_params,
    CursedJSON
)
from app import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.schemas import QueryParams
from fastapi import APIRouter, Depends, Query, Request
from app.models import (
    User,
    UserRole,
    Ticket,
    File,
    FileFormat,
    Session,
    Message,
    Message_Files,
    Subscription,
    PayHistory,
    Code,
    Packet,
    MethodOne,
    MethodTwo
)
from app.services import (
    delete_file
)
from botocore.exceptions import (
    BotoCoreError,
    ClientError,
    ParamValidationError,
    NoCredentialsError,
    EndpointConnectionError,
    ConnectionError,
    ReadTimeoutError
)
from app.schemas import EditUser, CreateUser, Reason
from config import settings, YesNo
from remnawave.exceptions import (
    ApiError,
    NotFoundError,
    ForbiddenError,
    UnauthorizedError,
    RateLimitError,
    BadRequestError,
    ServerError
)
import httpx
from app.services import (
    WGDashboardAPIError,
    WGDashboardAuthError,
    WGDashboardConnectionError,
    WGDashboardError,
    WGDashboardNotFoundError,
    WGDashboardResponseError
)


router = APIRouter(
    prefix="/v1/users",
    tags=["users"]
)

SEARCHABLE_COLUMNS = ["id","name", "surname", "balance", "region", "possible_region", "email", "avatar", "role", "blocked", "blocked_reason", "updated_at", "added_at"]
ALLOWED_FIELDS = ["avatar", "name", "surname", "password", "region"]
# Поля, которые никогда не должны попадать в ответы API
PRIVATE_USER_FIELDS = ["password"]

# Готов
@router.get("/{user_id}")
async def get_one_user(
    user_id: int,
    reason: Reason | None = Query(default=None, max_length=64),
    reason_value: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["guest", "user", "support", "admin"]))
):
    # Явная проверка is not None, чтобы reason_value=0 не пропускался как falsy
    if reason == Reason.ticket and reason_value is not None:
        ticket = (await db.execute(
            select(Ticket).where(Ticket.id == reason_value)
        )).scalar_one_or_none()

        # Если тикета нет
        if ticket is None:
            return CursedResponser(
                code=codes.FORBIDDEN_RESOURCE,
                data={},
                error=f"Ticket {reason_value} is not exists."
            )
        
        # Если саппорт то должно совпадать лол
        if auth["user"].role == UserRole.SUPPORT:
            if ticket.support_id != auth["user"].id:
                return CursedResponser(
                    code=codes.FORBIDDEN_RESOURCE,
                    data={},
                    error="Bad reason."
                )
            if ticket.user_id != user_id:
                return CursedResponser(
                    code=codes.FORBIDDEN_RESOURCE,
                    data={},
                    error="Bad reason."
                )

        # Проверка остальных ролей
        else:
            if ticket.user_id != auth["user"].id:
                return CursedResponser(
                    code=codes.FORBIDDEN_RESOURCE,
                    data={},
                    error="Bad reason."
                )

            if ticket.support_id != user_id:
                return CursedResponser(
                    code=codes.FORBIDDEN_RESOURCE,
                    data={},
                    error="Bad reason."
                )
                      
    else:
        check_resource_access(
            requesting_user=auth["user"],
            resource_owner_id=user_id,
            operation=ResourceOperation.GET
        )

    if user_id == auth["user"].id:
        return CursedResponser(
            code=codes.SUCCESS,
            data={"user": model_to_dict(model=auth["user"], exclude=PRIVATE_USER_FIELDS)}
        )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    result = result.scalar_one_or_none()

    if not result:
        raise CursedException(
            code = codes.NOT_FOUND,
            error = f"Resource {user_id} not found"
        )

    result_dict = model_to_dict(model=result, exclude=PRIVATE_USER_FIELDS)

    if reason == Reason.ticket and reason_value is not None:
        for delete_from_response in ["email", "password", "region", "possible_region"]:
            result_dict.pop(delete_from_response, None)

    return CursedResponser(
        code = codes.SUCCESS,
        data = {
            "user": result_dict
        }
    )

# Готов
@router.get("")
async def get_users(
    params: QueryParams,
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["admin"]))
):
    query = apply_query_params(
        query=select(User),
        model=User,
        params=params,
        searchable_columns=SEARCHABLE_COLUMNS
    )

    results = await db.execute(query)
    results = results.scalars().all()

    items = models_to_dict(models=results, exclude=PRIVATE_USER_FIELDS)

    return CursedResponser(
        code = codes.SUCCESS,
        data = {
            "users": items
        }
    )

# Готов
@router.post("")
async def create_user(
    data: CreateUser,
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["admin"]))
):
    data = data.model_dump(exclude_unset=True)

    data.pop("id", None)
    data.pop("updated_at", None)
    data.pop("added_at", None)
    if data.get("password"):
        data["password"] = hash_password(data["password"])
    data["updated_at"] = now()
    data["added_at"] = now()

    # Проверка существовании почты. Почта в реквесте обязательна
    exists = (await db.execute(
        select(User).where(User.email == data["email"])
    )).scalar_one_or_none()
    if exists:
        return CursedResponser(
            code=codes.OBJECT_FIELD_EXISTS,
            error=f"Email {data["email"]} already exists",
            data={}
        )

    if data.get("avatar"):
        exists = (await db.execute(
            select(File).where(File.id == data["avatar"])
        )).scalar_one_or_none()
        if not exists:
            return CursedResponser(
                code=codes.AVATAR_NOT_FOUND,
                error=f"File {data["avatar"]} not found.",
                data={}
            )

        if exists.format != FileFormat.IMAGE:
            return CursedResponser(
                code=codes.FILE_BAD_FORMAT,
                error=f"The file format {exists.format} is not suitable.",
                data={}
            )

    new_user = User(**data)
    db.add(new_user)
    try:
        # flush для того, чтобы IntegrityError (дубль email при гонке) поймать здесь,
        # а не на commit в get_db
        await db.flush()
    except IntegrityError:
        await db.rollback()
        return CursedResponser(
            code=codes.OBJECT_FIELD_EXISTS,
            error=f"Email {data["email"]} already exists",
            data={}
        )

    return CursedResponser(
        code=codes.CREATED,
        data={"user": model_to_dict(model=new_user, exclude=PRIVATE_USER_FIELDS)}
    )

# Готов
@router.patch("/{user_id}")
async def edit_user(
    user_id: int,
    data: EditUser,
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["guest", "user", "support", "admin"]))
):
    data = data.model_dump(exclude_unset=True)

    # Забираем old_password сразу: это не колонка User, в setattr попадать не должна
    old_password = data.pop("old_password", None)

    check_resource_access(
        requesting_user=auth["user"],
        resource_owner_id=user_id,
        operation=ResourceOperation.EDIT
    )

    if auth["user"].role != UserRole.ADMIN:
        check_fields(
            body=data,
            allowed_fields=ALLOWED_FIELDS
        )

    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()

    if not user:
        raise CursedException(code=codes.NOT_FOUND, error=f"Resource {user_id} not found")

    data.pop("id", None)
    data.pop("updated_at", None)
    data.pop("added_at", None)
    if data.get("password"):
        # Не-админ обязан подтвердить текущий пароль, чтобы сменить его
        if auth["user"].role != UserRole.ADMIN:
            if not old_password or not verify_password(
                password=old_password,
                hashed_password=user.password
            ):
                return CursedResponser(
                    code=codes.FIELDS_INCORRECT_AUTHORIZATION_ERROR,
                    error="old_password is required and must be correct to change password.",
                    data={}
                )
        data["password"] = hash_password(data["password"])
    data["updated_at"] = now()

    if data.get("email"):
        # Проверка на админа. Только админ может изменять email
        if auth["user"].role != UserRole.ADMIN:
            return CursedResponser(
                code=codes.FIELD_NOT_EDITABLE,
                error="This field 'email' not editable.",
                data={}
            )
        
        exists = (await db.execute(
            select(User).where(User.email == data["email"])
        )).scalar_one_or_none()
        # Сравниваем с редактируемым юзером (user_id), а не с запрашивающим:
        # админ мог бы иначе записать свой email другому пользователю
        if exists and exists.id != user_id:
            return CursedResponser(
                code=codes.OBJECT_FIELD_EXISTS,
                error=f"Email {data["email"]} already exists",
                data={}
            )

    if data.get("avatar"):
        exists = (await db.execute(
            select(File).where(File.id == data["avatar"])
        )).scalar_one_or_none()
        if not exists:
            return CursedResponser(
                code=codes.AVATAR_NOT_FOUND,
                error=f"Avatar {data["avatar"]} not found.",
                data={}
            )
        
        if exists.format != FileFormat.IMAGE:
            return CursedResponser(
                code=codes.FILE_BAD_FORMAT,
                error=f"The file format {exists.format} is not suitable.",
                data={}
        )

    for field, value in data.items():
        setattr(user, field, value)

    try:
        await db.flush()
    except IntegrityError:
        await db.rollback()
        return CursedResponser(
            code=codes.OBJECT_FIELD_EXISTS,
            error=f"Email {data.get("email")} already exists",
            data={}
        )

    return CursedResponser(
        code=codes.EDITED,
        data={
            "user": model_to_dict(model=user, exclude=PRIVATE_USER_FIELDS)
        }
    )

# НА РЕВЬЮ НАДО
@router.delete("/{user_id}")
async def delete_user(
    request: Request,
    user_id: int,
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["admin"]))
):
    # Валидация ДО стрима: после старта StreamingResponse менять HTTP-статус уже нельзя
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()

    if not user:
        raise CursedException(code=codes.NOT_FOUND, error=f"Resource {user_id} not found")

    async def delete_events():
        total = 0

        sessions = (await db.execute(select(Session).where(Session.user_id == user_id))).scalars().all()

        for session in sessions:
            await db.delete(session)
            yield CursedJSON(
                code=codes.DELETED,
                data={"deleted": "session", "id": session.id}
            )
        yield CursedJSON(
            code=codes.DELETED,
            data={"deleted": "sessions", "total": len(sessions)}
        )

        total += len(sessions)

        deleted_tickets = 0
        deleted_messages = 0

        query = select(Ticket).where(
            (Ticket.user_id == user_id) | (Ticket.support_id == user_id)
        )

        tickets = (await db.execute(query)).scalars().all()

        for ticket in tickets:
            messages = (await db.execute(
                select(Message).where(Message.ticket_id == ticket.id)
            )).scalars().all()
            for message in messages:
                message_files = (
                    await db.execute(
                        select(Message_Files).where(Message_Files.message_id == message.id))
                ).scalars().all()

                # Сервисная таблица. Уведомлять не надо
                for message_file in message_files:
                    await db.delete(message_file)

                await db.delete(message)
                yield CursedJSON(code=codes.DELETED,
                    data={"deleted": "message", "id": message.id}
                )

                deleted_messages += 1
            yield CursedJSON(
                code=codes.DELETED,
                data={"deleted": "messages", "total": len(messages)}
            )

            await db.delete(ticket)
            yield CursedJSON(
                code=codes.DELETED,
                data={"deleted": "ticket", "id": ticket.id}
            )
            deleted_tickets += 1
        yield CursedJSON(code=codes.DELETED,
            data={"deleted": "tickets", "total": len(tickets)}
        )

        files = (await db.execute(
            select(File).where(File.user_id == user_id))
        ).scalars().all()

        for file in files:
            if settings.s3_enabled == YesNo.YES:
                try:
                    delete_file(file.external_id)
                    yield CursedJSON(
                        code=codes.DELETED,
                        data={"deleted": "s3file", "id": file.external_id},
                    )

                except NoCredentialsError:
                    yield CursedJSON(
                        code=codes.S3_ERROR,
                        data={},
                        error="AWS credentials not found"
                    )

                except ParamValidationError as e:
                    yield CursedJSON(
                        code=codes.S3_ERROR,
                        data={},
                        error=f"Invalid S3 parameters: {e}"
                    )

                except EndpointConnectionError:
                    yield CursedJSON(
                        code=codes.S3_ERROR,
                        data={},
                        error="Could not connect to S3 endpoint"
                    )

                except ReadTimeoutError:
                    yield CursedJSON(
                        code=codes.S3_ERROR,
                        data={},
                        error="S3 request timed out"
                    )

                except ConnectionError:
                    yield CursedJSON(
                        code=codes.S3_ERROR,
                        data={},
                        error="Connection to S3 failed"
                    )

                except ClientError as e:
                    error = e.response.get("Error", {})
                    yield CursedJSON(
                        code=codes.S3_ERROR,
                        data={},
                        error={"error": error.get("Code", "S3Error"),"message": error.get("Message", str(e))}
                    )

                except BotoCoreError as e:
                    yield CursedJSON(
                        code=codes.S3_ERROR,
                        data={},
                        error=str(e)
                    )

            else:
                yield CursedJSON(
                    code=codes.S3_DISABLED,
                    data={}, error=f"Could not delete {file.external_id}"
                )
            await db.delete(file)
            yield CursedJSON(
                code=codes.DELETED,
                data={"deleted": "file", "id": file.id}
            )
        total += len(files)
        yield CursedJSON(
            code=codes.DELETED,
            data={"deleted": "files", "total": len(files)}
        )

        # 4. Подписки и история платежей
        subscriptions = (await db.execute(
            select(Subscription).where(Subscription.user_id == user_id))
        ).scalars().all()

        for subscription in subscriptions:
            datacenter_id = str(subscription.datacenter_id)
            datacenter_clients = request.app.state.datacenter_clients.get(datacenter_id)

            if datacenter_clients is None:
                yield CursedJSON(
                    code=codes.DATACENTER_NOT_FOUND,
                    data={},
                    error=f"Datacenter {datacenter_id} not found.",
                )

            remnawave_client = datacenter_clients.get("remnawave_client")
            if remnawave_client is None:
                yield CursedJSON(
                    code=codes.INTERNAL_SERVER_ERROR,   # добавьте в codes
                    data={},
                    error=f"Remnawave client for datacenter {datacenter_id} is not configured.",
                )

            if subscription.method_one == MethodOne.none:
                yield CursedJSON(
                    code=codes.DELETED,
                    data={"deleted": "remnawave", "id": None}
                )
            
            else:
                try:
                    await remnawave_client.users.delete_user(subscription.remnawave_id)          # -> None (204)
                    yield CursedJSON(
                        code=codes.DELETD,
                        data={"deleted": "remnawave", "id": subscription.remnawave_id}
                    )

                except NotFoundError:
                    # в панели юзера уже нет: для удаления это успех (идемпотентность)
                    pass

                except (UnauthorizedError, ForbiddenError) as e:
                    # плохой токен или нет прав, это конфиг ДЦ, а не вина клиента
                    yield CursedJSON(
                        code=codes.REMNAWAVE_ERROR,
                        data={},
                        error=f"Remnawave auth failed: {str(e.code)} {str(e.message)}",
                    )

                except RateLimitError as e:                  # обязательно ДО BadRequestError
                    yield CursedJSON(
                        code=codes.REMNAWAVE_ERROR,
                        data={}, error=f"Remnawave API has been rate limited. Error: {str(e.message)}"
                    )

                except BadRequestError as e:
                    yield CursedJSON(
                        code=codes.REMNAWAVE_ERROR,
                        data={},
                        error=f"Remnawave Bad Request {str(e.code)}: {str(e.message)}, ERRORS: {str(e.error.errors)}",
                    )

                except ServerError as e:
                    yield CursedJSON(
                        code=codes.REMNAWAVE_ERROR,
                        data={},
                        error=f"Remnawave unavailable: {e.message}"
                    )

                except ApiError as e:                        # всё остальное из SDK
                    yield CursedJSON(
                        code=codes.REMNAWAVE_ERROR,
                        data={},
                        error=f"{e.code}: {e.message} (HTTP {e.status_code})",
                    )

                except httpx.HTTPError as e:                 # таймаут, обрыв, DNS
                    yield CursedJSON(
                        code=codes.REMNAWAVE_ERROR,
                        data={},
                        error=f"Remnawave unreachable: {e!r}",
                    )

            wgdashboard_client = datacenter_clients.get("wgdashboard_client")
            if wgdashboard_client is None:
                yield CursedJSON(
                    code=codes.INTERNAL_SERVER_ERROR,
                    data={},
                    error=f"WGDasboard client for datacenter {datacenter_id} is not configured.",
                )

            if subscription.method_two == MethodTwo.none:
                yield CursedJSON(
                    code=codes.DELETED,
                    data={"deleted": "wgdashboard", "id": None}
                )

            else:
                if subscription.method_two == MethodTwo.amnezia:
                    subscription_if = datacenter_clients["amnezia_interface"]
                elif subscription.method_two == MethodTwo.wireguard:
                    subscription_if = datacenter_clients["wireguard_interface"]

                try:
                    if await wgdashboard_client.require_authentication() == False:
                        yield CursedJSON(
                            code=codes.WGDASHBOARD_ERROR,
                            data={},
                            error="WGDashboard server is not reacheable."
                        )
                    async with wgdashboard_client as client:
                        await client.peers.delete(
                            configuration=subscription_if,
                            peers=subscription.wgdashboard_public_key
                        )
                    yield CursedJSON(
                        code=codes.DELETED,
                        data={"deleted": "wgdashboard", "id": subscription.wgdashboard_public_key}
                    )

                except WGDashboardNotFoundError as error:
                    yield CursedJSON(
                        code=codes.WGDASHBOARD_ERROR,
                        data={},
                        error=f"WGDashboard peer or configuration not found: {str(error)}",
                    )
                except WGDashboardAuthError as error:
                    yield CursedJSON(
                        code=codes.WGDASHBOARD_ERROR,
                        data={},
                        error=f"WGDashboard authentication failed: {str(error)}",
                    )
                except WGDashboardConnectionError as error:
                    yield CursedJSON(
                        code=codes.WGDASHBOARD_ERROR,
                        data={},
                        error=f"Could not connect to WGDashboard: {str(error)}",
                    )
                except WGDashboardResponseError as error:
                    yield CursedJSON(
                        code=codes.WGDASHBOARD_ERROR,
                        data={},
                        error=f"Invalid response from WGDashboard: {str(error)}",
                    )
                except WGDashboardAPIError as error:
                    yield CursedJSON(
                        code=codes.WGDASHBOARD_ERROR,
                        data={},
                        error=f"WGDashboard API error: {str(error)}",
                    )
                except WGDashboardError as error:
                    yield CursedJSON(
                        code=codes.WGDASHBOARD_ERROR,
                        data={},
                        error=f"WGDashboard error: {str(error)}",
                    )

            await db.delete(subscription)
            yield CursedJSON(
                code=codes.DELETED,
                data={"deleted": "subscription", "id": subscription.id}
            )
        total += len(subscriptions)
        yield CursedJSON(
            code=codes.DELETED,
            data={"deleted": "subscriptions", "total": len(subscriptions)}
        )

        payments = (await db.execute(
            select(PayHistory).where(PayHistory.user_id == user_id))
        ).scalars().all()

        for payment in payments:
            await db.delete(payment)
            yield CursedJSON(
                code=codes.DELETED, 
                data={"deleted": "pay_history", "id": payment.id}
            )
        total += len(payments)
        yield CursedJSON(
            code=codes.DELETED,
            data={"deleted": "pay_history", "total": len(payments)}
        )

        user_codes = (await db.execute(
            select(Code).where(Code.user_id == user_id))
        ).scalars().all()

        for code in user_codes:
            await db.delete(code)
            yield CursedJSON(
                code=codes.DELETED,
                data={"deleted": "code", "id": code.id}
            )
        total += len(user_codes)
        yield CursedJSON(
            code=codes.DELETED,
            data={"deleted": "codes", "total": len(user_codes)}
        )

        user_packets = (await db.execute(
            select(Packet).where(Packet.user_id == user_id))
        ).scalar().all()
        for user_packet in user_packets:
            await db.delete(user_packet)
            yield CursedJSON(
                code=codes.DELETED,
                data={"deleted": "packet", "id": user_packet.id}
            )
        total += len(user_codes)
        yield CursedJSON(
            code=codes.DELETED,
            data={"deleted": "packets", "total": len(user_codes)}
        )

        # 5. Сам юзер
        await db.delete(user)
        total += 1
        yield CursedJSON(
            code=codes.DELETED,
            data={"deleted": "all", "total": total}
        )

    return CursedStreamingResponser(delete_events())
