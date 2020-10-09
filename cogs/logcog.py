from discord.ext import commands
import discord
import json


class LogCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Bot Commander")
    async def setlogchannel(self, ctx, channel_id):
        """Enter the id of the channel you want to set the log channel to"""
        channel_obj = await self.bot.fetch_channel(channel_id)
        if channel_obj == None:
            await ctx.send("Invalid channel!")
            return

        with open("config.json", "r") as f:
            config_dict = json.load(f)
            config_dict["logChannel"] = channel_id

        with open("config.json", "w") as f:
            json.dump(config_dict, f)

        await ctx.send(f"Log channel updated to {channel_obj.name}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return

        with open("config.json", "r") as f:
            config_dict = json.load(f)
            channel_id = config_dict["logChannel"]
            channel_obj = await self.bot.fetch_channel(channel_id)

        embed = discord.Embed(
            title=message.author.name, description=message.content, color=0xFF0000
        )
        await channel_obj.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        with open("config.json", "r") as f:
            config_dict = json.load(f)
            channel_id = config_dict["logChannel"]
            channel_obj = await self.bot.fetch_channel(channel_id)

        embed = discord.Embed(
            title=message_before.author.name, description="Message Edit", color=0xFF0000
        )
        embed.add_field(name="Before", value=message_before.content, inline=False)
        embed.add_field(name="After", value=message_after.content, inline=True)

        await channel_obj.send(embed=embed)


def setup(bot):
    bot.add_cog(LogCog(bot))
