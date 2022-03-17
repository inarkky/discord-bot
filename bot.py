import os
import platform
import random
import sys

import discord
import yaml
from discord.ext import commands, tasks
from discord.ext.commands import Bot

from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
ranker = AutoModelForSequenceClassification.from_pretrained('microsoft/DialogRPT-human-vs-machine')


if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


intents = discord.Intents.default()

bot = Bot(command_prefix=config["bot_prefix"], intents=intents)


# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()


# Setup the game status task of the bot
@tasks.loop(minutes=1.0)
async def status_task():
    statuses = ["with you!", f"{config['bot_prefix']}help"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))


# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")

if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


# The code in this event is executed every time someone sends a message, with or without the prefix
@bot.event
async def on_message(message):
    # Ignores if a command is being executed by a bot or by the bot itself
    if message.author == bot.user or message.author.bot:
        return

    # Ignores if a command is being executed by a blacklisted user
    if message.author.id in config["blacklist"]:
        return
    
    # If bot is mentioned
    if bot.user.mentioned_in(message):
	# Clean the message so that Peri doesn't get overfed with it's name
        x_clean_msg = " ".join(filter(lambda x:x[0]!='@', message.clean_content.split()))
        new_user_input_ids = tokenizer.encode(x_clean_msg + tokenizer.eos_token, return_tensors='pt')

	# We want Peri to try following the context so let's give her a memory
	# Also some fine tunning 
        chat_history_ids = model.generate(
            new_user_input_ids, 
	    max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            top_k=80, top_p=0.9, temperature=1, repetition_penalty=.6,
            num_beams=4, num_beam_groups=1, num_return_sequences=4,
            early_stopping=True)

	# Peri should should go for interesting response if she has a choice
        with torch.no_grad():
            ranker_results = ranker(chat_history_ids, return_dict=True)
            ranker_results = torch.sigmoid(ranker_results.logits)[0]

	# Rank possible responses (reddit upvotes model)
        responses = chat_history_ids[:, new_user_input_ids.shape[-1]:]
        responses = [responses[int(torch.argmax(ranker_results))]]
	
	# Run a lop to catch multipart messages (you never know)
	iterator = 0
        for it in responses:
            response = tokenizer.decode(it, skip_special_tokens=True)
            if iterator == 0:
                response2 = '{0.author.mention} '.format(message)
                iterator = 1 # If multipart Peri doesn't need to tag on every message
            else:
                response2 = ''
            print(response)

            await message.channel.send(response2 + response)

    # Parse command
    await bot.process_commands(message)


# The code in this event is executed every time a command has been *successfully* executed
@bot.event
async def on_command_completion(ctx):
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    print(
        f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})")


# The code in this event is executed every time a valid commands catches an error
@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title="Error!",
            description="This command is on a %.2fs cool down" % error.retry_after,
            color=config["error"]
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission `" + ", ".join(
                error.missing_perms) + "` to execute this command!",
            color=config["error"]
        )
        await context.send(embed=embed)
    raise error

# Run the bot with the token
bot.run(config["token"])
