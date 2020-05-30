import discord
from PIL import Image
import asyncio
import requests
import shutil
from DataManager import DataManager
from Librarian import Librarian
import time
from ImagePacker import ImagePacker
from DogModel import DogModel
from SquirrelModel import SquirrelModel

lib = Librarian()
m = DataManager()

imgSize = 64
client = discord.Client()
dogFinder = SquirrelModel(imgSize)
packer = ImagePacker(imgSize)

async def saveImage(attachment):
    resp = requests.get(attachment.url, stream=True)
    local_file = open(f"./collectedImages/{attachment.filename}", 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)
    del resp
    return

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message_delete(message):
    print(f"{message.author} deleted: {message.content}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$'):
        s = message.content[1:len(message.content)].lower()
        if s in lib.folders:
            id = m.getRandomIdFromClass(s)
            name = m.getFileNameFromId(id)
            await message.channel.send(file=discord.File(f"./raw-img/{s}/{name}"))
    react = False
    hasDog = False
    for e in message.attachments:
        if ".png" in e.filename or ".jpg" in e.filename:
            await saveImage(e)
            print(f"Saved file: {e.filename}")
            if dogFinder.isDog(e.filename):
                hasDog = True
            react = True
    emoji = '\N{EYE}'
    # or '\U0001f44d' or '👍'
    if react:
        await message.add_reaction(emoji)
        time.sleep(3)
        await message.remove_reaction(emoji, client.user)
    if hasDog:
        await message.add_reaction('\N{CHIPMUNK}')
        

client.run("PUT YOUR TOKEN HERE")