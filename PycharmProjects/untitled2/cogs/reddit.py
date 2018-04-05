import random as rand
from discord.ext import commands
import discord
import random as rand
import requests, json
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from lxml import html
import praw
import re
import urllib3
import urllib

r = praw.Reddit(client_id='xMveCNeS98Tw6Q',
                         client_secret='0m_pdFNMC5svMp97X_2eV3Iz5hA',
                         user_agent='scrapeBot 0.1')
class reddit:

    r = praw.Reddit(client_id='xMveCNeS98Tw6Q',
                         client_secret='0m_pdFNMC5svMp97X_2eV3Iz5hA',
                         user_agent='scrapeBot 0.1')

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context = True)
    async def reddit(self, ctx):
            """No command check"""
            if ctx.invoked_subcommand is None:
                await self.bot.say("Command inputted was invalid")

    @reddit.command(pass_context = True)
    async def surmeme(self,ctx):
        checkWords = ['i.imgur.com', 'jpg', 'png', 'gif', 'gfycat.com', 'webm', ]
        subreddit = r.subreddit("surrealmemes")
        subs = []
        for sub in subreddit.hot(limit = 300):
            subs.append(sub)

        print("check")
        i = 0
        while i == 0:
            print("check")
            submission = rand.choice(subs)
            url_text = submission.url
            has_domain = any(string in url_text for string in checkWords)
            if has_domain:
                await self.bot.say(url_text)
                i = 1

    @reddit.command(pass_context=True)
    async def dankmeme(self, ctx):
        checkWords = ['i.imgur.com', 'jpg', 'png', 'gif', 'gfycat.com', 'webm', ]
        subreddit = r.subreddit("dankmeme")
        subs = []
        for sub in subreddit.hot(limit=300):
            subs.append(sub)

        print("check")
        i = 0
        while i == 0:
            print("check")
            submission = rand.choice(subs)
            url_text = submission.url
            has_domain = any(string in url_text for string in checkWords)
            if has_domain:
                await self.bot.say(url_text)
                i = 1

    @reddit.command(pass_context=True)
    async def search(self, ctx,*,word : str = "pics"):
        checkWords = ['i.imgur.com', 'jpg', 'png', 'gif', 'gfycat.com', 'webm', ]
        subreddit = r.subreddit(word)
        subs = []
        for sub in subreddit.hot(limit=50):
            subs.append(sub)

        print("check")
        i = 0
        if(not subreddit.over18):
            while i == 0:
                print("check")
                submission = rand.choice(subs)
                url_text = submission.url
                has_domain = any(string in url_text for string in checkWords)
                if has_domain:
                    await self.bot.say(url_text)
                    i = 1
        else:
            await self.bot.say("naughty boi ͡(° ͜ʖ ͡ -)")

    @reddit.command(pass_context=True)
    async def jokes(self, ctx):
        subreddit = r.subreddit("jokes")
        subs = []
        for sub in subreddit.hot(limit=50):
            subs.append(sub)
        i = 0
        while i == 0:
            submission = rand.choice(subs)
            if(submission.over_18 != True and i==0):
                await self.bot.say(submission.title)
                await self.bot.say(submission.selftext)
                i = 1

        await self.bot.say(rand.choice(subs).selftext)

    @reddit.command(pass_context=True)
    async def space(self, ctx):
        checkWords = ['i.imgur.com', 'jpg', 'png', 'gif', 'gfycat.com', 'webm', ]
        subreddit = r.subreddit("spaceporn")
        subs = []
        for sub in subreddit.hot(limit=100):
            subs.append(sub)

        print("check")
        i = 0
        if (not subreddit.over18):
            while i == 0:
                print("check")
                submission = rand.choice(subs)
                url_text = submission.url
                has_domain = any(string in url_text for string in checkWords)
                if has_domain:
                    await self.bot.say(url_text)
                    i = 1
        else:
            await self.bot.say("naughty boi ͡(° ͜ʖ ͡ -)")
def setup(bot):
    bot.add_cog(reddit(bot))