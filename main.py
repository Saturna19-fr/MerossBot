from interactions_restful.backends.fastapi import FastAPIHandler
from fastapi import FastAPI
from interactions import Client, Intents, logger_name
from meross_iot.manager import MerossManager
from meross_iot.http_api import MerossHttpClient
import pkgutil
import asyncio
from logging import Logger
import os
from random import randint
from dotenv import load_dotenv
import httpx
load_dotenv()

app = FastAPI()

logger_name = "ipy"
print(__name__)
EMAIL = os.environ.get('MEROSS_EMAIL')
PASSWORD = os.environ.get('MEROSS_PASSWORD')

extension_names = [m.name for m in pkgutil.iter_modules(
    ["exts"], prefix="exts.")]
client = Client(
    token=os.environ.get("DISCORD_TOKEN"),
    intents=Intents.ALL, logger=Logger(logger_name))

FastAPIHandler(client, app)
# client.load_extension("utils.loggerservice.py", channel=1196038073897734164)
print("Lancement du bot..")


async def aa():
    print(extension_names)
    for extension in extension_names:
        client.load_extension(extension)
    async with httpx.AsyncClient() as cli:
        try:
            data = await cli.get("https://api.ipify.org")
            print(data.content.decode("utf-8"))
            ip = data.content.decode("utf-8")
        except Exception as e:
            print("Une erreur est survenue.", e)
        else:
            try:
                await cli.get(f"https://www.ovh.com/nic/update?system=dyndns&hostname=botmerosska.saturna19.fr&myip={ip}", auth=(os.environ.get("OVH_LOGIN"), os.environ.get("OVH_PWD")))
            except Exception as e:
                print("Une erreur est survenue.", e)
            finally:
                await cli.aclose()
    await client.astart()

asyncio.create_task(aa())
