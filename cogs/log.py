import discord
import logging

from discord.ext import commands
from .utils.checks import edit, getChannel, getGuild, getUser, getWithoutInvoke, save_config, save_log

log = logging.getLogger('LOG')


class Logging:

    def __init__(self, bot):
        self.bot = bot

    # Log Help
    @commands.group(aliases=["Log"])
    async def log(self, ctx):
        """Command group for managing logging."""
        if ctx.invoked_subcommand is None:
            await edit(ctx, content='\N{HEAVY EXCLAMATION MARK SYMBOL} ``on``, ``off``, ``status``, ``show``, ``key <word>``, ``guild``, ``channel``, ``blacklist channel`` or ``blacklist <word>````blacklist user <user>``', ttl=5)

    # Log On
    @log.command(aliases=["On"])
    async def on(self, ctx):
        """Set Logging to on."""
        await save_config('setlog', 'on')
        self.bot.setlog = 'on'
        await edit(ctx, content='\N{HEAVY CHECK MARK} Mention Log set to ``on``', ttl=3)

    # Log Off
    @log.command(aliases=["Off"])
    async def off(self, ctx):
        """Set Logging to off."""
        await save_config('setlog', 'off')
        self.bot.setlog = 'off'
        await edit(ctx, '\N{HEAVY CHECK MARK} Mention Log set to ``off``', ttl=3)

    # Log Status
    @log.command(aliases=["Status"])
    async def status(self, ctx):
        """Show Logging Status."""
        await edit(ctx, content='<:robot:273922151856209923> Mention logging is currently ``%s``' % self.bot.setlog, ttl=3)

    # Add Key-Word to Logger
    @log.command(aliases=["Key"])
    async def key(self, ctx, msg: str):
        """Add a keyword to the logger."""
        msg = msg.lower()
        keys = self.bot.log_key
        if msg in self.bot.log_block_key:
            await edit('\N{HEAVY EXCLAMATION MARK SYMBOL} Already in logger used',  ttl=5)
            return
        if msg in keys:
            keys.remove(msg)
            self.bot.key = keys
            await save_log('key', keys)
            await edit(ctx, content='\N{HEAVY CHECK MARK} Removed Keyword ``%s`` from Logger' % msg,  ttl=5)
        elif msg not in keys:
            keys.append(msg)
            self.bot.key = keys
            await save_log('key', keys)
            await edit(ctx, content='\N{HEAVY CHECK MARK} Added Keyword ``%s`` to Logger' % msg,  ttl=5)

    # log Guild
    @log.command(aliases=["Guild"])
    @commands.guild_only()
    async def guild(self, ctx):
        """Add a guild to the logger."""
        guilds = self.bot.log_guild
        guild = getGuild(ctx, getWithoutInvoke(ctx)).id
        if guild:
            if guild in guilds:
                guilds.remove(guild)
                self.bot.log_guild = guilds
                await save_log('guild', guilds)
                await edit(ctx, content='\N{HEAVY CHECK MARK} Removed guild with ID ``%s`` from logger' % guild,  ttl=5)
            else:
                guilds.append(guild)
                self.bot.log_guild = guilds
                await save_log('guild', guilds)
                await edit(ctx, content='\N{HEAVY CHECK MARK} Added guild with ID ``%s`` to logger' % guild,  ttl=5)
        else:
            await edit(ctx, content='\N{HEAVY EXCLAMATION MARK SYMBOL} No Guild found',  ttl=5)

    # Log Channel
    @log.command(aliases=["Channel"])
    @commands.guild_only()
    async def channel(self, ctx):
        """Add a channel to the logger."""
        channels = self.bot.log_channel
        channel = getChannel(ctx, getWithoutInvoke(ctx)).id
        if channel:
            if channel in self.bot.log_block_channel:
                await edit('\N{HEAVY EXCLAMATION MARK SYMBOL} Already in blacklist used',  ttl=5)
                return
            if channel in channels:
                channels.remove(channel)
                self.bot.log_channel = channels
                await save_log('channel', channels)
                await edit(ctx, content='\N{HEAVY CHECK MARK} Removed Channel with ID ``%s`` from logger' % channel,  ttl=5)
            else:
                channels.append(channel)
                self.bot.log_channel = channels
                await save_log('channel', channels)
                await edit(ctx, content='\N{HEAVY CHECK MARK} Added Channel with ID ``%s`` to logger' % channel,  ttl=5)
        else:
            await edit(ctx, content='\N{HEAVY EXCLAMATION MARK SYMBOL} No Chnnael found',  ttl=5)

    # Show Logging Infosconfig
    @log.command(aliases=["Show"])
    async def show(self, ctx):
        """Show Info about logged things."""
        ttl = None if ctx.message.content.endswith(' stay') else 20
        em = discord.Embed(title='Logging Info', colour=discord.Color.purple())

        keys = ', '.join(self.bot.log_key)
        if keys is not '':
            em.add_field(name="Logged Words[%s] " % len(self.bot.log_key), value=keys)

        guilds = ', '.join(str(self.bot.get_guild(i)) for i in self.bot.log_guild)
        if guilds is not '':
            if len(guilds) < 1024:
                em.add_field(name="Logged Guilds[%s]" % len(self.bot.log_guild), value=guilds, inline=False)
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
                        em.add_field(name="Logged Guilds[%s]" % len(self.bot.log_guild), value=x[:-2], inline=False)
                    else:
                        em.add_field(name=u"\u2063", value=x[:-2], inline=False)
        channel2 = ', '.join(str(self.bot.get_channel(i)) for i in self.bot.log_channel)
        if channel2 is not '':
            em.add_field(name="Logged Channels[%s]" % len(self.bot.log_channel), value=channel2, inline=False)

        blocked = ', '.join(self.bot.log_block_key)
        if blocked is not '':
            em.add_field(name="Blocked Words[%s] " % len(self.bot.log_block_key), value=blocked)

        blocked_users = self.bot.log_block_user
        for x in blocked_users:
            if discord.utils.find(lambda u: x == u.id, ctx.bot.users) is None:
                blocked_users.remove(x)
                self.bot.log_block_user = blocked_users
                await save_log('block-user', blocked_users)
                log.info('Removed User with the ID: {} from Blacklist due to not finding it.'.format(x))

        users = ', '.join(str(u) for u in self.bot.users if u.id in self.bot.log_block_user)
        if users is not '':
            em.add_field(name="Blocked Users[%s]" % len(self.bot.log_block_user), value=users, inline=False)

        channel = ', '.join(str(self.bot.get_channel(i)) for i in self.bot.log_block_channel)
        if channel is not '':
            em.add_field(name="Blocked Channels[%s]" % len(self.bot.log_block_channel), value=channel, inline=False)

        await edit(ctx, embed=em, ttl=ttl)

    @log.group(aliases=["Blacklist"])
    @commands.guild_only()
    async def blacklist(self, ctx):
        """Blacklist things from the Logger."""
        ...

    # Add Blocked-Key-Word to Logger
    @blacklist.command(name="key", aliases=["Key"])
    async def _key(self, ctx, msg: str):
        """Add Keywords to the Blacklist."""
        msg = msg.lower()
        keys = self.bot.log_block_key
        if msg in self.bot.log_key:
            await edit('\N{HEAVY EXCLAMATION MARK SYMBOL} Already in logger used',  ttl=5)
            return
        if msg in keys:
            keys.remove(msg)
            self.bot.log_block_key = keys
            await save_log('block-key', keys)
            await edit(ctx, content='\N{HEAVY CHECK MARK} Unblocked ``%s`` from Logger' % msg,  ttl=5)
        elif msg not in keys:
            keys.append(msg)
            self.bot.log_block_key = keys
            await save_log('block-key', keys)
            await edit(ctx, content='\N{HEAVY CHECK MARK} Blocked ``%s`` from Logger' % msg,  ttl=5)

    # Blacklist Channel
    @blacklist.command(name="channel", aliases=["Channel"])
    @commands.guild_only()
    async def _channel(self, ctx):
        """Add a Channel to the Blacklist."""
        channels = self.bot.log_block_channel
        channel = getChannel(ctx, getWithoutInvoke(ctx)).id
        if channel:
            if channel in self.bot.log_channel:
                await edit('\N{HEAVY EXCLAMATION MARK SYMBOL} Already in logger used',  ttl=5)
                return
            if channel in channels:
                channels.remove(channel)
                self.bot.log_block_channel = channels
                await save_log('block-channel', channels)
                await edit(ctx, content='\N{HEAVY CHECK MARK} Removed Channel with ID ``%s`` from blacklist' % channel,  ttl=5)
            else:
                channels.append(channel)
                self.bot.log_block_channel = channels
                await save_log('block-channel', channels)
                await edit(ctx, content='\N{HEAVY CHECK MARK} Added Channel with ID ``%s`` to blacklist' % channel,  ttl=5)
        else:
            await edit(ctx, content='\N{HEAVY EXCLAMATION MARK SYMBOL} No Chnnael found',  ttl=5)

    # Blacklist user
    @blacklist.command(aliases=["User"])
    async def user(self, ctx, msg: str):
        """Add a User to the Blacklist."""
        users = self.bot.log_block_user
        user = getUser(ctx, msg)
        if not user:
            await edit('\N{HEAVY EXCLAMATION MARK SYMBOL} User not found',  ttl=5)
            return
        if user.id in users:
            users.remove(user.id)
            self.bot.log_block_user = users
            await save_log('block-user', users)
            await edit(ctx, content='\N{HEAVY CHECK MARK} Removed %s with ID ``%s`` from blacklist' % (ctx.message.guild.get_member(user.id), user.id),  ttl=5)
        else:
            users.append(user.id)
            self.bot.log_block_user = users
            await save_log('block-user', users)
            await edit(ctx, content='\N{HEAVY CHECK MARK} Added %s with ID ``%s`` to blacklist' % (ctx.message.guild.get_member(user.id), user.id),  ttl=5)

    # Automatically remove channel and guilds from blacklist on leave
    async def on_guild_remove(self, guild):
        log.info('Left Guild "{}" '.format(guild.name))

        guilds = self.bot.log_guild
        if guild.id in guilds:
            guilds.remove(guild.id)
            self.bot.log_guild = guilds
            await save_log('guild', guilds)
            log.info('Removed Guild "{}" on leave from logger'.format(guild.name))

        block_channels = self.bot.log_block_channel
        for channel in guild.channels:
            if channel.id in block_channels:
                block_channels.remove(channel.id)
                self.bot.log_block_channel = block_channels
                await save_log('block-channel', block_channels)
                log.info('Removed Channel "{}" in Guild "{}" on leave from blacklist'.format(channel.name, guild.name))

        channels = self.bot.log_channel
        if channel.id in channels:
            channels.remove(channel.id)
            self.bot.log_channel = channels
            await save_log('channel', channels)
            log.info('Removed Channel "{}" in Guild "{}" on leave from logger'.format(channel.name, channel.guild.name))

    # Automatically remove channel if it get's deleted
    async def on_channel_delete(self, channel):
        block_channels = self.bot.log_block_channel
        if channel.id in block_channels:
            block_channels.remove(channel.id)
            self.bot.log_block_channel = block_channels
            await save_log('block-channel', block_channels)
            log.info('Removed Channel "{}" in Guild "{}" on leave from blacklist'.format(channel.name, channel.guild.name))

        channels = self.bot.log_channel
        if channel.id in channels:
            channels.remove(channel.id)
            self.bot.log_channel = channels
            await save_log('channel', channels)
            log.info('Removed Channel "{}" in Guild "{}" on leave from logger'.format(channel.name, channel.guild.name))


def setup(bot):
    bot.add_cog(Logging(bot))
