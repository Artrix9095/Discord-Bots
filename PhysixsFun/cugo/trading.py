import discord
from discord.ext import commands, tasks

import random
import time

import sqlite3
import json

class Trading(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.topic = 'Trade'

    @commands.command()
    async def give(self, ctx, arg, user:discord.User):
        if arg == int() or float():
            db = sqlite3.connect('users.json')
            c = db.cursor()
            conn = db.cursor()
            conn.execute(f"SELECT coins FROM usr WHERE user_id = '{ctx.author.id}'")
            c.execute(f"SELECT coins FROM usr WHERE user_id = '{user.id}'")
            Con = conn.fetchone()
            result = c.fetchone()
            if Con or result is None:
                await ctx.send("You Haven't Started yet!")
            if arg > Con[0]:
                await ctx.send(f"You dont have *{arg}* Coins!")
            sql = ("UPDATE usr SET coins = ? WHERE user_id = ?")
            val = (int(Con[0])-arg, str(ctx.author.id))
            conn.execute(sql, val)
            db.commit()
            sql1 = ("UPDATE usr SET coins = ? WHERE user_id = ?")
            val1 = (int(result[0])+arg, str(user.id))
            embed = discord.Embed(color=random.choice(culorz))
            embed.add_field(name=self.topic, value=f"<@{ctx.author.id}> has Given <@{user.id}> *{arg}* Coins!")
            await ctx.send(embed=embed)
            db.commit()
            db.close()

    
def setup(bot):
    bot.add_cog(Trading(bot))
