import discord
from discord.ext import commands, tasks

import random
import sqlite3

import time

class FX(commands.Cog):
    def __init__(self, bot):
        # self means the variable is usable throughout the cog
        self.bot = bot
        # change the topic for new cogs!
        self.topic = 'FX'
        self.CUZ_IT_WONT_WORK = ''

        """Effects Cog"""

    @commands.command()
    async def merge(self, ctx, arg, arg1):
        db = sqlite3.connect('users.sqlite')
        c = db.cursor()
        conn = db.cursor()
        c2 = db.cursor()
        conn.execute(f"SELECT total, selected FROM usr WHERE user_id = '{ctx.author.id}'")
        userinfo = conn.fetchone()
        c.execute(f"SELECT num, Level, HPiv, CCiv, CCDEFiv, FRiv, FRDEFiv, MGC, SPD, xp, Name FROM mons WHERE user_id = '{ctx.author.id}' and num = '{int(arg)}'")
        c2.execute(f"SELECT num, Level, HPiv, CCiv, CCDEFiv, FRiv, FRDEFiv, MGC, SPD, xp, Name FROM mons WHERE user_id = '{ctx.author.id}' and num = '{int(arg1)}'")
        givento = c.fetchone()
        giveto = c2.fetchone()
        if userinfo[1] == giveto[10]:
            await ctx.send("You Can't Merge Your Selected Weebmon!")
        if givento or giveto is None:
            await ctx.send("You have Either not Started yet or Have Given Invalid Arguments!!")
        end_lvl = givento[1]+giveto[1]
        end_hp = givento[2]+giveto[2]
        end_cc = givento[3]+giveto[3]
        end_ccdef = givento[4]+giveto[4]
        end_fr = givento[5]+giveto[5]
        end_frdef = givento[6]+giveto[6]
        end_mgc = givento[7]+giveto[7]
        end_spd = givento[8]+giveto[8]
        end_xp = givento[9]+giveto[9]
        name = givento[10]
        name1 = giveto[10]
        if end_hp > 31:
            end_hp = 31
        if end_cc > 31:
            end_cc = 31
        if end_ccdef > 31:
            end_ccdef = 31
        if end_fr > 31:
            end_fr = 31
        if end_frdef > 31:
            end_frdef = 31
        if end_mgc > 31:
            end_mgc = 31
        if end_spd > 31:
            end_spd = 31
        if end_lvl > 100:
            end_lvl = 100
        sql = ("UPDATE mons SET Level = ?, xp = ?, HPiv = ?, CCiv = ?, CCDEFiv = ?, FRiv = ?, FRDEFiv = ?, MGC = ?, SPD = ? WHERE user_id = ? and num = ?")
        val = (end_lvl, end_xp, end_hp, end_cc, end_ccdef, end_fr, end_frdef, end_mgc, end_spd, str(ctx.author.id), arg)
        c.execute(sql, val)
        db.commit()
        sql1 = ("UPDATE mons SET user_id = ?, Name = ?, xp = ?, HPiv = ?, CCiv = ?, CCDEFiv = ?, FRiv = ?, FRDEFiv = ?, MGC = ?, SPD = ? WHERE user_id = ? and num = ?")
        val1 = (None, None, None, None, None, None, None, None, None, None, str(ctx.author.id), arg1)
        c2.execute(sql1, val1)
        db.commit()
        sql2 = ("UPDATE usr SET total = ? WHERE user_id = ?")
        val2 = (int(userinfo[0])-1, str(ctx.author.id))
        conn.execute(sql2, val2)
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at, title=f"{ctx.author}:`You Have Sacrificed {arg1} To Power up {arg}!`")

        await ctx.send(embed=embed)
        db.commit()
        db.close()

    @commands.command()
    async def equip(self, ctx, arg, arg1):
        db = sqlite3.connect('users.sqlite')
        c = db.cursor()
        conn = db.cursor()
        conn.execute(f"SELECT item FROM bag WHERE user_id = '{ctx.author.id}' and item = '{arg1}'")
        item = conn.fetchone()
        if item is None:
            await ctx.send("Invalid Item Passed!")
        c.execute(f"SELECT item, num FROM mons WHERE user_id = '{ctx.author.id}' and num = '{arg}'")
        mon = c.fetchone()
        sql = ("UPDATE mons SET item = ? WHERE user_id = ? and num = ?")
        val = (item[0], str(ctx.author.id), arg)
        c.execute(sql, val)
        db.commit()
        sql1 = ("UPDATE bag SET user_id = ?, item = ? WHERE user_id = ? and item = ?")
        val1 = (None, None, str(ctx.author.id), arg1)
        conn.execute(sql1, val1)
        await ctx.send("Item Equipped!")
        db.commit()
        db.close()

    @commands.command()
    async def bag(self, ctx):
        db = sqlite3.connect('users.sqlite')
        c = db.cursor()
        c.execute(f"SELECT item FROM bag WHERE user_id = '{ctx.author.id}'")
        items = c.fetchall()
        run = 0
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at, title=f"<@{ctx.author.id}>'s Bag!")
        for x in items:
            run += 1
            embed.add_field(name=run, value=items[run][0] + "\n")
        await ctx.send(embed=embed)

    @commands.command()
    async def botinfo(self, ctx):
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at, title=self.bot.user.name, url="https://discordapp.com/api/oauth2/authorize?client_id=633033797205622832&permissions=2147352001&scope=bot", inline=False)
        embed.add_field(name='Library', value=f"Discord.py Rewrite (`{discord.__version__}`)", inline=False)
        embed.add_field(name=f"Dev(s)", value='<@361628174842593280> & <@462416556853559306>', inline=False)
        embed.add_field(name=f'Ping', value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        embed.add_field(name="Python Version", value="3.8a", inline=False)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)


    @commands.command()
    async def form(self, ctx, arg, arg1):
        db = sqlite3.connect('users.sqlite')
        main = sqlite3.connect('mons.sqlite')
        x = main.cursor()
        c = db.cursor()
        z = main.cursor()
        c.execute(f"SELECT name FROM mons WHERE num = '{arg}' and user_id = '{ctx.author.id}'")
        usr_mon = c.fetchone()
        if usr_mon is None:
            await ctx.send("Either you Haven't Started yet or you Have Passed a Invalid Weebmon Number!")
        x.execute(f"SELECT number FROM mons WHERE name = '{usr_mon[0]}'")
        mon_info = x.fetchone()
        z.execute(f"SELECT name FROM forms WHERE comp = '{mon_info[0]}' and name = '{arg1}'")
        form = z.fetchone()
        if form is None:
            await ctx.send("Invalid Form Passed!")
        ur_mean = "true"
        sql = ("UPDATE mons SET name = ? form = ? WHERE num = ? and user_id = ?")
        val = (form[0], ur_mean, arg, str(ctx.author.id))
        c.execute(sql, val)
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)
        embed.add_field(name="New Form!", value=f"You Have Changed Your {usr_mon[0]} to {form[0]}!")
        await ctx.send(embed=embed)
        db.commit()
        db.close()
        main.close()

    @commands.command()
    async def ultralize(self, ctx):
        pass


def setup(bot):
    bot.add_cog(FX(bot))
