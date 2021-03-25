from discord.ext import commands


class CountCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.count_map = await self.bot.db.get_count_map()

    @commands.command()
    async def mycount(self, ctx) -> None:
        count = self.count_map.get(ctx.author.id)
        await ctx.send(f"あなたのカウント: {count}")

    @commands.Cog.listener()
    async def on_member_join(self, member) -> None:
        await self.bot.db.add_user(member.id)
        self.count_map[member.id] = 0

    @commands.Cog.listener()
    async def on_member_remove(self, member) -> None:
        await self.bot.db.remove_user(member.id)
        self.count_map.pop(member.id)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id == 779693431835721728:
            return

        await self.bot.db.count_up(message.author.id)
        self.count_map[message.author.id] += 1


def setup(bot):
    bot.add_cog(CountCog(bot))
