import discord
from discord.ext import commands

import random
import sqlite3

# THE MAIN FILE IS THE TRUNK AND THE COG IS THE BRANCH
class Other (commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def ping(self, ctx):
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

        embed.set_author(name=f"Latency - {ctx.author}", icon_url=self.bot.user.avatar_url)


        embed.add_field(name=f"Pong", value=f"{round(self.bot.latency * 1000)}ms")

        await ctx.send(embed=embed)

    @commands.command()
    async def profile(self, ctx, user:discord.User=None):
        if user is not None:
            db = sqlite3.connect('users.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id, total, coins, redeems, upvotes FROM usr WHERE user_id = '{user.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send(f"{user.name} Hasn't Started yet!")
            else:
                culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

                embed.set_author(name=f"Profile! - {user.name}", icon_url=self.bot.user.avatar_url)

                embed.set_thumbnail(url=user.avatar_url)

                embed.add_field(name="**Weebmons:**", value=f"`{str(result[1])}`", inline=True)
                embed.add_field(name="**Coins:**", value=f"`{str(result[2])}`", inline=True)
                embed.add_field(name="**Redeems:**", value=f"`{str(result[3])}`", inline=True)
                embed.add_field(name="**Upvote Points**", value=f"`{str(result[4])}`", inline=True)


                await ctx.send(embed=embed)
        else:
            db = sqlite3.connect('users.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id, total, coins, redeems, upvotes FROM usr WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send(f"You Need to Start Before you can get a Profile!")
            else:
                culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

                embed.set_author(name=f"Profile! - {ctx.author}", icon_url=self.bot.user.avatar_url)

                embed.set_thumbnail(url=ctx.author.avatar_url)

                embed.add_field(name="**Weebmons:**", value=f"`{str(result[1])}`", inline=True)
                embed.add_field(name="**Coins:**", value=f"`{str(result[2])}`", inline=True)
                embed.add_field(name="**Redeems:**", value=f"`{str(result[3])}`", inline=True)

                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Other(bot))
