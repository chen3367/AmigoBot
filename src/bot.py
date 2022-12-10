import discord
import json
from discord import app_commands
from discord.ext import commands
from src import responses
from src import log

import asyncio
import os
from discord import Interaction


logger = log.setup_logger()

with open('config.json', 'r') as f:
    data = json.load(f)

isPrivate = False

async def send_message(message, user_message):
    await message.response.defer(ephemeral=isPrivate)
    try:
        response = '> **' + user_message + '** - <@' + \
            str(message.user.id) + '>\n\n'
        response += await responses.handle_response(user_message)
        if len(response) > 1900:
            # Split the response into smaller chunks of no more than 1900 characters each(discord limit is 2000 per chunk)
            response_chunks = [response[i:i+1900]
                               for i in range(0, len(response), 1900)]
            for chunk in response_chunks:
                await message.followup.send(chunk)
        else:
            await message.followup.send(response)
    except Exception as e:
        await message.followup.send("> **Error: Something went wrong, please try again later!**")
        print(e)

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    activity = discord.Activity(type=discord.ActivityType.watching, name="/chat | /private | /public | /reset")
    bot = commands.Bot(command_prefix='!', help_command=None, intents=intents, activity=activity)
            
    @bot.event
    async def on_ready():
        await bot.tree.sync()
        for file in os.listdir(f'./cogs'):
            if file.endswith('.py'):
                extension = file[:-3]
                try:
                    await bot.load_extension(f'cogs.{extension}')
                    print(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f'{type(e).__name__}: {e}'
                    print(f'Failed to load extension {extension}\n{exception}')
        logger.info(f'{bot.user} is now running!')

    @bot.tree.command(name="chat", description="Have a chat with ChatGPT")
    async def chat(interaction: discord.Interaction, *, message: str):
        if interaction.user == bot.user:
            return
        username = str(interaction.user)
        user_message = message
        channel = str(interaction.channel)
        logger.info(
            f"\x1b[31m{username}\x1b[0m : '{user_message}' ({channel})")
        await send_message(interaction, user_message)

    @bot.tree.command(name="private", description="Toggle private access")
    async def private(interaction: discord.Interaction):
        global isPrivate
        await interaction.response.defer(ephemeral=False)
        if not isPrivate:
            isPrivate = not isPrivate
            logger.warning("\x1b[31mSwitch to private mode\x1b[0m")
            await interaction.followup.send("> **Info: Next, the response will be sent via private message. If you want to switch back to public mode, use `/public`**")
        else:
            logger.info("You already on private mode!")
            await interaction.followup.send("> **Warn: You already on private mode. If you want to switch to public mode, use `/public`**")

    @bot.tree.command(name="public", description="Toggle public access")
    async def public(interaction: discord.Interaction):
        global isPrivate
        await interaction.response.defer(ephemeral=False)
        if isPrivate:
            isPrivate = not isPrivate
            await interaction.followup.send("> **Info: Next, the response will be sent to the channel directly. If you want to switch back to private mode, use `/private`**")
            logger.warning("\x1b[31mSwitch to public mode\x1b[0m")
        else:
            await interaction.followup.send("> **Warn: You already on public mode. If you want to switch to private mode, use `/private`**")
            logger.info("You already on public mode!")

    @bot.tree.command(name="reset", description="Complete reset ChatGPT conversation history")
    async def reset(interaction: discord.Interaction):
        responses.chatbot.reset_chat()
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("> **Info: I have forgotten everything.**")
        logger.warning(
            "\x1b[31mChatGPT bot has been successfully reset\x1b[0m")

    TOKEN = data['discord_bot_token']
    bot.run(TOKEN)
