import asyncio
import os
import random
import sys

import discord
import yaml
from discord.ext import commands

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="8ball")
    async def eight_ball(self, context, *args):
        """
        Ask Peri chan a question.
        """
        answers = ['It is certain.', 'It is decidedly so.', 'You may rely on it.', 'Without a doubt.',
                   'Yes - definitely.', 'As I see, yes.', 'Most likely.', 'Outlook good.', 'Yes.',
                   'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
                   'Cannot predict now.', 'Concentrate and ask again later.', 'Don\'t count on it.', 'My reply is no.',
                   'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{answers[random.randint(0, len(answers))]}",
            color=config["success"]
        )
        embed.set_footer(
            text=f"Question asked by: {context.message.author}"
        )
        await context.send(embed=embed)

    @commands.command(name="roll")
    async def roll(self, context, *args):
        """
        Ask Peri to roll a die .peri roll d20, .peri roll 3d6
        """
        roll = "".join(args)
        dices = roll.lower().split('d')
        if dices[0] == '':
            dices[0] = '1'
        result = tuple(random.randint(1, int(dices[1])) for _ in range(int(dices[0]))) 
        result_steps = '+'.join(map(str, result))
        result_sum = sum(result)

        embed = discord.Embed(
            title=f"**Rolled {result_sum}**",
            description=f"{result_steps}",
            color=config["success"]
        )
        embed.set_footer(
            text=f"Roll requested by: {context.message.author}"
        )

        await context.send(embed=embed)

    @commands.command(name="google")
    async def search(self, context, *args):
        """
        Ask Peri to google it for you
        """
        link = "+".join(args)
        await context.send(f"https://letmegooglethat.com/?q={link}")

    @commands.command(name="bigcoffee")
    async def bigcoffee(self, context, *args):
        """
        Ask Peri to make a big coffee (not mobile friendly)
        """
        response = """```
                              _____________________
                             (___________          |
                              [XXXXX]   |          |
                         __  /~~~~~~~\  |          |
     )))         )))    /  \|@@@@@@@@@\ |          |
    (((         (((     \   |@@@@@@@@@@||          |
  +-----+     +-----+       \@@@@@@@@@@||  ______  |
  |     |]    |     |]       \@@@@@@@@/ | |on|off| |
  `-----'     `-----'       __\@@@@@@/__|  ~~~~~~  |
___________ ___________    (____________|__________|
`---------' `---------'    |_______________________|
        ```"""

        await context.send(response)

    @commands.command(name="coffee")
    async def coffee(self, context, *args):
        """
        Ask Peri to make a coffee
        """
        response = "`ⅽ[] ͌ c[] ͌`"

        #await context.send(response)
        await context.send(file=discord.File('/home/narki/periBot/assets/peri_color_coffee.jpg'))


def setup(bot):
    bot.add_cog(Fun(bot))
