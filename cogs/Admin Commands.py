import re
import discord
import requests
from discord.ext import commands
import json
import os
from discord.utils import get
time_regex = re.compile(r"(\d{1,5}(?:[.,]?\d{1,5})?)([hdms])")
time_dict = {"h":3600, "d":86400, "m":60, "s" : 1}
class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        matches = time_regex.findall(argument.lower())
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*int(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/d/m/s are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time
time_regex2 = re.compile(r"(\d{1,5}(?:[.,]?\d{1,5})?)([hdmye])")
time_dict2 = {"h":3600, "d":86400, "m":2592000, "y": 31536000, "e" : 30}

class TimeConverter2(commands.Converter):
    async def convert(self, ctx, argument):
        matches = time_regex2.findall(argument.lower())
        time = 0
        for v, k in matches:
            try:
                time += time_dict2[k]*int(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/y/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time
class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    botinfo = json.load(open('config.json'))
    prefix = botinfo.get('Prefix')
    @commands.command(description=f"Restocks a current existing type for a gen type", usage = f"`{prefix}restock, Category(premium/free/booster), accounttype, a txt file with accounts`, Restocks a existing category", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def restock(self, ctx, category, accounts):

            attachment_url = ctx.message.attachments[0].url
            swallo = requests.get(attachment_url)
            poggywoggy = swallo.content
            poggywoggy.decode('utf-8')
            poggywoggy_2 = poggywoggy
            if os.path.exists(f"./alts/{category}/{accounts}.txt"):

             with open(f"./alts/{category}/{accounts}.txt", 'ab') as f:
                 f.write(poggywoggy_2)
                 await ctx.send(f"Added the {accounts} accounts to the {category} Stock successfully!")
            else:
                await ctx.send("Error!, this type/category does not exist!")


    @commands.command(description = f"Sets Cooldown For A type in a specfic category", usage =  f"`{prefix}setcooldown category(premium/booster/free), acctype, cooldown(timeunit)`")
    @commands.has_permissions(administrator = True)
    async def setcooldown(self, ctx, category, type , cooldown : TimeConverter):
        if os.path.exists(f'./alts/{category}/{type}.txt'):
            with open('cooldowns.json', 'r') as file:
                info = json.load(file)
            if info[str(type)]['type'] == category:

             info[str(type)]['cooldown'] = cooldown
            with open('cooldowns.json', 'w') as f:
                json.dump(info, f, indent = 4)
            embed = discord.Embed(title = f"Successfully Changed Cooldown!", description= f"Succsesfully Set Cooldown to {cooldown} For {type}!")
            embed.set_footer(icon_url=ctx.author.display_avatar.url, text=f"Command Executed By: {ctx.author}")
            await ctx.send(embed=embed)
        else:
                embed = discord.Embed(title = f"Error!", description= f"{type} Does Not Exist in {category}!")
                embed.set_footer(icon_url=ctx.author.display_avatar.url, text=f"Command Executed By: {ctx.author}")
                await ctx.send(embed=embed)
    @commands.command(description=f"Removes a account Category", usage = f"`{prefix}removecategory category(premium/free/booster), typename`")
    @commands.has_permissions(administrator=True)
    async def removecategory(self, ctx, category, type):

        if os.path.exists(f"./alts/{category}/{type}.txt"):
            os.remove(f"./alts/{category}/{type}.txt")
            embed = discord.Embed(title="Deleted Category", description=f"Successfully Deleted {type} Category from {category}!!",
                                  colour=0x2ecc71)
            embed.set_footer(icon_url=ctx.author.display_avatar.url, text = f"Command Executed By: {ctx.author}")
            await ctx.send(embed=embed)
            with open('cooldowns.json', 'r') as f:
                info = json.load(f)
            info.pop(str(type))
            with open('cooldowns.json', 'w') as file:
                json.dump(info, file, indent = 4)
        else:
            embed = discord.Embed(title="Critical Error!", description=f"Category {type} does not exist in {category}!",
                                  colour=0xe74c3c)
            embed.set_footer(icon_url=ctx.author.display_avatar.url, text = f"Command Executed By: {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(description = f"Clears all stock in a specific type",  usage =  f"{prefix}clearstock PremiumOrFreeOrBooster accounttype")
    @commands.has_permissions(administrator=True)
    async def clearstock(self, ctx, category, type):

            if os.path.exists(f"./alts/{category}/{type}.txt"):
                with open(f"./alts/{category}/{type}.txt", 'w+') as f:
                    f.truncate(0)
                    embed = discord.Embed(title = "Successfully Done!", description= f"Successfully Deleted All {type} Stock From {category}!", colour= discord.Colour.random())
                    embed.set_footer(icon_url=ctx.author.display_avatar.url, text = f"Command Executed By: {ctx.author}")

                    await ctx.reply(embed=embed)
            else:
                embed = discord.Embed(title="Critical Error!",
                                      description=f"{type} Does Not Exist In Category {category}", colour= discord.Colour.random())
                embed.set_footer(icon_url=ctx.author.display_avatar.url, text=f"Command Executed By: {ctx.author}")

                await ctx.reply(embed=embed)
    @commands.command(description = f"Creates a new account Category", usage =  f"{prefix}newcategory, PremiumOrFreeOrBooster, AccountTypeName, Cooldown")
    @commands.has_permissions(administrator = True)
    async def newcategory(self, ctx, category, type, cooldown):
        alist = ['Premium', 'Free', 'Booster']
        if category in alist:
           if os.path.exists(f'./alts/{category}/{type}.txt'):
               await ctx.send("This Account Type Already exists in {}!".format(category))
           else:
            with open(f'./alts/{category}/{type}.txt', 'a+') as f:
                pass
            with open('cooldowns.json','r') as file:
                info = json.load(file)
            info[str(type)] = {"cooldown" : cooldown, "type": category}
            with open('cooldowns.json', 'w') as fe:
                json.dump(info , fe, indent = 3)
            await ctx.send("Successfully created new account type in {} with the name of {} with cooldown {}".format(category, type, cooldown))
    @commands.command(description = f"Authorize A User", usage =  f"{prefix}auth, member, time")
    @commands.has_permissions(administrator = True)
    async def auth(self, ctx, member: discord.Member, time: TimeConverter2 = None):
        with open('admins.json', 'r') as fer:
            people = json.load(fer)
        if str(ctx.author.id) in list(people):

              with open('authedpeople.json', 'r') as f:
                  info = json.load(f)
              if str(member.id) in list(info):
                  await ctx.send("This user is already authorized!")
              elif str(member.id) not in list(info):


               user = ctx.author
               role = get(ctx.guild.roles, name="Premium")
               await member.add_roles(role)
               if time is None:
                   info[str(member.id)] = {"AuthedBy": str(user), "TimeLeft": "Lifetime"}

               else:
                   info[str(member.id)] = {"AuthedBy" : str(user), "TimeLeft" : time}

               with open('authedpeople.json', 'w') as file:
                   json.dump(info, file , indent = 4)
               await ctx.send(F"Successfully authorized {member}")

        elif str(ctx.author.id)  not in list(people):
                await ctx.send("Your are not allowed to use this command!")

    @commands.command(description = f"Blacklist a premium user", usage =  f"{prefix}blacklist, member")
    @commands.has_permissions(administrator = True)
    async def blacklist(self, ctx, member : discord.Member):

        with open('authedpeople.json', 'r') as file:
            info = json.load(file)
        try:
            info.pop(str(member.id))
            with open('authedpeople.json', 'w') as f:
               json.dump(info, f, indent = 4)
            await ctx.send("Blacklisted Member: {}".format(member))
            role = get(ctx.guild.roles, name="Premium")
            await member.remove_roles(role)
        except:
           await ctx.send("This member is not authorized!")
    @commands.command(description = f"Authorize a admin for sensitive commands The command is For UTA Only", usage = f"{prefix}addadmin Member")
    async def addadmin(self, ctx, member : discord.Member):
        if ctx.author.id != 968398398917083176:
            await ctx.send("You are not authorized to use this command.")
        elif ctx.author.id == 968398398917083176:
          with open('admins.json', 'r') as file:
                info = json.load(file)
          info[str(member.id)] = "True"
          with open('admins.json', 'w') as fer:
              json.dump(info, fer , indent = 4)
          await ctx.send("Added {} As admin successfully!".format(member))
async def setup(bot):
    await bot.add_cog(AdminCommands(bot))