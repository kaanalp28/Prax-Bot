# discord api
import discord
from discord.ext import commands

from discord.ext import commands, bridge
from discord.ext.commands import Context
from discord.ext.bridge import BridgeContext

# custom utilities
from Utilities import log
log = log.Logger("test")

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(
        name="test1",
        description="The test command",
        help="Test 1",
        aliases=["t1"],
        )
    async def test(self, ctx: BridgeContext):
        await ctx.send("Test succesful!")

def setup(bot):
    bot.add_cog(Test(bot))