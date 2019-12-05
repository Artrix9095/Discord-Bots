import discord
from discord.ext import commands

import random

# COG setup code

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    """
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

                await ctx.message.author.send(embed=embed)
        except:
                embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

                embed.set_author(name=f"Error! - {ctx.author}", icon_url=self.bot.user.avatar_url)

                embed.add_field(name=f'Erron in {ctx.command}!', value=error)

                await ctx.send(embed=embed)
                """

    @commands.command(pass_context=True, aliases=['Help', 'HELP'])
    async def help(self, ctx, *cog):
        if not cog:
            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
            embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)
            cugz_desc = ''
            for x in self.bot.cogs:
                cugz_desc += f"**{x}** - {self.bot.cogs[x].__doc__}\n"
            embed.set_author(name=f"Help! - {ctx.author}", icon_url=self.bot.user.avatar_url)

            embed.set_thumbnail(url=ctx.author.avatar_url)

            embed.add_field(name=f'PhysixsFun Commands!', value=cugz_desc[0:len(cugz_desc)-1], inline=True)

            await ctx.message.author.send(embed=embed)
        else:
            if len(cog) > 1:
                embed = discord.embed(title='Error', description='Too Many Cogs!')
                await ctx.message.author.send('', embed=embed)
            else:
                found = False
                for x in self.bot.cogs:
                    for y in cog:
                        if x == y:
                            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                            embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)
                            embed.set_author(name=f"Help! - {ctx.author}", icon_url=self.bot.user.avatar_url)

                            embed.set_thumbnail(url=ctx.author.avatar_url)
                            scog_info = ''
                            for c in self.bot.get_cog(y).get_commands():
                                if not c.hidden:
                                    scog_info += f'**{c.name}** - {c.help}\n'
                            embed.add_field(name=f'{cog[0]} - {self.bot.cogs[cog[0]].__doc__}', value=scog_info)
                            found = True
            if not found:
                for x in self.bot.cogs:
                    for c in self.bot.get_cog(x).get_commands():
                        if c.name == cog[0]:
                            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                            embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)
                            embed.set_author(name=f"Help! - {ctx.author}", icon_url=self.bot.user.avatar_url)

                            embed.set_thumbnail(url=ctx.author.avatar_url)
                            embed.add_field(name=f'{c.name} - {c.help}', value=f"Proper Syntax:\n`{c.qualified_name} {c.signature}`")
                    found = True
                if not found:
                    culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                    embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)
                    embed.set_author(name=f"Help! - {ctx.author}", icon_url=self.bot.user.avatar_url)

                    embed.set_thumbnail(url=ctx.author.avatar_url)

                    embed.add_field(name='Error', value='`Thats not a cog!`')
                    await ctx.message.author.send(embed=embed)
            await ctx.message.author.send(embed=embed)










def setup(bot):
    bot.add_cog(help(bot))
