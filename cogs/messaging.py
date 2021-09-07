import discord
import json
from discord.ext import commands


class Message(commands.Cog, description='Commands for messaging.'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('messaging.py loaded')

    @commands.command()
    async def dm(self, ctx, user: discord.User, *, message):
        if ctx.author.id == 296824773475041282:
            await user.send(message)

    @commands.Cog.listener()
    async def on_message(self, message):
        user_id = 296824773475041282
        user = self.client.get_user(user_id)
        with open('messages.json', 'r') as f:
            messages = json.load(f)
        if message.author.id == 296824773475041282 and message.guild is None:
            for key, value in messages.items():
                if value == 1:
                    channel_id = key
                    channel = self.client.get_channel(int(channel_id))
                    if 'py!' in message.content:
                        return
                    else:
                        if message.content != "":
                            await channel.send(message.content)
                        if message.attachments:
                            await channel.send(message.attachments[0].url)
        if message.guild is None and message.author != self.client.user and message.author.id != 296824773475041282:
            await user.send(f'{message.author}: {message.content}')
            if message.attachments:
                await user.send(message.attachments[0].url)
        if str(message.channel.id) not in messages or messages[str(message.channel.id)] == 0:
            return
        elif messages[str(message.channel.id)] == 1:
            if message.author != self.client.user:
                await user.send(f'{message.author} in #{message.channel.name}: {message.content} ')

    @commands.command()
    async def listen(self, ctx, channel_id):
        if ctx.author.id == 296824773475041282:
            with open('messages.json', 'r') as f:
                messages = json.load(f)
            messages[str(channel_id)] = 1
            with open('messages.json', 'w') as f:
                json.dump(messages, f, indent=4)
            await ctx.send(f'listening to channel: {channel_id}')

    @commands.command()
    async def unlisten(self, ctx):
        if ctx.author.id == 296824773475041282:
            with open('messages.json', 'r') as f:
                messages = json.load(f)
            for key, value in messages.items():
                if value == 1:
                    channel_id = key
                    messages[str(channel_id)] = 0
                    with open('messages.json', 'w') as f:
                        json.dump(messages, f, indent=4)
                    await ctx.send(f'stopped listening to channel: {channel_id}')


def setup(client):
    client.add_cog(Message(client))
