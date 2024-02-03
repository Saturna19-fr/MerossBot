import pkgutil
import asyncio
import os
from random import randint
from dotenv import load_dotenv
load_dotenv()
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from interactions import Client, Intents

EMAIL = os.environ.get('MEROSS_EMAIL')
PASSWORD = os.environ.get('MEROSS_PASSWORD')

color = []
def main2():
    extension_names = [m.name for m in pkgutil.iter_modules(["exts"], prefix="exts.")]
    client = Client(
        token = os.environ.get("DISCORD_TOKEN"),
        intents=Intents.ALL)
    
    for extension in extension_names:
        client.load_extension(extension)
    # client.load_extension("utils.loggerservice.py", channel=1196038073897734164)
    print("Lancement du bot..")    
    client.start()

main2()