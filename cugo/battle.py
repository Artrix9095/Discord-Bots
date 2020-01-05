import discord
from discord.ext import commands

import sqlite3
import math

import time
import random

import asyncio
import json

# COG setup code

class Battle(commands.Cog):
    """Battle your friends!"""
    def __init__(self, bot):
        self.bot = bot
        self.battlelist = {}

        self.bot.loop.create_task(self.save_battle())

        with open(r'./battle.json', 'r') as f:
            self.battle = json.load(f)

    async def save_battle(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(r'./battle.json', 'w') as f:
                json.dump(self.battle, f, indent=4)
            asyncio.sleep(5)
    class stats(object):
        """Class stats within battle class for gaining stats of a user."""

        def __init__(self, arg):
            super(getstats, self).__init__()
            self.arg = arg
        def getstats(self, id):
            db = sqlite3.connect('users.sqlite')
            main = sqlite3.connect('mon.sqlite')
            c = db.cursor()
            c.execute(f"SELECT selected FROM usr WHERE user_id = '{id}'")
            c_result = c.fetchone()
            conn = db.cursor()
            # Ok Now we have optained the user's information now to get the character's information
            if c_result is None:
                return False
            elif not c_result is None:
                select = c_result[0]
                conn.execute(f"SELECT Level, Name, HPiv, CCiv, CCDEFiv, FRiv, FRDEFiv, MGC, SPD, Total FROM mons WHERE user_id = '{str(id)}' and num = '{int(select)}' ")
                result = conn.fetchone()
                print(result[1])
                # Ok looks like we've gotten the IVS now time for the base stats
                cursor = db.cursor()
                cursor.execute(f"SELECT name, image, hp, CC, CC_DEF, FR, FR_DEF, MGC, SPD FROM mons WHERE name = '{result[1]}'")
                cur_result = main.fetchone()
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
                # Gotten All the base stats now for stat math
                total_hp = math.floor((round(int(bs_hp) * int(lvl)) + ((int(hpiv)*int(lvl)) / 100)))
                total_cc = math.floor((round(int(bs_cc) * int(lvl)) + ((int(CCiv)*int(lvl)) / 350)))
                total_ccdef = math.floor((round(int(bs_ccdef) * int(lvl)) + ((int(CCDEFiv)*int(lvl)) / 350)))
                total_fr = math.floor((round(int(bs_fr) * int(lvl)) + ((int(FRiv)*int(lvl)) / 350)))
                total_frdef = math.floor((round(int(bs_frdef) * int(lvl)) + ((int(FRDEFiv)*int(lvl)) / 350)))
                total_mgc = math.floor((round(int(bs_mgc) * int(lvl)) + ((int(MGC)*int(lvl)) / 350)))
                total_spd = math.floor((round(int(bs_spd) * int(lvl)) + ((int(SPD)*int(lvl)) / 350)))
                # Finished Math Now we add all this information to a list so we can access it in a command
                total = [total_hp, total_cc, total_ccdef, total_fr, total_frdef, total_mgc, total_spd]
                etc = [image, lvl, name]
                # Now to return the information
                return [total, etc]

        def dmgbar(self, monhp: int):
            nano = 0
            bruv = []
            run = 0
            bar = ''
            while not (monhp/5) < nano:
                bruv += str(nano)
                nano += 1
            for x in bruv:
                run += 1
                bar += '='
                if run > 25:
                    break
            return bar
        def death(self, battleid, id):
            if 0 >= self.battle[battleid][id]['weebmon']['stats']['hp']:
                return True
            else:
                return False
        def dmg(self, user_id, battleid, type):
            crit = random.randint(30, 100)
            stats = self.battle[battleid][user_id]['stats']
            dmg = math.floor((round(stats[type]*crit))/350)
            return dmg
        def end(self, battle_id, winnerid):
            del self.battle[battle_id]
            msg = 'Congrats <@{}> You Won the duel!'.format(winnerid)
            return msg







    @commands.command()
    async def duel(self, ctx, user: discord.user):
        """Duel Command!"""
        randomgen = random.randint(1, 300)
        randomgen2 = random.randint(2, 301)
        battleid = str(math.floor(((ctx.author.id/50)*(user.id/50))/randomgen)*randomgen2)
        await ctx.send('Getting Things Ready...')
        usrinfo = Battle.stats.getstats(self, user.id)
        authinfo = Battle.stats.getstats(self, ctx.author.id)
        usrstats = usrinfo[0]
        authstats = authinfo[0]
        usretc = usrinfo[1]
        authetc = authinfo[1]
        await ctx.send('Configuring Database...')
        self.battle[battleid] = {
            f'{ctx.author.id}': {
                'moved': False,
                'move': None,
                'weebmon': {
                    'name': authetc[2],
                    'level': authetc[1],
                    'image': authetc[0],
                    'stats': {
                        'hp': authstats[0],
                        'cc': authstats[1],
                        'ccdef': authstats[2],
                        'fr': authstats[3],
                        'frdef': authstats[4],
                        'mgc': authstats[5],
                        'spd': authstats[6]
                    }
                }
            },
            f'{user.id}': {
                'moved': False,
                'move': None,
                'weebmon': {
                    'name': usretc[2],
                    'level': usretc[1],
                    'image': usretc[0],
                    'stats': {
                        'hp': usrstats[0],
                        'cc': usrstats[1],
                        'ccdef': usrstats[2],
                        'fr': usrstats[3],
                        'frdef': usrstats[4],
                        'mgc': usrstats[5],
                        'spd': usrstats[6]
                    }
                }
            }
        }
        # remove the ctx.send(self.battle[battleid])
        await ctx.send("```json\n{}\n```".format(self.battle[battleid]))
        await ctx.send('Done!')
        await user.send(battleid)
        await ctx.author.send(battleid)
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=random.choice(culorz))
        embed.add_field(name=f"<@{user.id}>'s {usretc[2]}",
        value=Battle.stats.dmgbar(self.battle[battleid][ctx.author.id]['weebmon']['stats']['hp']))
        embed.set_image(url=usretc[0])
        await ctx.send(embed=embed)
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=random.choice(culorz))
        embed.add_field(name=f"<@{ctx.author.id}>'s {authetc[2]}",
        value=Battle.stats.dmgbar(self.battle[battleid][user.id]['weebmon']['stats']['hp']))
        await ctx.send(embed=embed)


    @commands.command()
    async def move(self, ctx, movetype: str, battle_id: str):
        """Make Your Move In Battle!"""
        if not battle_id in list(self.battle):
            await ctx.send(f'No Battle With the ID: "{battle_id}"!')
            return
        elif battle_id in list(self.battle):
            if not str(ctx.author.id) in list(self.battle[battle_id]):
                await ctx.send('Your not in this battle!')
                return
            elif str(ctx.author.id) in list(self.battle[battle_id]):
                if movetype in ['mgc', 'fr', 'cc']:
                    if movetype == 'mgc':
                        type = 'mgc'
                    elif movetype == 'fr':
                        type ='fr'
                    elif movetype == 'cc':
                        type = 'cc'
                    id = self.battle[battle_id]
                    hm = list(id)
                    for x in hm:
                        if x == str(ctx.author.id):
                            pass
                        else:
                            otheruser = self.battle[battle_id][x]
                    all = self.battle[battle_id]
                    await ctx.send(otheruser)
                    self.battle[battle_id][str(ctx.author.id)]['moved'] = True
                    self.battle[battle_id][str(ctx.author.id)]['move'] = movetype
                    await ctx.send('Waiting for <@{}>'.format(otheruser))
                    if self.battle[battle_id][str(ctx.author.id)]['moved'] == True and self.battle[battle_id][otheruser]['moved'] == True:
                        if all[str(ctx.author.id)]['stats']['spd'] > all[otheruser]['stats']['spd']:
                            authordmg = int(Battle.stats.dmg(self, ctx.author.id, battle_id, self.battle[battle_id][str(ctx.author.id)]['move']))
                            #ctx.author is faster
                            all[otheruser]['stats']['hp'] -= authordmg
                            await ctx.send("<@{}>'s Weebmon Dealt: `{}` DMG!".format(ctx.author.id, authordmg))
                            if not Battle.stats.death(self, battle_id, otheruser):
                                otherdmg = int(Battle.stats.dmg(self, otheruser, battle_id, self.battle[battle_id][otheruser]['move']))
                                all[str(ctx.author.id)]['stats']['hp'] -= otherdmg
                                await ctx.send("<@{}>'s Weebmon Dealt: `{}` DMG!".format(otheruser, otherdmg))
                                if not Battle.stats.death(self, battle_id, str(ctx.author.id)):
                                    self.battle[battle_id][str(ctx.author.id)]['moved'] = False
                                    self.battle[battle_id][str(ctx.author.id)]['move'] = None
                                    self.battle[battle_id][otheruser]['moved'] = False
                                    self.battle[battle_id][otheruser]['move'] = None
                                    culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                                    embed = discord.Embed(color=random.choice(culorz))
                                    embed.add_field(name=f"<@{otheruser}>'s {all[otheruser]['name']}",
                                    value=Battle.stats.dmgbar(self.battle[battle_id][otheruser]['weebmon']['stats']['hp']))
                                    embed.set_image(url=all[otheruser]['image'])
                                    await ctx.send(embed=embed)
                                    embed = discord.Embed(color=random.choice(culorz))
                                    embed.add_field(name=f"<@{ctx.author.id}>'s {all[ctx.author.id]['name']}",
                                    value=Battle.stats.dmgbar(self.battle[battle_id][ctx.author.id]['weebmon']['stats']['hp']))
                                    await ctx.send(embed=embed)
                                    return
                                else:
                                    await ctx.send(Battle.stats.end(self, battle_id, otheruser))
                                    return
                            else:
                                await ctx.send(Battle.stats.end(self, battle_id, ctx.author.id))
                                return
                        else:
                            authordmg = int(Battle.stats.dmg(self, ctx.author.id, battle_id, self.battle[battle_id][str(ctx.author.id)]['move']))
                            #otheruser is faster
                            otherdmg = int(Battle.stats.dmg(self, otheruser, battle_id, self.battle[battle_id][otheruser]['move']))
                            all[str(ctx.author.id)]['stats']['hp'] -= otherdmg
                            await ctx.send("<@{}>'s Weebmon Dealt: `{}` DMG!".format(otheruser, otherdmg))
                            """all[otheruser]['stats']['hp'] -= authordmg
                            await ctx.send("<@{}>'s Weebmon Dealt: `{}` DMG!".format(ctx.author.id, authordmg))"""
                            if not Battle.stats.death(self, battle_id, ctx.author.id):
                                all[otheruser]['stats']['hp'] -= authordmg
                                await ctx.send("<@{}>'s Weebmon Dealt: `{}` DMG!".format(ctx.author.id, authordmg))
                                """all[str(ctx.author.id)]['stats']['hp'] -= otherdmg
                                await ctx.send("<@{}>'s Weebmon Dealt: `{}` DMG!".format(otheruser, otherdmg))"""
                                if not Battle.stats.death(self, battle_id, otheruser):
                                    self.battle[battle_id][str(ctx.author.id)]['moved'] = False
                                    self.battle[battle_id][str(ctx.author.id)]['move'] = None
                                    self.battle[battle_id][otheruser]['moved'] = False
                                    self.battle[battle_id][otheruser]['move'] = None
                                    culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                                    embed = discord.Embed(color=random.choice(culorz))
                                    embed.add_field(name=f"<@{otheruser}>'s {all[otheruser]['name']}",
                                    value=Battle.stats.dmgbar(self.battle[battle_id][otheruser]['weebmon']['stats']['hp']))
                                    embed.set_image(url=all[otheruser]['image'])
                                    await ctx.send(embed=embed)
                                    embed = discord.Embed(color=random.choice(culorz))
                                    embed.add_field(name=f"<@{ctx.author.id}>'s {all[ctx.author.id]['name']}",
                                    value=Battle.stats.dmgbar(self.battle[battle_id][ctx.author.id]['weebmon']['stats']['hp']))
                                    await ctx.send(embed=embed)
                                    return
                                else:
                                    await ctx.send(Battle.stats.end(self, battle_id, otheruser))
                                    return
                            else:
                                await ctx.send(Battle.stats.end(self, battle_id, ctx.author.id))
                                return

                else:
                    await ctx.send('Invalid Movetype')






def setup(bot):
    bot.add_cog(Battle(bot))
