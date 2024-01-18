import asyncio
import os
from random import randint
from dotenv import load_dotenv
load_dotenv()
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

EMAIL = os.environ.get('MEROSS_EMAIL')
PASSWORD = os.environ.get('MEROSS_PASSWORD')

http_api_client = None
manager = None
async def define():
    global http_api_client
    global manager
    http_api_client = await MerossHttpClient.async_from_user_password(api_base_url='https://iotx-eu.meross.com', email=EMAIL, password=PASSWORD)
    manager = MerossManager(http_client=http_api_client)
    return http_api_client, manager

async def getInformationsOfLight(lightuuid):
    lightdata = {}
    await define()
    global http_api_client
    global manager
    light = await manager.async_device_discovery(meross_device_uuid=lightuuid)
    if len(light) <1:
        return False
    device = light[0]
    await device.async_update()
    print(device)
    lightdata['status'] = device.get_light_is_on()
    lightdata['currentColor'] = device.get_rgb_color()
    lightdata['device'] = device
    print(lightdata)
    return lightdata

async def setLightStatus(lightuuid, status):
    await define()
    light = await manager.async_device_discovery(meross_device_uuid=lightuuid)
    print(len(light))
    print(light)
    if len(light) < 1 and light[0] != None:
        print('No light')
        return False
    print(light[0])
    device = light[0]
    await device.async_update()
    if status == True:
        await device.async_turn_on(channel=0)
    else:
        await device.async_turn_off(channel=0)
    return

async def setLightColor(lightuuid, colorRGB):
    await define()
    light = await manager.async_device_discovery(meross_device_uuid=lightuuid)
    print(len(light))
    if len(light) < 1:
        print('No light')
        return False
    device = light[0]
    await device.async_update()
    
    await device.async_set_light_color(rgb = colorRGB)
    return