import discord
import logging

from discord.ext import commands
from .utils import config
from .utils.checks import getUser, edit, getwithoutInvoke, getGuild, getChannel

log = logging.getLogger('LOG')


class Logging:

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('config.json')
        self.logging = config.Config('log.json')

    # Log Help
    @commands.group(aliases=["Log"])
    async def log(self, ctx):
        if ctx.invoked_subcommand is None:
            await edit(ctx, content='\N{HEAVY EXCLAMATION MARK SYMBOL} ``on``, ``off``, ``status``, ``key <word>``, ``block <word>``, ``show``, ``blacklist guild``, ``blacklist channel`` or ``blacklist user <user>``', ttl=5)

    # Log On
    @log.command(aliases=["On"])
    async def on(self, ctx):
        await self.config.put('setlog', 'on')
        await edit(ctx, content='\N{HEAVY CHECK MARK} Mention Log set to ``on``', ttl=3)

    # Log Off
    @log.command(aliases=["Off"])
    async def off(self, ctx):
        await self.config.put('setlog', 'off')
        await edit(ctx, content='\N{HEAVY CHECK MARK} Mention Log set to ``off``', ttl=3)

    # Log Status
    @log.command(aliases=["Status"])
    async def status(self, ctx):
        await edit(ctx, content='<:robot:273922151856209923> Mention logging is currently ``%s``' % self.config.get('setlog', []), ttl=3)

    # Add Key-Word to Logger
    @log.command(aliases=["Key"])
    async def key(self, ctx, msg: str):
        msg = msg.lower()
        keys = self.logging.get('key', {})
        if msg in self.logging.get('block-key', {}):
            await edit('\N{HEAVY EXCLAMATION MARK SYMBOL} Already in logger used',  ttl=5)
            return
        if msg in keys:
            keys.remove(msg)
            await self.logging.put('key', keys)
            await edit(ctx, content='\N{HEAVY CHECK MARK} Removed Keyword ``%s`` from Logger' % msg,  ttl=5)
        elif msg not in keys:
            keys.append(msg)
            await self.logging.put('key', keys)
            await edit(ctx, content='\N{HEAVY CHECK MARK} Added Keyword ``%s`` to Logger' % msg,  ttl=5)

    # log Guild
    @log.command(aliases=["Guild"])
    @commands.guild_only()
    async def guild(self, ctx):
        guilds = self.logging.get('guild', {})
        guild = getGuild(ctx, getwithoutInvoke(ctx)).id
        if guild:
            if guild in guilds:
                guilds.remove(guild)
                await self.logging.put('guild', guilds)
                await edit(ctx, content='\N{HEAVY CHECK MARK} Removed guild with ID ``%s`` from logger' % guild,  ttl=5)
            else:
                guilds.append(guild)
                await self.logging.put('guild', guilds)
                await edit(ctx, content='\N{HEAVY CHECK MARK} Added guild with ID ``%s`` to logger' % guild,  ttl=5)
        else:
            await edit(ctx, content='\N{HEAVY EXCLAMATION MARK SYMBOL} No Guild found',  ttl=5)

    # Log Channel
    @log.command(aliases=["Channel"])
    @commands.guild_only()
    async def channel(self, ctx):
        channels = self.logging.get('channel', {})
        channel = getChannel(ctx, getwithoutInvoke(ctx)).id
        if channel:
            if channel in self.logging.get('block-channel', {}):
                await edit('\N{HEAVY EXCLAMATION MARK SYMBOL} Already in blacklist used',  ttl=5)
                return
            if channel in channels:
                channels.remove(channel)
                await self.logging.put('channel', channels)
                await edit(ctx, content='\N{HEAVY CHECK MARK} Removed Channel with ID ``%s`` from logger' % channel,  ttl=5)
            else:
                channels.append(channel)
                await self.logging.put('channel', channels)
                await edit(ctx, content='\N{HEAVY CHECK MARK} Added Channel with ID ``%s`` to logger' % channel,  ttl=5)
        else:
            await edit(ctx, content='\N{HEAVY EXCLAMATION MARK SYMBOL} No Chnnael found',  ttl=5)

    # Show Logging Infosconfig
    @log.command(aliases=["Show"])
    async def show(self, ctx):
        self.logging = config.Config('log.json')
        ttl = None if ctx.message.content.endswith(' stay') else 20
        em = discord.Embed(title='Logging Info', colour=discord.Color.purple())

        keys = ', '.join(self.logging.get('key', {}))
        if keys is not '':
            em.add_field(name="Logged Words[%s] " % len(self.logging.get('key', {})), value=keys)

        blocked = ', '.join(self.logging.get('block-key', {}))
        if blocked is not '':
            em.add_field(name="Blocked Words[%s] " % len(self.logging.get('block-key', {})), value=blocked)

        guilds = ', '.join(str(self.bot.get_guild(i)) for i in self.logging.get('guild', {}))
        if guilds is not '':
            if len(guilds) < 1024:
                em.add_field(name="Logged Guilds[%s]" % len(self.logging.get('guild', {})), value=guilds, inline=False)
            else:
                temp = []
                first = True
                count = 1
                se = ''
                for i in guilds.split(', '):
                    if len(se + i + ', ') < 1024:
                        if count == len(guilds.split(', ')):
                            se += i + ', '
                            temp.append(se)
                        else:
                            se += i + ', '
                            count += 1
                    else:
                        temp.append(se)
                        se = i + ', '
                        count += 1
                for x in temp:
                    if first:
                        first = False
                        em.add_field(name="Logged Guilds[%s]" % len(self.logging.get('guild', {})), value=x[:-2], inline=False)
                    else:
                        em.add_field(name=u"\u2063", value=x[:-2], inline=False)

        users = ', '.join(str(u) for u in self.bot.users if u.id in self.logging.get('block-user', {}))
        if users is not '':
            em.add_field(name="Blocked Users[%s]" % len(self.logging.get('block-user', {})), value=users, inline=False)

        channel = ', '.join(str(self.bot.get_channel(i)) for i in self.logging.get('block-channel', {}))
        if channel is not '':
            em.add_field(name="Blocked Channels[%s]" % len(self.logging.get('block-channel', {})), value=channel, inline=False)

        channel2 = ', '.join(str(self.bot.get_channel(i)) for i in self.logging.get('channel', {}))
        if channel2 is not '':
            em.add_field(name="Logged Channels[%s]" % len(self.logging.get('channel', {})), value=channel2, inline=False)

        await edit(ctx, embed=em, ttl=ttl)

    @log.group(aliases=["Blacklist"])
    @commands.guild_only()
    async def blacklist(self, ctx):
        ...

    # Add Blocked-Key-Word to Logger
    @blacklist.command(name="key", aliases=["Key"])
    async def _key(self, ctx, msg: str):
        msg = msg.lower()
        keys = self.logging.get('block-key', {})
        if msg in self.logging.get('key', {}):
            await edit('\N{HEAVY EXCLAMATION MARK SYMBOL} Already in logger used',  ttl=5)
            return
        if msg in keys:
            keys.remove(msg)
            await self.logging.put('block-key', keys)
            await edit(ctx, content='\N{HEAVY CHECK MARK} Unblocked ``%s`` from Logger' % msg,  ttl=5)
        elif msg not in keys:
            keys.append(msg)
            await self.logging.put('block-key', keys)
            await edit(ctx, content='\N{HEAVY CHECK MARK} Blocked ``%s`` from Logger' % msg,  ttl=5)

    # Blacklist Channel
    @blacklist.command(name="channel", aliases=["Channel"])
    @commands.guild_only()
    async def _channel(self, ctx):
        channels = self.logging.get('block-channel', {})
        channel = getChannel(ctx, getwithoutInvoke(ctx)).id
        if channel:
            if channel in self.logging.get('channel', {}):
                await edit('\N{HEAVY EXCLAMATION MARK SYMBOL} Already in logger used',  ttl=5)
                return
            if channel in channels:
                channels.remove(channel)
                await self.logging.put('block-channel', channels)
                await edit(ctx, content='\N{HEAVY CHECK MARK} Removed Channel with ID ``%s`` from blacklist' % channel,  ttl=5)
            else:
                channels.append(channel)
                await self.logging.put('block-channel', channels)
                await edit(ctx, content='\N{HEAVY CHECK MARK} Added Channel with ID ``%s`` to blacklist' % channel,  ttl=5)
        else:
            await edit(ctx, content='\N{HEAVY EXCLAMATION MARK SYMBOL} No Chnnael found',  ttl=5)

    # Blacklist user
    @blacklist.command(aliases=["User"])
    async def user(self, ctx, msg: str):
        await ctx.message.delete()
        users = self.logging.get('block-user', {})
        user = getUser(ctx, msg)
        if not user:
            await edit('\N{HEAVY EXCLAMATION MARK SYMBOL} User not found',  ttl=5)
            return
        if user.id in users:
            users.remove(user.id)
            await self.logging.put('block-user', users)
            await edit(ctx, content='\N{HEAVY CHECK MARK} Removed %s with ID ``%s`` from blacklist' % (ctx.message.guild.get_member(user.id), user.id),  ttl=5)
        else:
            users.append(user.id)
            await self.logging.put('block-user', users)
            await edit(ctx, content='\N{HEAVY CHECK MARK} Added %s with ID ``%s`` to blacklist' % (ctx.message.guild.get_member(user.id), user.id),  ttl=5)

    # Automatically remove channel and guilds from blacklist on leave
    async def on_guild_remove(self, guild):
        log.info('Left Guild "{}" '.format(guild.name))

        guilds = self.logging.get('guild', [])
        if guild.id in guilds:
            guilds.remove(guild.id)
            await self.logging.put('guild', guilds)
            log.info('Removed Guild "{}" on leave from logger'.format(guild.name))

        channels = self.logging.get('block-channel', [])
        for channel in guild.channels:
            if channel.id in channels:
                channels.remove(channel.id)
                await self.logging.put('block-channel', channels)
                log.info('Removed Channel "{}" in Guild "{}" on leave from blacklist'.format(channel.name, guild.name))

        channels2 = self.logging.get('channel', [])
        if channel.id in channels2:
            channels2.remove(channel.id)
            await self.logging.put('channel', channels)
            log.info('Removed Channel "{}" in Guild "{}" on leave from logger'.format(channel.name, channel.guild.name))

    # Automatically remove channel if it get's deleted
    async def on_channel_delete(self, channel):
        channels = self.logging.get('block-channel', [])
        if channel.id in channels:
            channels.remove(channel.id)
            await self.logging.put('block-channel', channels)
            log.info('Removed Channel "{}" in Guild "{}" on leave from blacklist'.format(channel.name, channel.guild.name))

        channels2 = self.logging.get('channel', [])
        if channel.id in channels2:
            channels2.remove(channel.id)
            await self.logging.put('channel', channels)
            log.info('Removed Channel "{}" in Guild "{}" on leave from logger'.format(channel.name, channel.guild.name))


def setup(bot):
    bot.add_cog(Logging(bot))
