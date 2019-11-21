import discord
from discord.ext import commands

import random

import sqlite3
import json


# COG setup code

# THE MAIN FILE IS THE TRUNK AND THE COG IS THE BRANCH
class Info(commands.Cog):
    def __init__(self, bot):
        # self means the variable is usable throughout the cog
        self.bot = bot
        # change the topic for new cogs!
        self.topic = 'Info'

    # Opening a Json File as a variable
        with open(r"G:\Artrix-botz\PhysixsFun\cugo\moninfo.json", 'r') as f:
            self.weeb = json.load(f)

        with open(r"G:\Artrix-botz\PhysixsFun\cugo\ability.json", 'r') as f:
            self.ability = json.load(f)


    @commands.group(pass_context=True, invoke_without_command=True, case_insensitive=False, aliases=['i'] )
    async def info(self, ctx, *, arg):
        db = sqlite3.connect('users.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id, selected FROM usr WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        selected = str(result[1])
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

        embed.set_author(name=f"{selected}! - {ctx.author}", icon_url=self.bot.user.avatar_url)

        embed.add_field(name="HP", value=self.weeb[selected]['HP'])
        embed.add_field(name="Type", value=self.weeb[selected]['Type'])
        embed.add_field(name="Close Combat", value=self.weeb[selected]['CC'])
        embed.add_field(name="CC Defence", value=self.weeb[selected]['CC DEF'])
        embed.add_field(name="Far Range", value=self.weeb[selected]['FR'])
        embed.add_field(name="FR Defence", value=self.weeb[selected]['FR DEF'])
        embed.add_field(name="Magic", value=self.weeb[selected]['MGC'])
        embed.add_field(name="Speed", value=self.weeb[selected]['SPD'])

        embed.set_image(url=self.weeb[selected]['Image link'])

        await ctx.send(embed=embed)
        db.commit()
        cursor.close()
        db.close()

    # The Command that Searches the variable that we set above and takes information in it and puts it into a embed """

    @info.command()
    async def ability(self, ctx, arg):
        if arg == None or False:
            await ctx.send("Please State a Ability!")
        else:
            if arg in self.ability:
                culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

                embed.set_author(name=f"{arg}! - {ctx.author}", icon_url=self.bot.user.avatar_url)

                embed.add_field(name=self.ability[arg], value=self.ability[arg]['Status'])

                embed.add_field(name="Description:", value=self.ability[arg]['Description'], inline=True)
                embed.add_field(name="Simple Description:", value=self.ability[arg]['Simple Description'], inline=True)
                embed.add_field(name="Rating:", value=self.ability[arg]['Rating 1-10'])

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{arg} Either Doesn't Exist or Isn't in our Databse yet!")

    @info.command()
    async def mon(self, ctx, arg):
        if arg == int() or float():
            await ctx.send("SOON") # Change when info numbers work
        if arg is None or False:
            await ctx.send(">info`<name>` To Find some info On a Weebmon! \n Unfortunently You Need to Start the Name With a Uppercase letter.")
        if arg in self.weeb:
            culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
            embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

            embed.set_author(name=f"{arg}! - {ctx.author}", icon_url=self.bot.user.avatar_url)

            embed.set_image(url=self.weeb[arg]['Image link'])

            embed.add_field(name="Type", value=self.weeb[arg]['Type'])
            embed.add_field(name="Ability", value=f"{self.weeb[arg]['AB']}\n")

            embed.add_field(name="HP", value=self.weeb[arg]['HP'])
            embed.add_field(name="Close Combat", value=self.weeb[arg]['CC'])
            embed.add_field(name="CC Defence", value=self.weeb[arg]['CC DEF'])
            embed.add_field(name="Far Range", value=self.weeb[arg]['FR'])
            embed.add_field(name="FR Defence", value=self.weeb[arg]['FR DEF'])
            embed.add_field(name="Magic", value=self.weeb[arg]['MGC'])
            embed.add_field(name="Speed", value=self.weeb[arg]['SPD'])
            embed.add_field(name="Total Power", value=self.weeb[arg]['Total Power'])
            embed.add_field(name="Power Ranking", value=self.weeb[arg]['PR'])

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{arg} Isn't A Weebmon!")
def setup(bot):
    bot.add_cog(Info(bot))
# This adds The cog to the bot
