import discord
from discord.ext import commands
from discord import Embed
from googletrans import Translator, LANGUAGES
import aiohttp
import asyncio
import json

# Load configuration from config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Create an instance of the Translator class for text translation
translator = Translator()

# Set up the Discord bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

# List of common languages for translation
common_languages = ['english', 'spanish', 'mandarin', 'hindi', 'arabic', 'bengali', 'portuguese', 'russian', 'urdu']

# Dictionary to store auto-translate languages for users
auto_translate_languages = {}

# Event handler when the bot is ready
@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user.name} ({bot.user.id})")

# Command to manually translate text
@bot.command(name="translate", aliases=["trns"])
async def translate_command(ctx, target_language, *, text):
    try:
        # Get user information for webhook
        user_display_name = ctx.author.display_name
        user_avatar_bytes = await ctx.author.avatar.read()

        # Create a webhook for sending translated messages
        webhook = await ctx.channel.create_webhook(name=user_display_name, avatar=user_avatar_bytes)

        # Delete the original command message
        await ctx.message.delete()

        if target_language.lower() == 'all':
            # Translate text to all supported languages
            translations = [(lang, translator.translate(text, dest=lang).text) for lang in LANGUAGES]
            translated_texts = [f"**Translated ({lang}):** {text}" for lang, text in translations]
            await webhook.send(content=f"{user_display_name} said:\n" + '\n'.join(translated_texts))
        else:
            # Translate text to the specified language
            translation = translator.translate(text, dest=target_language)
            translated_text = translation.text
            await webhook.send(content=f"{translated_text}")

        # Delete the webhook after sending the translated message
        await webhook.delete()

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Command to display supported languages
@bot.command(name="languages", aliases=["langs"])
async def languages_command(ctx):
    common_lang_dict = {code: lang for code, lang in LANGUAGES.items() if lang.lower() in common_languages}
    embed = Embed(title="Supported Languages", color=0x4CAF50)

    for code, lang in common_lang_dict.items():
        embed.add_field(name=f"{code}:", value=lang, inline=False)

    await ctx.send(embed=embed)

# Command to display bot commands
@bot.command(name="helpcommands")
async def help_commands(ctx):
    embed = Embed(title="Translation Bot Commands", color=0x4CAF50)
    
    embed.add_field(
        name="!translate (or !trns)",
        value="Translate text to the specified language. Usage: `!translate <target_language> [source_language] <text>`",
        inline=False
    )
    
    embed.add_field(
        name="!languages (or !langs)",
        value="Display a list of supported languages.",
        inline=False
    )

    embed.add_field(
        name="!auto",
        value="Set auto-translate language. Usage: `!auto <language>`",
        inline=False
    )

    embed.add_field(
        name="!stop",
        value="Stop auto-translation. Usage: `!stop`",
        inline=False
    )

    await ctx.send(embed=embed)

# Command to set auto-translate language for a user
@bot.command(name="auto")
async def set_auto_translate(ctx, language):
    language = language.lower()
    if language in LANGUAGES:
        auto_translate_languages[ctx.author.id] = language
        await ctx.send(f"Auto-translate language set to {language}.")
    else:
        await ctx.send("Invalid language. Please use a supported language code.")

# Command to stop auto-translate for a user
@bot.command(name="stop")
async def stop_auto_translate(ctx):
    if ctx.author.id in auto_translate_languages:
        del auto_translate_languages[ctx.author.id]
        await ctx.send("Auto-translate has been stopped.")
    else:
        await ctx.send("Auto-translate is not currently enabled for you.")

# Event handler for auto-translation when a message is sent
@bot.event
async def on_message(message):
    if message.author.id in auto_translate_languages:
        target_language = auto_translate_languages[message.author.id]
        translation = translator.translate(message.content, dest=target_language)
        translated_text = translation.text

        # Get user information for webhook
        user_display_name = message.author.display_name
        user_avatar_bytes = await message.author.avatar.read()

        # Create a webhook for sending translated messages
        webhook = await message.channel.create_webhook(name=user_display_name, avatar=user_avatar_bytes)

        # Delete the original message and send the translated message
        await message.delete()
        await webhook.send(content=f"{translated_text}")
        await webhook.delete()
        
    await bot.process_commands(message)

# Main function to start the bot
async def main():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    await bot.start(config["token"])

# Run the main function if the script is executed directly
if __name__ == "__main__":
    asyncio.run(main())
