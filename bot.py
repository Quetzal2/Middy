"""
   
   Core Discord Bot
   -------------
   Token is left blank here but under normal conditions you fill that in 
   All commnads and other parts of the bot are loaded via COGS which is in the initial_extensions 
   
"""

import logging
from logging.handlers import RotatingFileHandler
import discord
import datetime
from datetime import timedelta
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import platform
import requests
import base64
import feedparser
import random
import re
import threading, time
import sys, traceback

version = '18.09.27.1'

token = ''

description = '''
    This is a bot created by RaithSphere for the Mega Shogun discord 
    To help aid when trying to find a team mate for shogiebowl or anything else '''

initial_extensions = ['shogun']

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)

ts = time.time()
st1="""
______ _                       _
|  _  (_)                     | |
| | | |_ ___  ___ ___  _ __ __| |
| | | | / __|/ __/ _ \| '__/ _` |
| |/ /| \__ \ (_| (_) | | | (_| |
|___/ |_|___/\___\___/|_|  \__,_|.bot
  -BOT CREATED BY RAITHSPHERE -
 """


def get_prefix(bot, message):
    prefixes = ['?', '!']
    return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix=get_prefix, description=description)

@bot.event
async def on_ready():
    print(st1)
    print('Logged in as '+bot.user.name+' (ID:'+bot.user.id+') | Connected to '+str(len(bot.servers))+' servers | Connected to '+str(len(set(bot.get_all_members())))+' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(bot.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=0'.format(bot.user.id))
    print('--------')
    await bot.change_presence(game=discord.Game(name="Core Version %s " % (version) ,type=1))

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print(f'loaded extension {extension}.', file=sys.stderr)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


bot.run(token, bot=True, reconnect=True)

