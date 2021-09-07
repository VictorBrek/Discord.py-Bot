import discord
import os
from discord.ext import commands


class Minecraft(commands.Cog, description='Manage the Minecraft server.'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('minecraft.py loaded')

    @commands.command(help='Start the Minecraft server.')
    async def startserver(self, ctx):
        os.system('bash /home/victorbrek/start.sh')
        await ctx.send(f'Server started by {ctx.author.mention}')

    @commands.command(help='Stop the Minecraft server.')
    async def stopserver(self, ctx):
        os.system('bash /home/victorbrek/stop.sh')
        await ctx.send(f'Server stopped by {ctx.author.mention}')


def setup(client):
    client.add_cog(Minecraft(client))
