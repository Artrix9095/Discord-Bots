import discord
from discord.ext import commands, tasks

import random
import time

import sqlite3
import json

class Customize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def redirect(self, ctx, channel: discord.TextChannel):
        db = sqlite3.connect('servers.sqlite')
        x = db.cursor()
        x.execute(f"SELECT channel_id FROM channel WHERE server_id = '{ctx.guild.id}'")
        server = x.fetchone()
        if server is None:
            sql = ("INSERT INTO channel(server_id, channel_id) VALUES(?,?)")
            val = (str(ctx.guild.id), str(channel.id))
            x.execute(sql, val)
            db.commit()
        elif server is not None:
            sql = ("UPDATE channel SET channel_id = ? WHERE server_id = ?")
            val = (str(channel.id), str(ctx.guild.id))
            x.execute(sql, val)
            db.commit()
        await ctx.send(f"All Spawns Will now be Redirected to {channel.mention}")
        db.close()

        
    @commands.command()
    async def delredirect(self, ctx):
        db = sqlite3.connect('servers.sqlite')
        x = db.cursor()
        x.execute(f"SELECT channel_id FROM channel WHERE server_id = '{ctx.guild.id}'")
        server = x.fetchone()
        if server is None:
            await ctx.send("You have to add a redirect to Delete One!")
        elif server is not None:
            sql = ("UPDATE channel SET channel_id = ?, server_id = ? WHERE server_id = ?")
            val = (None, None, str(ctx.guild.id))
            await ctx.send("Deleted All Redirects to <#{}>!".format(server[0]))
            x.execute(sql, val)
            db.commit()


def setup(bot):
    bot.add_cog(Customize(bot))
