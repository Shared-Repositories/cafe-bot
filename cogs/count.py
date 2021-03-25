from discord.ext import commands


class CountCog(commands.Bot):
    def __init__(self, bot) -> None:
        self.bot = bot


def setup(bot):
    bot.add_cog(CountCog(bot))
