import discord
import cogs
import discord.server
from discord.ext import commands
import discord.emoji
import discord.reaction
import requests, json
import time
import random
import string
from PIL import Image
from io import BytesIO
import http as http
import datetime
from dateutil.relativedelta import relativedelta as rd
import math
import psycopg2
import asyncio

conn = psycopg2.connect(dbname="postgres", user="postgres", password="andymon89")
TOKEN = 'NDE4NjI0ODQ0ODYzNzY2NTM0.DXkeDw.pHaUR8UoKQ-zxFXqEk2ATDsszTQ'
api = "RGAPI-026e5f05-9548-4d8d-9dbf-7cf48dd6327f"
description = "kip mudkip"
bot = commands.Bot(command_prefix = ('~','!'))
mastery_emotes = {5 : ":mastery5:420518599963312129"   , 6 : ":mastery6:420518682524123136", 7 : ':mastery7:420518709220737034'}


@bot.event
async def on_ready():
    bot.self_bot = False
    print('Logged in as')
    status = discord.Game
    choicez = ["Piplup", "Squirtle", "Torchic"]
    str = "With" + random.choice(choicez)
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.load_extension('cogs.general')
    bot.load_extension('cogs.economy')
    bot.load_extension('cogs.meme')
    bot.load_extension('cogs.reddit')
    bot.load_extension('cogs.digimon')
    await bot.change_presence(game=discord.Game(type=0, name="With {0}".format(random.choice(choicez))))
    print("done")


@bot.event
async def on_message(message):
    cont = message.content.lower()
    table = cont.maketrans("", "", string.punctuation)
    check = cont.translate(table)
    if(check.startswith('no u' or 'no you') and message.author.bot != True):
       await bot.send_message(message.channel,'no u')

    if (((check.startswith('no you') or (check.startswith('no yu'))and message.author.bot != True))):
        await bot.send_message(message.channel, 'no u')
    if ((( 'sandshrew' in (message.content.lower()) and message.author.bot != True) and 'alolan' not in (message.content.lower()))):
        await bot.send_message(message.channel, 'Yeah alolan sandshrew is best')
        await bot.add_reaction(message, 'downdoot:420606340961140747')
    await bot.process_commands(message)

async def age_task():
    cur = conn.cursor()
    counter =0
    while not bot.is_closed:
        for server in list(bot.servers):
            cur.execute(
                "UPDATE DIGIMONS SET AGECOUNTER=AGECOUNTER+1 WHERE SERVER = '{0}' AND TYPE = 'HATCHED';".format(server))
            cur.execute("SELECT AGECOUNTER FROM DIGIMONS WHERE (SERVER = '{0}')AND (NAME != 'RIP');".format(server))
            age = cur.fetchone()
            cur.execute("SELECT AGE FROM DIGIMONS WHERE (SERVER = '{0}')AND (NAME != 'RIP');".format(server))
            age_r = cur.fetchone()
            if (age != None and age[0] != None):
                # evolution to in training check
                if (age[0] > 60):
                    cur.execute(
                        "UPDATE DIGIMONS SET AGECOUNTER=0 WHERE SERVER = '{0}' AND TYPE = 'HATCHED';".format(
                            server))
                    cur.execute(
                        "UPDATE DIGIMONS SET AGE=AGE+1 WHERE SERVER = '{0}' AND TYPE = 'HATCHED';".format(
                            server))
                    if (age_r[0] == 0 and age[0] > 60):
                        evolutions = ["koromon"]
                        cur.execute("SELECT NAME FROM DIGIMONS WHERE SERVER='{0}'".format(server))
                        name = cur.fetchone()
                        if (name[0] == "botamon"):
                            cur.execute("UPDATE DIGIMONS SET NAME='{1}' WHERE SERVER = '{0}';".format(server, "koromon"))
                            cur.execute(
                                "UPDATE DIGIMONS SET LIFE='250' WHERE SERVER = '{0}';".format(server))
                            cur.execute(
                                "UPDATE DIGIMONS SET CARE='0' WHERE SERVER = '{0}';".format(server))
                            cur.execute(
                                "UPDATE DIGIMONS SET HUNGER='0' WHERE SERVER = '{0}';".format(server))

                            conn.commit()
                            # dodomon evolutions
                        if (name[0] == "dodomon"):
                            cur.execute(
                                "UPDATE DIGIMONS SET NAME='{1}' WHERE SERVER = '{0}';".format(server, "dorimon"))

                            cur.execute(
                                "UPDATE DIGIMONS SET CARE='0' WHERE SERVER = '{0}';".format(server))
                            cur.execute(
                                "UPDATE DIGIMONS SET HUNGER='0' WHERE SERVER = '{0}';".format(server))

                            cur.execute(
                                "UPDATE DIGIMONS SET LIFE='250' WHERE SERVER = '{0}';".format(server))
                            conn.commit()
                            # end
                print(age_r)
                # In training to rookie check
                if (age_r[0] == (25)):
                    cur.execute("SELECT CARE FROM DIGIMONS WHERE SERVER='{0}'".format(server))
                    care = cur.fetchone()
                    cur.execute("SELECT NAME FROM DIGIMONS WHERE SERVER='{0}'".format(server))
                    name = cur.fetchone()
                    # botamon evolutions
                    if (name[0] == 'koromon'):

                        # agumon check
                        if (care[0] < 4):
                            cur.execute("UPDATE DIGIMONS SET NAME='agumon' WHERE SERVER = '{0}';".format(server))
                            cur.execute(
                                "UPDATE DIGIMONS SET LIFE='500' WHERE SERVER = '{0}';".format(server))
                        # betamon check
                        if (care[0] >= 4):
                            cur.execute("UPDATE DIGIMONS SET NAME='betamon' WHERE SERVER = '{0}';".format(server))
                            cur.execute(
                                "UPDATE DIGIMONS SET LIFE='500' WHERE SERVER = '{0}';".format(server))
                            # botamon evos end
                            # dodomon evolutions
                    if (name[0] == 'dodomon'):
                        # dorumon check
                        if (care[0] < 4):
                            cur.execute("UPDATE DIGIMONS SET NAME='dorumon' WHERE SERVER = '{0}';".format(server))
                            cur.execute(
                                "UPDATE DIGIMONS SET CARE='0' WHERE SERVER = '{0}';".format(server))
                            cur.execute(
                                "UPDATE DIGIMONS SET HUNGER='0' WHERE SERVER = '{0}';".format(server))
                            cur.execute(
                                "UPDATE DIGIMONS SET LIFE='500' WHERE SERVER = '{0}';".format(server))
                        # ryudamon check
                        if (care[0] >= 4):
                            cur.execute("UPDATE DIGIMONS SET NAME='ryudamon' WHERE SERVER = '{0}';".format(server))
                            cur.execute(
                                "UPDATE DIGIMONS SET CARE='0' WHERE SERVER = '{0}';".format(server))
                            cur.execute(
                                "UPDATE DIGIMONS SET HUNGER='0' WHERE SERVER = '{0}';".format(server))
                            cur.execute(
                                "UPDATE DIGIMONS SET LIFE='500' WHERE SERVER = '{0}';".format(server))
                    conn.commit()
            conn.commit()
        await asyncio.sleep(60) # task runs every 60 seconds


async def hunger_task():
    await bot.wait_until_ready()
    cur = conn.cursor()
    counter = 0
    print(71)
    while not bot.is_closed:
        counter += 1
        for server in list(bot.servers):
             cur.execute("UPDATE DIGIMONS SET HUNGER=HUNGER+1 WHERE SERVER = '{0}' AND TYPE = 'HATCHED';".format(server))
             cur.execute("UPDATE DIGIMONS SET LIFE=LIFE-1 WHERE SERVER = '{0}' AND TYPE = 'HATCHED';".format(server))

             cur.execute("SELECT LIFE FROM DIGIMONS WHERE SERVER = '{0}' AND TYPE = 'HATCHED' AND NAME != 'RIP';".format(server))
             life = cur.fetchone()

             cur.execute("SELECT HUNGER FROM DIGIMONS WHERE SERVER = '{0}' AND TYPE = 'HATCHED';".format(server))
             hunger = cur.fetchone()

             cur.execute("SELECT AGE FROM DIGIMONS WHERE (SERVER = '{0}')AND (NAME != 'RIP');".format(server))
             age_r = cur.fetchone()

             if(hunger != None and  hunger[0] > 9 and age_r != 0):
                 cur.execute("UPDATE DIGIMONS SET CARE=CARE+1 WHERE SERVER = '{0}';".format(server))



             if(life != None):
                 if(life[0] <= 0 ):
                     cur.execute(
                         "UPDATE DIGIMONS SET NAME = 'RIP', TYPE = 'DEAD', LIFE=0 WHERE SERVER = '{0}' AND TYPE = 'HATCHED';".format(server))

             conn.commit()
        await asyncio.sleep(3600) # task runs every 60 seconds

@bot.event
@commands.cooldown(1,5,commands.BucketType.server)
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        fmt = '{0.days} days {0.hours} hours {0.minutes} minutes {0.seconds} seconds'
        sec = error.retry_after
        hour = math.floor(sec /3600)
        sec -= hour * 3600
        minutes = math.floor(sec / 60)
        sec -= minutes * 60
        x =await bot.send_message(ctx.message.channel, "Please try again in {0} hours, {1} minutes and {2} seconds!".format(hour, minutes, math.floor(sec)))
        time.sleep(1)

@bot.event
async def on_message(message):
    cont = message.content.lower()

    sender = message.author



    table = cont.maketrans("", "", string.punctuation)
    check = cont.translate(table)
    if(check.startswith('no u' or 'no you') and message.author.bot != True):
       await bot.send_message(message.channel,'no u')

    if (((check.startswith('no you') or (check.startswith('no yu'))and message.author.bot != True))):
        await bot.send_message(message.channel, 'no u')
    if(check.startswith('im') and message.author.bot != True):
        ms = await bot.send_message(message.channel, 'Hi {0}'.format(check.split('im ')[1]))
        time.sleep(2)
        await bot.add_reaction(message, 'downdoot:420606340961140747')
        await bot.delete_message(ms)
    await bot.process_commands(message)


@bot.command(pass_context=True)
async def lolcheck(ctx, summoner_name : str,  region : str = "na1",  filter : int = 567, member : discord.Member = None):
        print(str)
        region = region.lower()
        if member is None:
            member = ctx.message.author
        choices = {'euw': 'euw1', 'na': 'na1', 'kr' : 'kr'}
        choices2 = {5: [5], 56: [5,6], 567 : [5,6,7], 67 : [6,7], 57 : [5,7], 6 : [6], 7: [7], 4 : [4]}
        region = choices.get(region,'euw1')
        filter = choices2.get(filter,5)
        lamoom  = ""
        lamoom += ("Please wait for a moment<:mastery5:420493163778539522>")
        print(str)
        response = requests.get('https://{2}.api.riotgames.com/lol/summoner/v3/summoners/by-name/{0}?api_key={1}'.format(summoner_name, api, region), verify = True)
        time.sleep(1)
        data = json.loads(response.text)
        print(data)

        champion_response = requests.get("https://{2}.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/{0}?api_key={1}".format(data['id'], api,region))
        print(data)
        print(champion_response)
        lamoom += ("```Summoner Name: {} ```".format(data['name']))
        lamoom += ("```Summoner Level: {}```".format(data['summonerLevel']))
        await bot.send_message(member, lamoom)
        lamoom = ""
        data_Champ = json.loads(champion_response.text)
        static_champs = {'data': {'89': {'id': 89, 'key': 'Leona', 'name': 'Leona', 'title': 'the Radiant Dawn'}, '110': {'id': 110, 'key': 'Varus', 'name': 'Varus', 'title': 'the Arrow of Retribution'}, '111': {'id': 111, 'key': 'Nautilus', 'name': 'Nautilus', 'title': 'the Titan of the Depths'}, '112': {'id': 112, 'key': 'Viktor', 'name': 'Viktor', 'title': 'the Machine Herald'}, '113': {'id': 113, 'key': 'Sejuani', 'name': 'Sejuani', 'title': 'Fury of the North'}, '114': {'id': 114, 'key': 'Fiora', 'name': 'Fiora', 'title': 'the Grand Duelist'}, '236': {'id': 236, 'key': 'Lucian', 'name': 'Lucian', 'title': 'the Purifier'}, '115': {'id': 115, 'key': 'Ziggs', 'name': 'Ziggs', 'title': 'the Hexplosives Expert'}, '117': {'id': 117, 'key': 'Lulu', 'name': 'Lulu', 'title': 'the Fae Sorceress'}, '90': {'id': 90, 'key': 'Malzahar', 'name': 'Malzahar', 'title': 'the Prophet of the Void'}, '238': {'id': 238, 'key': 'Zed', 'name': 'Zed', 'title': 'the Master of Shadows'}, '91': {'id': 91, 'key': 'Talon', 'name': 'Talon', 'title': "the Blade's Shadow"}, '119': {'id': 119, 'key': 'Draven', 'name': 'Draven', 'title': 'the Glorious Executioner'}, '92': {'id': 92, 'key': 'Riven', 'name': 'Riven', 'title': 'the Exile'}, '516': {'id': 516, 'key': 'Ornn', 'name': 'Ornn', 'title': 'The Fire below the Mountain'}, '96': {'id': 96, 'key': 'KogMaw', 'name': "Kog'Maw", 'title': 'the Mouth of the Abyss'}, '10': {'id': 10, 'key': 'Kayle', 'name': 'Kayle', 'title': 'The Judicator'}, '98': {'id': 98, 'key': 'Shen', 'name': 'Shen', 'title': 'the Eye of Twilight'}, '99': {'id': 99, 'key': 'Lux', 'name': 'Lux', 'title': 'the Lady of Luminosity'}, '11': {'id': 11, 'key': 'MasterYi', 'name': 'Master Yi', 'title': 'the Wuju Bladesman'}, '12': {'id': 12, 'key': 'Alistar', 'name': 'Alistar', 'title': 'the Minotaur'}, '13': {'id': 13, 'key': 'Ryze', 'name': 'Ryze', 'title': 'the Rune Mage'}, '14': {'id': 14, 'key': 'Sion', 'name': 'Sion', 'title': 'The Undead Juggernaut'}, '15': {'id': 15, 'key': 'Sivir', 'name': 'Sivir', 'title': 'the Battle Mistress'}, '16': {'id': 16, 'key': 'Soraka', 'name': 'Soraka', 'title': 'the Starchild'}, '17': {'id': 17, 'key': 'Teemo', 'name': 'Teemo', 'title': 'the Swift Scout'}, '18': {'id': 18, 'key': 'Tristana', 'name': 'Tristana', 'title': 'the Yordle Gunner'}, '19': {'id': 19, 'key': 'Warwick', 'name': 'Warwick', 'title': 'the Uncaged Wrath of Zaun'}, '240': {'id': 240, 'key': 'Kled', 'name': 'Kled', 'title': 'the Cantankerous Cavalier'}, '120': {'id': 120, 'key': 'Hecarim', 'name': 'Hecarim', 'title': 'the Shadow of War'}, '121': {'id': 121, 'key': 'Khazix', 'name': "Kha'Zix", 'title': 'the Voidreaver'}, '1': {'id': 1, 'key': 'Annie', 'name': 'Annie', 'title': 'the Dark Child'}, '122': {'id': 122, 'key': 'Darius', 'name': 'Darius', 'title': 'the Hand of Noxus'}, '2': {'id': 2, 'key': 'Olaf', 'name': 'Olaf', 'title': 'the Berserker'}, '245': {'id': 245, 'key': 'Ekko', 'name': 'Ekko', 'title': 'the Boy Who Shattered Time'}, '3': {'id': 3, 'key': 'Galio', 'name': 'Galio', 'title': 'the Colossus'}, '4': {'id': 4, 'key': 'TwistedFate', 'name': 'Twisted Fate', 'title': 'the Card Master'}, '126': {'id': 126, 'key': 'Jayce', 'name': 'Jayce', 'title': 'the Defender of Tomorrow'}, '5': {'id': 5, 'key': 'XinZhao', 'name': 'Xin Zhao', 'title': 'the Seneschal of Demacia'}, '127': {'id': 127, 'key': 'Lissandra', 'name': 'Lissandra', 'title': 'the Ice Witch'}, '6': {'id': 6, 'key': 'Urgot', 'name': 'Urgot', 'title': 'the Dreadnought'}, '7': {'id': 7, 'key': 'Leblanc', 'name': 'LeBlanc', 'title': 'the Deceiver'}, '8': {'id': 8, 'key': 'Vladimir', 'name': 'Vladimir', 'title': 'the Crimson Reaper'}, '9': {'id': 9, 'key': 'Fiddlesticks', 'name': 'Fiddlesticks', 'title': 'the Harbinger of Doom'}, '20': {'id': 20, 'key': 'Nunu', 'name': 'Nunu', 'title': 'the Yeti Rider'}, '21': {'id': 21, 'key': 'MissFortune', 'name': 'Miss Fortune', 'title': 'the Bounty Hunter'}, '22': {'id': 22, 'key': 'Ashe', 'name': 'Ashe', 'title': 'the Frost Archer'}, '23': {'id': 23, 'key': 'Tryndamere', 'name': 'Tryndamere', 'title': 'the Barbarian King'}, '24': {'id': 24, 'key': 'Jax', 'name': 'Jax', 'title': 'Grandmaster at Arms'}, '25': {'id': 25, 'key': 'Morgana', 'name': 'Morgana', 'title': 'Fallen Angel'}, '26': {'id': 26, 'key': 'Zilean', 'name': 'Zilean', 'title': 'the Chronokeeper'}, '27': {'id': 27, 'key': 'Singed', 'name': 'Singed', 'title': 'the Mad Chemist'}, '28': {'id': 28, 'key': 'Evelynn', 'name': 'Evelynn', 'title': "Agony's Embrace"}, '29': {'id': 29, 'key': 'Twitch', 'name': 'Twitch', 'title': 'the Plague Rat'}, '131': {'id': 131, 'key': 'Diana', 'name': 'Diana', 'title': 'Scorn of the Moon'}, '133': {'id': 133, 'key': 'Quinn', 'name': 'Quinn', 'title': "Demacia's Wings"}, '254': {'id': 254, 'key': 'Vi', 'name': 'Vi', 'title': 'the Piltover Enforcer'}, '497': {'id': 497, 'key': 'Rakan', 'name': 'Rakan', 'title': 'The Charmer'}, '134': {'id': 134, 'key': 'Syndra', 'name': 'Syndra', 'title': 'the Dark Sovereign'}, '498': {'id': 498, 'key': 'Xayah', 'name': 'Xayah', 'title': 'the Rebel'}, '136': {'id': 136, 'key': 'AurelionSol', 'name': 'Aurelion Sol', 'title': 'The Star Forger'}, '412': {'id': 412, 'key': 'Thresh', 'name': 'Thresh', 'title': 'the Chain Warden'}, '30': {'id': 30, 'key': 'Karthus', 'name': 'Karthus', 'title': 'the Deathsinger'}, '31': {'id': 31, 'key': 'Chogath', 'name': "Cho'Gath", 'title': 'the Terror of the Void'}, '32': {'id': 32, 'key': 'Amumu', 'name': 'Amumu', 'title': 'the Sad Mummy'}, '33': {'id': 33, 'key': 'Rammus', 'name': 'Rammus', 'title': 'the Armordillo'}, '34': {'id': 34, 'key': 'Anivia', 'name': 'Anivia', 'title': 'the Cryophoenix'}, '35': {'id': 35, 'key': 'Shaco', 'name': 'Shaco', 'title': 'the Demon Jester'}, '36': {'id': 36, 'key': 'DrMundo', 'name': 'Dr. Mundo', 'title': 'the Madman of Zaun'}, '37': {'id': 37, 'key': 'Sona', 'name': 'Sona', 'title': 'Maven of the Strings'}, '38': {'id': 38, 'key': 'Kassadin', 'name': 'Kassadin', 'title': 'the Void Walker'}, '39': {'id': 39, 'key': 'Irelia', 'name': 'Irelia', 'title': 'the Will of the Blades'}, '141': {'id': 141, 'key': 'Kayn', 'name': 'Kayn', 'title': 'the Shadow Reaper'}, '142': {'id': 142, 'key': 'Zoe', 'name': 'Zoe', 'title': 'the Aspect of Twilight'}, '143': {'id': 143, 'key': 'Zyra', 'name': 'Zyra', 'title': 'Rise of the Thorns'}, '266': {'id': 266, 'key': 'Aatrox', 'name': 'Aatrox', 'title': 'the Darkin Blade'}, '420': {'id': 420, 'key': 'Illaoi', 'name': 'Illaoi', 'title': 'the Kraken Priestess'}, '267': {'id': 267, 'key': 'Nami', 'name': 'Nami', 'title': 'the Tidecaller'}, '421': {'id': 421, 'key': 'RekSai', 'name': "Rek'Sai", 'title': 'the Void Burrower'}, '268': {'id': 268, 'key': 'Azir', 'name': 'Azir', 'title': 'the Emperor of the Sands'}, '427': {'id': 427, 'key': 'Ivern', 'name': 'Ivern', 'title': 'the Green Father'}, '429': {'id': 429, 'key': 'Kalista', 'name': 'Kalista', 'title': 'the Spear of Vengeance'}, '40': {'id': 40, 'key': 'Janna', 'name': 'Janna', 'title': "the Storm's Fury"}, '41': {'id': 41, 'key': 'Gangplank', 'name': 'Gangplank', 'title': 'the Saltwater Scourge'}, '42': {'id': 42, 'key': 'Corki', 'name': 'Corki', 'title': 'the Daring Bombardier'}, '43': {'id': 43, 'key': 'Karma', 'name': 'Karma', 'title': 'the Enlightened One'}, '44': {'id': 44, 'key': 'Taric', 'name': 'Taric', 'title': 'the Shield of Valoran'}, '45': {'id': 45, 'key': 'Veigar', 'name': 'Veigar', 'title': 'the Tiny Master of Evil'}, '48': {'id': 48, 'key': 'Trundle', 'name': 'Trundle', 'title': 'the Troll King'}, '150': {'id': 150, 'key': 'Gnar', 'name': 'Gnar', 'title': 'the Missing Link'}, '154': {'id': 154, 'key': 'Zac', 'name': 'Zac', 'title': 'the Secret Weapon'}, '432': {'id': 432, 'key': 'Bard', 'name': 'Bard', 'title': 'the Wandering Caretaker'}, '157': {'id': 157, 'key': 'Yasuo', 'name': 'Yasuo', 'title': 'the Unforgiven'}, '50': {'id': 50, 'key': 'Swain', 'name': 'Swain', 'title': 'the Noxian Grand General'}, '51': {'id': 51, 'key': 'Caitlyn', 'name': 'Caitlyn', 'title': 'the Sheriff of Piltover'}, '53': {'id': 53, 'key': 'Blitzcrank', 'name': 'Blitzcrank', 'title': 'the Great Steam Golem'}, '54': {'id': 54, 'key': 'Malphite', 'name': 'Malphite', 'title': 'Shard of the Monolith'}, '55': {'id': 55, 'key': 'Katarina', 'name': 'Katarina', 'title': 'the Sinister Blade'}, '56': {'id': 56, 'key': 'Nocturne', 'name': 'Nocturne', 'title': 'the Eternal Nightmare'}, '57': {'id': 57, 'key': 'Maokai', 'name': 'Maokai', 'title': 'the Twisted Treant'}, '58': {'id': 58, 'key': 'Renekton', 'name': 'Renekton', 'title': 'the Butcher of the Sands'}, '59': {'id': 59, 'key': 'JarvanIV', 'name': 'Jarvan IV', 'title': 'the Exemplar of Demacia'}, '161': {'id': 161, 'key': 'Velkoz', 'name': "Vel'Koz", 'title': 'the Eye of the Void'}, '163': {'id': 163, 'key': 'Taliyah', 'name': 'Taliyah', 'title': 'the Stoneweaver'}, '164': {'id': 164, 'key': 'Camille', 'name': 'Camille', 'title': 'the Steel Shadow'}, '201': {'id': 201, 'key': 'Braum', 'name': 'Braum', 'title': 'the Heart of the Freljord'}, '202': {'id': 202, 'key': 'Jhin', 'name': 'Jhin', 'title': 'the Virtuoso'}, '203': {'id': 203, 'key': 'Kindred', 'name': 'Kindred', 'title': 'The Eternal Hunters'}, '60': {'id': 60, 'key': 'Elise', 'name': 'Elise', 'title': 'the Spider Queen'}, '61': {'id': 61, 'key': 'Orianna', 'name': 'Orianna', 'title': 'the Lady of Clockwork'}, '62': {'id': 62, 'key': 'MonkeyKing', 'name': 'Wukong', 'title': 'the Monkey King'}, '63': {'id': 63, 'key': 'Brand', 'name': 'Brand', 'title': 'the Burning Vengeance'}, '64': {'id': 64, 'key': 'LeeSin', 'name': 'Lee Sin', 'title': 'the Blind Monk'}, '67': {'id': 67, 'key': 'Vayne', 'name': 'Vayne', 'title': 'the Night Hunter'}, '68': {'id': 68, 'key': 'Rumble', 'name': 'Rumble', 'title': 'the Mechanized Menace'}, '69': {'id': 69, 'key': 'Cassiopeia', 'name': 'Cassiopeia', 'title': "the Serpent's Embrace"}, '72': {'id': 72, 'key': 'Skarner', 'name': 'Skarner', 'title': 'the Crystal Vanguard'}, '74': {'id': 74, 'key': 'Heimerdinger', 'name': 'Heimerdinger', 'title': 'the Revered Inventor'}, '75': {'id': 75, 'key': 'Nasus', 'name': 'Nasus', 'title': 'the Curator of the Sands'}, '76': {'id': 76, 'key': 'Nidalee', 'name': 'Nidalee', 'title': 'the Bestial Huntress'}, '77': {'id': 77, 'key': 'Udyr', 'name': 'Udyr', 'title': 'the Spirit Walker'}, '78': {'id': 78, 'key': 'Poppy', 'name': 'Poppy', 'title': 'Keeper of the Hammer'}, '79': {'id': 79, 'key': 'Gragas', 'name': 'Gragas', 'title': 'the Rabble Rouser'}, '222': {'id': 222, 'key': 'Jinx', 'name': 'Jinx', 'title': 'the Loose Cannon'}, '101': {'id': 101, 'key': 'Xerath', 'name': 'Xerath', 'title': 'the Magus Ascendant'}, '102': {'id': 102, 'key': 'Shyvana', 'name': 'Shyvana', 'title': 'the Half-Dragon'}, '223': {'id': 223, 'key': 'TahmKench', 'name': 'Tahm Kench', 'title': 'the River King'}, '103': {'id': 103, 'key': 'Ahri', 'name': 'Ahri', 'title': 'the Nine-Tailed Fox'}, '104': {'id': 104, 'key': 'Graves', 'name': 'Graves', 'title': 'the Outlaw'}, '105': {'id': 105, 'key': 'Fizz', 'name': 'Fizz', 'title': 'the Tidal Trickster'}, '106': {'id': 106, 'key': 'Volibear', 'name': 'Volibear', 'title': "the Thunder's Roar"}, '80': {'id': 80, 'key': 'Pantheon', 'name': 'Pantheon', 'title': 'the Artisan of War'}, '107': {'id': 107, 'key': 'Rengar', 'name': 'Rengar', 'title': 'the Pridestalker'}, '81': {'id': 81, 'key': 'Ezreal', 'name': 'Ezreal', 'title': 'the Prodigal Explorer'}, '82': {'id': 82, 'key': 'Mordekaiser', 'name': 'Mordekaiser', 'title': 'the Iron Revenant'}, '83': {'id': 83, 'key': 'Yorick', 'name': 'Yorick', 'title': 'Shepherd of Souls'}, '84': {'id': 84, 'key': 'Akali', 'name': 'Akali', 'title': 'the Fist of Shadow'}, '85': {'id': 85, 'key': 'Kennen', 'name': 'Kennen', 'title': 'the Heart of the Tempest'}, '86': {'id': 86, 'key': 'Garen', 'name': 'Garen', 'title': 'The Might of Demacia'}}, 'type': 'champion', 'version': '8.4.1'}
        master = 5
        print(static_champs)
        data_Champ = sorted(data_Champ, key = lambda level :  level['championLevel'])
        for idx,champ in enumerate(data_Champ):
            if(data_Champ[idx]['championLevel'] in filter):


                if(data_Champ[idx]['championLevel'] != filter[0] and data_Champ[idx-1]['championLevel'] != data_Champ[idx]['championLevel']):
                    if(lamoom != ""):
                      x = await bot.send_message(member, lamoom)
                      await bot.add_reaction(x, mastery_emotes.get(data_Champ[idx-1]['championLevel']))
                    lamoom = ""

                else:
                    lamoom += "```\n {0} {2}: {1}       ```".format(static_champs['data'][str(data_Champ[idx]['championId'])]['name'],data_Champ[idx]['championPoints'],data_Champ[idx]['championLevel'])
        x = await bot.send_message(member, lamoom)
        await bot.add_reaction(x, mastery_emotes.get(data_Champ[idx - 1]['championLevel']))


@bot.command(pass_context=True)
async def hextech(ctx, summ : str,region : str, member : discord.Member = None):
    print(str)
    region = region.lower()
    if member is None:
        member = ctx.message.author
    choices = {'euw': 'euw1', 'na': 'na1', 'kr': 'kr'}
    region = choices.get(region, 'euw1')
    lamoom = ""
    lamoom += ("Please wait for a moment")
    print(str)
    response = requests.get('https://{2}.api.riotgames.com/lol/summoner/v3/summoners/by-name/{0}?api_key={1}'.format(summ, api,region), verify=True)
    data = json.loads(response.text)
    champion_response = requests.get(
        "https://{2}.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/{0}?api_key={1}".format(
            data['id'], api, region))
    lamoom += ("```Summoner Name: {} ```".format(data['name']))
    lamoom += ("```Summoner Level: {}```".format(data['summonerLevel']))
    await bot.send_message(member, lamoom)
    lamoom = ""
    data_Champ = json.loads(champion_response.text)
    static_champs = {'data': {'89': {'id': 89, 'key': 'Leona', 'name': 'Leona', 'title': 'the Radiant Dawn'},
                              '110': {'id': 110, 'key': 'Varus', 'name': 'Varus', 'title': 'the Arrow of Retribution'},
                              '111': {'id': 111, 'key': 'Nautilus', 'name': 'Nautilus',
                                      'title': 'the Titan of the Depths'},
                              '112': {'id': 112, 'key': 'Viktor', 'name': 'Viktor', 'title': 'the Machine Herald'},
                              '113': {'id': 113, 'key': 'Sejuani', 'name': 'Sejuani', 'title': 'Fury of the North'},
                              '114': {'id': 114, 'key': 'Fiora', 'name': 'Fiora', 'title': 'the Grand Duelist'},
                              '236': {'id': 236, 'key': 'Lucian', 'name': 'Lucian', 'title': 'the Purifier'},
                              '115': {'id': 115, 'key': 'Ziggs', 'name': 'Ziggs', 'title': 'the Hexplosives Expert'},
                              '117': {'id': 117, 'key': 'Lulu', 'name': 'Lulu', 'title': 'the Fae Sorceress'},
                              '90': {'id': 90, 'key': 'Malzahar', 'name': 'Malzahar',
                                     'title': 'the Prophet of the Void'},
                              '238': {'id': 238, 'key': 'Zed', 'name': 'Zed', 'title': 'the Master of Shadows'},
                              '91': {'id': 91, 'key': 'Talon', 'name': 'Talon', 'title': "the Blade's Shadow"},
                              '119': {'id': 119, 'key': 'Draven', 'name': 'Draven',
                                      'title': 'the Glorious Executioner'},
                              '92': {'id': 92, 'key': 'Riven', 'name': 'Riven', 'title': 'the Exile'},
                              '516': {'id': 516, 'key': 'Ornn', 'name': 'Ornn', 'title': 'The Fire below the Mountain'},
                              '96': {'id': 96, 'key': 'KogMaw', 'name': "Kog'Maw", 'title': 'the Mouth of the Abyss'},
                              '10': {'id': 10, 'key': 'Kayle', 'name': 'Kayle', 'title': 'The Judicator'},
                              '98': {'id': 98, 'key': 'Shen', 'name': 'Shen', 'title': 'the Eye of Twilight'},
                              '99': {'id': 99, 'key': 'Lux', 'name': 'Lux', 'title': 'the Lady of Luminosity'},
                              '11': {'id': 11, 'key': 'MasterYi', 'name': 'Master Yi', 'title': 'the Wuju Bladesman'},
                              '12': {'id': 12, 'key': 'Alistar', 'name': 'Alistar', 'title': 'the Minotaur'},
                              '13': {'id': 13, 'key': 'Ryze', 'name': 'Ryze', 'title': 'the Rune Mage'},
                              '14': {'id': 14, 'key': 'Sion', 'name': 'Sion', 'title': 'The Undead Juggernaut'},
                              '15': {'id': 15, 'key': 'Sivir', 'name': 'Sivir', 'title': 'the Battle Mistress'},
                              '16': {'id': 16, 'key': 'Soraka', 'name': 'Soraka', 'title': 'the Starchild'},
                              '17': {'id': 17, 'key': 'Teemo', 'name': 'Teemo', 'title': 'the Swift Scout'},
                              '18': {'id': 18, 'key': 'Tristana', 'name': 'Tristana', 'title': 'the Yordle Gunner'},
                              '19': {'id': 19, 'key': 'Warwick', 'name': 'Warwick',
                                     'title': 'the Uncaged Wrath of Zaun'},
                              '240': {'id': 240, 'key': 'Kled', 'name': 'Kled', 'title': 'the Cantankerous Cavalier'},
                              '120': {'id': 120, 'key': 'Hecarim', 'name': 'Hecarim', 'title': 'the Shadow of War'},
                              '121': {'id': 121, 'key': 'Khazix', 'name': "Kha'Zix", 'title': 'the Voidreaver'},
                              '1': {'id': 1, 'key': 'Annie', 'name': 'Annie', 'title': 'the Dark Child'},
                              '122': {'id': 122, 'key': 'Darius', 'name': 'Darius', 'title': 'the Hand of Noxus'},
                              '2': {'id': 2, 'key': 'Olaf', 'name': 'Olaf', 'title': 'the Berserker'},
                              '245': {'id': 245, 'key': 'Ekko', 'name': 'Ekko', 'title': 'the Boy Who Shattered Time'},
                              '3': {'id': 3, 'key': 'Galio', 'name': 'Galio', 'title': 'the Colossus'},
                              '4': {'id': 4, 'key': 'TwistedFate', 'name': 'Twisted Fate', 'title': 'the Card Master'},
                              '126': {'id': 126, 'key': 'Jayce', 'name': 'Jayce', 'title': 'the Defender of Tomorrow'},
                              '5': {'id': 5, 'key': 'XinZhao', 'name': 'Xin Zhao', 'title': 'the Seneschal of Demacia'},
                              '127': {'id': 127, 'key': 'Lissandra', 'name': 'Lissandra', 'title': 'the Ice Witch'},
                              '6': {'id': 6, 'key': 'Urgot', 'name': 'Urgot', 'title': 'the Dreadnought'},
                              '7': {'id': 7, 'key': 'Leblanc', 'name': 'LeBlanc', 'title': 'the Deceiver'},
                              '8': {'id': 8, 'key': 'Vladimir', 'name': 'Vladimir', 'title': 'the Crimson Reaper'},
                              '9': {'id': 9, 'key': 'Fiddlesticks', 'name': 'Fiddlesticks',
                                    'title': 'the Harbinger of Doom'},
                              '20': {'id': 20, 'key': 'Nunu', 'name': 'Nunu', 'title': 'the Yeti Rider'},
                              '21': {'id': 21, 'key': 'MissFortune', 'name': 'Miss Fortune',
                                     'title': 'the Bounty Hunter'},
                              '22': {'id': 22, 'key': 'Ashe', 'name': 'Ashe', 'title': 'the Frost Archer'},
                              '23': {'id': 23, 'key': 'Tryndamere', 'name': 'Tryndamere',
                                     'title': 'the Barbarian King'},
                              '24': {'id': 24, 'key': 'Jax', 'name': 'Jax', 'title': 'Grandmaster at Arms'},
                              '25': {'id': 25, 'key': 'Morgana', 'name': 'Morgana', 'title': 'Fallen Angel'},
                              '26': {'id': 26, 'key': 'Zilean', 'name': 'Zilean', 'title': 'the Chronokeeper'},
                              '27': {'id': 27, 'key': 'Singed', 'name': 'Singed', 'title': 'the Mad Chemist'},
                              '28': {'id': 28, 'key': 'Evelynn', 'name': 'Evelynn', 'title': "Agony's Embrace"},
                              '29': {'id': 29, 'key': 'Twitch', 'name': 'Twitch', 'title': 'the Plague Rat'},
                              '131': {'id': 131, 'key': 'Diana', 'name': 'Diana', 'title': 'Scorn of the Moon'},
                              '133': {'id': 133, 'key': 'Quinn', 'name': 'Quinn', 'title': "Demacia's Wings"},
                              '254': {'id': 254, 'key': 'Vi', 'name': 'Vi', 'title': 'the Piltover Enforcer'},
                              '497': {'id': 497, 'key': 'Rakan', 'name': 'Rakan', 'title': 'The Charmer'},
                              '134': {'id': 134, 'key': 'Syndra', 'name': 'Syndra', 'title': 'the Dark Sovereign'},
                              '498': {'id': 498, 'key': 'Xayah', 'name': 'Xayah', 'title': 'the Rebel'},
                              '136': {'id': 136, 'key': 'AurelionSol', 'name': 'Aurelion Sol',
                                      'title': 'The Star Forger'},
                              '412': {'id': 412, 'key': 'Thresh', 'name': 'Thresh', 'title': 'the Chain Warden'},
                              '30': {'id': 30, 'key': 'Karthus', 'name': 'Karthus', 'title': 'the Deathsinger'},
                              '31': {'id': 31, 'key': 'Chogath', 'name': "Cho'Gath", 'title': 'the Terror of the Void'},
                              '32': {'id': 32, 'key': 'Amumu', 'name': 'Amumu', 'title': 'the Sad Mummy'},
                              '33': {'id': 33, 'key': 'Rammus', 'name': 'Rammus', 'title': 'the Armordillo'},
                              '34': {'id': 34, 'key': 'Anivia', 'name': 'Anivia', 'title': 'the Cryophoenix'},
                              '35': {'id': 35, 'key': 'Shaco', 'name': 'Shaco', 'title': 'the Demon Jester'},
                              '36': {'id': 36, 'key': 'DrMundo', 'name': 'Dr. Mundo', 'title': 'the Madman of Zaun'},
                              '37': {'id': 37, 'key': 'Sona', 'name': 'Sona', 'title': 'Maven of the Strings'},
                              '38': {'id': 38, 'key': 'Kassadin', 'name': 'Kassadin', 'title': 'the Void Walker'},
                              '39': {'id': 39, 'key': 'Irelia', 'name': 'Irelia', 'title': 'the Will of the Blades'},
                              '141': {'id': 141, 'key': 'Kayn', 'name': 'Kayn', 'title': 'the Shadow Reaper'},
                              '142': {'id': 142, 'key': 'Zoe', 'name': 'Zoe', 'title': 'the Aspect of Twilight'},
                              '143': {'id': 143, 'key': 'Zyra', 'name': 'Zyra', 'title': 'Rise of the Thorns'},
                              '266': {'id': 266, 'key': 'Aatrox', 'name': 'Aatrox', 'title': 'the Darkin Blade'},
                              '420': {'id': 420, 'key': 'Illaoi', 'name': 'Illaoi', 'title': 'the Kraken Priestess'},
                              '267': {'id': 267, 'key': 'Nami', 'name': 'Nami', 'title': 'the Tidecaller'},
                              '421': {'id': 421, 'key': 'RekSai', 'name': "Rek'Sai", 'title': 'the Void Burrower'},
                              '268': {'id': 268, 'key': 'Azir', 'name': 'Azir', 'title': 'the Emperor of the Sands'},
                              '427': {'id': 427, 'key': 'Ivern', 'name': 'Ivern', 'title': 'the Green Father'},
                              '429': {'id': 429, 'key': 'Kalista', 'name': 'Kalista',
                                      'title': 'the Spear of Vengeance'},
                              '40': {'id': 40, 'key': 'Janna', 'name': 'Janna', 'title': "the Storm's Fury"},
                              '41': {'id': 41, 'key': 'Gangplank', 'name': 'Gangplank',
                                     'title': 'the Saltwater Scourge'},
                              '42': {'id': 42, 'key': 'Corki', 'name': 'Corki', 'title': 'the Daring Bombardier'},
                              '43': {'id': 43, 'key': 'Karma', 'name': 'Karma', 'title': 'the Enlightened One'},
                              '44': {'id': 44, 'key': 'Taric', 'name': 'Taric', 'title': 'the Shield of Valoran'},
                              '45': {'id': 45, 'key': 'Veigar', 'name': 'Veigar', 'title': 'the Tiny Master of Evil'},
                              '48': {'id': 48, 'key': 'Trundle', 'name': 'Trundle', 'title': 'the Troll King'},
                              '150': {'id': 150, 'key': 'Gnar', 'name': 'Gnar', 'title': 'the Missing Link'},
                              '154': {'id': 154, 'key': 'Zac', 'name': 'Zac', 'title': 'the Secret Weapon'},
                              '432': {'id': 432, 'key': 'Bard', 'name': 'Bard', 'title': 'the Wandering Caretaker'},
                              '157': {'id': 157, 'key': 'Yasuo', 'name': 'Yasuo', 'title': 'the Unforgiven'},
                              '50': {'id': 50, 'key': 'Swain', 'name': 'Swain', 'title': 'the Noxian Grand General'},
                              '51': {'id': 51, 'key': 'Caitlyn', 'name': 'Caitlyn', 'title': 'the Sheriff of Piltover'},
                              '53': {'id': 53, 'key': 'Blitzcrank', 'name': 'Blitzcrank',
                                     'title': 'the Great Steam Golem'},
                              '54': {'id': 54, 'key': 'Malphite', 'name': 'Malphite', 'title': 'Shard of the Monolith'},
                              '55': {'id': 55, 'key': 'Katarina', 'name': 'Katarina', 'title': 'the Sinister Blade'},
                              '56': {'id': 56, 'key': 'Nocturne', 'name': 'Nocturne', 'title': 'the Eternal Nightmare'},
                              '57': {'id': 57, 'key': 'Maokai', 'name': 'Maokai', 'title': 'the Twisted Treant'},
                              '58': {'id': 58, 'key': 'Renekton', 'name': 'Renekton',
                                     'title': 'the Butcher of the Sands'},
                              '59': {'id': 59, 'key': 'JarvanIV', 'name': 'Jarvan IV',
                                     'title': 'the Exemplar of Demacia'},
                              '161': {'id': 161, 'key': 'Velkoz', 'name': "Vel'Koz", 'title': 'the Eye of the Void'},
                              '163': {'id': 163, 'key': 'Taliyah', 'name': 'Taliyah', 'title': 'the Stoneweaver'},
                              '164': {'id': 164, 'key': 'Camille', 'name': 'Camille', 'title': 'the Steel Shadow'},
                              '201': {'id': 201, 'key': 'Braum', 'name': 'Braum', 'title': 'the Heart of the Freljord'},
                              '202': {'id': 202, 'key': 'Jhin', 'name': 'Jhin', 'title': 'the Virtuoso'},
                              '203': {'id': 203, 'key': 'Kindred', 'name': 'Kindred', 'title': 'The Eternal Hunters'},
                              '60': {'id': 60, 'key': 'Elise', 'name': 'Elise', 'title': 'the Spider Queen'},
                              '61': {'id': 61, 'key': 'Orianna', 'name': 'Orianna', 'title': 'the Lady of Clockwork'},
                              '62': {'id': 62, 'key': 'MonkeyKing', 'name': 'Wukong', 'title': 'the Monkey King'},
                              '63': {'id': 63, 'key': 'Brand', 'name': 'Brand', 'title': 'the Burning Vengeance'},
                              '64': {'id': 64, 'key': 'LeeSin', 'name': 'Lee Sin', 'title': 'the Blind Monk'},
                              '67': {'id': 67, 'key': 'Vayne', 'name': 'Vayne', 'title': 'the Night Hunter'},
                              '68': {'id': 68, 'key': 'Rumble', 'name': 'Rumble', 'title': 'the Mechanized Menace'},
                              '69': {'id': 69, 'key': 'Cassiopeia', 'name': 'Cassiopeia',
                                     'title': "the Serpent's Embrace"},
                              '72': {'id': 72, 'key': 'Skarner', 'name': 'Skarner', 'title': 'the Crystal Vanguard'},
                              '74': {'id': 74, 'key': 'Heimerdinger', 'name': 'Heimerdinger',
                                     'title': 'the Revered Inventor'},
                              '75': {'id': 75, 'key': 'Nasus', 'name': 'Nasus', 'title': 'the Curator of the Sands'},
                              '76': {'id': 76, 'key': 'Nidalee', 'name': 'Nidalee', 'title': 'the Bestial Huntress'},
                              '77': {'id': 77, 'key': 'Udyr', 'name': 'Udyr', 'title': 'the Spirit Walker'},
                              '78': {'id': 78, 'key': 'Poppy', 'name': 'Poppy', 'title': 'Keeper of the Hammer'},
                              '79': {'id': 79, 'key': 'Gragas', 'name': 'Gragas', 'title': 'the Rabble Rouser'},
                              '222': {'id': 222, 'key': 'Jinx', 'name': 'Jinx', 'title': 'the Loose Cannon'},
                              '101': {'id': 101, 'key': 'Xerath', 'name': 'Xerath', 'title': 'the Magus Ascendant'},
                              '102': {'id': 102, 'key': 'Shyvana', 'name': 'Shyvana', 'title': 'the Half-Dragon'},
                              '223': {'id': 223, 'key': 'TahmKench', 'name': 'Tahm Kench', 'title': 'the River King'},
                              '103': {'id': 103, 'key': 'Ahri', 'name': 'Ahri', 'title': 'the Nine-Tailed Fox'},
                              '104': {'id': 104, 'key': 'Graves', 'name': 'Graves', 'title': 'the Outlaw'},
                              '105': {'id': 105, 'key': 'Fizz', 'name': 'Fizz', 'title': 'the Tidal Trickster'},
                              '106': {'id': 106, 'key': 'Volibear', 'name': 'Volibear', 'title': "the Thunder's Roar"},
                              '80': {'id': 80, 'key': 'Pantheon', 'name': 'Pantheon', 'title': 'the Artisan of War'},
                              '107': {'id': 107, 'key': 'Rengar', 'name': 'Rengar', 'title': 'the Pridestalker'},
                              '81': {'id': 81, 'key': 'Ezreal', 'name': 'Ezreal', 'title': 'the Prodigal Explorer'},
                              '82': {'id': 82, 'key': 'Mordekaiser', 'name': 'Mordekaiser',
                                     'title': 'the Iron Revenant'},
                              '83': {'id': 83, 'key': 'Yorick', 'name': 'Yorick', 'title': 'Shepherd of Souls'},
                              '84': {'id': 84, 'key': 'Akali', 'name': 'Akali', 'title': 'the Fist of Shadow'},
                              '85': {'id': 85, 'key': 'Kennen', 'name': 'Kennen', 'title': 'the Heart of the Tempest'},
                              '86': {'id': 86, 'key': 'Garen', 'name': 'Garen', 'title': 'The Might of Demacia'}},
                     'type': 'champion', 'version': '8.4.1'}
    print(static_champs)
    data_Champ = sorted(data_Champ, key=lambda level: level['championPoints'])
    for idx, champ in enumerate(data_Champ):
        if(data_Champ[idx]['chestGranted'] == False):
            if(lamoom.__len__()>2000):
                x = await bot.send_message(member, lamoom)
            lamoom += "```\n {0}```".format(static_champs['data'][str(data_Champ[idx]['championId'])]['name'])
    x = await bot.send_message(member, lamoom)
bot.loop.create_task(hunger_task())
bot.loop.create_task(age_task())
bot.run(TOKEN)
