import discord
from discord.ext import tasks, commands

import time
import random

import sqlite3

import asyncio

# COG setup code

class Catch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.broadcast = False
        self.spawn = ''
        self.counter = 0
        self.Zz = None



    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        self.counter += 1
        print(self.counter)
        if message.content.startswith(">"):
            return
        if self.counter >= 15:
            x = sqlite3.connect('servers.sqlite').cursor()
            x.execute(f"SELECT channel_id FROM channel WHERE server_id = '{str(message.guild.id)}'")
            server = x.fetchone()
            if server is None:
                channel = message.channel
            elif server is not None:
                channel = self.bot.get_channel(id=int(server[0]))
            rarez = random.randint(1,5000)
            if rarez == 4999:
                self.Zz = 1, 2, 4, 7, 8, 9, 10, 11, 
            elif rarez <= 100:
                self.Zz = 0, 3, 6, 16, 17, 18, 20
            elif rarez > 100 and not rarez == 4999:
                self.Zz = 5, 7, 12, 13, 14, 15, 19
            pz = random.choice(self.Zz)
            random_sleep = 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,30
            db = sqlite3.connect('mons.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT name, image FROM mons')
            result = cursor.fetchall()
            image = result[pz][1]
            monname = result[pz][0]
            self.counter -= self.counter

            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
            embed = discord.Embed(color=random.choice(culorz), timestamp=message.created_at)

            embed.set_author(name=f"{monname}! - {str(message.author)[:-5]}", icon_url=self.bot.user.avatar_url)

            embed.set_image(url=image)

            await channel.send(embed=embed)
            self.spawn = monname

            self.broadcast = True

            self.Zz = None
        else:
            return

    @commands.command()
    async def tame(self, ctx, arg):
        if self.broadcast == True:
            if arg == self.spawn:
                try:
                    db = sqlite3.connect('users.sqlite')
                    conn = db.cursor()
                    c = db.cursor()
                    c.execute(f"SELECT user_id, total FROM usr WHERE user_id = '{ctx.author.id}'")
                    result = c.fetchone()
                    total = int(result[1])
                    if result is None:
                        await ctx.send("You Haven't Started yet!")
                    ivs = 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31
                    hpiv = random.choice(ivs)
                    CCiv = random.choice(ivs)
                    CCDEFiv = random.choice(ivs)
                    FRiv = random.choice(ivs)
                    FRDEFiv = random.choice(ivs)
                    MGC = random.choice(ivs)
                    SPD = random.choice(ivs)
                    sql1 = (f"INSERT INTO mons(user_id, Level, xp, Name, HPiv, CCiv, CCDEFiv, FRiv, FRDEFiv, MGC, SPD, num, item) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)")
                    val1 = (str(ctx.author.id), 5, 0, str(arg), int(hpiv), int(CCiv), int(CCDEFiv), int(FRiv), int(FRDEFiv), int(MGC), int(SPD), int(total+1), None)
                    conn.execute(sql1, val1)
                    sql = (f"UPDATE usr SET total = ? WHERE user_id = ?")
                    val = (total + 1, str(ctx.author.id))
                    c.execute(sql, val)
                    db.commit()
                    db.close()
                except Exception as error:
                    print(error)
                else:
                    culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                    embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)
                    embed.add_field(name='Congrats!', value=f'<@{ctx.author.id}> Has Tamed a {arg}!')
                    await ctx.send(embed=embed)

            else:
                await ctx.send(f"{arg} Ins't the Correct Weebmon!")
        else:
            await ctx.send("Nothing To Tame!")



def setup(bot):
    bot.add_cog(Catch(bot))
