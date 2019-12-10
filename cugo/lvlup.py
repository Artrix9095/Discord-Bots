import discord
from discord.ext import commands, tasks

import random
import math

import sqlite3

class LvlUp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def select(self, ctx, arg):
        # c is character information Conn is user information
        db = sqlite3.connect('users.sqlite')
        c = db.cursor()
        conn = db.cursor()
        conn.execute(f"SELECT user_id, selected FROM usr WHERE user_id = '{ctx.author.id}'")
        Con = conn.fetchone()
        if Con is None:
            await ctx.send(f"You Can't Select {arg} Because you Haven't Started yet!")
        c.execute(f"SELECT user_id, num FROM mons WHERE user_id = '{ctx.author.id}' and num = '{int(arg)}'")
        result = c.fetchone()
        if result is None:
            await ctx.send("You Don't Have any Weebmons With That Number!")
        sql = ("UPDATE usr SET selected = ? WHERE user_id = ?")
        val = (arg, str(ctx.author.id))
        conn.execute(sql, val)
        await ctx.send(f"You have Selected {arg}!")
        db.commit()
        db.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        db = sqlite3.connect('users.sqlite')
        c = db.cursor()
        x = db.cursor()
        x.execute(f"SELECT selected FROM usr WHERE user_id = '{str(message.author.id)}'")
        selected = x.fetchone()
        if selected is None:
            return
        c.execute(f"SELECT Level, xp, Name FROM mons WHERE user_id = '{str(message.author.id)}' and num = '{selected[0]}'")
        mon = c.fetchone()
        sql = ("UPDATE mons SET xp = ? WHERE user_id = ? and num = ?")
        val = (mon[1]+2, str(message.author.id), selected[0])
        c.execute(sql, val)
        db.commit()
        if mon[0] >= 100:
            return
        if mon[1] >= (mon[0]*mon[0]) / 10:
            try:
                sql1 = ("UPDATE mons SET xp = ?, Level = ? WHERE user_id = ? and num = ?")
                val1 = (0, mon[0]+1, str(message.author.id), selected[0])
                c.execute(sql1, val1)
                db.commit()
                culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                embed = discord.Embed(color=random.choice(culorz))
                embed.add_field(name="Congrats!", value=f"Your {mon[2]} has Leveld up to Level {mon[0]+1}!")
                await message.channel.send(embed=embed)
                db.close()
            except:
                print("err")
def setup(bot):
    bot.add_cog(LvlUp(bot))
