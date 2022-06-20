import asyncio
import datetime
import json
import os

import discord
from discord.ext import commands, tasks
from discord.utils import get

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
botinfo = json.load(open('config.json'))

prefix = botinfo.get('Prefix')
bot = commands.Bot(command_prefix=prefix, intents = intents, case_insensitive=True)
botinfo = json.load(open('config.json'))
token = botinfo.get('Token')
bot.remove_command("help")





async def main():
    async with bot:
        for filepy in os.listdir("./cogs"):
            if filepy.endswith(".py"):
                await bot.load_extension("cogs." + filepy[:-3])
        await bot.start(token)




@tasks.loop(seconds=1)
async def updatesubscription():
    with open('authedpeople.json', 'r') as file:
        info = json.load(file)
    try:
        for element in list(info):
            if info[str(element)]['TimeLeft'] == 0:
                guild = bot.get_guild(987271164009267200)
                role = get(guild.roles, name="Premium")
                member = int(element)
                member2 = guild.get_member(member)
                await member2.remove_roles(role)
                info.pop(element)
                print(f"Removed Member {member2} Successfully")
            elif info[str(element)]['TimeLeft'] > 0:
                info[str(element)]['TimeLeft'] -= 1
    except TypeError:
        pass
    with open('authedpeople.json', 'w') as f:
        json.dump(info, f, indent=3)
@bot.event
async def on_ready():
    try:
        with open('config.json', 'r') as f:
            cfg = json.load(f)
            logch = cfg["notificationChannel"]
            onlnch = bot.get_channel(int(logch))
            today = datetime.datetime.now()
            date_time = today.strftime("%m/%d/%Y, %H:%M:%S")
            await onlnch.send(f"Back online, {date_time}")

    except:
        print(f"No notification channel set {bot.user}")
    updatesubscription.start()





@bot.command()
async def help(ctx, command = None):
   if command is None:
    gencmds = []
    admincmds = []
    modcmds = []
    ew = bot.get_cog("GenCommands")
    ew2 = bot.get_cog("AdminCommands")
    ewi2 = ew2.get_commands()
    ewi = ew.get_commands()
    ew3 = bot.get_cog("ModCommands")
    ew33 = ew3.get_commands()
    for commandname in ewi:
        gencmds.append(prefix + commandname.name)
    for commandname2 in ewi2:
        admincmds.append(prefix + commandname2.name)
    for commandnam3 in ew33:
        modcmds.append(prefix + commandnam3.name)

    embed = discord.Embed(title="Help Command", description="Commands to Use!", colour=discord.Colour.random())
    embed.add_field(name="Admin Commands", value="\n".join(admincmds))
    embed.add_field(name=chr(173), value=chr(173))
    embed.add_field(name=chr(173), value=chr(173))
    embed.add_field(name="User Commands", value="\n".join(gencmds))
    embed.add_field(name=chr(173), value=chr(173))
    embed.add_field(name=chr(173), value=chr(173))
    embed.add_field(name="Mod Commands", value="\n".join(modcmds))
    embed.set_footer(icon_url=ctx.author.display_avatar.url, text = f"Command Executed By: {ctx.author}")
    await ctx.send(embed=embed)
   elif command != None:
     try:
       cmd = bot.get_command(command)
       embed = discord.Embed(title = prefix+cmd.name, colour= discord.Colour.random())
       embed.add_field(name = "Description", value = cmd.description)
       embed.add_field(name = "Usage", value= cmd.usage)
       await ctx.send(embed=embed)
     except:
         await ctx.send(f"{command} Command Does Not Exist, try using .help to get list of commands.")
asyncio.run(main())

