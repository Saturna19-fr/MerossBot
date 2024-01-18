from interactions import Client, Extension
from utils.embeds import new_notify_embed
class Logger():
    def __init__(self, client, channel = 0):
        self.client: Client = client
        self.channel = channel

        self.LOGS_LEVEL = {"ERROR": "FF0000", "INFO": "0091FF", "CHANGE": "FFBF00"}

    
    async def sendLog(self, type, embed):
        try:
            color = self.LOGS_LEVEL["type"]
        except:
            color = "FFBF00"
        channel = await self.client.fetch_channel(self.channel)
        if channel:
            await channel.send(embeds=[new_notify_embed(embed)])

        

def setup(client):
    Logger(client, channel)