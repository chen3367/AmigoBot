import discord
from discord.ext import commands
from discord.ext.commands import Bot

class Greetings(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')

    @commands.command(description = 'Say hello to Amigo', aliases = ['Hello', 'HELLO', 'HI', 'Hi', 'hi', '哈囉', '安安', '嗨', '你好'])
    async def hello(self, ctx):
        await ctx.send('Hello!')
    
async def setup(bot: Bot):
    await bot.add_cog(Greetings(bot))