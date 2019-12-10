import discord
from discord.ext import commands

import random
import math

import sqlite3
import json


# COG setup code

# THE MAIN FILE IS THE TRUNK AND THE COG IS THE BRANCH
class Info(commands.Cog):
    def __init__(self, bot):
        # self means the variable is usable throughout the cog
        self.bot = bot
        # change the topic for new cogs!
        self.topic = 'Info'
        self.broadcast = ''



    @commands.group(invoke_without_command=True, pass_context=True, aliases=['i', 'I'])
    async def info(self, ctx):
        db = sqlite3.connect('mons.sqlite')
        main = sqlite3.connect('users.sqlite')
        conn = main.cursor()
        c = main.cursor()
        c.execute(f"SELECT selected FROM usr WHERE user_id = '{ctx.author.id}'")
        c_result = c.fetchone()
        if c_result == None:
            await ctx.send("You Have to Start First!")
        select = c_result[0]
        print(select)
        print(type(select))
        conn.execute(f"SELECT Level, Name, HPiv, CCiv, CCDEFiv, FRiv, FRDEFiv, MGC, SPD, Total FROM mons WHERE user_id = '{str(ctx.author.id)}' and num = '{int(select)}' ")
        result = conn.fetchone()
        print(result[1])

        cursor = db.cursor()
        cursor.execute(f"SELECT name, image, hp, CC, CC_DEF, FR, FR_DEF, MGC, SPD FROM mons WHERE name = '{result[1]}'")
        cur_result = cursor.fetchone()
        print(cur_result)
        image = cur_result[1]
        print(type(image))
        bs_hp = cur_result[2]
        bs_cc = cur_result[3]
        bs_ccdef = cur_result[4]
        bs_fr = cur_result[5]
        bs_frdef = cur_result[6]
        bs_mgc = cur_result[7]
        bs_spd = cur_result[8]
        lvl = result[0]
        name = result[1]
        hpiv = result[2]
        CCiv = result[3]
        CCDEFiv = result[4]
        FRiv = result[5]
        FRDEFiv = result[6]
        MGC = result[7]
        SPD = result[8]
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(
        color=random.choice(culorz),
        timestamp=ctx.message.created_at,
        title=f"{ctx.author}'s Level {lvl} {name}!",
        )
        """int(round(int((stat) * int(level)) + int(stativ)*int(lvl))) / 350 if is health than /100"""
        embed.add_field(name=f"**HP**:", value=f"**IV**:`{int(hpiv)}`| {(round(int(bs_hp) * int(lvl)) + ((int(hpiv)*int(lvl)) / 100))} \n")
        embed.add_field(name=f"**Close Combat**:", value=f"**IV**:`{int(CCiv)}`| {math.floor(round(int(bs_cc) * int(lvl)) + ((int(CCiv)*int(lvl)) / 350))} \n")
        embed.add_field(name=f"**CC Defence**:", value=f"**IV**:`{int(CCDEFiv)}`| {math.floor(round(int(bs_ccdef) * int(lvl)) + ((int(CCDEFiv)*int(lvl))) / 350)} \n")
        embed.add_field(name=f"**Far Range**:", value=f"**IV**:`{int(FRiv)}`| {math.floor(round(int(bs_fr) * int(lvl)) + ((int(FRiv)*int(lvl)) / 350))} \n")
        embed.add_field(name=f"**FR Defence**:", value=f"**IV**:`{int(FRDEFiv)}`| {math.floor(round(int(bs_frdef) * int(lvl)) + ((int(FRDEFiv)*int(lvl)) / 350))} \n")
        embed.add_field(name=f"**Magic**:", value=f"**IV**:`{int(MGC)}`| {math.floor(round(int(bs_mgc) * int(lvl)) + ((int(MGC)*int(lvl)) / 350))} \n")
        embed.add_field(name=f"**Speed**:", value=f"**IV**:`{int(SPD)}`| {math.floor(round(int(bs_spd) * int(lvl)) + ((int(SPD)*int(lvl)) / 350))} \n")
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @info.command(pass_context=True, aliases=['n', 'N'])
    async def number(self, ctx, mon: int):
        db = sqlite3.connect('mons.sqlite')
        main = sqlite3.connect('users.sqlite')
        conn = main.cursor()
        conn.execute(f"SELECT Level, Name, HPiv, CCiv, CCDEFiv, FRiv, FRDEFiv, MGC, SPD, Total FROM mons WHERE user_id = '{str(ctx.author.id)}' and num = '{mon}' ")
        result = conn.fetchone()
        print(result[1])

        cursor = db.cursor()
        cursor.execute(f"SELECT name, image, hp, CC, CC_DEF, FR, FR_DEF, MGC, SPD FROM mons WHERE name = '{result[1]}'")
        cur_result = cursor.fetchone()
        print(cur_result)
        image = cur_result[1]
        print(type(image))
        bs_hp = cur_result[2]
        bs_cc = cur_result[3]
        bs_ccdef = cur_result[4]
        bs_fr = cur_result[5]
        bs_frdef = cur_result[6]
        bs_mgc = cur_result[7]
        bs_spd = cur_result[8]
        lvl = result[0]
        name = result[1]
        hpiv = result[2]
        CCiv = result[3]
        CCDEFiv = result[4]
        FRiv = result[5]
        FRDEFiv = result[6]
        MGC = result[7]
        SPD = result[8]
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(
        color=random.choice(culorz),
        timestamp=ctx.message.created_at,
        title=f"{ctx.author}'s Level {lvl} {name}!",
        )
        """int(round(int((stat) * int(level)) + int(stativ)*int(lvl))) / 350 if is health than /100"""
        embed.add_field(name=f"**HP**:", value=f"**IV**:`{int(hpiv)}`| {math.floor(round(int(bs_hp) * int(lvl)) + ((int(hpiv)*int(lvl)) / 100))} \n")
        embed.add_field(name=f"**Close Combat**:", value=f"**IV**:`{int(CCiv)}`| {math.floor(round(int(bs_cc) * int(lvl)) + ((int(CCiv)*int(lvl)) / 350))} \n")
        embed.add_field(name=f"**CC Defence**:", value=f"**IV**:`{int(CCDEFiv)}`| {math.floor(round(int(bs_ccdef) * int(lvl)) + ((int(CCDEFiv)*int(lvl))) / 350)} \n")
        embed.add_field(name=f"**Far Range**:", value=f"**IV**:`{int(FRiv)}`| {math.floor(round(int(bs_fr) * int(lvl)) + ((int(FRiv)*int(lvl)) / 350))} \n")
        embed.add_field(name=f"**FR Defence**:", value=f"**IV**:`{int(FRDEFiv)}`| {math.floor(round(int(bs_frdef) * int(lvl)) + ((int(FRDEFiv)*int(lvl)) / 350))} \n")
        embed.add_field(name=f"**Magic**:", value=f"**IV**:`{int(MGC)}`| {math.floor(round(int(bs_mgc) * int(lvl)) + ((int(MGC)*int(lvl)) / 350))} \n")
        embed.add_field(name=f"**Speed**:", value=f"**IV**:`{int(SPD)}`| {math.floor(round(int(bs_spd) * int(lvl)) + ((int(SPD)*int(lvl)) / 350))} \n")
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @info.command(pass_context=True, aliases=['m', 'M'])
    async def mon(self, ctx, mon: str):
        main = sqlite3.connect('mons.sqlite')
        conn = main.cursor()
        conn.execute(f"SELECT name, image, hp, CC, CC_DEF, FR, FR_DEF, MGC, SPD FROM mons WHERE name = '{mon}'")
        cur_result = conn.fetchone()
        if cur_result is None:
            await ctx.send(f"{mon} Isn't a Weebmon!")
        image = cur_result[1]
        bs_hp = cur_result[2]
        bs_cc = cur_result[3]
        bs_ccdef = cur_result[4]
        bs_fr = cur_result[5]
        bs_frdef = cur_result[6]
        bs_mgc = cur_result[7]
        bs_spd = cur_result[8]
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(
        color=random.choice(culorz),
        timestamp=ctx.message.created_at,
        title=f"{str(mon)}!",
        )
        embed.add_field(name="HP:", value=bs_hp)
        embed.add_field(name="Close Combat", value=bs_cc)
        embed.add_field(name="CC Defence", value=bs_ccdef)
        embed.add_field(name="Far Range", value=bs_fr)
        embed.add_field(name="FR Defence", value=bs_frdef)
        embed.add_field(name="Magic", value=bs_mgc)
        embed.add_field(name="Speed", value=bs_spd)
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    # showing the end-user all the characters that they have.
    @commands.group(invoke_without_command=True, pass_context=True, aliases=['W', 'w'])
    async def weebmons(self, ctx):
        db = sqlite3.connect('users.sqlite')
        c = db.cursor()
        c.execute(f"SELECT Level, xp, Name, num FROM mons WHERE user_id = '{ctx.author.id}'")
        result = c.fetchall()
        if result is None:
            await ctx.send("You Have to Start First!")
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_author(icon_url=self.bot.user.avatar_url, name="Your Weebmons!")
        run = 0
        for x in result:
            embed.add_field(name=f"__**{result[run][3]}**__", value=f"**{result[run][2]}**|->`Level {result[run][0]}`\n")
            run += 1
        await ctx.send(embed=embed)


    @weebmons.command()
    async def page(self, ctx, p: int):
        if not p == False:
            db = sqlite3.connect('users.sqlite')
            c = db.cursor()
            c.execute(f"SELECT Level, xp, Name, num FROM mons WHERE user_id = '{ctx.author.id}'")
            result = c.fetchall()
            if result is None:
                await ctx.send("You Have to Start First!")
            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
            embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_author(icon_url=self.bot.user.avatar_url, name="Your Weebmons!")
            run = 25*p
            for x in result:
                embed.add_field(name=f"__**{result[run][3]}**__", value=f"**{result[run][2]}**|->`Level {result[run][0]}`\n")
                run += 1
            await ctx.send(embed=embed)




    @info.command(pass_context=True, aliases=['Latest', 'new', 'LATEST', 'NEW'])
    async def latest(self, ctx):
        db = sqlite3.connect('mons.sqlite')
        main = sqlite3.connect('users.sqlite')
        conn = main.cursor()
        c = main.cursor()
        c.execute(f"SELECT total FROM usr WHERE user_id = '{ctx.author.id}'")
        c_result = c.fetchone()
        if c_result == None:
            await ctx.send("You Have to Start First!")
        select = c_result[0]
        print(select)
        print(type(select))
        conn.execute(f"SELECT Level, Name, HPiv, CCiv, CCDEFiv, FRiv, FRDEFiv, MGC, SPD, Total FROM mons WHERE user_id = '{str(ctx.author.id)}' and num = '{int(select)}' ")
        result = conn.fetchone()
        print(result[1])

        cursor = db.cursor()
        cursor.execute(f"SELECT name, image, hp, CC, CC_DEF, FR, FR_DEF, MGC, SPD FROM mons WHERE name = '{result[1]}'")
        cur_result = cursor.fetchone()
        print(cur_result)
        image = cur_result[1]
        print(type(image))
        bs_hp = cur_result[2]
        bs_cc = cur_result[3]
        bs_ccdef = cur_result[4]
        bs_fr = cur_result[5]
        bs_frdef = cur_result[6]
        bs_mgc = cur_result[7]
        bs_spd = cur_result[8]
        lvl = result[0]
        name = result[1]
        hpiv = result[2]
        CCiv = result[3]
        CCDEFiv = result[4]
        FRiv = result[5]
        FRDEFiv = result[6]
        MGC = result[7]
        SPD = result[8]
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(
        color=random.choice(culorz),
        timestamp=ctx.message.created_at,
        title=f"{ctx.author}'s Level {lvl} {select}!",
        )
        """int(round(int((stat) * int(level)) + int(stativ)*int(lvl))) / 350 if is health than /100"""
        embed.add_field(name=f"**HP**:", value=f"**IV**:`{int(hpiv)}`| {(round(int(bs_hp) * int(lvl)) + ((int(hpiv)*int(lvl)) / 100))} \n")
        embed.add_field(name=f"**Close Combat**:", value=f"**IV**:`{int(CCiv)}`| {math.floor(round(int(bs_cc) * int(lvl)) + ((int(CCiv)*int(lvl)) / 350))} \n")
        embed.add_field(name=f"**CC Defence**:", value=f"**IV**:`{int(CCDEFiv)}`| {math.floor(round(int(bs_ccdef) * int(lvl)) + ((int(CCDEFiv)*int(lvl))) / 350)} \n")
        embed.add_field(name=f"**Far Range**:", value=f"**IV**:`{int(FRiv)}`| {math.floor(round(int(bs_fr) * int(lvl)) + ((int(FRiv)*int(lvl)) / 350))} \n")
        embed.add_field(name=f"**FR Defence**:", value=f"**IV**:`{int(FRDEFiv)}`| {math.floor(round(int(bs_frdef) * int(lvl)) + ((int(FRDEFiv)*int(lvl)) / 350))} \n")
        embed.add_field(name=f"**Magic**:", value=f"**IV**:`{int(MGC)}`| {math.floor(round(int(bs_mgc) * int(lvl)) + ((int(MGC)*int(lvl)) / 350))} \n")
        embed.add_field(name=f"**Speed**:", value=f"**IV**:`{int(SPD)}`| {math.floor(round(int(bs_spd) * int(lvl)) + ((int(SPD)*int(lvl)) / 350))} \n")
        embed.set_image(url=image)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
# This adds The cog to the bot
