import asyncio
import datetime
import discord
import logging

from discord import utils
from discord.ext import commands
from .utils.checks import edit, getChannel, getColor, getRole, getUser, getWithoutInvoke

log = logging.getLogger('LOG')


class Mod:

    def __init__(self, bot):
        self.bot = bot

    # Do cleanup
    async def do_purge(self, ctx, limit, predicate):
        if limit:
            deleted = await ctx.channel.purge(limit=limit, before=ctx.message, check=predicate)
            await edit(ctx, content='Cleaned `{}` messages out of `{}` checked.'.format(len(deleted), limit), ttl=5)
            log.info('Pruned {} messages out of {} checked'.format(len(deleted), limit))
        else:
            await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Don't forget to give the amount you wanna delte".format(len(deleted), limit), ttl=5)

    # Purge group
    @commands.group(aliases=['purge', 'Purge', 'Clean'])
    @commands.guild_only()
    async def clean(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    # Remove embeds
    @clean.command(aliases=['Embed', 'embed', 'Embeds'])
    @commands.has_permissions(manage_messages=True)
    async def embeds(self, ctx, search: int = None):
        await self.do_purge(ctx, search, lambda e: len(e.embeds))

    # Remove images/attachments
    @clean.command(aliases=['Attachments', 'Attachment', 'attachment'])
    @commands.has_permissions(manage_messages=True)
    async def attachments(self, ctx, search: int = None):
        await self.do_purge(ctx, search, lambda e: len(e.attachments))

    # Remove all
    @clean.command(name='all', aliases=['All'])
    @commands.has_permissions(manage_messages=True)
    async def _all(self, ctx, search: int = None):
        await self.do_purge(ctx, search, lambda e: True)

    # Remove from specific user
    @clean.command(aliases=['User'])
    @commands.has_permissions(manage_messages=True)
    async def user(self, ctx, mem: str, search: int = None):
        member = getUser(ctx, mem)
        await self.do_purge(ctx, search, lambda e: e.author == member)

    # remove your own message, works everywhere not like all other purges.
    @clean.command(aliases=['Mine'])
    async def mine(self, ctx, search: int = None):
        await self.do_purge(ctx, search, lambda e: e.author == ctx.author)

    # Mute a Member
    @commands.command(aliases=['Mute'])
    @commands.has_permissions(manage_roles=True)
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def mute(self, ctx, mem: str):
        member = getUser(ctx, mem)
        if member:
            if not utils.find(lambda r: "Muted" == r.name, ctx.message.guild.roles):
                perms = utils.find(lambda r: "@everyone" == r.name, ctx.message.guild.roles).permissions
                role = await ctx.guild.create_role(name="Muted", permissions=perms)
                log.info('Created role: Muted')
                for channel in ctx.guild.text_channels:
                    await channel.set_permissions(role, overwrite=discord.PermissionOverwrite(send_messages=False, add_reactions=False))
                for channel in ctx.guild.voice_channels:
                    await channel.set_permissions(role, overwrite=discord.PermissionOverwrite(speak=False))
                log.info('Prepared Mute role for mutes in channels')
            if utils.find(lambda r: "Muted" == r.name, ctx.message.guild.roles) not in member.roles:
                role = utils.find(lambda r: "Muted" == r.name, ctx.message.guild.roles)
                roles = member.roles
                roles.append(role)
                asyncio.sleep(0.5)
                await member.edit(roles=roles)
                log.info(f'Muted {member}')

                e = discord.Embed(color=discord.Color.purple())
                e.set_author(name="\N{SPEAKER WITH CANCELLATION STROKE} Muted " + str(member))
                await edit(ctx, embed=e)
            else:
                await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Already muted", ttl=5)

    # Mute a Member
    @commands.command(aliases=['Unmute'])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def unmute(self, ctx, mem: str):
        member = getUser(ctx, mem)
        if member:
            if utils.find(lambda r: "Muted" == r.name, ctx.message.guild.roles) in member.roles:
                role = utils.find(lambda r: "Muted" == r.name, ctx.message.guild.roles)
                roles = member.roles
                roles.remove(role)
                asyncio.sleep(0.5)
                await member.edit(roles=roles)
                log.info(f'Unmuted {member}')

                e = discord.Embed(color=discord.Color.purple())
                e.set_author(name="\N{SPEAKER} Unmuted " + str(member))
                await edit(ctx, embed=e)
            else:
                await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Member is not muted", ttl=5)

    # Kick a Member
    @commands.command(aliases=['Kick'])
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx):
        member = getUser(ctx, getWithoutInvoke(ctx))
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
    @commands.command(aliases=['Ban'])
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx):
        if ctx.invoked_subcommand is None:
            member = getUser(ctx, getWithoutInvoke(ctx))
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
    @commands.command(aliases=['Softban'])
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def softban(self, ctx):
        member = getUser(ctx, getWithoutInvoke(ctx))
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

    @commands.command(name="role-color", aliases=['role-colour', 'Role-Colour', 'Role-Color'])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def _colour(self, ctx, role: str, colour: str):
        role = getRole(ctx, role)
        colour = getColor(colour)
        if not role:
            return await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Role not found", ttl=5)
        elif not colour:
            return await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Colour not found", ttl=5)
        else:
            value = discord.Colour(int((colour.hex_l.strip('#')), 16))
            try:
                await role.edit(colour=value)
            except discord.HTTPException:
                await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Missing permissions to edit this role", ttl=5)
            else:
                e = discord.Embed(color=value)
                e.set_author(name="Changed Role Color of: " + str(role))
                await edit(ctx, embed=e)

    @commands.command(aliases=['Permissions', 'Perms', 'perms'])
    @commands.guild_only()
    async def permissions(self, ctx):
        member = getUser(ctx, getWithoutInvoke(ctx))
        if member:
            true = '\n'.join(name.replace('_', ' ').title() for name, value in ctx.channel.permissions_for(member) if value is True)
            false = '\n'.join(name.replace('_', ' ').title() for name, value in ctx.channel.permissions_for(member) if value is False)

            e = discord.Embed(title="Permissions", color=discord.Color.purple(), timestamp=datetime.datetime.now())
            e.set_author(name=member, icon_url=member.avatar_url)
            e.add_field(name="True", value=true, inline=False)
            e.add_field(name="False", value=false, inline=False)

            await edit(ctx, embed=e, ttl=20)

    # Add or remove a role to a Member
    @commands.command(aliases=['Addrole'])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def addrole(self, ctx, mem: str, ro: str):
        member = getUser(ctx, mem)
        role = getRole(ctx, ro)
        if member and role:
            if role not in member.roles:
                roles = member.roles
                roles.append(role)
                asyncio.sleep(0.5)
                await member.edit(roles=roles)
                log.info(f'Added {role.name} to {member}')

                e = discord.Embed(color=role.color)
                e.set_author(name=f"Added {role.name} to {member}")
                await edit(ctx, embed=e, ttl=5)
            else:
                await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Member already has the selected role", ttl=5)
        elif not member and role:
            await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Member not found", ttl=5)
        elif not role and member:
            await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Role not found", ttl=5)
        else:
            await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Member and Role not found", ttl=5)

    # Add or remove a role to a Member
    @commands.command(aliases=['Removerole'])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def removerole(self, ctx, mem: str, ro: str):
        member = getUser(ctx, mem)
        role = getRole(ctx, ro)
        if member and role:
            if role in member.roles:
                roles = member.roles
                roles.remove(role)
                asyncio.sleep(0.5)
                await member.edit(roles=roles)
                log.info(f'Removed {role.name} to {member}')

                e = discord.Embed(color=role.color)
                e.set_author(name=f"Removed {role.name} from {member}")
                await edit(ctx, embed=e, ttl=5)
            else:
                await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Member does not have the selected role", ttl=5)
        elif not member and role:
            await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Member not found", ttl=5)
        elif not role and member:
            await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Role not found", ttl=5)
        else:
            await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Member and Role not found", ttl=5)

    # Add or remove a role to a Member
    @commands.command(aliases=['Lock'])
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def lock(self, ctx):
        channel = getChannel(ctx, getWithoutInvoke(ctx))
        if channel:
            if channel in ctx.guild.text_channels:
                perms = channel.overwrites_for(ctx.guild.default_role)
                perms.send_messages = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
                log.info(f'Locked down channel #{ctx.channel}')

                e = discord.Embed(color=discord.Color.purple())
                e.set_author(name=f'Locked down channel #{ctx.channel}')
                await edit(ctx, embed=e)
            else:
                await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Selected Channel is not in this guild", ttl=5)
        else:
            await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Channel not found", ttl=5)

    # Add or remove a role to a Member
    @commands.command(aliases=['Unlock'])
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def unlock(self, ctx):
        channel = getChannel(ctx, getWithoutInvoke(ctx))
        if channel:
            if channel in ctx.guild.text_channels:
                perms = channel.overwrites_for(ctx.guild.default_role)
                perms.send_messages = True
                await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
                log.info(f'Unlocked channel #{ctx.channel}')

                e = discord.Embed(color=discord.Color.purple())
                e.set_author(name=f'Unlocked channel #{ctx.channel}')
                await edit(ctx, embed=e)
            else:
                await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Selected Channel is not in this guild", ttl=5)
        else:
            await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} Channel not found", ttl=5)


def setup(bot):
    bot.add_cog(Mod(bot))
