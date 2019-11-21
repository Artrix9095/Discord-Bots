import discord
from discord.ext import tasks, commands

import time
import random

import sqlite3
import json

import asyncio

# COG setup code

class Catch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.broadcast = False
        self.time_amount = 1, 2, 3, 4, 6, 8, 9, 13, 19, 20, 0.1, 24.6

        self.bot.loop.create_task(self.random_loop())

        with open(r"G:\Artrix-botz\PhysixsFun\cugo\moninfo.json", 'r') as f:
            self.catch = json.load(f)

    async def random_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            if self.broadcast ==  True:
                return
            else:
                self.random = random.choice(self.catch)
                print(self.random)
                print(self.random['Type'])
                await asyncio.sleep(15)







    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        else:
            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
# This code embeds an random image from HTTPS links in a json file.
            embed = discord.Embed(color=random.choice(culorz), timestamp=message.created_at)

            embed.set_author(name=f"{self.random}! - {message.author}", icon_url=self.bot.user.avatar_url)

            embed.set_image(url="https://cdn.discordapp.com/attachments/618573859024535585/643286280926396478/latest.png")

            embed.add_field(name=None, value=f"A Untammed {self.random} has spawned who will tame it!")

            await message.channel.send(embed=embed)

            self.broadcast = True

            time.sleep(random.choice(self.time_amount))


    @commands.command(case_insensitive=False)
    async def tame(self, ctx, *, arg):
        if self.broadcast == False:
            await ctx.send("Nothing to tame!")
        else:
            if arg == None or False:
                await ctx.send("Please state a Weebmon to catch!")
            else:
                print(type(arg)) # To see if arg is registered as False or None by defualt when its not given a argument.
                if arg == self.random:
                    self.broadcast = False
                    db = sqlite3.connect('users.sqlite')
                    cursor = db.cursor()
                    cursor.execute(f"SELECT user_id, total, mons, FROM usr WHERE user_id = '{ctx.author.id}'")
                    result = cursor.fetchone()
                    if result is None:
                        sql = (f"INSERT INTO usr(user_id, mons, total) VALUES(?,?,?)")
                        val = (ctx.author.id, arg, 1)
                        cursor.execute(sql, val)
                        db.commit()
                        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                        embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

                        embed.set_author(name=f"Caught! - {ctx.author}", icon_url=self.bot.user.avatar_url)

                        embed.set_thumbnail(url=ctx.author.avatar_url)

                        embed.add_field(name=None, value=f"{ctx.author} has Caught a {arg}!")

                        await ctx.send(embed=embed)

                        self.broadcast = False
                    else:
                        # change all the lines bellow when you finish the start command
                        cursor.execute(f"SELECT user_id, mons, total FROM usr WHERE user_id = '{ctx.author.id}'")
                        result1 = cursor.fetchone()
                        total = int(result1[2])
                        sql = ("UPDATE usr SET total = ? and mon = ? WHERE user_id = ?")
                        val = (total + 1, str(arg), str(ctx.author.id))
                        cursor.execute(sql, val)
                        db.commit()
                        cursor.close()
                        db.close()
                        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                        embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

                        embed.set_author(name=f"Caught! - {ctx.author}", icon_url=self.bot.user.avatar_url)

                        embed.set_thumbnail(url=ctx.author.avatar_url)

                        embed.add_field(name=None, value=f"{ctx.author} has Caught a {arg}!")

                        await ctx.send(embed=embed)

                        self.broadcast = False
                else:
                    await ctx.send(f"{arg} Isn't the Correct Weebmon!")


def setup(bot):
    bot.add_cog(Catch(bot))
