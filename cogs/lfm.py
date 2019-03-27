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

class Looking_For_Team(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='lft', aliases=['queue'])
    async def lft(self, ctx, member: discord.Member=None):
        """Add yourself to the looking for teammate queue."""

        member = ctx.message.author

        embed = discord.Embed(title='Looking for Group:', colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        embed.add_field(name='\uFEFF', value="I have set you to looking for a teammate")

        await ctx.send(content=None, embed=embed)

    @commands.command(pass_context=True, name='remove', aliases=['noqueue'])
    async def remove(self, ctx, member: discord.Member=None):
        """Remove yourself from looking for a teammate."""

        member = ctx.message.author

        url = "https://raithsphe.re/shogun/add.php"
        payload = {'function': 'remove', 'who': member  }
        r = requests.post(url, data=payload)
        data = '%s' % (r.text)

        # And to make it look nice, we wrap it in an Embed.
        embed = discord.Embed(title='Looking for Group:', colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
        embed.add_field(name='\uFEFF', value=data)

        await ctx.send(content=None, embed=embed)


    @commands.command(pass_context=True, name='lfm', aliases=['teammate','find'])
    async def lfm(self, ctx, member: discord.Member=None):
        """Search for a teammate."""

        member = ctx.message.author

        url = "https://raithsphe.re/shogun/add.php"
        payload = {'function': 'find', 'who': member  }
        r = requests.post(url, data=payload)
        data = '%s' % (r.text)

        # And to make it look nice, we wrap it in an Embed.
        embed = discord.Embed(title='Looking for Player:', colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
        embed.add_field(name='\uFEFF', value=data)

        await ctx.send(content=None, embed=embed)


def setup(bot):
    bot.add_cog(Looking_For_Team(bot))
