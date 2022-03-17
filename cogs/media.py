import json
import os
import platform
import random
import sys

import aiohttp
import discord
import yaml

from discord.ext import commands
from youtubesearchpython import VideosSearch

from googleapiclient.discovery import build


if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


class Media(commands.Cog, name="media"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play")
    async def play(self, context, *args):
        """
        Ask Perri chan to play a song.
        """
        search = " ".join(args)
        videosSearch = VideosSearch(search, limit = 1)
        playlist = videosSearch.result()
        response = playlist['result'][0]['id']
        await context.send("https://youtu.be/"+response)

    @commands.command(name="drunk")
    async def drunk(self, context):
        """
        Ask Perri chan to play a song.
        """
        a = ["Pop","Rock","Hip Hop","Electronica","Punk Rock","Jazz","Blues","Country","Classical","Latin","Folk","Acoustic","Indie","Soul","Kpop"]
        b = ["Happy","Romance","Sleep","Party","Study","Chill","Sad","Positive","Funny","Workout","Gaming","Inspirational","Dinner","Travel"]
        a = random.choice(a)
        b = random.choice(b)
        videosSearch = VideosSearch(a + " " + b, limit = 1)
        playlist = videosSearch.result()
        response = playlist['result'][0]['id']
        await context.send("https://youtu.be/"+response)


def setup(bot):
    bot.add_cog(Media(bot))
