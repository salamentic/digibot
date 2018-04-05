import random as rand
from discord.ext import commands
import discord
import random as rand
import requests, json
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from lxml import html
from PIL import ImageFont
from PIL import ImageDraw
import math
import urllib3
import urllib
import pyppeteer
from pyppeteer import launch
import numpy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class meme:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context = True)
    async def meme(self, ctx):
            """No command check"""
            if ctx.invoked_subcommand is None:
                await self.bot.say("Command inputted was invalid")

    @meme.command(pass_context = True)
    async def bill(self,ctx,*, words : str):
        options = {"name" : "", "text" : "", "sex" : "m"}
        options["name"] = ctx.message.author
        options["text"] = "This is Bill\n\n\n{0}\n\n\nBe Like Bill".format(words)
        img = requests.post("http://belikebill.azurewebsites.net/billgen-API.php", data = options)
        img2 = Image.open(BytesIO(img.content))
        await self.bot.send_file(ctx.message.channel, BytesIO(img.content), filename='img.png', content='content')

    @meme.command(pass_context=True)
    async def vs(self, ctx, words: str):
        options = {"template_id" : "101910402", "username": "AniruddhRao","password" : "andymon89", "text0": ctx.message.mentions[0].name, "text1": words}
        options["name"] = ctx.message.author
        options["text"] = "This is Bill\n\n\n{0}\n\n\nBe Like Bill".format(words)
        img = requests.post("https://api.imgflip.com/caption_image", data=options)
        url = json.loads(img.text)
        emb = discord.Embed()
        array = ctx.message.mentions
        bg = requests.get(array[0].avatar_url, stream = True)
        img  = requests.get(url["data"]["url"], stream = True)
        bg2 = Image.open((img.raw))
        img2 = Image.open((bg.raw))

        img_w, img_h = img2.size

        bg_w, bg_h = bg2.size
        img2 = img2.resize((200,200),Image.ANTIALIAS)
        offset = (125, 250)
        bg2.paste(img2, offset)
        bg2.save("op.png")
        await self.bot.send_file(ctx.message.channel, "op.png", filename='img.png', content='content')

    @meme.command(pass_context=True)
    async def reddit(self, ctx):
        url = "http://www.reddit.com"
        htmll = requests.get(url)
        tree = html.fromstring(htmll.content)
        images = tree.xpath('//img[@class="itemImage"]/@src')
        print(images)

    @meme.command(pass_context=True)
    async def dollah(self, ctx, name : str):
        img = Image.open("drrr_template.png")
        array = ctx.message.mentions
        if(array.__len__() == 0):

            draw = ImageDraw.Draw(img)
            W, H = 348, 300
            # font = ImageFont.truetype(<font-file>, <font-size>)
            size = 18 - math.floor((name.__len__() / 6))
            print(size)
            font = ImageFont.truetype("impact.ttf", size)
            w, h = draw.textsize("but {0} walks in".format(name), font=font)
            draw.text(((W - w) / 2, H - H + 250), "but {0} walks in".format(name), fill=(255, 255, 255), font=font)
            img.save('{0}.png'.format(ctx.message.server))
            await self.bot.send_file(ctx.message.channel, "{0}.png".format(ctx.message.server), filename='img.jpg',
                                     content='content')
        else:
            bg = requests.get(array[0].avatar_url, stream = True)
            bg2 = Image.open((bg.raw))
            bg2 = bg2.resize((50, 50), Image.ANTIALIAS)
            draw = ImageDraw.Draw(img)
            img_w, img_h = img.size
            bg_w, bg_h = bg2.size
            W, H = 348, 300
            # font = ImageFont.truetype(<font-file>, <font-size>)
            size = 18 - math.floor((name.__len__()/6))
            print(size)
            font = ImageFont.truetype("impact.ttf", size)
            w,h = draw.textsize("but {0} walks in".format(name), font = font)
            draw.text(((W-w)/2,H-H+ 250), "but {0} walks in".format(name), fill = (255, 255, 255), font=font)
            offset = (150, 75)
            bg2.putalpha(25)
            img.paste(bg2, offset, bg2)
            img.save('{0}.png'.format(ctx.message.server))
            await self.bot.send_file(ctx.message.channel, "{0}.png".format(ctx.message.server), filename = 'img.jpg', content = 'content')

    @meme.command(pass_context=True)
    async def mars(self, ctx):
        sol = rand.randrange(0,2700)
        print("s")
        pic = requests.get("https://mars-photos.herokuapp.com/api/v1/rovers/Curiosity/photos?sol={0}".format(sol))
        print(pic)
        pic_array = json.loads(pic.text)
        print(pic_array["photos"])
        pic_specific = rand.choice(pic_array["photos"])
        print(pic_specific)
        pic_url = pic_specific["img_src"]

        print()
        await self.bot.say(pic_specific["camera"]["full_name"])
        await self.bot.say(pic_url)


def setup(bot):
    bot.add_cog(meme(bot))