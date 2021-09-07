import discord
import asyncio
import json
from discord.ext import commands


class Moderation(commands.Cog, description='Commands for moderating the server.'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('moderation.py loaded')

    @commands.command(help='Clear the chat.')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

    @commands.command(help='Kick a user.')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason='No reason'):
        await member.kick(reason=reason)
        await ctx.send(f'kicked {member.mention} for: {reason}')

    @commands.command(help='Ban a user.')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason='No reason'):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention} for: {reason}')

    @commands.command(help='Unban a user.')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.name}#{user.discriminator}')

    @commands.command(usage=f'<member> <time><duration>\ns = seconds\nm = minutes\nh = hours\n'
                            f'd = days\neg. py!mute mention 5m', help='Mute an annoying user.')
    @commands.has_any_role('Victor', 'Moderator')
    async def mute(self, ctx, member: discord.Member, time_d='5m', *, reason='No reason'):
        await ctx.channel.purge(limit=1)
        with open('server-info.json', 'r') as f:
            mutedrole = json.load(f)
        role = discord.utils.get(member.guild.roles, name=mutedrole[f'{str(ctx.guild.id)}_muterole'])
        time = int(time_d[:-1])
        d = time_d[-1]

        if role not in member.roles:
            await member.add_roles(role)

        if d == "s":
            _d = 'second(s)'
            await ctx.send(f'{member.mention} muted for {time} {_d}')
            await ctx.send(f'Reason: {reason}')
            await asyncio.sleep(time)

        if d == "m":
            _d = 'minute(s)'
            await ctx.send(f'{member.mention} muted for {time} {_d}')
            await ctx.send(f'Reason: {reason}')
            await asyncio.sleep(time * 60)

        if d == "h":
            _d = 'hour(s)'
            await ctx.send(f'{member.mention} muted for {time} {_d}')
            await ctx.send(f'Reason: {reason}')
            await asyncio.sleep(time * 60 * 60)

        if d == "d":
            _d = 'day(s)'
            await ctx.send(f'{member.mention} muted for {time} {_d}')
            await ctx.send(f'Reason: {reason}')
            await asyncio.sleep(time * 60 * 60 * 24)

        await member.remove_roles(role)  # removes the role

    @commands.command(help='Unmute a forgiven user.')
    @commands.has_any_role('Victor', 'Moderator')
    async def unmute(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        with open('server-info.json', 'r') as f:
            mutedrole = json.load(f)
        role = discord.utils.get(member.guild.roles, name=mutedrole[f'{str(ctx.guild.id)}_muterole'])

        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f'{member.display_name} has been unmuted')
        else:
            await ctx.send('That user is not muted')

    @commands.command(help='Warn a user.')
    @commands.has_any_role('Victor', 'Moderator')
    async def warn(self, ctx, member: discord.Member):
        with open('server-info.json', 'r') as f:
            mutedrole = json.load(f)
        role = discord.utils.get(member.guild.roles, name=mutedrole[f'{str(ctx.guild.id)}_muterole'])
        with open('warns.json', 'r') as f:
            warns = json.load(f)
        if str(member.id) not in warns:
            warns[str(member.id)] = 1
        else:
            warns[str(member.id)] += 1
        if warns[str(member.id)] >= 3:
            warns[str(member.id)] = 0
        with open('warns.json', 'w') as f:
            json.dump(warns, f, indent=4)
        if warns[str(member.id)] == 1:
            await ctx.send(f'This is   {member.mention}\'s first warning.')
        if warns[str(member.id)] == 2:
            await ctx.send(f'This is {member.mention}\'s last warning!')
        if warns[str(member.id)] == 0:
            await ctx.send(f'{member.mention} was warned. Muted for 30 minutes')
            await member.add_roles(role)
            await asyncio.sleep(30 * 60)
            await member.remove_roles(role)

    @commands.command(help='Remove a warn from a user')
    @commands.has_any_role('Victor', 'Moderator')
    async def unwarn(self, ctx, member: discord.Member, amount: int = 1):
        with open('warns.json', 'r') as f:
            warns = json.load(f)
        if str(member.id) not in warns or warns[str(member.id)] == 0:
            await ctx.send('User has no warns')
        else:
            warns[str(member.id)] -= amount
            await ctx.send(f'{amount} warn(s) removed from {member.mention}')
        with open('warns.json', 'w') as f:
            json.dump(warns, f, indent=4)

    @commands.command(help='change the muted role name.')
    @commands.has_permissions(administrator=True)
    async def changemute(self, ctx, rolename):
        with open('server-info.json', 'r') as f:
            mutedrole = json.load(f)
        mutedrole[f'{str(ctx.guild.id)}_muterole'] = rolename
        with open('server-info.json', 'w') as f:
            json.dump(mutedrole, f, indent=4)
        await ctx.send(f'Muted role changed to \'{rolename}\'')


def setup(client):
    client.add_cog(Moderation(client))
