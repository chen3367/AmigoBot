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
client = commands.Bot(command_prefix='!', help_command=None, intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.command()
async def help(ctx):
    response = []
    response.append('\n'.join(['`!regroup [名字(逗號分開)] [幾組(default=2)]`', '分組']))
    response.append('\n'.join(['`!roll [幾顆(default=1)]`', '骰骰子']))
    await ctx.send('\n\n'.join(response))

@client.command()
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

@client.command()
async def roll(ctx, number: int = 1):
    if number == 1:
        await ctx.send(file=nextcord.File(f'./images/dice/{random.choice(range(1, 7))}.png'))
    else:
        dice = [
            str(random.choice(range(1, 7)))
            for _ in range(number)
        ]
        await ctx.send(', '.join(dice))

client.run(TOKEN)