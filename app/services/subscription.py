from app.services import WGDashboardClient
from sqlalchemy.ext.asyncio import AsyncSession
from remnawave import RemnawaveSDK
from app.models import Subscription
from sqlalchemy import select


class SubscriptionNotFound(Exception):
    pass
