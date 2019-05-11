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

    @commands.command(name='cstats', aliases=['clookup'])
    async def do_addition(self, ctx, first: str, second: str):
        """Lookup your rocket league stats. usage: !stats name platform - For steam please use !ranks name"""
        url = "http://kyuu.moe/extra/rankapi.php"
        order = ['duel', 'doubles', 'solo', 'standard', 'hoops', 'rumble', 'dropshot', 'snowday']
        payload = {'channel': 'none', 'user': first, 'plat': second  }
        r = requests.get(url, params=payload)
        # And to make it look nice, we wrap it in an Embed.
        

        if second == "ps":
           platform = "https://cdn.discordapp.com/attachments/443021734497615873/576119031158013957/d69yvt3-5b8e9bba-2238-4b33-8e3f-619e41b71073.png"
           title = '%s\'s Rocket League Stats on PS4' % (first)
        if second == "xbox":
           platform = "https://cdn.discordapp.com/attachments/443021734497615873/576119385266192384/xbox.png"
           title = '%s\'s Rocket League Stats on Xbox' % (first)

        embed = discord.Embed(title=title, colour=0xff8000)
        embed.set_thumbnail(url=platform)


        print(r.url)
        data = '%s' % (r.text)
        parts = data.replace('|', '\n')
        ranks = data.split('|')
        x = len(ranks)
        for x in ranks[1:]:
           print(x)
           moreranks = x.split(':')
           print(moreranks)
           list = moreranks[0].strip()
           totalmmr = moreranks[1].strip()
           embed.add_field(name=list, value=totalmmr)

        embed.set_author(icon_url=jarvisavatar , name='RLStats')

        await ctx.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(RLStats(bot))