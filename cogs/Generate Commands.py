import json
from discord.ext import commands
import random
import os.path
import re
import discord
def premium(message):
    with open('cooldowns.json', 'r') as file:
        meow = json.load(file)
    for element in list(meow):
        if str(element).lower() in message.content.lower():
            return commands.Cooldown(1, meow[str(element)]['cooldown'])


def free(message):
    with open('cooldowns.json', 'r') as file:
        meow = json.load(file)
    for element in list(meow):
        if str(element).lower() in message.content.lower():
            if meow[str(element)]['type'] == "Free":
                return commands.Cooldown(1, meow[str(element)]['cooldown'])
        else:
            pass


def booster(message):
    with open('cooldowns.json', 'r') as file:
        meow = json.load(file)
    for element in list(meow):
        if str(element).lower() in message.content.lower():
            if meow[str(element)]['type'] == "Booster":
                return commands.Cooldown(1, meow[str(element)]['cooldown'])
        else:
            pass


class GenCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_vari = ""
    botinfo = json.load(open('config.json'))
    prefix = botinfo.get('Prefix')
    @commands.dynamic_cooldown(premium, commands.BucketType.user)
    @commands.command(description = f"Gens a existing account type from Premium Gen", usage = f"{prefix}premgen accounttype")
    @commands.has_role("Premium")
    async def premgen(self, ctx, type):
        botinfo = json.load(open('config.json'))
        premgenchannel = botinfo.get('PremiumGenChannel')
        with open('authedpeople.json', 'r') as file:
            info = json.load(file)
        for element in list(info):
            if str(element) == str(ctx.author.id):
              if ctx.channel.id != premgenchannel:
                  await ctx.reply(f"Please generate in <#{premgenchannel}> ")
                  ctx.command.reset_cooldown(ctx)
              else:
                  try:

                      if os.path.exists(f'./alts/Premium/{type}.txt'):

                          with open(f"./alts/Premium/{type}.txt", "r") as f:
                              accs = f.readlines()
                              accountsend = random.choice(accs)
                              PATTERN = "[:]"
                              email, password = re.split(PATTERN, accountsend, maxsplit=1)
                              embed = discord.Embed(title=f"{type.capitalize()} Account", description="",
                                                    colour=discord.Colour.random())
                              embed.add_field(name="Email", value=email)
                              embed.add_field(name=chr(173), value=chr(173))
                              embed.add_field(name="Passowrd", value=password)
                              embed.add_field(name="Combo", value=accountsend)
                              embed.add_field(name=chr(173), value=chr(173))

                              await ctx.author.send(embed=embed)
                              accs.remove(accountsend)
                          with open(f"./alts/Premium/{type}.txt", "w+") as f:

                              f.write(''.join(accs))
                              em = discord.Embed(title=f'Successfully Generated!',
                                                 description=f"{ctx.author.mention} I have Sent the {type} Account to your DM",
                                                 colour=discord.Colour.random())
                          logchannel = botinfo.get("ModLogChannel")
                          logchannel2 = self.bot.get_channel(logchannel)
                          em1 = discord.Embed(title=f"Account Generated From Premium, Type: {type}", description=accountsend,
                                              colour=discord.Colour.random())
                          await logchannel2.send(embed=em1)
                          await ctx.send(embed=em)
                          await ctx.message.delete()
                      elif not os.path.exists(f'./alts/Premium/{type}.txt'):
                          embe = discord.Embed(title="Invalid Type",
                                               description="This Account Type Does not exist in Premium Gen!")
                          await ctx.send(embed=embe)
                          ctx.command.reset_cooldown(ctx)
                  except:
                      eme = discord.Embed(title=f"Error! {type} is Out Of Stock!", description="",
                                          colour=discord.Colour.random())
                      await ctx.send(embed=eme)
                      ctx.command.reset_cooldown(ctx)
            else:
                await ctx.reply("You Are Not Authorized To use the bot, Please contact Staff to use The bot!!")
    @commands.dynamic_cooldown(free, commands.BucketType.user)
    @commands.command(description = f"Gens a existing account type from Free Gen", usage = f"{prefix}gen accounttype")
    @commands.has_role("Free")
    async def gen(self, ctx, type):
        botinfo = json.load(open('config.json'))
        freegenchannel = botinfo.get('FreeGenChannel')
        if ctx.channel.id != freegenchannel:
            await ctx.reply(f"Please generate in <#{freegenchannel}> ")
        else:

            if os.path.exists(f'./alts/Free/{type}.txt'):
                if len(open(f'./alts/Free/{type}.txt', 'r').readlines()) < 0:
                    embed = discord.Embed(title=f"Error! {type} is Out Of Stock!", description="",
                                          colour=discord.Colour.random())
                    await ctx.send(embed=embed)
                    ctx.reset_cooldown(ctx)
                elif len(open(f'./alts/Free/{type}.txt', 'r').readlines()) > 0:
                    with open(f"./alts/Free/{type}.txt", "r") as f:
                        accs = f.readlines()
                        accountsend = random.choice(accs)
                        PATTERN = "[:]"
                        email, password = re.split(PATTERN, accountsend, maxsplit=1)
                        embed = discord.Embed(title=f"{type.capitalize()} Account", description="",
                                              colour=discord.Colour.random())
                        embed.add_field(name="Email", value=email)
                        embed.add_field(name=chr(173), value=chr(173))
                        embed.add_field(name="Passowrd", value=password)
                        embed.add_field(name="Combo", value=accountsend)
                        embed.add_field(name=chr(173), value=chr(173))
                        embed.set_footer(icon_url=ctx.author.display_avatar.url,
                                         text=f"Command Executed By: {ctx.author}")
                        await ctx.author.send(embed=embed)
                        accs.remove(accountsend)

                    logchannel = botinfo.get("ModLogChannel")
                    logchannel2 = self.bot.get_channel(logchannel)
                    em1 = discord.Embed(title=f"Account Generated From Free, Type: {type}", description=accountsend,
                                        colour=discord.Colour.random())
                    await logchannel2.send(embed=em1)
                    with open(f"./alts/Free/{type}.txt", "w+") as f:

                        f.write(''.join(accs))
                        em = discord.Embed(title=f'Successfully Generated!',
                                           description=f"{ctx.author.mention} I have Sent the {type} Account to your DM",
                                           colour=discord.Colour.random())

                    await ctx.send(embed=em)
                    await ctx.message.delete()
            elif not os.path.exists(f'./alts/Free/{type}.txt'):
                embe = discord.Embed(title="Invalid Type",
                                     description="This Account Type Does not exist in Free Gen!")
                embe.set_footer(icon_url=ctx.author.display_avatar.url, text=f"Command Executed By: {ctx.author}")
                await ctx.send(embed=embe)

    @commands.dynamic_cooldown(booster, commands.BucketType.user)
    @commands.command(description = f"Gens a existing account type from Booster Gen", usage = f"{prefix}boostgen accounttype")
    @commands.has_role("Server Booster")
    async def boostgen(self, ctx, type):
        botinfo = json.load(open('config.json'))
        boostergenchannel = botinfo.get('BoosterGenChannel')
        if ctx.channel.id != boostergenchannel:
            await ctx.reply(f"Please generate in <#{boostergenchannel}> ")
        else:

            if os.path.exists(f'./alts/Booster/{type}.txt'):
                if len(open(f'./alts/Booster/{type}.txt', 'r').readlines()) < 0:
                    embed = discord.Embed(title=f"Error! {type} is Out Of Stock!", description="",
                                          colour=discord.Colour.random())
                    await ctx.send(embed=embed)
                    ctx.reset_cooldown(ctx)
                elif len(open(f'./alts/Booster/{type}.txt', 'r').readlines()) > 0:
                    with open(f"./alts/Booster/{type}.txt", "r") as f:
                        accs = f.readlines()
                        accountsend = random.choice(accs)
                        PATTERN = "[:]"
                        email, password = re.split(PATTERN, accountsend, maxsplit=1)
                        embed = discord.Embed(title=f"{type.capitalize()} Account", description="",
                                              colour=discord.Colour.random())
                        embed.add_field(name="Email", value=email)
                        embed.add_field(name=chr(173), value=chr(173))
                        embed.add_field(name="Passowrd", value=password)
                        embed.add_field(name="Combo", value=accountsend)
                        embed.add_field(name=chr(173), value=chr(173))
                        embed.set_footer(icon_url=ctx.author.display_avatar.url,
                                         text=f"Command Executed By: {ctx.author}")
                        logchannel = botinfo.get("ModLogChannel")
                        logchannel2 = self.bot.get_channel(logchannel)
                        em1 = discord.Embed(title=f"Account Generated From Booster Gen, Type: {type}",
                                            description=accountsend,
                                            colour=discord.Colour.random())
                        await logchannel2.send(embed=em1)
                        await ctx.author.send(embed=embed)
                        accs.remove(accountsend)
                    with open(f"./alts/Booster/{type}.txt", "w+") as f:

                        f.write(''.join(accs))
                        em = discord.Embed(title=f'Successfully Generated!',
                                           description=f"{ctx.author.mention} I have Sent the {type} Account to your DM",
                                           colour=discord.Colour.random())

                    await ctx.send(embed=em)
                    await ctx.message.delete()
            elif not os.path.exists(f'./alts/Booster/{type}.txt'):
                embe = discord.Embed(title="Invalid Type",
                                     description="This Account Type Does not exist in Booster Gen!")
                embe.set_footer(icon_url=ctx.author.display_avatar.url, text=f"Command Executed By: {ctx.author}")
                await ctx.send(embed=embe)

    @commands.command(description=f"Shows the current stock.", usage = f"{prefix}stock")
    async def stock(self, ctx):


        Premium = []
        Free = []
        Booster = []
        embed = discord.Embed(title="UTA Gen Stock", colour=discord.Colour.random(), description="All generators")
        try:
            dictionary = './alts/Premium'
            if not os.listdir(dictionary):
                embed.add_field(name="Premium", value="❌ No Types")
            elif os.listdir(dictionary):
                for file in os.listdir(dictionary):
                    if file.endswith('.txt'):
                        file2 = file[:-4]
                        rere = len(open(f'./alts/Premium/{file}', 'r').readlines())
                        if rere == 0:
                           Premium.append(file2.capitalize() + '\n' + f"❌ No Stock")
                        elif rere != 0:
                            Premium.append(file2.capitalize() +'\n' + f":white_check_mark: {rere} Alts!")
                embed.add_field(name = f"**Premium**", value = '\n'.join(Premium))

        except:
            pass
        try:
            dictionary2 = './alts/Free'
            if not os.listdir(dictionary2):
                embed.add_field(name= "Free", value= "❌ No Types")
            elif os.listdir(dictionary2):
                for file2 in os.listdir(dictionary2):
                    if file2.endswith('.txt'):
                        file3 = file2[:-4]
                        rere = len(open(f'./alts/Free/{file2}', 'r').readlines())
                        if rere == 0:
                            Free.append(f"**{(file3.capitalize())}**" + '\n' + f"❌ No Stock")
                        elif rere != 0:
                            Free.append(file3.capitalize() + '\n' + f":white_check_mark: {rere} Alts!")
                embed.add_field(name = "Free", value= '\n'.join(Free))


        except:
            pass
        try:
            dictionary2 = './alts/Booster'
            if not os.listdir(dictionary2):
                    embed.add_field(name= "Booster", value= "❌ No Types")
            elif os.listdir(dictionary2):
                for file2 in os.listdir(dictionary2):
                    if file2.endswith('.txt'):
                        file4 = file2[:-4]
                        rere = len(open(f'./alts/Booster/{file2}', 'r').readlines())
                        if rere == 0:
                            Booster.append(f"**{(file4.capitalize())}**" + '\n' + f"❌ No Stock")
                        elif rere != 0:
                            Booster.append(file4.capitalize() + '\n' + f":white_check_mark: {rere} Alts!")
                embed.add_field(name="Booster", value='\n'.join(Booster))

        except:
            pass

        embed.set_footer(icon_url=ctx.author.display_avatar.url, text=f"Command Executed By: {ctx.author}")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(GenCommands(bot))