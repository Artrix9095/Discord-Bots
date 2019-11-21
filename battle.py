import discord
from discord.ext import commands

import json
import sqlite3

import random

import asyncio
import time

class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # change the topic for new cogs!
        self.topic = 'Battle'
        self.broadcast = False
        self.end = False

        self.bot.loop.create_task(self.save_file())
        # self.bot.loop.create_task(self.save_file()) is an attribute where *.bot and *.loop are folders., *.create_task() is the section, and self.save_file() is paper name.
        # Creates background task

        with open(r"G:\Artrix-botz\PhysixsFun\cugo\battle.json", 'r') as f:
            self.battle = json.load(f)
            # Opens a file battle.json and sets it as a variable, this one if for logging information and writing to battle.json;

        with open(r"G:\Artrix-botz\PhysixsFun\cugo\moninfo.json", 'r') as f:
            self.mon = json.load(f)
            # Opens a file moninfo.json and sets it as a variable, this one is for viewing only, this is where im getting all the information for each character at.

        with open(r"G:\Artrix-botz\PhysixsFun\cugo\ability.json", 'r') as f:
            self.ability = json.load(f)

    # This Uses the background task and saves battle.json every 10 secounds forever until I shutdown the bot
    async def save_file(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(r"G:\Artrix-botz\PhysixsFun\cugo\battle.json", 'w') as f:
                json.dump(self.battle, f, indent=4)
            await asyncio.sleep(10)

    @commands.command()
    async def cancel(self, ctx):
        if ctx.author.id in self.battle:
            self.pun = ctx.author.id
            self.end = True
            self.fite = False


    # This is the command itself
    @commands.command()
    async def duel(self, ctx, user: discord.User = None):
        self.turn = 0
        self.end = False
    # cursor1 is defender, cursor is offender
        if user == None:
            await ctx.send("Please State a User to Duel!")
            print("Error 1")
        else:
            # Setting 2 variables, the offender id and the defender id, the defender id is the one being mentioned the offender id is the one mentioning
            off_id = str(ctx.author.id)
            def_id = str(user.id)
            # Checking if someones try to battle themselve.
            if off_id == def_id:
                await ctx.send("You Can't Battle Yourself!")
                # Checking if One of them is already in a battle
            else:
                # Connecting to the database and grabbing all their info that is listed in the columns so it can be inputed into battle.json
                db = sqlite3.connect('users.sqlite')
                cursor = db.cursor()
                cursor1 = db.cursor()
                cursor.execute(f"SELECT user_id, selected, coins FROM usr WHERE user_id = '{ctx.author.id}'")
                cursor1.execute(f"SELECT user_id, selected, coins FROM usr WHERE user_id = '{user.id}'") # 1 is defender None is offender
                result = cursor.fetchone()
                result1 = cursor1.fetchone()
                # Goes in their information and finds their selected character. 1 is the defender
                selected_mon = str(result[1])
                selected_mon1 = str(result1[1])
                # Grabs their ID out of sqlite3 from column [0] for further troubleshooting.
                id = str(result[0])
                id1 = str(result1[0])
                if id1 or id == None:
                    await ctx.send("You Haven't Started Yet!")
                user_names = str(f"{ctx.author.id}, {user.id}")
                # Checking if they have started
                if selected_mon or selected_mon1 == None:
                    print("Error 2")
                    # Checking if they have a Character selected
                    await ctx.send("Please Select a Weebmon")
                else:
                    hm1 = self.mon[selected_mon1]['AB']
                    hm = self.mon[selected_mon]['AB']
                    # After all the troubleshooting it starts writing to battle.json with the information it collected from the variables and the database
                    self.battle[user_names] = {}
                    self.battle[user_names][off_id] = {}
                    self.battle[user_names][def_id] = {}
                    self.battle[user_names][off_id]['Selected'] = {}
                    self.battle[user_names][def_id]['Selected'] = {}
                    self.battle[user_names][off_id]['Selected']['Name'] = selected_mon1
                    self.battle[user_names][def_id]['Selected']['Name'] = selected_mon
                    self.battle[user_names][off_id]['Selected']['Ability'] = hm1
                    self.battle[user_names][def_id]['Selected']['Ability'] = hm
                    self.battle[user_names][off_id]['Selected']['Type'] = self.mon[selected_mon1]['Type']
                    self.battle[user_names][def_id]['Selected']['Type'] = self.mon[selected_mon]['Type']
                    self.battle[user_names][off_id]['Selected']['HP'] = self.mon[selected_mon1]['HP']
                    self.battle[user_names][def_id]['Selected']['HP'] = self.mon[selected_mon]['HP']
                    self.battle[user_names][off_id]['Selected']['Atk'] = self.mon[selected_mon1]['CC']
                    self.battle[user_names][def_id]['Selected']['Atk'] = self.mon[selected_mon]['CC']
                    self.battle[user_names][off_id]['Selected']['Def'] = self.mon[selected_mon1]['CC DEF']
                    self.battle[user_names][def_id]['Selected']['Def'] = self.mon[selected_mon]['CC DEF']
                    self.battle[user_names][off_id]['Selected']['Fr Rnge'] = self.mon[selected_mon1]['FR']
                    self.battle[user_names][def_id]['Selected']['Fr Rnge'] = self.mon[selected_mon]['FR']
                    self.battle[user_names][off_id]['Selected']['Fr Rnge Def'] = self.mon[selected_mon1]['FR DEF']
                    self.battle[user_names][def_id]['Selected']['Fr Rnge Def'] = self.mon[selected_mon]['FR DEF']
                    self.battle[user_names][off_id]['Selected']['MGC'] = self.mon[selected_mon1]['MGC']
                    self.battle[user_names][def_id]['Selected']['MGC'] = self.mon[selected_mon]['MGC']
                    self.battle[user_names][off_id]['Selected']['Spd'] = self.mon[selected_mon1]['SPD']
                    self.battle[user_names][def_id]['Selected']['Spd'] = self.mon[selected_mon]['SPD']
                    await ctx.send("Getting Things Ready...")
                    # since the file takes 4 secounds to save, Before we can do anything we need to save it, so I added a cooldown
                    time.sleep(4)
                    if self.end == True and self.pun == self.battle[user_names][off_id] or self.battle[user_names][def_id]:
                        if user_names in self.battle:
                                del self.battle[user_names]
                                return False
                    print("Error 3")
                    # Lines 115 to 124 loads the imagery to let them know how their character is doing in the battle.
                    culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                    embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

                    embed.set_author(name=f"Fight! - {ctx.author} & {user.name}", icon_url=self.bot.user.avatar_url)

                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_thumbnail(url=user.avatar_url)

                    embed.add_field(name=f"{ctx.author}'s {self.battle[user_names][off_id]['Selected']['Name']}", value=f"{self.battle[user_names][off_id]['Selected']['HP']}/{self.battle[user_names][off_id]['Selected']['HP']}", inline=True)
                    embed.add_field(name=f"{user.name}'s {self.battle[user_names][def_id]['Selected']['Name']}", value=f"{self.battle[user_names][def_id]['Selected']['HP']}/{self.battle[user_names][def_id]['Selected']['HP']}", inline=True)
                    self.fite = True

                    await ctx.send(embed=embed)
                    await ctx.send("Say Move to move on with the battle! (wait 2 secounds before saying this!)")
                    time.sleep(2)
                    if self.broadcast == True:
                        def_ability = self.battle[user_names][def_id]['Selected']['Ability']
                        off_ability = self.battle[user_names][off_id]['Selected']['Ability']
                        coins = int(result[2])
                        coins1 = int(result1[2])
                        knumz = 20, 30, 40, 50, 60, 70, 80, 90, 100
                        choices = random.choice(knumz)
                        off_spd = self.battle[user_names][off_id]['Selected']['Spd']
                        def_spd = self.battle[user_names][def_id]['Selected']['Spd']
                        print("Error 4")
                        def_abil = self.battle[user_names][def_id]['Selected']['Ability']
                        off_abil = self.battle[user_names][off_id]['Selected']['Ability']
                        atk = self.battle[user_names][def_id]['Selected']['Atk']
                        atk1 = self.battle[user_names][off_id]['Selected']['Atk']
                        spatk = self.battle[user_names][def_id]['Selected']['Fr Rnge']
                        spatk1 = self.battle[user_names][off_id]['Selected']['Fr Rnge']
                        spdef = self.battle[user_names][def_id]['Selected']['Fr Rnge Def']
                        spdef1 = self.battle[user_names][off_id]['Selected']['Fr Rnge Def']
                        Def1 = self.battle[user_names][off_id]['Selected']['Def']
                        Def = self.battle[user_names][def_id]['Selected']['Def']
                        if def_abil == "Regeneration" and def_health =< self.mon[selected_mon]['HP']:
                            def_health += def_health / 5
                        if off_abil == "Regeneration" and off_health =< self.mon[selected_mon1]['HP']:
                            off_health += off_health / 5
                        if atk > spatk:
                            dmg = round((atk * choices) / def1)
                            self.def_atkz = True
                        else:
                            dmg = round((spatk * choices) / spdef1)
                            self.def_spatkz = True
                        if atk1 > spatk1:
                            dmg1 = round((atk1 * choices)  / Def)
                            self.off_atkz = True
                        else:
                            self.off_spatkz = True
                            dmg1 = round((spatk * choices) / spdef)
                        if off_abil == "Full Counter" and self.def_spatkz == True:
                            dmg -= dmg
                            dmg1 += dmg*2
                        if def_abil == "Full Counter" and self.off_spatkz == True:
                            dmg1 -= dmg1
                            dmg += dmg1*2
                        embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

                        embed.add_field(name="Header", value=f"{sl} has Dealt {dmg} Damage!")

                        await ctx.send(embed=embed)

                        embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

                        embed.add_field(name="Header", value=f"{sl1} has Dealt {dmg1} Damage!")

                        await ctx.send(embed=embed)
                        print("Error 5")

                        off_health = self.battle[user_names][off_id]['Selected']['HP']
                        def_health = self.battle[user_names][def_id]['Selected']['HP']
                        if def_spd > off_spd:
                            def_health -= dmg1
                            off_health -= dmg
                        elif def_spd == off_spd:
                            off_health -= dmg
                            def_health -= dmg1
                        else:
                            off_health -= dmg
                            def_health -= dmg1
                        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                        embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

                        embed.set_author(name=f"Fight! - {ctx.author} & {user.name}", icon_url=self.bot.user.avatar_url)

                        embed.set_thumbnail(url=ctx.author.avatar_url)
                        embed.set_thumbnail(url=user.avatar_url)

                        embed.add_field(name=f"{ctx.author}'s {self.battle[user_names][off_id]['Selected']['Name']}", value=f"{off_health}/{self.mon[selected_mon1]['HP']}", inline=True)
                        embed.add_field(name=f"{user.name}'s {self.battle[user_names][def_id]['Selected']['Name']}", value=f"{def_health}/{self.mon[selected_mon]['HP']}", inline=True)
                        self.fite = False
                        time.sleep(1.5)
                        self.end = True
                if 0 >= off_health: # defender won
                    coins += (dmg / 2) * self.turn
                    embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

                    embed.set_author(name=f"Fight! - {ctx.author} & {user.name}", icon_url=self.bot.user.avatar_url)

                    embed.add_field(name=f"{user.name} Has Won the Battle!", value=f"And has been Rewarded {coins}c!")

                    await ctx.send(embed=embed)
                    sql = ("UPDATE usr SET coins = ? WHERE user_id = ?")
                    val = (coins, str(user.id))
                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()
                    self.fite = False
                    time.sleep(1.5)
                    self.end = True
                    print("Error 6")
                elif 0 >= def_health: # offender won
                    coins1 += (dmg1 / 2) * self.turn
                    embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

                    embed.add_field(name=f"{ctx.author} Has Won the Battle!", value="body")

                    await ctx.send(embed=embed)


                    sql = ("UPDATE usr SET coins = ? WHERE user_id = ?")
                    val = (coins1, str(ctx.author.id))
                    cursor1.execute(sql, val)
                    db.commit()
                    cursor1.close()
                    db.close()
                    self.fite = False
                    time.sleep(1.5)
                    self.end = True
                else:
                    return

    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        else:
            if message.author.id in self.battle:
                if self.fite == True:
                    if message.content == "move" or "Move":
                        self.broadcast = True
                        self.turn += 1
                    else:
                        return
                else:
                    return
            else:
                return

def setup(bot):
    bot.add_cog(Battle(bot))
