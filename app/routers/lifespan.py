from app.services import create_datacenters_clients
from contextlib import asynccontextmanager
from app.models import Datacenter
from sqlalchemy import select
from app import manual_get_db
from config import settings, Level
from fastapi import FastAPI
import random


MAGENTA = "\033[95m"
RED = "\033[91m"
YELLOW = "\033[93m"
ORANGE = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

ZL_LINES = [
    f"{ORANGE}{BOLD}╔══════════════════════════════════════════════════════════════════════╗{RESET}",
    f"{ORANGE}{BOLD}║{RESET}      {CYAN}  Z E R O L I N K   A P I  {RESET}                                     {ORANGE}{BOLD}║{RESET}",
    f"{ORANGE}{BOLD}╚══════════════════════════════════════════════════════════════════════╝{RESET}",
    f"{YELLOW}>> version: {settings.version}{RESET}",
    f"{YELLOW}>> FastAPI here!...{RESET}",
]

GOODBYE_ZL_LINES = [
    f"{ORANGE}{BOLD}╔══════════════════════════════════════════════════════════════════════╗{RESET}",
    f"{ORANGE}{BOLD}║{RESET}      {CYAN}  Z E R O L I N K   A P I  {RESET}                                     {ORANGE}{BOLD}║{RESET}",
    f"{ORANGE}{BOLD}╚══════════════════════════════════════════════════════════════════════╝{RESET}",
    f"{YELLOW}>> Goodbye! {RESET}"
]

CURSED_PHRASES = [
    "In cursedapi the power!",
    "In CursedAPI we trust!",
    "CursedAPI has entered the chat!",
    "Feel the CursedAPI!",
    "Powered by CursedAPI!",
    "CursedAPI never sleeps!",
    "Trust the API. Embrace the curse.",
    "Where HTTP meets the curse!",
    "One API. Infinite curses.",
    "Code in. Curse out.",
    "Request the curse. Receive the response.",
    "Keep calm and call CursedAPI.",
    "Born to serve requests!",
    "Your backend, but cursed.",
    "Making APIs a little more cursed!",
    "Cursed by design. Built for requests."
]

GOODBYE_CURSED_PHRASES = [
    "See you in the next request!",
    "Until the next response!",
    "Stay cursed, stay coding!",
    "The curse never ends. See you soon!",
    "Request completed. Goodbye!",
    "Connection closed. Stay cursed!",
    "See you on the backend!",
    "May your responses be fast!",
    "Until we meet in another request!",
    "Keep coding. Keep it cursed!",
    "The API says goodbye!",
    "No more requests. For now.",
    "Goodbye, and don't forget the API!",
    "Session terminated. Curse preserved.",
    "Until the next HTTP request!",
]

CURSED_BANNERS = [
    r"  ____   _   _   ____     ____    _____    ____           _       ____    _ ",
    r" / ___| | | | | |  _ \   / ___|  | ____|  |  _ \         / \     |  _ \  | |",
    r"| |     | | | | | |_) |  | (_    | |      | | |         / _ \    | |_) | | |",
    r"| |     | | | | |  __/   \___ \  | |___|  | | | |      / ___ \   |  __/  | |",
    r"| |___  | |_| | |_|  \\   __) |  | |___   | |_|       / /   \ \  | |     | |",
    r" \___|   \___/  |_|   \\ (____/  |_____|  |____/     /_/     \_\ |_|     |_|",
]

def hello_cursed_print(CURSED_BANNERS: list = CURSED_BANNERS, CURSED_PHRASES: list = CURSED_PHRASES):
    for cursed_banner in CURSED_BANNERS:
        print(f"{BOLD}{cursed_banner}{RESET}")

    print("")
    print(f"{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"                    {BOLD}{RED}{random.choice(CURSED_PHRASES)}{RESET}                    ")
    print(f"{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print("")    
    return

def hello_zl_print(ZL_LINES: list = ZL_LINES):
    for zl_line in ZL_LINES:
        print(zl_line)
    return

def goodbye_cursed_print(GOODBYE_CURSED_BANNERS: list = CURSED_BANNERS, GOODBYE_CURSED_PHRASES: list = GOODBYE_CURSED_PHRASES):
    for cursed_banner in GOODBYE_CURSED_BANNERS:
        print(f"{BOLD}{cursed_banner}{RESET}")
    print("")
    print(f"{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"                    {BOLD}{YELLOW}{random.choice(GOODBYE_CURSED_PHRASES)}{RESET}                    ")
    print(f"{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print("")
    return

def goodbye_zl_print(GOODBYE_ZL_LINES: list):
    for goodbye_zl_line in GOODBYE_ZL_LINES:
        print(goodbye_zl_line)
    return
    

@asynccontextmanager
async def lifespan(app: FastAPI):
    # PRINT Cursed and ZeroLink hello.
    hello_cursed_print()
    hello_zl_print()

    app.state.datacenter_clients = {}
    if settings.level != Level.TEST:
        async with manual_get_db() as session:
            datacenters = await session.execute(
                select(Datacenter)
            )
            datacenters = datacenters.scalars().all()
            app.state.datacenter_clients = create_datacenters_clients(datacenters=datacenters)

    # Запуск
    yield

    # PRINT Goodbye cursed and ZeroLink
    goodbye_cursed_print()
    goodbye_zl_print()