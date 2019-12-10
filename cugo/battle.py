import discord
from discord.ext import commands, tasks

import random
import time

import sqlite3
import json

class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.broadcast = False
        self.memes = False
        self.turn = 0
        self.authuz = ''
        self.usaz = ''
        self.movetype = ''
        self.bruv = ''
        self.dmg_choice = 0
        self.authdmg = 0
        self.usrdmg = 0
        self.extra = ''
        # stat algorithem: """(bs_ccdef * lvl) + ((CCDEFiv*lvl) / 5"""

        #self.loop.create_task(self.open_battles)

    async def open_battles(self):
        return


    @commands.command()
    async def duel(self, ctx, user:discord.User):
        if user == None:
            await ctx.send("Please State a User to Duel!")
        usrid = str(user.id)
        authorid = str(ctx.author.id)
        await ctx.send("Getting things Ready...")
        # we need the character's information, their indevidual values that the author's one has, and there own profile
        db = sqlite3.connect('users.sqlite')
        main = sqlite3.connect('mons.sqlite')
        auth_mons = main.cursor()
        usr_mons = main.cursor()
        auth_bttle = db.cursor()
        usr_bttle = db.cursor()
        battle = db.cursor()
        auth_c = db.cursor()
        usr_c = db.cursor()
        auth = db.cursor()
        usr = db.cursor()
        auth.execute(f"SELECT selected, coins FROM usr WHERE user_id = '{authorid}'")
        usr.execute(f"SELECT selected, coins FROM usr WHERE user_id = '{usrid}'")
        usr_result = usr.fetchone()
        auth_result = auth.fetchone()
        auth_c.execute(f"SELECT Level, Name, HPiv, CCiv, CCDEFiv, FRiv, FRDEFiv, MGC, SPD, Total, num FROM mons WHERE user_id = '{authorid}' and num = '{auth_result[0]}'")
        usr_c.execute(f"SELECT Level, Name, HPiv, CCiv, CCDEFiv, FRiv, FRDEFiv, MGC, SPD, Total, num FROM mons WHERE user_id = '{usrid}' and num = '{usr_result[0]}'")
        authinfo = auth_c.fetchone()
        usrinfo = usr_c.fetchone()
        auth_mons.execute(f"SELECT name, image, hp, CC, CC_DEF, FR, FR_DEF, MGC, SPD FROM mons WHERE name = '{authinfo[1]}'")
        auth_mon_info = auth_mons.fetchone()
        usr_mons.execute(f"SELECT name, image, hp, CC, CC_DEF, FR, FR_DEF, MGC, SPD FROM mons WHERE name = '{usrinfo[1]}'")
        usr_mon_info = usr_mons.fetchone()
        usr_hp = (round(((int(usr_mon_info[2]) * int(usrinfo[0])) + (int(usrinfo[2])*int(usrinfo[0]))))/100)
        auth_hp = (round(((int(auth_mon_info[2]) * int(authinfo[0])) + (int(authinfo[2])*int(authinfo[0]))))/100)
        sql = ("INSERT INTO battles(usrid, authorid, auth_red, usr_red, auth_sel, usr_sel, auth_hp, usr_hp) VALUES(?,?,?,?,?,?,?,?)")
        val = (usrid, authorid, "No", "No", str(authinfo[10]), str(usrinfo[10]), int(auth_hp), int(usr_hp))
        battle.execute(sql, val)
        usr_cc = int(round(int((usr_mon_info[3]) * int(usrinfo[0])) + int(usrinfo[3])*int(usrinfo[0]))) / 350
        usr_ccdef = int(round(int((usr_mon_info[4]) * int(usrinfo[0])) + int(usrinfo[4])*int(usrinfo[0]))) / 350
        usr_fr = int(round(int((usr_mon_info[5]) * int(usrinfo[0])) + int(usrinfo[5])*int(usrinfo[0]))) / 350
        usr_frdef = int(round(int((usr_mon_info[6]) * int(usrinfo[0])) + int(usrinfo[6])*int(usrinfo[0]))) / 350
        usr_mgc = int(round(int((usr_mon_info[7]) * int(usrinfo[0])) + int(usrinfo[7])*int(usrinfo[0]))) / 350
        usr_spd = int(round(int((usr_mon_info[8]) * int(usrinfo[0])) + int(usrinfo[8])*int(usrinfo[0]))) / 350
        auth_cc = int(round(int((auth_mon_info[3]) * int(authinfo[0])) + int(authinfo[3])*int(authinfo[0]))) / 350
        auth_ccdef = int(round(int((auth_mon_info[4]) * int(authinfo[0])) + int(authinfo[4])*int(authinfo[0]))) / 350
        auth_fr = int(round(int((auth_mon_info[5]) * int(authinfo[0])) + int(authinfo[5])*int(authinfo[0]))) / 350
        auth_frdef = int(round(int((auth_mon_info[6]) * int(authinfo[0])) + int(authinfo[6])*int(authinfo[0]))) / 350
        auth_mgc = int(round(int((auth_mon_info[7]) * int(authinfo[0])) + int(authinfo[7])*int(authinfo[0]))) / 350
        auth_spd = int(round(int((auth_mon_info[8]) * int(authinfo[0])) + int(authinfo[8])*int(authinfo[0]))) / 350
        db.commit()
        time.sleep(2)
        auth_health_stuff = ''
        usr_health_stuff = ''
        auth_health_stuff += '=========================='

        usr_health_stuff += '=========================='
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=random.choice(culorz))
        embed.add_field(name=usrinfo[1], value=f"{usr_hp}/{usr_hp} \n `<|-{usr_health_stuff}+|>`")
        embed.set_image(url=usr_mon_info[1])
        await ctx.send(embed=embed)
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=random.choice(culorz))
        embed.add_field(name=authinfo[1], value=f"{auth_hp}/{auth_hp} \n `<|-{auth_health_stuff}+|>`")
        embed.set_image(url=auth_mon_info[1])
        await ctx.send(embed=embed)
        self.broadcast = True
        stuffing_in_bag = ['usr' 'auth']
        self.bruv = random.choice(stuffing_in_bag)
        if self.bruv == 'auth':
            waiting = ("UPDATE battles SET auth_red = ? WHERE usrid = ? and authorid = ?")
            needed_stuff = ("Waiting", usrid, authorid)
            battle.execute(waiting, needed_stuff)
            db.commit()
            while True:
                battle.execute(f"SELECT auth_red, usr_red WHERE usrid = '{usrid}' and authorid = '{authorid}'")
                self.extra = battle.fetchone()
                time.sleep(15)
            if self.extra[0] == "Moved":
                self.bruv = 'usr'
            await ctx.send(f"Waiting for <@{authorid}>")
        elif self.bruv == 'usr':
            waiting = ("UPDATE battles SET auth_red = ? WHERE usrid = ? and authorid = ?")
            needed_stuff = ("Waiting", usrid, authorid)
            battle.execute(waiting, needed_stuff)
            db.commit()
            battle.execute(f"SELECT auth_red, usr_red WHERE usrid = '{usrid}' and authorid = '{authorid}'")
            self.extra = battle.fetchone()
            if self.extra[1] == "Moved":
                self.bruv = 'auth'
            await ctx.send(f"Waiting for <@{usrid}>")

        if self.memes == True and self.usaz == usrid and not self.broadcast == False and self.extra[1] == "Moved":
            if self.montype == "Magic":
                self.usrdmg = int(round((usr_mgc * self.dmg_choice) / auth_frdef))
            elif self.montype == "Fr":
                self.usrdmg = int(round((usr_fr * self.dmg_choice) / auth_frdef))
            elif self.montype == "Cc":
                self.usrdmg = int(round((usr_cc * self.dmg_choice) / auth_ccdef))
        elif self.memes == True and self.authuz == authorid and not self.broadcast == False and self.extra[1] == "Moved":
            if self.montype == "Magic":
                self.authdmg = int(round((auth_mgc * self.dmg_choice) / usr_frdef))
            elif self.montype == "Fr":
                self.authdmg = int(round((auth_fr * self.dmg_choice) / usr_frdef))
            elif self.montype == "Cc":
                self.authdmg = int(round((auth_cc * self.dmg_choice) / usr_ccdef))
        while self.extra[2] and self.extra[3] > 0 and self.broadcast == True:
            violence = ("UPDATE battles SET auth_hp = ? and usr_hp = ? WHERE authorid = ? and usrid = ?")
            more = (self.usrdmg-auth_hp, self.authdmg-usr_hp, authorid, usrid)
            battle.execute(violence, more)
            db.commit()
            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
            embed = discord.Embed(color=random.choice(culorz))
            embed.add_field(name=str(ctx.author)[:-5], val=f"Has Dealt {round(self.authdmg)}")
            await ctx.send(embed=embed)
            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
            embed = discord.Embed(color=random.choice(culorz))
            embed.add_field(name=str(user.name)[:-5], val=f"Has Dealt {round(self.usrdmg)}")
            await ctx.send(embed=embed)
            self.authdmg = 0
            self.usrdmg = 0
            self.montype = ''
            self.broadcast = False

        battle.execute(f"SELECT auth_hp, usr_hp FROM battles WHERE authorid = '{authorid}' and usrid = '{usrid}'")
        battle_info = battle.fetchone()
        if 0 >= battle_info[0]: # usr won
            usr_won = (f"UPDATE battle SET usrid = '{None}' authorid = '{None}' auth_sel = '{None}' usr_sel = '{None}' auth_hp = '{None}', usr_hp = '{None}' WHERE usrid = '{usrid}' and authorid = '{authorid}'")
            battle.execute(usr_won)
            db.commit()
            usr_coins = (f"UPDATE usr SET coins = '{(usr_result[1] * self.turn) / 2}' WHERE user_id = '{usrid}'")
            usr.execute(usr_coins)
            db.commit()
            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
            embed = discord.Embed(color=random.choice(culorz))
            embed.add_field(name=f"<@{usrid}> Has won the Duel!", value=f"And has Been Rewarded `{(usr_result[1] * self.turn) / 2}` Coins!")
            await ctx.send(embed=embed)
            self.broadcast = False
            self.memes = False
            db.close()

        elif 0 >= battle_info[1]: # auth won
            auth_won = (f"UPDATE battle SET usrid = '{None}' authorid = '{None}' auth_sel = '{None}' usr_sel = '{None}' auth_hp = '{None}', usr_hp = '{None}' WHERE usrid = '{usrid}' and authorid = '{authorid}'")
            battle.execute(auth_won)
            db.commit()
            auth_coins = (f"UPDATE usr SET coins = '{(auth_result[1] * self.turn) / 2}' WHERE user_id = '{authorid}'")
            auth.execute(auth_coins)
            db.commit()
            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
            embed = discord.Embed(color=random.choice(culorz))
            embed.add_field(name=f"<@{authorid}> Has won the Duel!", value=f"And has Been Rewarded `{(auth_result[1] * self.turn) / 2}` Coins!")
            await ctx.send(embed=embed)
            self.broadcast = False
            self.memes = False
            db.close()


    @commands.command()
    async def move(self, ctx, arg):
        if arg in ['mgc', 'MGC', 'Mgc', 'MAGIC', 'Magic', 'magic']:
            self.movetype = 'Magic'
        elif arg in ['FR', 'fr', 'Fr']:
            self.movetype = 'Fr'
        elif arg in ['CC', 'Cc', 'cc']:
            self.movetype = 'Cc'
        else:
            await ctx.send("Invalid Move-type Chosen!")
            return
        if self.broadcast == True:
            if self.memes == False:
                self.turn += 1
                self.memes = True
        if self.bruv == 'usr':
            self.usaz = str(ctx.author.id)
        elif self.bruv == 'auth':
            self.authuz = str(ctx.author.id)

        self.dmg_choice = random.randint(10, 200)


def setup(bot):
    bot.add_cog(Battle(bot))
