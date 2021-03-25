from discord.ext import commands


class CountCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.count_map = await self.db.get_count_map()

    @commands.command()
    async def mycount(self, ctx) -> None:
        count = self.count_map.get(ctx.author.id)
        await ctx.send(f"あなたのカウント: {count}")

    @commands.Cog.listener()
    async def on_member_join(self, member) -> None:
        await self.db.add_user(member.id)

    @commands.Cog.listener()
    async def on_member_remove(self, member) -> None:
        await self.db.remove_user(member.id)


def setup(bot):
    bot.add_cog(CountCog(bot))
