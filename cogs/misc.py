import discord
import aiohttp
import re
import traceback
import aiohttp

from bs4 import BeautifulSoup as b_soup
from datetime import datetime
from random import choice
from io import BytesIO
from urllib.parse import quote_plus

from discord.ext import commands

aiosession = aiohttp.ClientSession()

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="retro", brief="make retro banners")
    async def make_retro(self, ctx, *, content:str):
        texts = [t.strip() for t in content.split("|")]
        if len(texts) != 3:
            await ctx.send("\N{CROSS MARK} Sorry! That input couldn't be parsed. Do you have 2 seperators? ( `|` )")
            return

        async with ctx.channel.typing():
            _tmp_choice = choice([1, 2, 3, 4])

            data = dict(
                bg=_tmp_choice,
                txt=_tmp_choice,
                text1=texts[0],
                text2=texts[1],
                text3=texts[2]
            )

            async with aiosession.post("https://photofunia.com/effects/retro-wave", data=data) as response:
                if response.status != 200:
                    await ctx.send("\N{CROSS MARK} Could not connect to server. Please try again later")
                    return

                soup = b_soup(await response.text(), "lxml")
                download_url = soup.find("div", class_="downloads-container").ul.li.a["href"]

                result_embed = discord.Embed()
                result_embed.set_image(url=download_url)
                result_embed.set_footer(text="The image gets removed after an hour, so save it")
                await ctx.send(embed=result_embed)

    @commands.command(name="chalk", brief="make chalk banners")
    async def make_chalk(self, ctx, *, content:str):
        texts = [t.strip() for t in content.split("|")]
        if len(texts) != 2:
            await ctx.send("\N{CROSS MARK} Sorry! That input couldn't be parsed. Do you have 1 seperator? ( `|` )")
            return

        async with ctx.channel.typing():
            _tmp_choice = choice(["duck", "duck"])

            data = dict(
                symbol=_tmp_choice,
                bg=_tmp_choice,
                txt=_tmp_choice,
                text=texts[0],
                text2=texts[1]
            )

            async with aiosession.post("https://photofunia.com/effects/chalkboard", data=data) as response:
                if response.status != 200:
                    await ctx.send("\N{CROSS MARK} Could not connect to server. Please try again later")
                    return

                soup = b_soup(await response.text(), "lxml")
                download_url = soup.find("div", class_="downloads-container").ul.li.a["href"]

                result_embed = discord.Embed()
                result_embed.set_image(url=download_url)
                result_embed.set_footer(text="The image gets removed after an hour, so save it")

                await ctx.send(embed=result_embed)


def setup(bot):
    bot.add_cog(Misc(bot))
