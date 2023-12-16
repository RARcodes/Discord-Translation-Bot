import discord
from discord.ext import commands
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

intents = discord.Intents.default()
intents.message_content = True
intents.message_content = True

bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user.name} ({bot.user.id})")

if __name__ == "__main__":
    bot.load_extension("bot.translation")
    bot.run(config["token"])
