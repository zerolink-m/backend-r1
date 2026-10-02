import asyncio
from app.tasks import sync_traffic, expire_subscriptions

_tasks: list[asyncio.Task] = []

def start_all():
    _tasks.append(asyncio.create_task(sync_traffic.run(60)))
    _tasks.append(asyncio.create_task(expire_subscriptions.run(300)))

async def stop_all():
    for t in _tasks:
        t.cancel()
    await asyncio.gather(*_tasks, return_exceptions=True)