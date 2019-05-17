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
        self.loop = asyncio.get_event_loop()
        spinner = Spinner('Loading Modules... ')
        for extension in startup_extensions:
            try:
                bot.load_extension(f'cogs.{extension}')
                spinner.next()
            except Exception as e:
                exc = f'{type(e).__name__}: {e}'
                print(f'Failed to load extension {extension}\n{exc}')
				
        print("\nConnecting to Discord....")


		# Allows reactions to commands - await post_reaction(ctx.message, failure=True)
		# Credit goes to AnonymousDapper for this code
        async def post_reaction(message, emoji=None, **kwargs):
            reaction_emoji = ""

            if emoji is None:
                if kwargs.get("success"):
                    reaction_emoji = "\N{WHITE HEAVY CHECK MARK}"

                elif kwargs.get("failure"):
                    reaction_emoji = "\N{CROSS MARK}"

                elif kwargs.get("warning"):
                    reaction_emoji = "\N{WARNING SIGN}"

                else:
                    reaction_emoji = "\N{NO ENTRY}"

            else:
                reaction_emoji = emoji

            try:
                await message.add_reaction(reaction_emoji)

            except Exception as e:
                if not kwargs.get("quiet"):
                    await message.channel.send(reaction_emoji)


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

        # COGS LOADER VERSION 2
        @bot.command(name="load", brief="load cog")
        @commands.is_owner()
        async def load_cog(ctx, name: str):
            """Loads Cog"""
            cog_name = "cogs." + name.lower()

            if bot.extensions.get(cog_name) is not None:
                await post_reaction(ctx.message, emoji="\N{SHRUG}")
            else:
                try:
                    bot.load_extension(cog_name)

                except Exception as e:
                    await ctx.send(f"Failed to load {name}: [{type(e).__name__}]: `{e}`")
                else:
                    await post_reaction(ctx.message, success=True)

        @bot.command(name="unload", brief="unload cog")
        @commands.is_owner()
        async def unload_cog(ctx, name: str):
            """Unloads Cog"""
            cog_name = "cogs." + name.lower()

            if bot.extensions.get(cog_name) is None:
                await post_reaction(ctx.message, emoji="\N{SHRUG}")
            else:
                try:
                    bot.unload_extension(cog_name)

                except Exception as e:
                    await ctx.send(f"Failed to unload {name}: [{type(e).__name__}]: `{e}`")

                else:
                    await post_reaction(ctx.message, success=True)

        @bot.command(name="list")
        @commands.is_owner()
        async def list_cogs(ctx, name: str = None):
            """Lists Cog"""
            if name is None:
                await ctx.send(f"Currently loaded cogs:\n{' '.join('`' + cog_name + '`' for cog_name in bot.extensions)}" if len(bot.extensions) > 0 else "No cogs loaded")
            else:
                if self.bot.extensions.get("cogs." + name) is None:
                    await post_reaction(ctx.message, failure=True)
                else:
                    await post_reaction(ctx.message, success=True)
					
        @bot.command(name="reload")
        @commands.is_owner()
        async def reload_cog(ctx, name: str):
            """Reloads Cog"""
            cog_name = "cogs." + name.lower()

            if bot.extensions.get(cog_name) is None:
                await post_reaction(ctx.message, emoji="\N{SHRUG}")

            else:
                try:
                    bot.unload_extension(cog_name)
                    bot.load_extension(cog_name)

                except Exception as e:
                    await ctx.send(f"Failed to reload {name}: [{type(e).__name__}]: `{e}`")

                else:
                    await post_reaction(ctx.message, success=True)


		## END OF COGS LOADER
		
        @bot.command()
        @commands.is_owner()
        async def shutdown(ctx):
            """Does what it says on the tin"""
            await ctx.send("Cya later o/")
            await bot.logout()
            bot.loop.close()

        @shutdown.error
        async def shutdow_error(ctx, error):
            """Handle shutdown's errors"""
            if isinstance(error, commands.errors.NotOwner):
                await ctx.send("You're not my daddy, only daddy can use this function.")
                await post_reaction(ctx.message, failure=True)

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
