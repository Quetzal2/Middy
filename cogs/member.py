import discord
from discord.ext import commands

class member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx):
        """Provides information about the mentioned user"""
        try:
            user = ctx.message.mentions[0]
        except IndexError:
            await ctx.send("You didn't mention any users.")
            return

        usermsg = discord.Embed(
            title=":open_file_folder: User information about {}#{}.".format(user.name, user.discriminator),
            colour=0x9b59b6,  # purple
        )
        usermsg.add_field(
            name="Username:",
            value=user.name,
            inline=False,
        )
        usermsg.add_field(
            name="Nickname:",
            value=user.nick,
            inline=False,
        )
        usermsg.add_field(
            name="Status",
            value=user.status,
            inline=False,
        )
        usermsg.add_field(
            name="Joined Discord on:",
            value=str(user.created_at)[:16],
            inline=False,
        )
        usermsg.add_field(
            name="Joined server on:",
            value=str(user.joined_at)[:16],
            inline=False,
        )
        usermsg.set_thumbnail(
            url=user.avatar_url
        )
        await ctx.send(embed=usermsg)

def setup(bot):
    bot.add_cog(member(bot))
