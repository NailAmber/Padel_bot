import random
from utils.core import logger
from pyrogram import Client
from pyrogram.raw.functions.messages import RequestAppWebView, RequestWebView
from pyrogram.raw.types import InputBotAppShortName, InputPeerChat
from pyrogram.raw.types import InputBotAppShortName
import asyncio
from urllib.parse import unquote, quote
from data import config
import aiohttp
from fake_useragent import UserAgent
from aiohttp_socks import ProxyConnector

class CatsGang:
    def __init__(self, thread: int, session_name: str, phone_number: str, proxy: [str, None]):
        self.account = session_name + '.session'
        self.thread = thread
        self.ref = random.choice(config.REFS)
        self.proxy = f"{config.PROXY['TYPE']['REQUESTS']}://{proxy}" if proxy is not None else None
        connector = ProxyConnector.from_url(self.proxy) if proxy else aiohttp.TCPConnector(verify_ssl=False)
        self.phone_number = phone_number

        if proxy:
            proxy = {
                "scheme": config.PROXY['TYPE']['TG'],
                "hostname": proxy.split(":")[1].split("@")[1],
                "port": int(proxy.split(":")[2]),
                "username": proxy.split(":")[0],
                "password": proxy.split(":")[1].split("@")[0]
            }

        self.client = Client(
            name=session_name,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            workdir=config.WORKDIR,
            proxy=proxy,
            lang_code='ru'
        )

        headers = {
            'User-Agent': UserAgent(os='android', browsers='chrome').random
        }
        self.session = aiohttp.ClientSession(headers=headers, trust_env=True, connector=connector)
        # print('proxy is =', proxy)
        # context = ssl.create_default_context()
        # context.load_verify_locations(certifi.where()) 
        # self.session = httpx.AsyncClient(verify=context,headers=headers, proxy=self.proxy)  
        

    async def stats(self):
        await asyncio.sleep(random.uniform(*config.DELAYS['ACCOUNT']))
        self.ref = random.choice(config.REFS)
        query = await self.get_tg_web_data()
        
        # query = query.replace('sender', 'private')
        # query = query.replace('5152930056796874085','-5338747828399073772')
        if query is None:
            logger.error(f"Thread {self.thread} | {self.account} | Session {self.account} invalid")
            await self.logout()
            return None, None
        # print('query is =', query)
        # self.session.headers['Authorization'] = 'tma ' + query
        # query = 'user=%7B%22id%22%3A374069367%2C%22first_name%22%3A%22%D0%98%D0%B2%D0%B0%D0%BD%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22Zzjjjuuu%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&chat_instance=5828640237240840140&chat_type=private&start_param=M1o0iuj&auth_date=1725828534&hash=0928f32cc8c9503788de285273326ad8a0aadd7a430ad1ba3a77f414f20b7d88'

        headers = {
            'initData':query,
            'param':self.ref
        }

            # URL запроса
        url = "https://api.giveshare.ru/index"

        # Заголовки запроса
        headers = {
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Sec-Ch-Ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            "Accept": "application/json, text/plain, */*",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Ch-Ua-Mobile": "?0",
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Origin": "https://app.giveshare.ru",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://app.giveshare.ru/",
            "Accept-Language": "en-US,en;q=0.9",
            "Dnt": "1",
            "Sec-Gpc": "1",
            "Accept-Encoding": "gzip, deflate, br",
        }

        proxy = "http://127.0.0.1:8080"
        r = await self.session.get('https://ifconfig.me/ip', proxy=proxy)
        print('r = ', await r.text())
        true_proxy = await r.text()

        r = await self.session.get(f'https://app.giveshare.ru/?tgWebAppStartParam={self.ref}', proxy=proxy)
        # r = await self.session.post(f'https://api.giveshare.ru/member/create', json=json_data, headers=headers, proxy=proxy)
        # r_json = await r.json()
        # print('create = ', r_json)

        json_data = {
            "initData": query,
            "raffle": "500191"
        }
        
        r = await self.session.post(f'https://api.giveshare.ru/member/check', json=json_data, headers=headers, proxy=proxy)
        print('status = ', r)
        r_json = await r.json()
        tickets = [i['ticket'] for i in r_json['tickets']]
        phone_number = self.phone_number
        name = self.client.name

        return [phone_number, name, tickets, true_proxy]

    async def user(self):
        resp = await self.session.get('https://cats-backend-cxblew-prod.up.railway.app/user')
        return await resp.json()

    async def logout(self):
        await self.session.close()

    async def check_task(self, task_id: int):
        try:
            resp = await self.session.post(f'https://cats-backend-cxblew-prod.up.railway.app/tasks/{task_id}/check')
            return (await resp.json()).get('completed')
        except:
            return False

    async def complete_task(self, task_id: int):
        try:
            resp = await self.session.post(f'https://cats-backend-cxblew-prod.up.railway.app/tasks/{task_id}/complete')
            return (await resp.json()).get('success')
        except:
            return False

    async def get_tasks(self):
        resp = await self.session.get('https://cats-backend-cxblew-prod.up.railway.app/tasks/user?group=cats')
        return (await resp.json()).get('tasks')

    async def register(self):
        resp = await self.session.post(f'https://cats-backend-cxblew-prod.up.railway.app/user/create?referral_code={random.choice(config.REFS)}')
        return resp.status == 200

    async def login(self):
        await asyncio.sleep(random.uniform(*config.DELAYS['ACCOUNT']))
        self.ref = random.choice(config.REFS)
        query = await self.get_tg_web_data()
        
        # query = query.replace('sender', 'private')
        # query = query.replace('5152930056796874085','-5338747828399073772')
        if query is None:
            logger.error(f"Thread {self.thread} | {self.account} | Session {self.account} invalid")
            await self.logout()
            return None, None
        # print('query is =', query)
        # self.session.headers['Authorization'] = 'tma ' + query
        # query = 'user=%7B%22id%22%3A374069367%2C%22first_name%22%3A%22%D0%98%D0%B2%D0%B0%D0%BD%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22Zzjjjuuu%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&chat_instance=5828640237240840140&chat_type=private&start_param=M1o0iuj&auth_date=1725828534&hash=0928f32cc8c9503788de285273326ad8a0aadd7a430ad1ba3a77f414f20b7d88'

        headers = {
            'initData':query,
            'param':self.ref
        }

            # URL запроса
        url = "https://api.giveshare.ru/index"

        # Заголовки запроса
        headers = {
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Sec-Ch-Ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            "Accept": "application/json, text/plain, */*",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Ch-Ua-Mobile": "?0",
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Origin": "https://app.giveshare.ru",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://app.giveshare.ru/",
            "Accept-Language": "en-US,en;q=0.9",
            "Dnt": "1",
            "Sec-Gpc": "1",
            "Accept-Encoding": "gzip, deflate, br",
        }

        # Данные запроса (в формате JSON)
        json_data = {
            "initData": query,
            "param": self.ref,
            "token": ""
        }

        # json_param = json.dumps(headers)
        proxy = "http://127.0.0.1:8080"
        r = await self.session.get(f'https://app.giveshare.ru/?tgWebAppStartParam={self.ref}', proxy=proxy)
        r = await self.session.post(f'https://api.giveshare.ru/member/create', json=json_data, headers=headers, proxy=proxy)
        r_json = await r.json()
        print('create = ', r_json)

        json_data = {
            "initData": query,
            "raffle": "500191"
        }

        r = await self.session.post(f'https://api.giveshare.ru/member/check', json=json_data, headers=headers, proxy=proxy)
        r_json = await r.json()
        print('check = ', [i['ticket'] for i in r_json['tickets']])
        

    async def get_tg_web_data(self):
        try:
            await self.client.connect()
            web_view = await self.client.invoke(RequestAppWebView(
                peer=await self.client.resolve_peer('giveawaybot'),
                app=InputBotAppShortName(bot_id=await self.client.resolve_peer('giveawaybot'), short_name="app"),
                platform='android',
                write_allowed=True,
                start_param=self.ref
            ))
            await self.client.disconnect()

            auth_url = web_view.url
            query = unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
            return query

        except Exception as e:
            print('e = ', e)
            return None
