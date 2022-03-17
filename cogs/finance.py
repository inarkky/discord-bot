import json
import os
import platform
import random
import sys
import requests

import aiohttp
import discord
import yaml
from discord.ext import commands


if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


class Finance(commands.Cog, name="finance"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="crypto")
    async def crypto(self, context, *args):
        """
        Get the current price of crypto currency (pass currency code as an argument).
        """
        currency = " ".join(args)
        url = "https://api.coincap.io/v2/assets?search=" + currency
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            number = '{:.2f}'.format(float(response['data'][0]['priceUsd']))
            embed = discord.Embed(
                title=":information_source: Info",
                description=f"{response['data'][0]['name']} price is: ${str(number)}",
                color=config["success"]
            )
            await context.send(embed=embed)

    @commands.command(name="stonks-search")
    async def stonks_search(self, context, *args):
        """
        Have Peri check the stock
        """
        search = " ".join(args)
        url = "https://alpha-vantage.p.rapidapi.com/query"
        querystring = {"keywords":search,"function":"SYMBOL_SEARCH","datatype":"json"}
        headers = {
            'x-rapidapi-key': "32237662c6msh5256a5bdca47c0cp11bb24jsne42e087eea3e",
            'x-rapidapi-host': "alpha-vantage.p.rapidapi.com"
        }
        response_full = requests.request("GET", url, headers=headers, params=querystring)
        response = response_full.json()
        embed = discord.Embed(
            title=f"**{response['bestMatches'][0]['1. symbol']}** {response['bestMatches'][0]['2. name']}",
            description=f"Score: {response['bestMatches'][0]['9. matchScore']}\nCurrency: {response['bestMatches'][0]['8. currency']}",
            color=config["success"]
        )
        await context.send(embed=embed)

    @commands.command(name="stonks")
    async def stonks(self, context, *args):
        """
        Have Peri check the stock prices
        """
        symbol = " ".join(args)
        url = "https://alpha-vantage.p.rapidapi.com/query"
        querystring = {"function":"GLOBAL_QUOTE","symbol":symbol,"datatype":"json"}
        headers = {
            'x-rapidapi-key': "32237662c6msh5256a5bdca47c0cp11bb24jsne42e087eea3e",
            'x-rapidapi-host': "alpha-vantage.p.rapidapi.com"
        }
        response_full = requests.request("GET", url, headers=headers, params=querystring)
        response = response_full.json()
        embed = discord.Embed(
            title=f"**{response['Global Quote']['01. symbol']}**",
            description=f"High: {response['Global Quote']['03. high']}\nLow: {response['Global Quote']['04. low']}\n**{response['Global Quote']['05. price']}** ({response['Global Quote']['10. change percent']})",
            color=config["success"]
        )
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Finance(bot))
