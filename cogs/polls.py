import discord
from discord.ext import commands

import re


class Polls(commands.Cog):
    
    bot = None          #  The bot
    polls = None        #  List of created polls
    active_poll = None  #  Poll currently being used
    
    def __init__(self, bot):
        self.bot = bot
        polls = []
    
    
    class PollParser(commands.Converter):
        async def convert(self, ctx, message):
            pattern_option_choice = re.compile(r"^\s*(\w+|:\w+:)\s*(:.*|\s*\n?$)")
            pattern_option_value = re.compile(r"^\s*(\w+|:\w+:)\s*:\s*(.*[^\s])\s*\n?")
            
            pattern_parameter = re.compile(r"^\s*;")
            
            
            message_lines = message.splitlines()
            poll = Poll()
            
            ## Get the title
            poll.title = message_lines[0]
            
            ## Get the options and the parameters
            for line in message_lines:
                
                # parameter?
                parameter = re.match(pattern_parameter, line)
                option = re.match(pattern_option_choice, line)
                if parameter != None:
                    pass###TODO### Manage parameters
                elif option != None:
                    poll_option = PollOption()
                    poll_option.choice = option.group(1)
                    
                    ## Get the value
                    
                    value = re.match(pattern_option_value, line)
                    if value != None: #there's a value
                        value = value.group(2)
                        pattern_input = self.inputPattern()
                        inputs = []
                        spans = []
                        for i in pattern_input.finditer(value):
                            o_input = OptionInput()
                            o_input.i_environment = i.group(3)
                            o_input.i_name = i.group(5)
                            o_input.i_type = i.group(7)
                            o_input.i_default = i.group(9)
                            inputs += [o_input]
                            spans += [i.span()]
                        if inputs != []:
                            patterns = [value[:spans[0][0]]]
                            for s_i in range(len(spans)-1):
                                patterns += [value[spans[s_i][1]:spans[s_i+1][0]]]
                            patterns += [value[spans[-1][1]:]]
                            poll_option.inputs = inputs
                            poll_option.patterns = patterns
                        else:
                            poll_option.inputs = []
                            poll_option.patterns = [value]
                    poll.options += [poll_option]
            return poll
        
        
        def inputPattern(self):
            
            catch = r"(\w+)"
            s = r"\s*"
            
            inp_env = r"("+catch+s+r":"+s+r")?"
            
            inp_name = catch
            inp_type = r"("+s+r"\("+s+catch+s+r"\)"+s+r")?"
            inp_def = r"("+s+r"="+s+catch+r")?"
            inp_body = r"("+inp_name+inp_type+inp_def+r")?"
            
            input_pattern = r"\["+s+r"("+inp_env+inp_body+r")"+s+r"\]"
            return re.compile(input_pattern)
    
    
    @commands.command(pass_context=True, name='poll')
    async def poll(self, ctx, *, poll: PollParser):
        answer = discord.Embed(
            title=poll.title,
            colour=0x124D43,
        )
        for option in poll.options:
            answer.add_field(
                name=option.choice,
                value=option.valueToString(),
                inline=False,
            )
        answer.set_thumbnail(
            url=ctx.message.author.avatar_url
        )

        await ctx.send(embed=answer)
    




class EPollState:
    init = "init"
    running = "running"
    complete = "complete"
    archived = "archived"

class Poll:
    title = None
    options = None
    
    state = None
    parameters = {
         "grow": False
        ,"match_strict":70
        }
    
    def __init__(self):
        self.state = EPollState.init
        self.options = []
    
    def toString(self):
        string = self.title + "\n"
        for o in self.options:
            string += o.toString() + "\n"
        return string
    


class PollOption:
    choice=None
    inputs=[]
    patterns=[]
    
    def toString(self):
        string = self.choice + " : "
        for i in range(len(self.patterns)-1):
            string += self.patterns[i]
            string += self.inputs[i].toString()
        string += self.patterns[-1]
        return string

    def valueToString(self):
        string = ""
        for i in range(len(self.patterns)-1):
            string += self.patterns[i]
            string += self.inputs[i].toString()
        string += self.patterns[-1]
        return string



class OptionInput:
    i_environment = None
    i_name = None
    i_type = None
    i_default = None

    def toString(self):
        env = self.i_environment+":" if self.i_environment != None else ""
        name = self.i_name if self.i_name != None else ""
        itype = "("+self.i_type+")" if self.i_type != None else ""
        default = "="+self.i_default if self.i_default != None else ""
        return "[" + env + name + itype + default + "]"



def setup(bot):
    bot.add_cog(Polls(bot))