import random as rand
from discord.ext import commands
import discord
import random as rand
import requests, json
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from threading import Timer
import traceback
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE
import asyncio
import time
from PIL import ImageFont, ImageDraw
from psycopg2 import pool
import pathlib

class economy:

    def __init__(self, bot):
        self.bot = bot
        self.playing = []

    @commands.group(pass_context = True)
    async def economy(self, ctx):
            """No command check"""
            if ctx.invoked_subcommand is None:
                await self.bot.say("Command inputted was invalid")

    @economy.command(pass_context = True)
    @commands.cooldown(1, 3600*24  , commands.BucketType.user)
    async def daily(self,ctx):
        userdata = json.load((open("userData.json")))
        print(userdata)
        print("mommy")
        if("{}".format(ctx.message.author.id+ctx.message.server.id) not in userdata):
            userdata["{}".format(ctx.message.author.id+ctx.message.server.id)] = {}
        if ("money" not in userdata["{}".format(ctx.message.author.id + ctx.message.server.id)]):
            userdata["{}".format(ctx.message.author.id + ctx.message.server.id)]["money"] = 1000
        else:
            userdata["{}".format(ctx.message.author.id + ctx.message.server.id)]["money"] +=1000


        print(userdata)
        json.dump(userdata, open("userData.json", 'w'))
        await self.bot.say("You collected your daily bits! Your balance is {0} bits".format( userdata[ctx.message.author.id + ctx.message.server.id]['money']))

    @economy.command(pass_context=True)
    async def ecard(self, ctx, word : str):
        print(self.playing)
        if(ctx.message.mentions[0] == None or not (ctx.message.mentions[0] in ctx.message.server.members) or ctx.message.mentions[0] == ctx.message.author or ctx.message.mentions[0] == "@everyone"):
            await self.bot.say("cant play with nobody ")
            return
        #check for freelo
        if (ctx.message.author in self.playing):
            await self.bot.say("You are already in a game!")
            return
        else:
            self.playing.append(ctx.message.author)
        print(self.playing)
        #check freelo end

        #variables end
        winner = None
        loser = None
        amount = 0
        member = ctx.message.mentions[0]
        print(member.id)

        #Variables end


        #Message wait for accepting
        msg = await self.bot.wait_for_message(content= "~accept", author= member, timeout=60)
        if(msg == None):
            await self.bot.say("Timeout")
            self.playing.remove(ctx.message.author)
            return

        #checks for stupidity begin
        if (ctx.message.author == member):
            await self.bot.say("Can't play with yourself fren *wink*")
            self.playing.remove(ctx.message.author)
            return

        if (not (member in self.playing)):
            self.playing.append(member)
        else:
            await self.bot.say("The person you challenged is already playing a game!")
            self.playing.remove(ctx.message.author)
            return
        print(self.playing)
        await self.bot.send_message(ctx.message.channel, '{0} accepted the challenge!'.format(ctx.message.mentions[0].mention))
        #checks for stupidity end

        #Array of possible entries.
        special = ["Slave", "Emperor"]
        challenger = rand.sample(["Citizen", "Citizen", "Citizen", "Citizen", rand.choice(special)], 5)
        print(challenger)

        challenged = ["Citizen", "Citizen", "Citizen", "Citizen", "Slave"]
        if (challenger.__contains__("Slave")):
            challenged[4] = "Emperor"
        challenged = rand.sample(challenged, 5)
        print(challenged)

        await self.bot.send_message(ctx.message.author, "{}".format(challenger))
        await self.bot.send_message(member, "{}".format((challenged)))
        win = False

        def check(msg):
            return msg.content in (0,1,2,3,4)

        turn = 4
        cards = ["0", "1", "2", "3", "4"]
        while(win == False):
            def check(msg):
                x = msg.content in cards
                return x
            msg1 = await self.bot.wait_for_message(author=ctx.message.author, check=check, timeout=60)
            if (msg1 == None):
                await self.bot.say("Timeout")
                self.playing.remove(ctx.message.author)
                self.playing.remove(member)
                return
            msg2 = await self.bot.wait_for_message(author= member, check=check, timeout=60)
            if (msg == None):
                await self.bot.say("Timeout")
                self.playing.remove(ctx.message.author)
                self.playing.remove(member)

                return
            print("xx")
            print(msg1.content)
            print(msg2.content)
            print(challenger[(int(msg1.content))])
            await self.bot.send_file(ctx.message.channel,"ecard/{}.png".format(challenger[int(msg1.content)]),filename='img.png', content="The challenger played {}".format(challenger[int(msg1.content)]))
            await self.bot.send_file(ctx.message.channel,"ecard/{}.png".format(challenged[int(msg2.content)]),filename='img2.png', content="The challengee played {}".format(challenged[int(msg2.content)]))
            if(challenger[int(msg1.content)] == "Emperor" and challenged[int(msg2.content)] == "Citizen"):
                win = True
                winner = msg1.author
                loser = msg2.author
                amount = 1000

            if (challenged[int(msg2.content)] == "Emperor" and challenger[int(msg1.content)] == "Citizen"):
                win = True
                winner = msg2.author
                loser = msg1.author
                amount = 1000

            if (challenged[int(msg2.content)] == "Citizen" and challenger[int(msg1.content)] == "Slave"):
                win = True
                winner = msg2.author
                loser = msg1.author
                amount = 1000

            if (challenged[int(msg2.content)] == "Slave" and challenger[int(msg1.content)] == "Citizen"):
                win = True
                winner = msg1.author
                loser = msg2.author
                amount = 1000


            if (challenged[int(msg2.content)] == "Slave" and challenger[int(msg1.content)] == "Emperor"):
                win = True
                winner = msg2.author
                loser = msg1.author
                amount = 5000

            if (challenged[int(msg2.content)] == "Emperor" and challenger[int(msg1.content)] == "Slave"):
                win = True
                winner = msg1.author
                loser = msg2.author
                amount = 5000

            print(str(turn))
            cards.remove(str(turn))
            print(2)
            turn -= 1
            challenger.remove(challenger[int(msg1.content)])
            challenged.remove(challenged[int(msg2.content)])
            await self.bot.send_message(ctx.message.author, "{}".format(challenger))
            await self.bot.send_message(member, "{}".format((challenged)))


        self.playing.remove(winner)
        self.playing.remove(loser)
        await self.bot.say("Winner is {}".format(winner))
        userdata = json.load((open("userData.json")))
        if ("{}".format(ctx.message.author.id + ctx.message.server.id) not in userdata):
            userdata["{}".format(ctx.message.author.id + ctx.message.server.id)] = {}
        if ("money" not in userdata["{}".format(ctx.message.author.id + ctx.message.server.id)]):
            userdata["{}".format(ctx.message.author.id + ctx.message.server.id)]["money"] = 1000

        if ("{}".format(member.id + ctx.message.server.id) not in userdata):
            userdata["{}".format(member.id + ctx.message.server.id)] = {}
        if ("money" not in userdata["{}".format(member.id + ctx.message.server.id)]):
            userdata["{}".format(member.id + ctx.message.server.id)]["money"] = 1000

        userdata["{}".format(winner.id + ctx.message.server.id)]["money"] += amount
        print("winwin")
        userdata["{}".format(loser.id + ctx.message.server.id)]["money"] -= amount
        json.dump(userdata, open("userData.json", 'w'))
        await self.bot.say("{0} : {1}".format(ctx.message.author,userdata["{}".format(ctx.message.author.id + ctx.message.server.id)]["money"]))
        await self.bot.say("{0} : {1}".format(member,userdata["{}".format(member.id + ctx.message.server.id)]["money"]))





def setup(bot):
    bot.add_cog(economy(bot))
