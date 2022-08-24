import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Bot

class General(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def invite_amigo(self, ctx):
        await ctx.send('https://discord.com/api/oauth2/authorize?client_id=1010464728763613234&permissions=8&scope=bot')
    
def setup(bot: Bot):
    bot.add_cog(General(bot))