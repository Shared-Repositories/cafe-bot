from discord.ext import commands


class CountCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.count_map = await self.db.get_count_map()

    @commands.command()
    async def mycount(self, ctx) -> None:
        count = self.count_map.get(ctx.author.id)
        await ctx.send(f"あなたのカウント: {count}")


def setup(bot):
    bot.add_cog(CountCog(bot))
