import discord
from discord.ext import commands

import json
import sqlite3

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # change the topic for new cogs!
        self.topic = 'Shop'

        with open(r"G:\Artrix-botz\PhysixsFun\cugo\items.json", 'r') as f:
            self.itmes = json.load(f)


    @commands.group(invoke_without_command=True)
    async def shop(self, ctx):
        culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
        embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

        embed.set_author(name=f"{self.topic}! - {ctx.author[:-5]}")

        embed.add_field(name=f"**Mythical Items:", value=f"`>shop mythical`", inline=True)
        # Change when you add more categories
        await ctx.send(embed=embed)

    @shop.command()
    async def mythical(self, ctx, arg):
        if arg == None or False:
            embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)
            cugz_desc = ''
            for x in self.items['Mythical Items']:
                cugz_desc += f"**{x}** - `{self.Items[x].__doc__}` \n"
            embed.set_author(name=f"Mythical Items! - {ctx.author}", icon_url=self.bot.user.avatar_url)

            embed.set_thumbnail(url=ctx.author.avatar_url)

            embed.add_field(name=f'Mythical Items', value=cugz_desc)

            await ctx.send(embed=embed)
        else:
            if not arg in self.items:
                await ctx.send(f"{arg} Isn't a Item")
            else:
                db = sqlite3.connect('usr.sqlite')
                cursor = db.cursor()
                cursor.execute(f"SELECT user_id, coins, bag FROM usr WHERE user_id = '{ctx.author.id}'")
                result = cursor.fetchone()
                coins = result[1]
                bag = result[2]
                if coins < self.items[arg]['Cost']:
                    await ctx.send(f"{arg} Costs {self.items[arg]['Cost']} you Only have {coins}!")
                else:
                    coins -= self.items[arg]['Cost']
                    bag += arg
                    sql = ("UPDATE usr SET bag = ? WHERE coins = ? and user_id = ?")
                    val = (bag, coins, str(ctx.author.id))
                    cursor.execute(sql, val)
                    culorz = [0x9750C7, 0x000066, 0xA200FF, 0x0008FF]
                    embed = discord.Embed(color=random.choice(culorz), timestamp=ctx.message.created_at)

                    embed.set_author(name=f"{arg}! - {ctx.author[:-5]}")

                    embed.add_field(name=f"{ctx.author} Has Bought:", value=arg)
                    db.commit()
                    cursor.close()
                    db.close()


def setup(bot):
    bot.add_cog(Shop(bot))
