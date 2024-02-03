## API Service for UptimeRobots
import interactions
from interactions_restful import route
from utils.light import getInformationsOfLight

class MyAPI(interactions.Extension):
    def __init__(self, client):
        self.client : interactions.Client = client
        print("e")

    
    @route("GET", "/")
    def index(self):
        print("e")
        return {"status": "I'm Alive !"}
    
    @route("GET", "/lightstatus")
    async def lightstatus(self):
        lightdata = await getInformationsOfLight("2009100001005090829048e1e931c89a")
        return {"isTurnedOn": lightdata['status']}