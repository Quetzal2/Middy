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

config = configparser.ConfigParser()
config.read('/home/raithsphere/Middy/config.ini')

secret_key = config['DEFAULT']['DISCORD_TOKEN']
prefix = config['DEFAULT']['COMMANDPREFIX']
owner = config['DEFAULT']['ADMIN_ID']

startup_extensions = ["member","misc","rlstats","lfm"]
bot_description = """An all-purpose bot written By RaithSphere."""

bot = commands.Bot(command_prefix=prefix, description=bot_description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
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
async def unload(ctx, extension_name :str):
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
async def reload(ctx, extension_name :str):
    """Reload a given cog"""
    await unload(ctx, extension_name)
    await load(ctx, extension_name)
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

if __name__ == "__main__":
    print("Loading modules....")
    for extension in startup_extensions:
        try:
            bot.load_extension(f'cogs.{extension}')
        except Exception as e:
            exc = f'{type(e).__name__}: {e}'
            print(f'Failed to load extension {extension}\n{exc}')
    print("Connecting to Discord....")


bot.run(secret_key, bot=True, reconnect=True)
