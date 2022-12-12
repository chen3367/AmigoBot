import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ui import Select, View

class MySelectView(View):
    @discord.ui.select(
            placeholder = 'Select a board',
            options = [
                discord.SelectOption(
                    label = 'Gossiping',
                    description = '八卦版'
                ),
                discord.SelectOption(
                    label = 'Gamesale',
                    description = '二手遊戲版'
                )
            ]
        )
    async def select_callback(self, interaction, select):
        select.disabled = True
        print('123')
        await interaction.response.edit_message(view = self)
        await interaction.followup.send(f'You chose: {select.values}')

class Test(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        
    @commands.command(hidden = True)
    async def test(self, ctx):
        view = MySelectView()  
        await ctx.send('Select a board', view = view)

async def setup(bot: Bot):
    await bot.add_cog(Test(bot))