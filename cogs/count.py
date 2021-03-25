from discord.ext import commands, tasks
import time


class CountCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.count_map = await self.bot.db.get_count_map()
        self.count_task.start()

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

    @tasks.loop(seconds=60)
    async def count_task(self):
        await self.bot.wait_until_ready()
        now = time.localtime()
        check = all(
            now.tm_wday == 0,
            now.tm_hour == 0,
            now.tm_min == 0
        )
        if not check:
            return

        guild = self.bot.get_guild(778297702781419520)
        role = guild.get_role(808714730998988810)
        for member in role.members:
            await member.remove_roles(role)
        for user_id, count in self.count_map.items():
            if count >= 200:
                member = guild.get_member(user_id)
                await member.add_roles(role)
            self.count_map[user_id] = 0
        await self.bot.db.reset_count()



def setup(bot):
    bot.add_cog(CountCog(bot))
