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

#age is not capital, int
#hunger is not capital, capped at 6,int
#life, int tracks life of digi
#name name of digi, starts as po, can be any digi
#type type of egg hatched dead
#age age of digi hatched, int

class digimon:

    bot = commands.Bot(command_prefix = '~')
    def __init__(self, bot):
        self.bot = bot
        self.conn = psycopg2.connect(dbname = "postgres", user = "postgres",password = "andymon89")

    @commands.group(pass_context = True, name = "d")
    async def digimon(self, ctx):
            """No command check"""
            if ctx.invoked_subcommand is None:
                await self.bot.say("Command inputted was invalid")

    @bot.event
    async def on_ready(self):
        self.db = pool.SimpleConnectionPool(0, 10,dbname = "postgres", user = "postgres",password = "andymon89")

    @digimon.command(pass_context=True, hide = True)
    async def tableDev(self, ctx, column, datatype):
        cur = self.conn.cursor()
        if(ctx.message.author == ctx.message.server.get_member("210049271116857344")):
            cur.execute("ALTER TABLE DIGIMONS ADD {0} {1};".format(column, datatype))
            self.conn.commit()
            print("done")

    @digimon.command(pass_context=True, hide=True)
    async def getter(self, ctx, column):
        cur = self.conn.cursor()
        if (ctx.message.author == ctx.message.server.get_member("210049271116857344")):
            cur.execute("SELECT {1} FROM DIGIMONS WHERE SERVER = '{0}'".format(ctx.message.server,column))
            cn = cur.fetchone()
            await self.bot.say(cn[0])
            self.conn.commit()

    @digimon.command(pass_context=True, hide=True)
    async def SQL(self, ctx,*, word):
        cur = self.conn.cursor()
        cur.execute("")
        self.conn.commit()
        print("done")

    @digimon.command(pass_context=True)
    async def setter(self, ctx,column : str, number ):
        cur = self.conn.cursor()
        if (ctx.message.author == ctx.message.server.get_member("210049271116857344")):
            cur.execute(
                    "UPDATE DIGIMONS SET {2} = '{1}' WHERE SERVER='{0}';".format(ctx.message.server, number, column))

            self.conn.commit()
            print("done")

    @digimon.command(pass_context = True)
    async def start(self,ctx):
        conn = psycopg2.connect(dbname = "postgres", user = "postgres",password = "andymon89")
        print("done")
        cur = conn.cursor()
        """Make check for if already there!!!"""
        cur.execute("SELECT SERVER from DIGIMONS")
        rows = cur.fetchall()
        print (rows)
        cur.execute(
            "SELECT TYPE FROM DIGIMONS WHERE SERVER = '{0}';".format(ctx.message.server))
        d_check = cur.fetchone()
        print(d_check)
        if(d_check[0] == 'DEAD'):
            egg = rand.choice(['Pink', 'Green', 'Red', 'Blue'])
            cur.execute("UPDATE DIGIMONS SET TYPE ='{1}',NAME='po', COUNTER=0 WHERE SERVER='{0}';".format(ctx.message.server,egg))
            print('haha')
            conn.commit()
            await self.bot.say("Your server found a new egg")

        elif(((str(ctx.message.server),) in rows)):
            await self.bot.say("Your server has an egg!")
        else:
            egg = rand.choice(['Pink', 'Green', 'Red', 'Blue'])
            cur.execute("INSERT INTO DIGIMONS (SERVER,NAME,COUNTER,TYPE) \
                              VALUES ('{0}', 'po', 0,'{1}')".format(ctx.message.server,egg))
            await self.bot.say("Your server found an egg!")
            conn.commit()

        rows = cur.fetchall()

    @digimon.command(pass_context = True)
    async def egg(self,ctx):
        await self.egg_Sub(ctx)

    async def egg_Sub(self,ctx):
        try:
            print("done")
            cur = self.conn.cursor()
            """Make check for if already there!!!"""
            cur.execute("SELECT SERVER,COUNTER,TYPE from DIGIMONS")
            rows = cur.fetchall()
            print(rows)
            for row in rows:
                if row[0] == str(ctx.message.server):
                    if(row[2] == 'Green'):
                        await self.bot.send_file(ctx.message.channel, "egg_pics/green.png",
                                                 filename='img.jpg')
                    if (row[2] == 'Pink'):
                        await self.bot.send_file(ctx.message.channel, "egg_pics/pink.png",
                                                 filename='img.jpg')
                    if (row[2] == 'Red'):
                        await self.bot.send_file(ctx.message.channel, "egg_pics/digiegg red.png",
                                                 filename='img.jpg')
                    if (row[2] == 'Blue'):
                        await self.bot.send_file(ctx.message.channel, "egg_pics/digiegg.png",
                                                 filename='img.jpg')
                    if (row[2] == 'HATCHED'):
                        cur.execute("SELECT NAME from DIGIMONS WHERE SERVER = '{0}';".format(str(ctx.message.server)))
                        digi = cur.fetchone()
                        print(digi)
                        await self.bot.send_file(ctx.message.channel, "digimon/{0}/{0}_happy.png".format(digi[0]))

        except commands.CommandOnCooldown  as e:
            await self.bot.say(str(e))

    @digimon.command(pass_context=True)
    @commands.cooldown(1,2, commands.BucketType.user)
    async def rub(self, ctx):
        eggs = ["dodomon", "botamon", "pichimon"]
        print("done")
        cur = self.conn.cursor()
        print("done")
        """Make check for if already there!!!"""
        cur.execute("SELECT TYPE FROM DIGIMONS WHERE SERVER = '{0}'".format(ctx.message.server   ))
        print(97)
        cn = cur.fetchone()
        if(cn[0] != 'HATCHED'):
             cur.execute("UPDATE DIGIMONS SET COUNTER=COUNTER+1  WHERE SERVER = '{0}'".format(ctx.message.server))
             cur.execute("SELECT SERVER,COUNTER FROM DIGIMONS")
             rows = cur.fetchall()
             await self.bot.send_message(ctx.message.channel, "You patted the egg!")
             print(rows)
             print(rows)
             for row in rows:
                 if row[0] == str(ctx.message.server):
                     if row[1] > 15 and row[1] < 30:
                         await self.bot.say("The egg is shaking!")
                     if (row[1] == 30):
                         await self.bot.say("The egg hatched!")
                         cur.execute("UPDATE DIGIMONS SET NAME='{1}', TYPE='HATCHED' WHERE SERVER = '{0}'".
                                     format(ctx.message.server, rand.choice(eggs)))
                         cur.execute(
                             "UPDATE DIGIMONS SET COUNTER=0 WHERE SERVER = '{0}'".format(ctx.message.server))
                         cur.execute(
                             "UPDATE DIGIMONS SET CARE=0 WHERE SERVER = '{0}'".format(ctx.message.server))
                         cur.execute(
                             "UPDATE DIGIMONS SET LIFE=100 WHERE SERVER = '{0}'".format(ctx.message.server))
                         cur.execute(
                             "UPDATE DIGIMONS SET age=0 WHERE SERVER = '{0}'".format(ctx.message.server))
                         cur.execute(
                             "UPDATE DIGIMONS SET AGECOUNTER=0 WHERE SERVER = '{0}'".format(ctx.message.server))
                         cur.execute(
                             "UPDATE DIGIMONS SET hunger=0 WHERE SERVER = '{0}'".format(ctx.message.server))
                     if (row[1] > 30):
                         await self.bot.say("The egg has hatched already!")
                         cur.execute(
                             "UPDATE DIGIMONS SET COUNTER=0 WHERE SERVER = '{0}'".format(ctx.message.server))

             await self.egg_Sub(ctx)
        else:
            await self.bot.send_message(ctx.message.channel, "Egg has already hatched")
        self.conn.commit()
        cur.close()

    @digimon.command(pass_context = True)
    async def eggStats(self, ctx):
        print("done")
        print("done")
        cur = self.conn.cursor()
        emb = discord.Embed(title="{0}'s egg".format(str(ctx.message.server)), color=0x00ff00)
        cur.execute("SELECT SERVER,COUNTER,TYPE FROM DIGIMONS")
        rows = cur.fetchall()
        type = str
        print(rows)
        for row in rows:
            print("good")
            if row[0] == str(ctx.message.server):
                emb.add_field(name = "Counter", value = row[1], inline = True)
                if (row[2] == 'Green'):
                     emb.set_image(url= "https://i.imgur.com/LqKmJBK.png")
                if (row[2] == 'Pink'):
                     emb.set_image(url= "https://i.imgur.com/LqKmJBK.png")

                if (row[2] == 'Red'):
                     emb.set_image(url= "https://i.imgur.com/e7AhueU.png")

                if (row[2] == 'Blue'):
                     emb.set_image(url= "https://imgur.com/CaiyaaL.png")
                if(row[2] == 'HATCHED'):
                    cur.execute("SELECT NAME FROM DIGIMONS WHERE SERVER = '{0}';".format(ctx.message.server))
                    digi = cur.fetchone()
                    await self.bot.send_file(ctx.message.channel, "digimon/{0}/{0}_stats.png".format(digi[0]))
                    emb.title = "{0}'s {1}".format(ctx.message.server, digi[0])
        print("done")
        await self.bot.send_message(ctx.message.channel, embed= emb)

    @digimon.command(pass_context=True)
    async def digiStats(self, ctx):
        print("done")
        print("done")
        cur = self.conn.cursor()
        emb = discord.Embed(title="{0}'s egg".format(str(ctx.message.server)), color=0x00ff00)
        cur.execute("SELECT SERVER,COUNTER,TYPE FROM DIGIMONS WHERE SERVER = '{0}';".format(ctx.message.server))
        rows = cur.fetchall()

        cur.execute("SELECT NAME FROM DIGIMONS WHERE SERVER = '{0}';".format(ctx.message.server))
        digi = cur.fetchone()
        print("197")

        bg = Image.open("digimon/{0}/{0}_stats.png".format(digi[0]))
        img = Image.open("UI/heart.png")
        print("197")
        cur.execute("SELECT HUNGER FROM DIGIMONS WHERE SERVER = '{0}';".format(ctx.message.server))
        hunger = cur.fetchone()
        print(hunger)
        print("197")

        for x in range(0,6 - hunger[0]):
            offset = (x * 20, 0)
            bg.paste(img, offset,img)
            print("l o o p")

        font = ImageFont.truetype("alterebro-pixel-font.ttf", 19)
        cur.execute("SELECT AGE FROM DIGIMONS WHERE SERVER = '{0}';".format(ctx.message.server))
        age = cur.fetchone()
        draw = ImageDraw.Draw(bg)
        w, h = draw.textsize("AGE : {0}".format(age[0]), font=font)
        draw.text(((160 - w), 160 - h ), "AGE : {0}".format(age[0]), fill=(0, 0, 0), font=font)

        pathlib.Path('{0}'.format(ctx.message.server)).mkdir(exist_ok=True)
        filepath = "{0}/{0}.png".format(ctx.message.server)
        print(filepath)
        bg.save(filepath)
        print("197")
        print("21")
        for row in rows:
            emb.add_field(name="Age", value=age[0], inline=True)
            if (row[2] == 'HATCHED'):
                cur.execute("SELECT NAME FROM DIGIMONS WHERE SERVER = '{0}';".format(ctx.message.server))
                digi = cur.fetchone()

                print("205")

                await self.bot.send_file(ctx.message.channel, "{0}/{0}.png".format(ctx.message.server))
                print("205")
                emb.title = "{0}'s {1}".format(ctx.message.server, digi[0])
        await self.bot.send_message(ctx.message.channel, embed= emb)

    def hunger(self,ctx, p1 : int, p2 : int):
        cur = self.conn.cursor()
        print("anima")

    @digimon.command(pass_context=True)
    @commands.cooldown(1,1800, commands.BucketType.user)
    async def feed(self, ctx):
        print("done")
        print("done")

        cur = self.conn.cursor()
        cur.execute("SELECT NAME FROM DIGIMONS WHERE SERVER = '{0}';".format(ctx.message.server))
        cur.execute("SELECT HUNGER FROM DIGIMONS WHERE SERVER = '{0}';".format(ctx.message.server))
        print("anima")
        hunger = cur.fetchone()
        print("anima")

        hunger2 = hunger[0]
        cur.execute("SELECT NAME FROM DIGIMONS WHERE SERVER = '{0}';".format(ctx.message.server))
        print(hunger2)
        digi = cur.fetchone()
        if (hunger2 == 0):
            cur.execute("UPDATE DIGIMONS SET HUNGER=0   WHERE SERVER = '{0}';".format(ctx.message.server))
            #await self.bot.send_file(ctx.message.channel, "digimon/{0}/{0}_no.gif".format(digi[0]))
        if (hunger2 < 0):
            await self.bot.say("Your digimon ate it, but it seems famished")
            cur.execute("UPDATE DIGIMONS SET HUNGER=0 WHERE SERVER = '{0}';".format(ctx.message.server))
            #await self.bot.send_file(ctx.message.channel, "digimon/{0}/{0}_refuse.gif".format(digi[0]))
        if (hunger2 > 6):
            await self.bot.say("You digimon is full!")
            cur.execute("UPDATE DIGIMONS SET LIFE=LIFE -({1}-6) WHERE SERVER = '{0}';".format(ctx.message.server,hunger2))
            cur.execute("UPDATE DIGIMONS SET HUNGER=6 WHERE SERVER = '{0}';".format(ctx.message.server))
            #await self.bot.send_file(ctx.message.channel, "digimon/{0}/{0}_overhunger.png".format(digi[0]))

        if(hunger2 != 0):
            await self.bot.say("You fed your digimon!")
            cur.execute("UPDATE DIGIMONS SET HUNGER=HUNGER-1  WHERE SERVER = '{0}'".format(ctx.message.server))
            print(hunger2)
            cur.execute("UPDATE DIGIMONS SET LIFE=LIFE+2 WHERE SERVER = '{0}';".format(ctx.message.server))
            #await self.bot.send_file(ctx.message.channel, "digimon/{0}/{0}_happy.png".format(digi[0]))

        print("done")
        self.conn.commit()

def setup(bot):
    bot.add_cog(digimon(bot))


    ''''@commands.cooldown(1,3600, commands.BucketType.server)'''






