import discord
from discord.ext import commands

import random
import math

import time
import sqlite3

# COG setup code

# THE MAIN FILE IS THE TRUNK AND THE COG IS THE BRANCH
class Lvl(commands.Cog): # THE MAIN FILE IS THE TRUNK AND THE COG IS THE BRANCH
    def __init__(self, bot): # THE MAIN FILE IS THE TRUNK AND THE COG IS THE BRANCH
        self.bot = bot
    """

    @commands.Cog.listener()
    # If it doesn't work you could try to change all the 'message.author.guild.id' to 'message.guild.id'
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        else:
            db = sqlite3.connect('LEVEL.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id FROM levels WHERE guild_id = '{message.author.guild.id}' and user_id = '{message.author.id}'")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO levels(guild_id, user_id, exp, lvl) VALUES(?,?,?,?)")
                val = (message.author.guild.id, message.author.id, 2, 0)
                cursor.execute(sql, val)
                db.commit()
            else:
                cursor.execute(f"SELECT user_id, exp, lvl  FROM levels WHERE guild_id = '{message.author.guild.id}' and user_id = '{message.author.id}'")
                result1 = cursor.fetchone()
                # if it doesnt work this is probably the reason why, change float to int. (tests)
                exp = float(result1[1])
                sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")
                val = (exp + 2, str(message.author.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()

                cursor.execute(f"SELECT user_id, exp, lvl  FROM levels WHERE guild_id = '{message.author.guild.id}' and user_id = '{message.author.id}'")
                result2 = cursor.fetchone()
                # another float instead of int if it doesnt work try to change it
                xp_start = float(result2[1])
                lvl_start = float(result2[2])
                xp_end = float(round(math.floor((5 * lvl_start) - 5)))
                if xp_end < xp_start:
                    guild = message.author.guild.id
                    author = message.author.id
                    # not following directions so.... if it doesnt work delete the lvl_start += 1 and add a {lvl start + 1} in the embed
                    lvl_start += round(1)
                    if lvl_start >= 10:
                        xp_end = math.floor(lvl_start * lvl_start)
                    mention = message.author.mention
                    channel = message.channel.send
                    culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                    embed = discord.Embed(color=random.choice(culorz), timestamp=message.created_at)

                    embed.set_author(name=f"Level Up! - {message.author}", icon_url=self.bot.user.avatar_url)

                    embed.set_thumbnail(url=message.author.avatar_url)

                    embed.add_field(name=f'{message.author} Has Leveled up to Level', value=f'{round(lvl_start)}')

                    await channel(embed=embed)

                    sql = ("UPDATE levels SET lvl = ? WHERE guild_id = ? and user_id = ?")

                    val = (int(lvl_start + 0), str(guild), str(author))
                    cursor.execute(sql, val)
                    db.commit()
                    sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")

                    val = (0, str(guild), str(author))
                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()

    @commands.command(pass_context=True, aliases=['r', 'R','rank' 'lvl', 'LVL', 'Lvl', 'RANK', 'Rank', 'Level', 'LEVEL'])
    async def level(self, ctx, message, user:discord.User=None):
        if user is not None:
            db = sqlite3.connect('LEVEL.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{ctx.author.guild.id}' and user_id = '{user.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send("This User Doesn't Have a Level")
            elif user is None:
                culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

                embed.set_author(name=f"Level! - {user}", icon_url=self.bot.user.avatar_url)

                embed.set_thumbnail(url=message.author.avatar_url)

                embed.add_field(name=f'{user} Is Currently Level', value=f'{result[2]} \n')
                embed.add_field(name=f'With `{result[1]}` EXP!', value=None)


                await ctx.send(embed=embed)
                cursor.close()
                db.close()

        else:
            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
            embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

            embed.set_author(name=f"Level! - {ctx.author}", icon_url=self.bot.user.avatar_url)

            embed.set_thumbnail(url=message.author.avatar_url)

            embed.add_field(name=f'{ctx.author} Is Currently Level', value=f'{result[2]} \n')
            embed.add_field(name=f'With `{result[1]}` EXP!', value=None)

            await ctx.send(embed=embed)

    """




def setup(bot): # THE MAIN FILE IS THE TRUNK AND THE COG IS THE BRANCH
    bot.add_cog(Lvl(bot))
