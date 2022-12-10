import discord
from discord.ext import commands
from discord.ext.commands import Bot

class General(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(description = 'Generate an Amigo Helper invite link')
    async def invite_amigo(self, ctx):
        await ctx.send('https://discord.com/api/oauth2/authorize?client_id=1010464728763613234&permissions=8&scope=bot')
    
async def setup(bot: Bot):
    await bot.add_cog(General(bot))