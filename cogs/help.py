import discord
from discord.ext import commands
from discord.ext.commands import Bot

class Help(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(description = 'Help command for Amigo Helper')
    async def help(self, ctx):
        embed = discord.Embed(title = 'Amigo Helper', description = 'Help command for Amigo Helper!!')
        for command in self.bot.walk_commands():
            if not command.hidden:
                description = command.description
                if not description:
                    description = 'No description provided'
                embed.add_field(name = f'!{command.brief if command.brief else command.name}', value = description)
        await ctx.send(embed=embed)

async def setup(bot: Bot):
    await bot.add_cog(Help(bot))