import re
import random
import aiohttp
import discord

from Utilities import log

from discord.ext import commands, bridge
from discord.ext.commands import Context
from discord.ext.bridge import BridgeContext
import bot

log = log.Logger("reddit")

meme_types = ["memes", "dankmemes", "facepalm", "funny", "therewasanattempt", "notfunny", "fakehistoryporn", "ScottishPeopleTwitter", "meirl", "2meirl4meirl", "gametheorymemes", "BlackPeopleTwitter", "wholesomememes"]

class Meme(commands.Cog):

    def __init__(self, bot: bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await log.info("Reddit cog loaded.")

    global meme_types

    async def meme(self, meme_type):
        hex_color = random.randint(0, 0xFFFFFF)
        mediatype = None
        retry = 0

        async with aiohttp.ClientSession() as cs:
            while mediatype != 'i' and retry <= 75:

                if meme_type not in meme_types:
                    memetype = random.choice(meme_types)
                else:
                    memetype = meme_type

                async with cs.get(f'https://www.reddit.com/r/{memetype}/new.json?sort=hot&limit=100') as r:
                    res = await r.json()

                    try:
                        retry += 1
                        rand = random.randint(0, 99)

                        title = res['data']['children'][rand]['data']['title']
                        content = res['data']['children'][rand]['data']['selftext']
                        img = res['data']['children'][rand]['data']['url']

                        link = res['data']['children'][rand]['data']['permalink']
                        link = 'https://www.reddit.com'+link

                        mediatype = re.search('https://(.*).redd.it/', img).group(1)
                    except Exception as e:
                        print(e, memetype)
                
        embed = discord.Embed(title=title, description="", url=link, color=hex_color)
        embed.add_field(name="", value=content, inline=False)
        embed.set_image(url=img)
        embed.set_footer(text=f"See the trending memes on r/{memetype}!")

        return embed


    @bridge.bridge_command(
    name="meme",
    description="Want to read some memes? But don't wanna leave discord? Lemme help you!",
    help="Only the best memes!",
    aliases=["reddit","memes","meem","mmee","mme","mee","eemm","mem","memem"],
    )
    @discord.option("meme_type", choices=meme_types, description="Select the subreddit you want to see a meme from!", required=False)
    async def _meme(self, ctx: BridgeContext, meme_type: str=None):
        await ctx.defer()
        embed = await self.meme(meme_type)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Meme(bot))