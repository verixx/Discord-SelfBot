import datetime
import discord

from .utils.checks import edit, getUser, getwithoutInvoke
from .utils import config
from discord.ext import commands


class Mod:

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('config.json')

    # Do cleanup
    async def do_purge(self, ctx, limit, predicate):
        if limit:
            deleted = await ctx.channel.purge(limit=limit, before=ctx.message, check=predicate)
            await edit(ctx, content='Cleaned `{}` messages out of `{}` that were checked.'.format(len(deleted), limit), ttl=5)
        else:
            await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Don't forget to give the amount you wanna delte".format(len(deleted), limit), ttl=5)

    # Purge group
    @commands.group(aliases=['purge'])
    @commands.guild_only()
    async def clean(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    # Remove embeds
    @clean.command()
    @commands.has_permissions(manage_messages=True)
    async def embeds(self, ctx, search: int = None):
        await self.do_purge(ctx, search, lambda e: len(e.embeds))

    # Remove images/attachments
    @clean.command()
    @commands.has_permissions(manage_messages=True)
    async def attachments(self, ctx, search: int = None):
        await self.do_purge(ctx, search, lambda e: len(e.attachments))

    # Remove all
    @clean.command(name='all')
    @commands.has_permissions(manage_messages=True)
    async def _all(self, ctx, search: int = None):
        await self.do_purge(ctx, search, lambda e: True)

    # Remove from specific user
    @clean.command()
    @commands.has_permissions(manage_messages=True)
    async def user(self, ctx, mem: str, search: int = None):
        member = getUser(ctx, mem)
        await self.do_purge(ctx, search, lambda e: e.author == member)

    # remove your own message, works everywhere not like all other purges.
    @clean.command()
    async def mine(self, ctx, search: int = None):
        await self.do_purge(ctx, search, lambda e: e.author == ctx.author)

    # Kick a Member
    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx):
        member = getUser(ctx, getwithoutInvoke(ctx))
        if member:
            try:
                await ctx.guild.kick(member)
            except discord.Forbidden:
                await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Missing permissions to kick this Member", ttl=5)
            except discord.HTTPException:
                await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Something went wrong while trying to kick...", ttl=5)
            else:
                e = discord.Embed(color=discord.Color.purple())
                e.set_author(icon_url="https://cdn.discordapp.com/attachments/278603491520544768/301084579660300289/301063051296374794.png",
                             name="Kicked: " + str(member))
                await edit(ctx, embed=e)

    # Ban a Member
    @commands.group()
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def ban(self, ctx):
        if ctx.invoked_subcommand is None:
            member = getUser(ctx, getwithoutInvoke(ctx))
            if member:
                try:
                    await ctx.guild.ban(member)
                except discord.Forbidden:
                    await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Missing permissions to ban this Member", ttl=5)
                except discord.HTTPException:
                    await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Something went wrong while trying to ban...", ttl=5)
                else:
                    e = discord.Embed(color=discord.Color.purple())
                    e.set_author(icon_url="https://cdn.discordapp.com/attachments/278603491520544768/301087009408024580/273910007857414147.png",
                                 name="Banned: " + str(member))
                    await edit(ctx, embed=e)

    # SoftBan a Member (ban, delelte messagea and unban)
    @ban.command()
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def soft(self, ctx):
        member = getUser(ctx, getwithoutInvoke(ctx))
        if member:
            try:
                await ctx.guild.ban(member)
                await ctx.guild.unban(member)
            except discord.Forbidden:
                await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Missing permissions to ban this Member", ttl=5)
            except discord.HTTPException:
                await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Something went wrong while trying to ban...", ttl=5)
            else:
                e = discord.Embed(color=discord.Color.purple())
                e.set_author(icon_url="https://cdn.discordapp.com/attachments/278603491520544768/301087009408024580/273910007857414147.png",
                             name="Soft Banned: " + str(member))
                await edit(ctx, embed=e)

    @commands.command(aliases=['color'])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def colour(self, ctx, colour: discord.Colour, role: discord.Role):
        try:
            await role.edit(colour=colour)
        except discord.HTTPException:
            await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Missing permissions to edit this role", ttl=5)
        else:
            e = discord.Embed(color=colour)
            e.set_author(name="Changed Role Color of: " + str(role))
            await edit(ctx, embed=e)

    @commands.command()
    @commands.guild_only()
    async def permissions(self, ctx):
        member = getUser(ctx, getwithoutInvoke(ctx))
        if member:
            true = '\n'.join(name.replace('_', ' ').title() for name, value in ctx.channel.permissions_for(member) if value is True)
            false = '\n'.join(name.replace('_', ' ').title() for name, value in ctx.channel.permissions_for(member) if value is False)

            e = discord.Embed(title="Permissions", color=discord.Color.purple(), timestamp=datetime.datetime.now())
            e.set_author(name=member, icon_url=member.avatar_url)
            e.add_field(name="True", value=true, inline=False)
            e.add_field(name="False", value=false, inline=False)

            await edit(ctx, embed=e)


def setup(bot):
    bot.add_cog(Mod(bot))
