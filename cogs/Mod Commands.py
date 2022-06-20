import json
import discord
from discord.ext import commands

class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    botinfo = json.load(open('config.json'))
    prefix = botinfo.get('Prefix')
    @commands.command(description = f"Sets the notificaiton Channel !", usage = f"{prefix}setnotifchannel channel")
    @commands.has_permissions(administrator=True)
    async def setnotifchannel(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            try:
                with open("config.json", 'r') as f:
                    cfg = json.loads(f.read())
                    cfg[str("notificationChannel")] = ""
                    json.dump(cfg, open("config.json", 'w'), indent=4)
                    await ctx.message.reply(f"Successfully Reset the logchannel by {ctx.author}")
            except:
                await ctx.message.reply("There's no channel set already")

        else:

            with open("config.json", "r") as f:
                cfg = json.load(f)

            cfg[str("notificationChannel")] = channel.id
            with open("config.json", "w") as f:
                json.dump(cfg, f, indent=4)
                embed = discord.Embed(title="Success",
                                      description=f"Successfully set the notification channel to {channel.mention}!",
                                      colour=discord.Colour.random())
                embed.set_footer(icon_url=ctx.author.display_avatar.url, text = f"Command Executed By: {ctx.author}")

                await ctx.message.reply(embed=embed)
    @commands.command(description = f"Sets The moderation log channel", usage = f"{prefix}setmodlogchannel channel")
    @commands.has_permissions(administrator=True)
    async def setmodlogchannel(self, ctx, channel : discord.TextChannel = None):
        if channel == None:
            try:
                with open("config.json", 'r') as f:
                    cfg = json.loads(f.read())
                    cfg[str("ModLogChannel")] = ""
                    json.dump(cfg, open("config.json", 'w'), indent=4)
                    await ctx.message.reply(f"Successfully Reset the Moderation Log Channel by {ctx.author}")
            except:
                await ctx.message.reply("There's no channel set already")

        else:

            with open("config.json", "r") as f:
                cfg = json.load(f)

            cfg[str("ModLogChannel")] = channel.id
            with open("config.json", "w") as f:
                json.dump(cfg, f, indent=4)
                embed = discord.Embed(title="Success",
                                      description=f"Successfully set the notification channel to {channel.mention}!",
                                      colour=discord.Colour.random())
                embed.set_footer(icon_url=ctx.author.display_avatar.url, text = f"Command Executed By: {ctx.author}")
                await ctx.message.reply(embed=embed)
    @commands.command(description= "Sets the generation channel for a existing gen type", usage = f"{prefix} gentype channel")
    @commands.has_permissions(administrator=True)
    async def setgenchannel(self,ctx, type, channel : discord.TextChannel):
      if type == "Premium":
        with open("config.json", "r") as f:
            cfg = json.load(f)

        cfg[str("PremiumGenChannel")] = channel.id
        with open("config.json", "w") as f:
            json.dump(cfg, f, indent=4)
            embed = discord.Embed(title="Success",
                                  description=f"Successfully set the Premium Gen channel to {channel.mention}!",
                                  colour=discord.Colour.random())
            embed.set_footer(icon_url=ctx.author.display_avatar.url, text = f"Command Executed By: {ctx.author}")

            await ctx.message.reply(embed=embed)
      elif type == "Free":
          with open("config.json", "r") as f:
              cfg = json.load(f)

          cfg[str("FreeGenChannel")] = channel.id
          with open("config.json", "w") as f:
              json.dump(cfg, f, indent=4)
              embed = discord.Embed(title="Success",
                                    description=f"Successfully set the Free Gen channel to {channel.mention}!",
                                    colour=discord.Colour.random())
              embed.set_footer(icon_url=ctx.author.display_avatar.url, text = f"Command Executed By: {ctx.author}")

              await ctx.message.reply(embed=embed)
      elif type == "Booster":
          with open("config.json", "r") as f:
              cfg = json.load(f)

          cfg[str("BoosterGenChannel")] = channel.id
          with open("config.json", "w") as f:
              json.dump(cfg, f, indent=4)
              embed = discord.Embed(title="Success",
                                    description=f"Successfully set the Free Gen channel to {channel.mention}!",
                                    colour=discord.Colour.random())
              embed.set_footer(icon_url=ctx.author.display_avatar.url, text = f"Command Executed By: {ctx.author}")

              await ctx.message.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(ModCommands(bot))