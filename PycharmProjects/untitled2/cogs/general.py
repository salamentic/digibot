import random as rand
from discord.ext import commands
import discord
from io import BytesIO
from PIL import Image
import requests

class General:


    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context = True,name = "g")
    async def general(self, ctx):
            """No command check"""
            if ctx.invoked_subcommand is None:
                await self.bot.say("Command inputted was invalid")

    @general.command(pass_context = True)
    async def lenny(self,ctx):
        lenny = rand.choice([
            "( ͡° ͜ʖ ͡°)", "( ͠° ͟ʖ ͡°)", "ᕦ( ͡° ͜ʖ ͡°) ᕤ", "( ͡~ ͜ʖ ͡°)",
            "( ͡o ͜ʖ ͡o)", "͡(° ͜ʖ ͡ -)", "( ͡͡ ° ͜ ʖ ͡ °)﻿", "(ง ͠° ͟ل͜ ͡°)ง",
            "ヽ༼ຈل͜ຈ༽ﾉ"
          ])
        await self.bot.say(lenny)


    @general.command(pass_context=True)
    async def fite(self,ctx):
        memlist = ctx.message.server.members
        attaccs = ["I would fight ", "Noob more like ", "Level 1 mudkips exp source? ", "Mudkips will rule over bots like "]
        str = rand.choice(attaccs)
        bots = []
        for member in memlist:
            if(member.bot == True):
                bots.append(member)
        await self.bot.say(rand.choice(attaccs) + " " + rand.choice(bots).mention)


    @general.command(pass_context=True, name = "8ball")
    async def eightball(self,ctx, question):
        attaccs = ["Most likely ", "Time will tell ", "The outlook is poor ", "No ", "Yes", "Maybe"]
        await self.bot.say("{} {}".format(ctx.message.author.mention,rand.choice(attaccs)))






def setup(bot):
    bot.add_cog(General(bot))