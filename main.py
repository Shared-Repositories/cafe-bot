from discord.ext import commands
import discord
import dotenv
import os
import traceback

dotenv.load_dotenv()


class CafeBot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        extensions = [f[:-3] for f in os.listdir("./cogs") if f.endswith(".py")]
        for exts in extensions:
            try:
                self.load_extension(f"cogs.{exts}")
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print(f"bot logged in as {self.bot.name} ({self.bot.id})")


if __name__ == "__main__":
    intents = discord.Intents.all()
    bot = CafeBot("!", intents=intents)
    bot.run(os.environ["TOKEN"])