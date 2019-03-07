
"""
   Shogun Cog
   -------------
   We offload alot of work here via HTTP to a webserver due to the bot running on a seperate box
   to the database, plus it was easier to work on something via PHP than Python at tha time
"""

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

class Looking_For_Team():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='lft', aliases=['queue'])
    async def lft(self, ctx, member: discord.Member=None):
        """Add yourself to the looking for teammate queue."""

        member = ctx.message.author

        url = ""
        payload = {'function': 'add', 'who': member  }
        r = requests.post(url, data=payload)
        data = '%s' % (r.text)

        embed = discord.Embed(title='Looking for Group:', colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        embed.add_field(name='\uFEFF', value=data)

        await self.bot.say(content=None, embed=embed)

    @commands.command(pass_context=True, name='remove', aliases=['noqueue'])
    async def remove(self, ctx, member: discord.Member=None):
        """Remove yourself from looking for a teammate."""

        member = ctx.message.author

        url = ""
        payload = {'function': 'remove', 'who': member  }
        r = requests.post(url, data=payload)
        data = '%s' % (r.text)

        embed = discord.Embed(title='Looking for Group:', colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        embed.add_field(name='\uFEFF', value=data)

        await self.bot.say(content=None, embed=embed)

    @commands.command(pass_context=True, name='lfm', aliases=['teammate','find'])
    async def lfm(self, ctx, member: discord.Member=None):
        """Search for a teammate."""

        member = ctx.message.author

        url = ""
        payload = {'function': 'find', 'who': member  }
        r = requests.post(url, data=payload)
        data = '%s' % (r.text)

        embed = discord.Embed(title='Looking for Player:', colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        embed.add_field(name='\uFEFF', value=data)

        await self.bot.say(content=None, embed=embed)

def setup(bot):
    bot.add_cog(Looking_For_Team(bot))
