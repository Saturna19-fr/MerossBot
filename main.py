import pkgutil
import asyncio
from logging import Logger
import os
from random import randint
from dotenv import load_dotenv
load_dotenv()
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from interactions import Client, Intents, logger_name

from fastapi import FastAPI
from interactions_restful.backends.fastapi import FastAPIHandler


app = FastAPI()

logger_name = "ipy"
print(__name__)
EMAIL = os.environ.get('MEROSS_EMAIL')
PASSWORD = os.environ.get('MEROSS_PASSWORD')

extension_names = [m.name for m in pkgutil.iter_modules(["exts"], prefix="exts.")]
client = Client(
    token = os.environ.get("DISCORD_TOKEN"),
    intents=Intents.ALL, logger=Logger(logger_name))
    
FastAPIHandler(client, app)
# client.load_extension("utils.loggerservice.py", channel=1196038073897734164)
print("Lancement du bot..")    

async def aa():
    print(extension_names)
    for extension in extension_names:
        client.load_extension(extension)
    await client.astart()

asyncio.create_task(aa())