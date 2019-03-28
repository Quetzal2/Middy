import discord
from discord.ext import commands

import logging
from logging.handlers import RotatingFileHandler
import datetime
from datetime import timedelta
import asyncio
import time
import platform
import requests
import base64
import feedparser
import random
import re
import threading, time

jarvisavatar = 'https://cdn.discordapp.com/avatars/284368851070877697/fb838b7fa492e35c9094d3f21d47bf91.png'

class RLStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stats', aliases=['lookup'])
    async def do_addition(self, ctx, first: str, second: str):
        """Lookup your rocket league stats. usage: !stats name platform"""
        url = "http://kyuu.moe/extra/rankapi.php"
        payload = {'channel': 'none', 'user': first, 'plat': second  }
        r = requests.get(url, params=payload)
        print(r.url)
        data = '%s' % (r.text)
        parts = data.replace('|', '\n')
        title = '%s\'s Rocket League Stats on %s' % (first, second)


        # And to make it look nice, we wrap it in an Embed.
        embed = discord.Embed(title=title, colour=0xff8000)
        embed.set_author(icon_url=jarvisavatar , name='RLStats')


        # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
        embed.add_field(name='\uFEFF', value=str(parts))

        await ctx.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(RLStats(bot))
