import discord
from discord.ext import commands

import json
import sqlite3

import random

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # change the topic for new cogs!
        self.topic = 'Shop'

    @commands.group(invoke_without_command=True)
    async def shop(self, ctx):
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at, title='Shop')

        embed.add_field(name=f"**Battle Items**", value=f"`shop battle`", inline=False)
        embed.add_field(name=f"**Mythical Items**", value=f"`shop mythical`", inline=False)
        # for each new section add a field
        await ctx.send(embed=embed)

    @shop.command()
    async def battle(self, ctx):
        platform = 'Battle'
        db = sqlite3.connect('mons.sqlite')
        c = db.cursor()
        c.execute(f"SELECT num, name, cost, type FROM items WHERE type = '{platform}'")
        result = c.fetchall()
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at, title=f'{platform} Items')
        cringe =  0
        for x in result:
            cringe += 1
            embed.add_field(name=f"__**{result[cringe][0]}**__ |**{result[cringe][1]}**", value=f"`{result[cringe][2]}`", inline=False)

        embed.add_field(name="To buy Say", value=f"`buy {platform} <item>`")
        await ctx.send(embed=embed)

    @shop.command()
    async def mythical(self, ctx):
        platform = 'Mythical'
        db = sqlite3.connect('mons.sqlite')
        c = db.cursor()
        c.execute(f"SELECT num, name, cost, type FROM items WHERE type = '{platform}'")
        result = c.fetchall()
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at, title=f'{platform} Items')
        cringe =  0
        for x in result:
            cringe += 1
            embed.add_field(name=f"__**{result[cringe][0]}**__ |**{result[cringe][1]}**", value=f"`{result[cringe][2]}`", inline=False)

        embed.add_field(name="To buy Say", value=f"`buy {platform} <item>`")
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, arg, arg1):
        main = sqlite3.connect('mons.sqlite')
        db = sqlite3.connect('users.sqlite')
        cursor = main.cursor()
        cursor.execute(f"SELECT num, name, cost, type FROM items WHERE type = '{arg}' and name = '{arg1}'")
        item = cursor.fetchone()
        if item is None:
            await ctx.send("Invalid Item!")
        conn = db.cursor()
        conn.execute(f"SELECT user_id, coins, FROM usr WHERE user_id = '{ctx.author.id}'")
        usr = conn.fetchone()
        if usr is None:
            await ctx.send("You Have to Start First")
        c = db.cursor()
        if usr[1] < item[2]:
            await ctx.send("You Don't Have Enough Coins to buy This Item")
        else:
            sql = ("INSERT INTO bag(user_id, item) VALUES(?,?)")
            val = (str(ctx.author.id), item[1])
            c.execute(sql, val)
            db.commit()
            sql1 = ("UPDATE usr SET coins = ? WHERE user_id = ?")
            val1 = (usr[1]-item[2], str(ctx.author.id))
            await ctx.send(f"{ctx.author.mention} has Bought a {item[2]}")
            conn.execute(sql1, val1)
            db.commit()
            db.close()




def setup(bot):
    bot.add_cog(Shop(bot))
