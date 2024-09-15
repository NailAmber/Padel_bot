import random
from utils.padel_bot import CatsGang
from data import config
from utils.core import logger
import datetime
import pandas as pd
from utils.core.telegram import Accounts
import asyncio
import os


async def start(thread: int, session_name: str, phone_number: str, proxy: [str, None]):
    cats = CatsGang(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy)
    account = session_name + '.session'
    await asyncio.sleep(random.uniform(3,20))
    
    try:
        await cats.client.connect()
        await cats.client.join_chat('padel_people')
        await asyncio.sleep(2)
        await cats.client.join_chat('padelclub_ru')
        await cats.client.disconnect()
    except:
        logger.error(f"Padel | Thread {thread} | {account} | Cant subscribe")
    await asyncio.sleep(2)
    logger.success(f"Padel | Thread {thread} | {account} | Subscribed!")
    await cats.login()

    await cats.logout()


async def stats():
    accounts = await Accounts().get_accounts()

    tasks = []
    for thread, account in enumerate(accounts):
        session_name, phone_number, proxy = account.values()
        tasks.append(asyncio.create_task(CatsGang(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy).stats()))

    data = await asyncio.gather(*tasks)
    path = f"statistics/statistics_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    columns = ['Phone number', 'Name', 'tickets', 'Proxy (login:password@ip:port)']

    if not os.path.exists('statistics'): os.mkdir('statistics')
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(path, index=False, encoding='utf-8-sig')

    logger.success(f"Saved statistics to {path}")
