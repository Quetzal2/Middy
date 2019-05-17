import subprocess

from functools import partial
from discord.ext import commands

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.newline = "\n" # f-strings dont allow backslaches, screw that

    def clean(self, code): # Strip codeblock formatting from the message
        if code.startswith("```") and code.endswith("```"):
            return "\n".join(code.split("\n")[1:-1])
        return code.strip("` \n")

    @commands.command(name="debug", brief="eval", hidden=True)
    @commands.is_owner()
    async def debug_statement(self, ctx, *, content:str):
        code = self.clean(content)
        results = await self.bot.run_eval(code, ctx) # only one shard, so only one output
        await ctx.send(results) # only one shard, no comprehension needed

    @commands.command(name="run", brief="exec", hidden=True)
    @commands.is_owner()
    async def run_statement(self, ctx, *, content:str):
        code = self.clean(content)
        results = await self.bot.run_exec(code, ctx) # just as above
        await ctx.send(results)


    @commands.command(name="sys", brief="system terminal", hidden=True)
    @commands.is_owner()
    async def system_terminal(self, ctx, *, command:str):
        result = await self.bot.loop.run_in_executor(None, partial( # blocking function in non-blocking way
            subprocess.run,
            command,
            stdout=subprocess.PIPE,
            shell=True,
            universal_newlines=True
        ))
        result = result.stdout

        if len(result) > 1900:
            gist_result = await self.bot.upload_to_gist(result, 'output.txt')
            await ctx.send(f"Output too long. View results at {gist_result}") # bypass 2000 char limit with gist
        else:
            await ctx.send(f"```py\n{result}\n```")

def setup(bot):
    bot.add_cog(Debug(bot))
