import aiohttp
import asyncio

from discord.ext import commands
import logging


class DiscordBotListAPI(commands.Cog):
    def __init__(self, bot):
        self.token = open("TOKEEN.txt", "r").read()
        self.bot = bot
        self.updating = self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your stats"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://discordbotlist.com/api/bots/633033797205622832/",
                    headers={"Authorization": f"Bot {self.token}"},
                    json={
                        "guilds": len(self.bot.guilds),
                        "users": len([*self.bot.get_all_members()]),
                    },
                ) as resp:
                    resp.raise_for_status()
                    logger.info(
                        f"Posted server count to dblcom: ({len(self.bot.guilds)})"
                    )
        except Exception as e:
            logger.exception(
                f"Failed to post server count to dblcom\n{type(e).__name__}: {e}"
            )
        await asyncio.sleep(1800)


def setup(bot):
    global logger
    logger = logging.getLogger("bot")
    bot.add_cog(DiscordBotListAPI(bot))
