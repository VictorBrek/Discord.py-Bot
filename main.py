def main():
    import discord
    import os
    import json
    from discord.ext.tasks import loop
    from discord.ext import commands
    from info import TOKEN

    intents = discord.Intents().all()

    def get_prefix(client, message):  # pulls prefix from prefixes.json
        if message.guild is None:
            return 'py!'
        else:
            with open('server-info.json', 'r') as f:
                prefixes = json.load(f)
            return prefixes[f'{str(message.guild.id)}_prefix']

    client = commands.Bot(command_prefix=get_prefix, intents=intents)

    class NewHelpName(commands.MinimalHelpCommand):  # Better help command
        async def send_pages(self):
            destination = self.get_destination()
            for page in self.paginator.pages:
                emby = discord.Embed(description=page)
                await destination.send(embed=emby)

    client.help_command = NewHelpName(no_category='Other')

    @client.event
    async def on_ready():
        activity_loop.start()
        print(f'Logged in as {client.user}')

    @loop(seconds=5)
    async def activity_loop():  # resets the discord status every 5 seconds, in case something modifies it
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game('py!help'))

    @client.event
    async def on_guild_join(guild):
        with open('server-info.json', 'r') as f:
            file = json.load(f)

        file[f'{str(guild.id)}_muterole'] = 'muted'
        file[f'{str(guild.id)}_prefix'] = 'py!'

        with open('server-info.json', 'w') as f:
            json.dump(file, f, indent=4)

    @client.event
    async def on_guild_remove(guild):
        with open('server-info.json', 'r') as f:
            file = json.load(f)

        file.pop(f'{str(guild.id)}_prefix')
        file.pop(f'{str(guild.id)}_muterole')

        with open('server-info.json', 'w') as f:
            json.dump(file, f, indent=4)

    @client.command(help='Change the prefix.')
    @commands.has_permissions(administrator=True)
    async def prefix(ctx, prefix_):
        with open('server-info.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[f'{str(ctx.guild.id)}_prefix'] = prefix_
        with open('server-info.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f'prefix changed to {prefix_}.')

    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Invalid command.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permission to use this command.')
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send('You do not have the role for this command.')

    @client.event
    async def on_member_join(member):
        guild_name = str(member.guild.name)
        print(f'{member} has joined {guild_name}.')

    @client.event
    async def on_member_remove(member):
        guild_name = str(member.guild.name)
        print(f'{member} has left {guild_name}.')

    @client.command(help='Load a cog.')
    @commands.has_permissions(administrator=True)
    async def load(extension):
        client.load_extension(f'cogs.{extension}')

    @client.command(help='Unload a cog.')
    @commands.has_permissions(administrator=True)
    async def unload(extension):
        client.unload_extension(f'cogs.{extension}')

    for filename in os.listdir('./cogs'):  # loads all cogs on runtime
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

    @client.command(help='Reload a cog.')
    @commands.has_permissions(administrator=True)
    async def reload(extension):
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')

    client.run(TOKEN)


if __name__ == '__main__':
    main()
