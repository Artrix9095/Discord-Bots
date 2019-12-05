import discord
from discord.ext import commands as cmd
from discord.ext import tasks

import random
import math

import sqlite3
from asyncio import sleep as repeat


# COG setup code

# THE MAIN FILE IS THE TRUNK AND THE COG IS THE BRANCH
class Boss(cmd.Cog):
    def __init__(self, bot):
        # self means the variable is usable throughout the cog
        self.bot = bot
        self.spawnrate = 0
        self.counter = 0


    @tasks.loop(seconds=3600.0)
    async def create_msg(self):
        self.spawnrate = random.randint(1, 10)
        

    @create_msg.before_loop
    async def before_printer(self):
        print('waiting...')
        await self.bot.wait_until_ready()

    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        msg_amount = random.randint(50,150)
        self.counter += msg_amount
        if self.counter >= self.spawnrate:
            self.counter = 0
            x = sqlite3.connect('servers.sqlite').cursor()
            x.execute(f"SELECT channel_id FROM channel WHERE server_id = '{str(message.guild.id)}'")
            server = x.fetchone()
            if server is None:
                channel = message.channel
            elif server is not None:
                channel = self.bot.get_channel(id=int(server[0]))
            pz = random.randint(1, 3)
            db = sqlite3.connect('mons.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT name, image FROM forms')
            result = cursor.fetchall()
            image = result[pz][1]
            monname = result[pz][0]
            lvl = random.randint(70, 250)
            await ctx.send("A Boss has Spawned! Who Dares to Challenge it!")
            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
            embed = discord.Embed(color=random.choice(culorz), timestamp=message.created_at, title=f"It's a Level {lvl} {monname}!")
            embed.set_image(url=image)

            await channel.send(embed=embed)





def setup(bot):
    bot.add_cog(Boss(bot))