import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Bot

class Help(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(description = 'Help command for Amigo Helper')
    async def help(self, ctx):
        embed = nextcord.Embed(title = 'Amigo Helper', description = 'Help command for Amigo Helper!!')
        for command in self.bot.walk_commands():
            if command.name != 'say':
                description = command.description
                if not description:
                    description = 'No description provided'
                embed.add_field(name = f'!{command.brief if command.brief else command.name}', value = description)
        await ctx.send(embed=embed)

def setup(bot: Bot):
    bot.add_cog(Help(bot))