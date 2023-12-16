from discord.ext import commands
from googletrans import Translator

class TranslationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()

    @commands.command(name="translate", aliases=["trans"])
    async def translate_command(self, ctx, target_language, *, text):
        """
        Translate text to the specified language.

        Example:
        !translate es Hello, how are you?
        """
        try:
            translation = self.translator.translate(text, dest=target_language)
            translated_text = translation.text
            await ctx.send(f"**Translated ({target_language}):** {translated_text}")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

def setup(bot):
    bot.add_cog(TranslationCog(bot))
