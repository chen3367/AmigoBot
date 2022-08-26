import nextcord
import random
from nextcord.ext import commands
from nextcord.ext.commands import Bot

class Fun(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(description = 'Select a winner online')
    async def raffle(self, ctx):
        online_members = list(filter(lambda x: x.status != nextcord.Status.offline and not x.bot, ctx.guild.members))
        await ctx.send(f'Congratulations {random.choice(online_members).mention}!!')

    @commands.command(name = 'regroup <ID1,ID2,...> <n_groups>', description = 'Regroup into n groups')
    async def regroup(self, ctx, player_list, number_of_groups: int = 2):
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
    
def setup(bot: Bot):
    bot.add_cog(Fun(bot))