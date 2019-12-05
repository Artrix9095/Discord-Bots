import discord
from discord.ext import commands

import random as rand

import json
import sqlite3

# THE MAIN FILE IS THE TRUNK AND THE COG IS THE BRANCH
class Other (commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        with open(r"G:\Artrix-botz\PhysixsFun\cugo\moninfo.json", 'r') as f:
            self.weeb = json.load(f)


    @commands.command()
    async def ping(self, ctx):
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=rand.choice(culorz), timestamp=ctx.message.created_at)

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
                embed = discord.Embed(color=rand.choice(culorz), timestamp=ctx.message.created_at)

                embed.set_author(name=f"Profile! - {str(user.name)[:-5]}", icon_url=self.bot.user.avatar_url)

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
                embed = discord.Embed(color=rand.choice(culorz), timestamp=ctx.message.created_at)

                embed.set_author(name=f"Profile! - {ctx.author}", icon_url=self.bot.user.avatar_url)

                embed.set_thumbnail(url=ctx.author.avatar_url)

                embed.add_field(name="**Weebmons:**", value=f"`{str(result[1])}`", inline=True)
                embed.add_field(name="**Coins:**", value=f"`{str(result[2])}`", inline=True)
                embed.add_field(name="**Redeems:**", value=f"`{str(result[3])}`", inline=True)
                embed.add_field(name="**Upvote Points**", value=f"`{str(result[4])}`", inline=True)


                await ctx.send(embed=embed)
    @commands.command()
    async def start(self, ctx):
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=rand.choice(culorz), timestamp=ctx.message.created_at)

        embed.set_author(name=f"Start! - {ctx.author}", icon_url=self.bot.user.avatar_url)
        embed.add_field(name="**Sakura**", value="`A Mid Tier Healer.`")
        embed.add_field(name="**Gowther**", value="`A Mid Tier Sage.`")
        embed.add_field(name="**Ash**", value="`Mid Tier Human.`")

        await ctx.send(embed=embed)
        await ctx.send("Say `>pick <name>` To start!")

    @commands.command()
    async def pick(self, ctx, *, text):
        starters = ['Sakura', 'Ash', 'Gowther']
        if text in starters:
            ivs = 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31
            hpiv = rand.choice(ivs)
            CCiv = rand.choice(ivs)
            CCDEFiv = rand.choice(ivs)
            FRiv = rand.choice(ivs)
            FRDEFiv = rand.choice(ivs)
            MGC = rand.choice(ivs)
            SPD = rand.choice(ivs)
            print(type(hpiv))
            amount_total = None
            db = sqlite3.connect('users.sqlite')
            cursor = db.cursor()
            cursor1 = db.cursor()
            cursor.execute(f"SELECT user_id FROM usr WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            if result is None:
                sql1 = ("INSERT INTO mons(user_id, xp, Level, Name, HPiv, CCiv, CCDEFiv, FRiv, FRDEFiv, MGC, SPD, Total, num, item) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)")
                val1 = (str(ctx.author.id), 0, int(5), str(text), int(hpiv), int(CCiv), int(CCDEFiv), int(FRiv), int(FRDEFiv), int(MGC), int(SPD), amount_total, int(1), None)
                cursor1.execute(sql1, val1)
                sql = ("INSERT INTO usr(user_id, selected, total, coins, redeems, upvotes) VALUES(?,?,?,?,?,?)")
                val = (str(ctx.author.id), 1, 1, 5000, 2, 0)
                cursor.execute(sql, val)
                db.commit()
                db.close()
                await ctx.send(f"You now Have a {text}!")
            else:
                await ctx.send("You have already Started!")


    """
    @commands.command()
    async def redeem(self, ctx, *, text):
        if text == None:
            await ctx.send("Stat Something to redeem \n You can redeem Coins, or Weebmons! redeem <weebmon> or redeem coins")
        else:
            db = sqlite3.connect('users.sqlite')
            main = sqlite3.connect('mons.sqlite')
            conn = db.cursor()
            conn.execute(f"SELECT user_id, redeems, total, coins FROM usr WHERE user_id = '{ctx.author.id}'")
            Con = conn.fetchone()
            if Con is None:
                await ctx.send(f"{ctx.author.mention} You haven't Started yet!")
            c = db.cursor()
            cursor = main.cursor()
            cursor.execute(f"SELECT name FROM mons WHERE name = '{text}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send("Invalid Weebmon Passed!")
            if not int(Con[1]) >= 1:
                await ctx.send(f"You Don't Have Enough Redeems to Purchase {text}!")
            ivs = 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31
            hpiv = rand.choice(ivs)
            CCiv = rand.choice(ivs)
            CCDEFiv = rand.choice(ivs)
            FRiv = rand.choice(ivs)
            FRDEFiv = rand.choice(ivs)
            MGC = rand.choice(ivs)
            SPD = rand.choice(ivs)
            cuz_u_mean = int(Con[1]) + 1
            amount_total = None
            sql = ("INSERT INTO mons(user_id, xp, Level, Name, HPiv, CCiv, CCDEFiv, FRiv, FRDEFiv, MGC, SPD, Total, num, item) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)")
            val = (str(ctx.author.id), int(0), int(5), str(result[0]), int(hpiv), int(CCiv), int(CCDEFiv), int(FRiv), int(FRDEFiv), int(MGC), int(SPD), str(amount_total), str(cuz_u_mean), None)
            c.execute(sql, val)
            db.commit()
            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
            embed = discord.Embed(color=rand.choice(culorz), timestamp=ctx.message.created_at)
            embed.add_field(name=str(ctx.author)[:-5], value=f"Has Redeemed a {text}!")
            await ctx.send(embed=embed)
            sql1 = ("UPDATE usr SET redeems = ?, total = ? WHERE user_id = ?")
            val1 = (str(int(Con[1])-1), str(int(Con[2]+1), str(ctx.author.id)))
            conn.execute(sql, val)
            db.commit()
            db.close()
    """



def setup(bot):
    bot.add_cog(Other(bot))
