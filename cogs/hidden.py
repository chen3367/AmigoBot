import discord
from discord.ext import commands
from discord.ext.commands import Bot

class Hidden(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(hidden=True)
    async def say(self, ctx, msg, channel: int = 1004062992301830278):
        channel = self.bot.get_channel(channel)
        await channel.send(msg)

async def setup(bot: Bot):
    await bot.add_cog(Hidden(bot))