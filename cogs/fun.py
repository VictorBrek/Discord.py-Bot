import discord
import random
from discord.ext import commands


class Fun(commands.Cog, description='Commands made for fun.'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('fun.py loaded')

    @commands.command(help='Check bot latency.')
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(usage='<dice>d<sides> eg. 1d20', help='Roll some dice!')
    async def roll(self, ctx, dice_d_sides):
        dice = str(dice_d_sides).split('d')[0]
        sides = str(dice_d_sides).split('d')[1]
        while True:
            if not dice.isdigit():
                await ctx.send('Must be a number')
                break
            if not sides.isdigit():
                await ctx.send('Must be a number')
                break
            else:
                break
        max_roll = int(dice) * int(sides)
        roll = range(1, max_roll)
        await ctx.send(dice + 'd' + sides)
        await ctx.send(random.choice(roll))

    @commands.command(help='A number guessing game.')
    async def guess(self, ctx, guess):
        lowest_number = 1
        highest_number = 100
        numbers = range(lowest_number, highest_number)
        number = random.choice(list(numbers))

        while True:
            if not guess.isdigit():
                await ctx.send('Must be a number!')
                break
            elif int(guess) < lowest_number:
                await ctx.send('Must be greater than or equal to ' + str(lowest_number))
                break
            elif int(guess) > highest_number:
                await ctx.send('Must be less than or equal to' + str(highest_number))
                break
            elif int(guess) == number:
                await ctx.send('Good job')
                break
            else:
                await ctx.send('Sorry, the number was '+str(number))
                break

    @commands.command(aliases=['rockpaperscissors'], help='Rock, paper, scissors!')
    async def rps(self, ctx, choice):
        rock = 'rock'
        paper = 'paper'
        scissors = 'scissors'
        choices = [rock, paper, scissors]
        bot_choice = random.choice(choices)

        win = 'You Win!'
        lose = 'You Lose...'
        await ctx.send(f'I picked {bot_choice}!')
        if choice.lower() == scissors and bot_choice == paper:
            await ctx.send(win)
        elif bot_choice == scissors and choice.lower() == paper:
            await ctx.send(lose)
        if choice.lower() == rock and bot_choice == scissors:
            await ctx.send(win)
        elif bot_choice == rock and choice.lower() == scissors:
            await ctx.send(lose)
        if choice.lower() == paper and bot_choice == rock:
            await ctx.send(win)
        elif bot_choice == paper and choice.lower() == rock:
            await ctx.send(lose)
        if bot_choice.lower() == choice.lower():
            await ctx.send('It\'s a tie!')

    @commands.command(aliases=['8ball'], help='Ask the mystical 8ball a question.')
    async def _8ball(self, ctx, *, question):
        responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.",
                     "Very doubtful.", "Without a doubt.",
                     "Yes.", "Yes – definitely.", "You may rely on it."]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command(aliases=['hardping'], help='Get someone\'s attention')
    @commands.has_any_role('Victor', 'Member')
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def spamping(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'```asciidoc\n[Spamping in Progress]```')
        await ctx.send(f'{member.mention} 1')
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{member.mention} 2')
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{member.mention} 3')
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{member.mention} 4')
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{member.mention} 5')
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{member.mention} 6')
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{member.mention} 7')
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{member.mention} 8')
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{member.mention} 9')
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{member.mention} 10')
        await ctx.channel.purge(limit=2)
        await ctx.send(f'{ctx.author.mention} needs {member.mention}\'s attention')

    @spamping.error
    async def spamping_mention_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send('Please mention a user to spamping.')

    @spamping.error
    async def spamping_cooldown_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_left = str(error)
            await ctx.send('Woah, you must really need them, try again in '+cooldown_left.split('in')[2])


def setup(client):
    client.add_cog(Fun(client))
