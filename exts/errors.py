from interactions import Extension, Client, listen, SlashCommand
from utils.light import setLightStatus, getInformationsOfLight, setLightColor
from utils.embeds import create_success_embed, new_embed, create_error_embed
from colorama import Fore
import traceback
from interactions.api.events import CommandError
from asyncio import sleep

class ErrorHandler(Extension):
    def __init__(self, client):
        self.client: Client = client
        
  

    @listen(CommandError, disable_default_listeners=True)  # tell the dispatcher that this replaces the default listener
    async def on_command_error(self, event: CommandError):
        print(Fore.RED, event.error, Fore.RESET)

        print(Fore.GREEN, event.error.args, Fore.RESET)
        traceback.print_exception(event.error)
        if not event.ctx.responded:
            await event.ctx.send("Something went wrong.")
            
            

def setup(client):
    ErrorHandler(client)