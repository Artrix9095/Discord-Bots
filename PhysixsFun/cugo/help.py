import discord
from discord.ext import commands

import random

# COG setup code

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            if hasattr(ctx.command, 'on_error'):
                return
            else:
                culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

                embed.set_author(name=f"Error! - {ctx.author}", icon_url=self.bot.user.avatar_url)

                embed.add_field(name=f'Error in {ctx.command}!', value=error)

                await ctx.send(embed=embed)
        except:
                embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

                embed.set_author(name=f"Error! - {ctx.author}", icon_url=self.bot.user.avatar_url)

                embed.add_field(name=f'Erron in {ctx.command}!', value=error)

                await ctx.send(embed=embed)
    
    @commands.command(pass_context=True, aliases=['Help', 'HELP'])
    async def help(self, ctx, *cog):
        if not cog:
            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
            embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)
            cugz_desc = ''
            for x in self.bot.cogs:
                cugz_desc += f"**{x}** - {self.bot.cogs[x].__doc__} \n"
            embed.set_author(name=f"Help! - {ctx.author}", icon_url=self.bot.user.avatar_url)

            embed.set_thumbnail(url=ctx.author.avatar_url)

            embed.add_field(name=f'PhysixsFun Commands!', value=cugz_desc)

            await ctx.send(embed=embed)










def setup(bot):
    bot.add_cog(help(bot))
