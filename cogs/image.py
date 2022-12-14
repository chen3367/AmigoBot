import discord
import random
from discord.ext import commands
from discord.ext.commands import Bot

class Image(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(brief = 'roll <number>', description = 'Roll n dices (must less than 7), default number = 1')
    async def roll(self, ctx, number: int = 1):
        if number < 7:
            dices = [
                f'./images/dice/{random.choice(range(1, 7))}.png'
                for _ in range(number)
            ]
            await ctx.send(files=[discord.File(dice) for dice in dices])
        else:
            await ctx.send('骰子數不能超過6')
    
async def setup(bot: Bot):
    await bot.add_cog(Image(bot))