import discord
import asyncio
import sys
from discord.ext import commands
import docker
import os
import time
import threading


class MyClient(discord.Client):
    async def on_ready(self):
        print('Connected!')
        print('Username: {0.name}\nID: {0.id}'.format(self.user))
    async def on_message(self, message):
        docclient = docker.from_env()

        if message.content.startswith('!code'):
            ## Sends a message back with the code without the trigger word
            msg = await message.channel.send(message.content[6:])
            authorfile = str(message.id) + ".py"
            container_name = str(message.id)
            ## writes the code to a file
            f= open("/home/ubuntu/pyfiles/" + authorfile,"w+")
            f.write(message.content[6:])
            ## Runs the container
            docclient.containers.run("python:3.10-rc", "timeout 20 python -u /usr/src/pyfiles/" + authorfile,  auto_remove=False, network_disabled=True, detach=True, volumes={'/home/ubuntu/pyfiles': {'bind': '/usr/src/pyfiles', 'mode': 'rw'}}, name=str(message.id))
            ## Prints the container name (for debugging purposes)
            print(container_name)

            ## Completely breaks the docker container for no discernible reason, but this would have sent the logs from the container as a message to the user
            #time.sleep(23)
            #if str(docclient.containers.get(container_name).status) == "exited":
            #    print(docclient.containers.get(container_name).logs()) ## debugging
            #    msg = await message.channel.send(docclient.containers.get(container_name).logs())
            #    if os.path.exists("/usr/src/pyfiles/" + authorfile):
            #        os.remove("/usr/src/pyfiles/" + authorfile)
            #    docclient.containers.get(container_name).remove()
            #elif str(docclient.containers.get(container_name).status) == "running":
            #    print("Error, exceeded runtime")
            #    docclient.containers.get(container_name).remove(force=True)
            #else:
            #    print("Error, try again")

client = MyClient()
client.run(INSERT AUTH CODE)