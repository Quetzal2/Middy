import discord
from discord.ext import commands
import hashlib

from explanations_list import explanations

import datetime
import json
import sys

import requests


class Calculated_gg(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def get_json(url):
        try:
            return requests.get(url).json()
        except json.decoder.JSONDecodeError as e:
            print("Error decoding JSON for url:", url)
            raise e
    
    def get_user_id(user):
            url = "https://calculated.gg/api/player/{}".format(user)
            id = Calculated_gg.get_json(url)
            return id


    def get_player_profile(id):
            response_profile = Calculated_gg.get_json("https://calculated.gg/api/player/{}/profile".format(id))

            avatar_link = response_profile["avatarLink"]
            avatar_name = response_profile["name"]
            platform = response_profile["platform"]
            past_names = response_profile["pastNames"]

            return avatar_link, avatar_name, platform, past_names


    def resolve_custom_url(url):
	# fetches the ID for the given username
            response_id = Calculated_gg.get_json("https://calculated.gg/api/player/{}".format(url))
            if str(type(response_id)) == "<class 'dict'>":
                response_id = "User not found"
            return response_id


    def chunks(l, n):
            """Yield successive n-sized chunks from l."""
            for i in range(0, len(l), n):
                yield l[i:i + n]

    @commands.command(pass_context=True, name='profile', aliases=['p'])
    async def get_profile(self, ctx, *, player: str):
        """lookup your profile on calculated.gg"""
        
        args = ctx.message.content.split(" ")
		
        if len(args) < 2:
            await bot.send_message(ctx.message.channel, f"Not enough arguments! The proper form of this command is: `{BOT_PREFIX}profile <id>`")
            return
        elif len(args) > 2:
            await bot.send_message(ctx.message.channel, f"Too many arguments! The proper form of this command is: `{BOT_PREFIX}profile <id>`")
            return

        print("Args Given:", args[1])
	
        id = Calculated_gg.resolve_custom_url(args[1])		

		
        """Shows the profile for the given id."""
        response_stats = Calculated_gg.get_json("https://calculated.gg/api/player/{}/profile_stats".format(id))
        car_name = response_stats["car"]["carName"]
        car_percentage = str(round(response_stats["car"]["carPercentage"] * 100, 1)) + "%"

        try:
            avatar_link, avatar_name, platform, past_names = Calculated_gg.get_player_profile(id)
        except KeyError:
            await ctx.send("User could not be found, please try again.")
            return
	
        list_past_names = ""
        for name in past_names:
            list_past_names = list_past_names + name + "\n"

                # creates stats_embed
        stats_embed = discord.Embed(
                color=discord.Color.blue()
                 )

        stats_embed.set_author(name=avatar_name, url="https://calculated.gg/players/{}/overview".format(id), icon_url="https://media.discordapp.net/attachments/495315775423381518/499488781536067595/bar_graph-512.png")
        stats_embed.set_thumbnail(url=avatar_link)
        stats_embed.add_field(name="Favourite car", value=car_name + " (" + car_percentage + ")")
        stats_embed.add_field(name="Past names", value=list_past_names)
        stats_embed.set_footer(text="Stats collected from calculated.gg")

	   # send message
        await ctx.send(content=None, embed=stats_embed)

    @commands.command(pass_context=True, name='ranks', aliases=['stats'])
    async def get_rank(self, ctx, *, player: str):
        """lookup your ranks on calculated.gg"""        
        args = ctx.message.content.split(" ")
		
        if len(args) < 2:
            await bot.send_message(ctx.message.channel, f"Not enough arguments! The proper form of this command is: `{BOT_PREFIX}profile <id>`")
            return
        elif len(args) > 2:
            await bot.send_message(ctx.message.channel, f"Too many arguments! The proper form of this command is: `{BOT_PREFIX}profile <id>`")
            return
	
        id = Calculated_gg.resolve_custom_url(args[1])		

		
        """Shows the profile for the given id."""

        order = ['duel', 'doubles', 'solo', 'standard', 'hoops', 'rumble', 'dropshot', 'snowday']

        try:
            avatar_link, avatar_name, platform, past_names = Calculated_gg.get_player_profile(id)
        except KeyError:
            await ctx.send("User could not be found, please try again.")
            return

        ranks = Calculated_gg.get_json("https://calculated.gg/api/player/{}/ranks".format(id))	
        list_past_names = ""
        for name in past_names:
            list_past_names = list_past_names + name + "\n"

                # creates stats_embed
        stats_embed = discord.Embed(
                color=discord.Color.blue()
                 )

        stats_embed.set_author(name=avatar_name, url="https://calculated.gg/players/{}/overview".format(id), icon_url="https://media.discordapp.net/attachments/495315775423381518/499488781536067595/bar_graph-512.png")
        stats_embed.set_thumbnail(url=avatar_link)

        for playlist in order:
            stats_embed.add_field(name=playlist.title(), value=ranks[playlist]['name'] + " - " + str(ranks[playlist]['rating']))

        stats_embed.set_footer(text="Stats collected from calculated.gg")

	   # send message
        await ctx.send(content=None, embed=stats_embed)



def setup(bot):
    bot.add_cog(Calculated_gg(bot))
