import discord
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Mod Cog loaded ✅")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *,reason: str):
        """Kicks a member from the server"""
        await member.kick(reason=reason)
        embed = discord.Embed(description=f"<:tick:1323972567924740169> | {member} has been successfully kicked out!",color=0x00FFB3)
        await ctx.send(embed=embed) 

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str):
        """Ban a member."""
        await member.ban(reason=reason)
        embed = discord.Embed(description=f"<:tick:1323972567924740169> | {member} has been successfully banned.",color=0x00FFB3)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str):
        """Warns a member."""
        embed = discord.Embed(description=f"<:tick:1323972567924740169> | {member} has been warned",color=0x00FFB3)
        await ctx.send(embed=embed,ephemeral=True)
        embed2 = discord.Embed(title="Be Careful!",description=f"You have been warned for `{reason}`.",color=0x00FFB3)
        await member.send(embed=embed2)



async def setup(bot: commands.Bot):
    await bot.add_cog(Mod(bot))
