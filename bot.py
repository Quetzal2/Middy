st1="""\033[1;33;40m
\033[1;31;40m  _______ __     __     __
\033[1;33;40m |   |   |__|.--|  |.--|  |.--.--.
\033[1;32;40m |       |  ||  _  ||  _  ||  |  |
\033[1;36;40m |__|_|__|__||_____||_____||___  |
\033[1;37;40m      -- DISCORD BOT --  \033[1;35;40m  |_____|

\033[1;37;40m Revision -\033[1;31;40m 3
\033[1;37;40m Version  - \033[1;31;40m1.2
\033[1;37;40m https://github.com/raithsphere/Middy
\033[1;37;40m At times I question you RaithSphere...
"""

import configparser
import discord
from discord.ext import commands

import asyncio
import os
import logging
import sys
import functools
import traceback
import aiohttp
import json
import subprocess
import signal
import platform
from progress.spinner import Spinner
from contextlib import contextmanager
from datetime import datetime

config = configparser.ConfigParser()
config.read('./config.ini')

secret_key = config['DEFAULT']['DISCORD_TOKEN']
prefix = config['DEFAULT']['COMMANDPREFIX']
owner = config['DEFAULT']['ADMIN_ID']

log = logging.getLogger(__name__)

startup_extensions = ["member","misc","rlstats","lfm","raith","calculated"]
bot_description = """An all-purpose bot written By RaithSphere."""

def get_prefix(bot, message):
    prefixes = [prefix, "?"]
    return commands.when_mentioned_or(*prefixes)(bot, message)

def get_json(url, fuck):
    try:
        return requests.get(url).json()
    except json.decoder.JSONDecodeError as e:
        print("Error decoding JSON for url:", url)
        raise e

class Middy(commands.AutoShardedBot):
    def __init__(self):
        bot = commands.Bot(command_prefix=get_prefix, description=bot_description)
        bot.boot_time = datetime.now()
        print(st1)
        spinner = Spinner('Loading Modules... ')
        for extension in startup_extensions:
            try:
                bot.load_extension(f'cogs.{extension}')
                spinner.next()
            except Exception as e:
                exc = f'{type(e).__name__}: {e}'
                print(f'Failed to load extension {extension}\n{exc}')
        print("\nConnecting to Discord....")

        @bot.event
        async def on_ready():

            if not hasattr(bot, 'appinfo'):
                bot.appinfo = await bot.application_info()

            print('Logged in as '+bot.user.name+' (ID:'+str(bot.user.id)+') | '+str(len(set(bot.get_all_members())))+' users')
            print('--------')
            print('My Owner is '+bot.appinfo.owner.name+' (ID:'+str(bot.appinfo.owner.id)+')')
            print('--------')
            print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
            print('--------\n')
            print(' \033[1;31;40m\u2665\u2665\u2665 \033[1;32;40mMiddy is loaded and waiting for commands \033[1;31;40m\u2665\u2665\u2665\033[1;37;40m')

            activity = discord.Game(name=f'Type {prefix}help')
            await bot.change_presence(status=discord.Status.online, activity=activity)

            file_name = "pid.txt"
            try:
                pid = open(file_name, 'r').read()
                os.kill(int(pid), signal.SIGKILL)
                os.remove(file_name)
            except FileNotFoundError:
                pass
            except ProcessLookupError:
                pass

        @bot.command()
        @commands.is_owner()
        async def list_cogs(self, ctx, name: str = None):
            if name is None:
                await ctx.send(f"Currently loaded cogs:\n{' '.join('`' + cog_name + '`' for cog_name in self.bot.extensions)}" if len(self.bot.extensions) > 0 else "No cogs loaded")
            else:
                if self.bot.extensions.get("cogs." + name) is None:
                    await self.bot.post_reaction(ctx.message, failure=True)
                else:
                    await self.bot.post_reaction(ctx.message, success=True)


        @bot.command()
        @commands.is_owner()
        async def load(ctx, extension_name :str):
            """Load an extension"""
            bot.load_extension(extension_name)
            await ctx.send(f"{extension_name} was successfully loaded.")


        @load.error
        async def load_error(ctx, error):
            """Handle load's errors"""
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f"Usage: {prefix}load(<extension name>).")
            if isinstance(error, commands.errors.CommandInvokeError):
                await ctx.send("Module not found.")
            if isinstance(error, commands.errors.NotOwner):
                await ctx.send("You're not my daddy, only daddy can use this function.")


        @bot.command()
        @commands.is_owner()
        async def unload(self, ctx, *, extension_name :str):
            if bot.get_cog(extension_name[extension_name.rfind(".")+1:]):
                bot.unload_extension(extension_name)
                await ctx.send(f"{extension_name} was successfully unloaded.")

            else:
                await ctx.send(f"Could not unload {extension_name}, module not found.")


        @unload.error
        async def unload_error(ctx, error):
            """Handle load's errors"""
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f"Usage: {prefix}unload(<extension name>).")
            if isinstance(error, commands.errors.NotOwner):
                await ctx.send("You're not my daddy, only daddy can use this function.")


        @bot.command()
        @commands.is_owner()
        async def reload(ctx, cog:str):
            """Reload a given cog"""
            bot.unload_extension(cog)
            bot.load_extension(cog)
            await ctx.send(f"{extension} reloaded successfully.")


        @bot.command()
        @commands.is_owner()
        async def shutdown(ctx):
            await ctx.send("Cya later o/")
            await bot.logout()
            bot.loop.close()


        @shutdown.error
        async def shutdow_error(ctx, error):
            """Handle shutdown's errors"""
            if isinstance(error, commands.errors.NotOwner):
                await ctx.send("You're not my daddy, only daddy can use this function.")


        @bot.command()
        @commands.is_owner()
        async def update(ctx):
            """Pull the newest updates from github"""
            with open("pid.txt", 'w') as file:
                file.write(str(os.getpid()))
            subprocess.run("sh update.sh", shell=True)

        @update.error
        async def update_error(ctx, error):
            """Handle update's errors"""
            if isinstance(error, commands.errors.NotOwner):
                await ctx.send("You're not my daddy, only daddy can use this function.")


        @bot.command()
        async def hello(ctx):
            """Ping command"""
            await ctx.send("world.")

        bot.run(secret_key, bot=True, reconnect=True)
