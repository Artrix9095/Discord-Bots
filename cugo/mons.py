import discord
from discord.ext import commands

import random as rand

import json
import sqlite3

class Mons(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    with open("./moves.artrix", "r") as f:
        self.moves = json.load(f)

    @commands.command(pass_context=True, aliases=['learn skill'])
    async def learn_skill(self, ctx, __num__: int=None, *, move: str=None):
        if __num__ is None:
            await ctx.send(f'`learn skill slot_number skill`')
        elif __num__ is not None:
            if move is None:
                await ctx.send('State A Skill to learn!')
            elif move is not None:
                if __num__ > 4:
                    await ctx.send("Numbers 1-4!")
                elif not __num__ > 4:
                    usr = sqlite3.connect('users.sqlite').cursor()
                    mon = sqlite3.connect('mons.sqlite').cursor()
                    db = sqlite3.connect('users.sqlite')
                    exe = db.cursor()
                    usr.execute("SELECT selected FROM usr WHERE user_id = '{}'".format(str(ctx.author.id)))
                    selected = usr.fetchone()
                    if selected is None:
                        await ctx.send("You have to start first!")
                    usr.execute(f"SELECT Name FROM mons WHERE user_id = '{str(ctx.author.id)}' and num = '{int(selected[0])}'")
                    moninfo = usr.fetchone()
                    mon.execute(f"SELECT number FROM mons WHERE name = '{moninfo[0]}'")
                    num = mon.fetchone()
                    if move in self.moves[0]:
                        if str(num) in self.moves[0][move]['Com']:
                            exe.execute(f"SELECT user_id FROM moves WHERE user_id = '{str(ctx.author.id)}' and num = '{int(selected[0])}'")
                            moveset = exe.fetchone()
                            if moveset is None:
                                sql = (f"INSERT INTO moves(user_id, num, move{__num__}) VALUES(?,?,?)")
                                val = (str(ctx.author.id), selected[0], move)
                            elif moveset is not None:
                                sql = (f"UPDATE moves SET move{__num__} = ? WHERE user_id = ? and num = ?")
                                val = (move, str(ctx.author.id), selected[0])
                            exe.execute(sql, val)
                            await ctx.send(f"{moninfo[0]} Has Learned {move}! \n `skill slot{__num__}`")
                            db.commit()
                        else:
                            await ctx.send(f"{moninfo[0]} Can't Learn {move}!")
    @commands.command()
    async def skillset(self, ctx, page:int=None):
        if page is None:
            usr = sqlite3.connect('users.sqlite').cursor()
            mon = sqlite3.connect('mons.sqlite').cursor()
            usr.execute(f"SELECT selected FROM usr WHERE user_id = '{str(ctx.author.id)}'")
            select = usr.fetchone()
            usr.execute(f"SELECT num, Name FROM mons WHERE user_id = '{str(ctx.author.id)}' and num = '{select[0]}'")
            moninfo = usr.fetchone()
            mon.execute(f"SELECT number FROM mons WHERE name = '{moninfo[1]}'")
            __mon__ = mon.fetchone()
            numberz = str(__mon__[0])
            __movenum__ = 0
            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
            embed = discord.Embed(color=random.choice(culorz))
            embed.set_footer(title="Page 1")
            for x in self.moves[1]:
                lol = list(self.moves[0])
                movename = lol[__movenum__]
                __movenum__ += 1
                for numberz in self.moves[0][movename]['Com']:
                    if __movenum__ < 25:
                        dmg = self.moves[0][movename]['DMG']
                        name = self.moves[0][movename]['Name']
                        type = self.moves[0][movename]['type']
                        embed.add_field(name=__movenum__, value=f"{name} - DMG: `{dmg}`, Type: `{type}`")
                    elif __movenum__ > 25:
                        return
            await ctx.send(embed=embed)
        elif page is not None:
            usr = sqlite3.connect('users.sqlite').cursor()
            mon = sqlite3.connect('mons.sqlite').cursor()
            usr.execute(f"SELECT selected FROM usr WHERE user_id = '{str(ctx.author.id)}'")
            select = usr.fetchone()
            usr.execute(f"SELECT num, Name FROM mons WHERE user_id = '{str(ctx.author.id)}' and num = '{select[0]}'")
            moninfo = usr.fetchone()
            mon.execute(f"SELECT number FROM mons WHERE name = '{moninfo[1]}'")
            __mon__ = mon.fetchone()
            __movenum__ = page
            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
            embed = discord.Embed(color=random.choice(culorz))
            embed.set_footer(title="Page {}".format(page))
            for x in self.moves[1]:
                movename = str(list(self.moves[0][__movenum__]))
                __movenum__ += 1
                for str(__mon__[0]) in self.moves[0][movename]['Com']:
                    if __movenum__ < page+25:
                        dmg = self.moves[0][movename]['DMG']
                        name = self.moves[0][movename]['Name']
                        type = self.moves[0][movename]['type']
                        embed.add_field(name=__movenum__+1, value=f"{name} - DMG: `{dmg}`, Type: `{type}`")
                    elif __movenum__ > page+25:
                        return
            await ctx.send(embed=embed)


    @commands.command()
    async def skills(self, ctx):
        usr = sqlite3.connect('users.sqlite').cursor()
        usr.execute(f"SELECT selected FROM usr WHERE user_id = '{str(ctx.author.id)}'")
        select = usr.fetchone()
        usr.execute(f"SELECT num, Name FROM mons WHERE user_id = '{str(ctx.author.id)}' and num = '{select[0]}'")
        moninfo = usr.fetchone()
        usr.execute(f"SELECT move1, move2 move3, move4 FROM moves WHERE user_id = '{str(ctx.author.id)}' and num = '{select[0]}'")
        moveset = usr.fetchone()
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=random.choice(culorz))
        run = 0
        for x in moveset:
            embed.add_field(name=f"Move {run+1}:", value=f'{moveset[run]}\n')
            run+=1
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Mons(bot))
