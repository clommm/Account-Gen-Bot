import datetime
import json
from discord.ext import commands


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('This command is on Cooldown! Please Try again in %.2fs ' % error.retry_after)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Please fill all {ctx.command.name} Requirements!, Type !help {ctx.command.name} For more info")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.reply("This command Does Not Exist! Type .help for more commands!")
        raise error

async def setup(bot):
    await bot.add_cog(events(bot))
