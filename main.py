
import asyncio
import sys

import discord
from discord.ext import commands, tasks

import ast
import os
import requests
import signal
import random
import time

import httplist

owners = [401849772157435905, 876488885419520020] # Owner account IDs


with open('token.txt', 'r') as f:
    bottoken = f.readline().strip()

totalmessages = 0


with open('userdata.txt', 'r') as f:
    userdata = ast.literal_eval(f.read())


def save_all():
    with open('userdata.txt', 'w') as f:
        f.write(repr(userdata))


def timeout_handler(signal, frame):
    print(f'BOT: Timeout! Saving data and exiting...')
    save_all()
    sys.exit(0)


signal.signal(signal.SIGALRM, timeout_handler)



intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '%', help_command=None, intents=intents) #Makes the bot prefix.

    # https://discord.com/api/oauth2/authorize?client_id=1079242361491693658&permissions=8&scope=applications.commands%20bot

class LeaderBoardPosition:
    def __init__(self, user, xp):
        self.user = user
        self.xp = xp

@client.event
async def on_ready():
    print("========")
    print(f"current UNIX time is {time.time()}.")
    print("========")
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('========')


@client.event
async def on_message(message):
    global totalmessages
    if message.author.id not in userdata.keys():
        userdata[message.author.id] = {'xp': 0, 'time': -1, 'money': 0, 'inventory': []}
    if userdata[message.author.id]['time'] + 30 < time.time():
        userdata[message.author.id]['time'] = time.time()
        userdata[message.author.id]['xp'] += random.randint(5, 10)
    totalmessages += 1

    save_all()

    await client.process_commands(message)

#@client.command()
#async def getmoney(ctx): # TODO: Show current amount of money the user has

#@client.command()
#async def convert(ctx, xp): # TODO: Convert XP to money at a rate of $1 for every 100 XP

#@client.command()
#async def give(ctx, money, item = 0, amount = 0): # TODO: Give some amount of money, between players, as well as items

    


@client.command()
async def shell(ctx,cmd):
    if ctx.author.id in owners:
       out = os.popen(str(cmd))
       try:
           await ctx.send(str(out.read()))
       except:
          os.system(cmd)


@client.command()
async def awardxp(ctx, user: discord.User, amount = 0):
    if ctx.message.author.id in owners:
        if user.id not in userdata:
            userdata[user.id] = {'xp': 0, 'time': -1}
        userdata[user.id]['xp'] += amount
        await ctx.send(f'Gave {user.mention} {amount} XP!')
    
    
  
@client.command()
async def links(ctx):
    embed = discord.Embed(title="Links", description="", color=0xFF0000)
    embed.add_field(name="README", value="This bot is for development! Don't use me!")

    await ctx.send(embed=embed)


@client.command()
async def getxp(ctx, user: discord.User = None):
    user = ctx.author if not user else user
    if user.id not in userdata:
        await ctx.send(f'{user.mention} has 0 XP!')
    await ctx.send(f'{user.mention} has {userdata[user.id]["xp"]} XP!')


@client.command()
async def getleaderboard(ctx):
    leaderboards = []
    for key in userdata:
        leaderboards.append(LeaderBoardPosition(key, userdata[key]['xp']))
    top = sorted(leaderboards, key=lambda x: x.xp, reverse=True)
    text = ''
    for i in range(0, 6):
        try:
            text += f'{i + 1}. {client.get_user(top[i].user)} - {top[i].xp} XP\n'
        except IndexError:
            break
    embed = discord.Embed(title=text, description="Top 6 XP counts!", color=0xFF0000)
    await ctx.send(embed=embed)
    
    

@client.command()
async def help(ctx):
   
  

    embed = discord.Embed(title="help", description="", color=0xFF0000)#Declaring the help command is an embed.

    

    embed.add_field(name="README", value="This bot is for development! Don't use me!")



    await ctx.send(embed=embed)#sends the embed.


@client.command()
async def serverstatus(ctx):
    text = ["Checking 3 site(s)\n", "Note: This may or may not be accurate. Do not trust these results.\n",
            "*https://taskjourney.org:449*\n"]
    code = urlcheck("https://taskjourney.org:449/")
    if code != 200:
        text.append("The server sent an abnormal response. If it's 301 or 302, the server redirected the bot. If it's not those, the server might be down. The HTTP code sent was: {http}. ({phrase})\n".format(http=str(code), phrase=httplist[code]))
    else:
        text.append("The server is currently up. (It sent a response code of 200 OK)\n")
        text.append("If your game is frozen, it's most likely that the client froze or crashed. The game is still relatively unstable, you'll have to reload the game.\n")
        code = urlcheck("https://survivreloaded.com/")
    text.append("*https://survivreloaded.com/*\n")
    code = urlcheck("https://survivreloaded.com/")
    if code != 200:
        text.append("The server sent an abnormal response. If it's 301 or 302, the server redirected the bot. If it's not those, the server might be down. The HTTP code sent was: {http}. ({phrase})\n".format(http=str(code), phrase=httplist[code]))
    else:
        text.append("The server is currently up. (It sent a response code of 200 OK)\n")
        text.append("If your game is frozen, it's most likely that the client froze or crashed. The game is still relatively unstable, you'll have to reload the game.\n")  
    code = urlcheck("https://resurviv.io/")
    text.append("*https://resurviv.io/*\n")
    if code != 200:
        text.append("The server sent an abnormal response. If it's 301 or 302, the server redirected the bot. If it's not those, the server might be down. The HTTP code sent was: {http}. ({phrase})\n".format(http=str(code), phrase=httplist[code]))
    else:
        text.append("The server is currently up. (It sent a response code of 200 OK)\n")
        text.append("If your game is frozen, it's most likely that the client froze or crashed. The game is still relatively unstable, you'll have to reload the game.\n")
    embed = discord.Embed(title="Surviv Reloaded Status", description=''.join(text), color=0x00FF00)
    await ctx.send(embed=embed)


@client.command()
async def checkurl(ctx,site):
    code = urlcheck(site)
    if code != 200:
        await ctx.send("The server is currently down or unresponsive. The HTTP code sent was: {http}. ({phrase})".format(http=str(code), phrase=httplist[code]))
    else:
        await ctx.send("The server is currently up. (It sent a response code of 200 OK)")

@client.command()
async def resetbot(ctx):
    if ctx.message.author.id in owners:
        await ctx.send("Bot is reloading, please wait a few seconds before sending commands.")
        exit()
    else:
        await ctx.send("hey, wait a minute, you're not the owner! you can't do that! >:(")        

@client.command()
async def ownersonly(ctx):
    if ctx.message.author.id in owners:
        await ctx.send("You are the owner of this application.")
        exit()
    else:
        await ctx.send("You're not the owner of this application.")         
        
        
def urlcheck(url):
    signal.alarm(httplist.TIMEOUT)
    try:
        r = requests.head(url, timeout=3)
        return r.status_code
    except:
        return 999

@tasks.loop(minutes=10)
async def save():
    save_all()



save.start()
client.run(bottoken)
