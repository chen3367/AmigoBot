import asyncio
import random
import os
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = nextcord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', help_command=None, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def help(ctx):
    response = []
    response.append('\n'.join(['`!regroup [名字(逗號分開)] [幾組(default=2)]`', '分組']))
    response.append('\n'.join(['`!roll [幾顆(default=1, 不超過6)]`', '骰骰子']))
    await ctx.send('\n\n'.join(response))

@bot.command()
async def regroup(ctx, player_list, number_of_groups: int = 2):
    # Convert player list from a string into a list
    player_list = list(filter(None, player_list.split(',')))

    # Shuffle list of students
    random.shuffle(player_list)
    
    # Create groups
    all_groups = []
    for index in range(number_of_groups):
        group = player_list[index::number_of_groups]
        all_groups.append(group)
    
    # Format and display groups
    response = []
    for index, group in enumerate(all_groups):
        response.append(f"Group {index+1}: {' / '.join(group)}")

    await ctx.send('\n'.join(response))

@bot.command()
async def roll(ctx, number: int = 1):
    if number <= 6:
        dices = [
            f'./images/dice/{random.choice(range(1, 7))}.png'
            for _ in range(number)
        ]
        await ctx.send(files=[nextcord.File(dice) for dice in dices])
    else:
        await ctx.send('骰子數不能超過6')

def load_cogs():
    '''
    The code in this function is executed whenever the bot will start.
    '''
    for file in os.listdir(f'./cogs'):
        if file.endswith('.py'):
            extension = file[:-3]
            try:
                bot.load_extension(f'cogs.{extension}')
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f'{type(e).__name__}: {e}'
                print(f'Failed to load extension {extension}\n{exception}')

load_cogs()
bot.run(TOKEN)