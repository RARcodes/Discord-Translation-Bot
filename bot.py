import discord
from discord.ext import commands
from discord import Embed
from googletrans import Translator, LANGUAGES
import asyncio
import json

"""instance of the Translator class for text translation."""
translator = Translator()

"""Set up for the Discord bot"""
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

"""Define common languages for translation."""
common_languages = ['english', 'spanish', 'mandarin', 'hindi', 'arabic', 'bengali', 'portuguese', 'russian', 'urdu']

@bot.event
async def on_ready():
    """Event handler for when the bot is ready."""
    print(f"Bot is ready. Logged in as {bot.user.name} ({bot.user.id})")

@bot.command(name="translate", aliases=["trans"])
async def translate_command(ctx, target_language, *, text):
    """Translate the specified text to the target language."""
    try:
        if target_language.lower() == 'all':
            """Translate to all supported languages if 'all' is specified."""
            translations = [(lang, translator.translate(text, dest=lang).text) for lang in LANGUAGES]
            translated_texts = [f"**Translated ({lang}):** {text}" for lang, text in translations]
            await ctx.send('\n'.join(translated_texts))
        else:
            """Translate to the specified language."""
            translation = translator.translate(text, dest=target_language)
            translated_text = translation.text
            await ctx.send(f"**({target_language}):** {translated_text}")

    except Exception as e:
        """Handle and notify about any errors during translation."""
        await ctx.send(f"An error occurred: {e}")

@bot.command(name="languages", aliases=["langs"])
async def languages_command(ctx):
    """Command to list common languages supported for translation."""
    common_lang_dict = {code: lang for code, lang in LANGUAGES.items() if lang.lower() in common_languages}
    embed = Embed(title="Supported Languages", color=0x4CAF50)

    for code, lang in common_lang_dict.items():
        embed.add_field(name=f"{code}:", value=lang, inline=False)

    await ctx.send(embed=embed)

async def main():
    """start the bot using the token from the config file."""
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    await bot.start(config["token"])

if __name__ == "__main__":
    asyncio.run(main())
