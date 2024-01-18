from interactions import Client, Extension
from utils.embeds import new_embed
class Logger():
    def __init__(self, client, channel = 0):
        self.client: Client = client
        self.channel = channel

        self.LOGS_LEVEL = {"ERROR": 0xFF0000, "INFO": 0x0091FF, "EDIT": 0xFFBF00}

    
    async def sendLog(self, logtype, embed):
        try:
            color = self.LOGS_LEVEL[logtype]
        except:
            color = "FFBF00"
        channel = await self.client.fetch_channel(self.channel)
        if channel:
            await channel.send(embeds=[new_embed(title=logtype, description=embed, color=color)])

        

def setup(client):
    Logger(client, channel)