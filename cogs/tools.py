import datetime
import discord
import os
import platform
import psutil

from discord import utils
from discord.ext import commands
from .utils.checks import edit, getColor, getRole, getTimeDiff, getWithoutInvoke, save_config


class Tools:

    def __init__(self, bot):
        self.bot = bot

    # Command usage stats
    @commands.command(aliases=["Cmdstats"])
    async def cmdstats(self, ctx):
        """A Statistik about your used commands."""
        counter = self.bot.commands_triggered
        width = len(max(counter, key=len))
        total = sum(counter.values())
        fmt = '{0:<{width}}: {1}'
        output = '\n'.join(fmt.format(key, count, width=width) for key, count in counter.most_common())
        await edit(ctx, content='```{}\n{}```'.format(fmt.format('Total', total, width=width), output))

    @commands.command(aliases=["Socketstats"])
    async def socketstats(self, ctx):
        """A Statistik about Discords Socket Events you see."""
        delta = datetime.datetime.utcnow() - self.bot.uptime
        minutes = delta.total_seconds() / 60
        total = sum(self.bot.socket_stats.values())
        cpm = total / minutes

        fmt = '%s socket events observed (%.2f/minute):\n%s'
        await edit(ctx, content=fmt % (total, cpm, self.bot.socket_stats))

    # Ping Time
    @commands.command(aliases=["Ping"])
    async def ping(self, ctx):
        """Time the websocket takes to rspond."""
        ttl = None if ctx.message.content.endswith(' stay') else 10
        before = datetime.datetime.utcnow()
        await (await self.bot.ws.ping())
        ping = (datetime.datetime.utcnow() - before) * 1000
        pong = discord.Embed(title='Pong!', colour=discord.Color.purple())
        pong.add_field(name="Response Time:", value='{:.2f}ms'.format(ping.total_seconds()))
        pong.set_thumbnail(url='http://i.imgur.com/SKEmkvf.png')
        await edit(ctx, embed=pong, ttl=ttl)

    # Time Since Bot is running
    @commands.command(aliases=["Uptime"])
    async def uptime(self, ctx):
        """Show how long the Bot is running already."""
        ttl = None if ctx.message.content.endswith(' stay') else 20
        embed = discord.Embed(title='\N{CLOCK FACE THREE OCLOCK} UPTIME', colour=discord.Color.purple())
        embed.add_field(name='﻿ ', value=getTimeDiff(self.bot.uptime), inline=False)
        embed.set_thumbnail(url='http://i.imgur.com/mfxd06f.gif')
        await edit(ctx, embed=embed, ttl=ttl)

    # Various stat about the bot since startup
    @commands.command(aliases=["Stats"])
    async def stats(self, ctx):
        """Several interesting informations about your Bot."""
        ttl = None if ctx.message.content.endswith(' stay') else 20
        unique_online = len(dict((m.id, m) for m in self.bot.get_all_members() if m.status != discord.Status.offline))
        voice = sum(len(g.voice_channels) for g in self.bot.guilds)
        text = sum(len(g.text_channels) for g in self.bot.guilds)
        embed = discord.Embed(title='\N{ELECTRIC LIGHT BULB} Bot Info', colour=discord.Color.purple())
        embed.add_field(name='\N{CLOCK FACE THREE OCLOCK} UPTIME',
                        value=getTimeDiff(self.bot.uptime), inline=True)
        embed.add_field(name='\N{INBOX TRAY} Messages Received',
                        value=(self.bot.message_count - self.bot.icount), inline=True)
        embed.add_field(name='\N{OUTBOX TRAY} Messages Sent',
                        value=self.bot.icount, inline=True)
        embed.add_field(name='\N{SPEAKING HEAD IN SILHOUETTE} Members [%s]' % len(self.bot.users),
                        value='%s Online' % unique_online, inline=True)
        embed.add_field(name='\N{SPIRAL NOTE PAD} Channels [%s]' % (text + voice),
                        value='%s Text | %s Voice' % (text, voice), inline=True)
        embed.add_field(name='\N{TICKET} Guilds',
                        value=len(self.bot.guilds))
        embed.add_field(name='\N{BELL} Mentions [%s]' % (self.bot.mention_count + self.bot.mention_count_name),
                        value='%s Pings | %s Names' % (self.bot.mention_count, self.bot.mention_count_name), inline=True)
        embed.add_field(name='\N{SPEECH BALLOON} Commands Used',
                        value=sum(self.bot.commands_triggered.values()), inline=True)
        try:
            embed.add_field(name='\N{ANTICLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS} Most Used',
                            value='%s [%s]' % (self.bot.commands_triggered.most_common()[0][0], self.bot.commands_triggered.most_common()[0][1]))
        except:
            embed.add_field(name='\N{ANTICLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS} Most Used',
                            value='﻿None')
        await edit(ctx, embed=embed, ttl=ttl)

    # Host System Infos
    @commands.command(aliases=["Sysinfo"])
    async def sysinfo(self, ctx):
        """Several interesting informations about your Host System."""
        ttl = None if ctx.message.content.endswith(' stay') else 20
        process = psutil.Process(os.getpid())
        memory_usage = process.memory_full_info().uss / 1024**2
        avai = psutil.virtual_memory().total / 1024**2
        mepro = process.memory_percent()
        prosys = psutil.cpu_percent()
        sys = '%s %s' % (platform.linux_distribution(full_distribution_name=1)[0].title(), platform.linux_distribution(full_distribution_name=1)[1])
        embed = discord.Embed(title='\N{ELECTRIC LIGHT BULB} Host Info', colour=discord.Color.purple())
        embed.add_field(name='\N{CLOCK FACE THREE OCLOCK} UPTIME',
                        value=getTimeDiff(datetime.datetime.fromtimestamp(int(process.create_time())), datetime.datetime.now()))
        embed.add_field(name='\N{DESKTOP COMPUTER} SYSTEM',
                        value='{0}, {1}'.format(platform.system(), sys, platform.release()))
        embed.add_field(name='\N{FLOPPY DISK} MEMORY',
                        value='{:.2f} MiB / {:.2f} MiB\nBot uses: {:.2f}%'.format(memory_usage, avai, mepro))
        embed.add_field(name='\N{DVD} CPU',
                        value='{:.2f}%'.format(prosys))
        await edit(ctx, embed=embed, ttl=ttl)

    # Change Gamestatus - blank is no game
    @commands.command(aliases=["Game"])
    async def game(self, ctx):
        """Change or remove your game."""
        ttl = None if ctx.message.content.endswith(' stay') else 5
        game = getWithoutInvoke(ctx)
        if game == '':
            await save_config('gamestatus', None)
            self.bot.gamename = None
            await edit(ctx, content='\N{VIDEO GAME} Removed Game Status',  ttl=ttl)
        else:
            await save_config('gamestatus', game)
            self.bot.gamename = game
            await edit(ctx, content='\N{VIDEO GAME} Now playing: ``%s``' % self.bot.gamename,  ttl=ttl)

    # Find message with specific Text in Channel History...    Search Term(s) | Text
    @commands.command(aliases=["Quote"])
    async def quote(self, ctx):
        """Quote messages by Id or text."""
        search = getWithoutInvoke(ctx)
        content = '\U0000200d'
        if '|' in search:
            msg = search.split(" | ")
            search = msg[0]
            content = msg[1]
        mess = None
        if search.isdigit():
            async for message in ctx.message.channel.history(limit=500):
                if message.id == int(search):
                    mess = message
        else:
            async for message in ctx.message.channel.history(limit=500):
                if message.id != ctx.message.id and search in message.content:
                    mess = message
        if mess is not None:
            em = discord.Embed(description=mess.clean_content, timestamp=mess.created_at, colour=0x33CC66)
            em.set_author(name=mess.author.display_name, icon_url=mess.author.avatar_url)
            await edit(ctx, content=content, embed=em)
        else:
            await edit(ctx, content='Message not found!', ttl=3)

    # Colours
    @commands.command(aliases=['colour', 'Colour', 'Color'])
    async def color(self, ctx):
        """Convert Color from HEX to RGB or simply search for webcolors."""
        color = getColor(getWithoutInvoke(ctx).strip())
        if color is None:
            role = getRole(ctx, getWithoutInvoke(ctx))
            if role:
                color = getColor(str(role.color))
        if color:
            value = color.hex_l.strip('#')
            rgb = tuple(int(value[i:i + len(value) // 3], 16) for i in range(0, len(value), len(value) // 3))

            e = discord.Embed(title=color.web.title(), colour=int((value), 16))
            e.url = f'http://www.colorhexa.com/{value}'
            e.add_field(name='HEX', value=color.hex_l, inline=False)
            e.add_field(name='RGB', value=rgb, inline=False)
            e.set_thumbnail(url=f'http://www.colorhexa.com/{value}.png')
            await edit(ctx, embed=e)
        else:
            await edit(ctx, '\N{HEAVY EXCLAMATION MARK SYMBOL} Could not find color', ttl=3)

    # Jumbo Emote
    @commands.command(aliases=["Jumbo"])
    async def jumbo(self, ctx):
        """Display your favorite emotes in large."""
        e = self.emoji_reg.findall(ctx.message.content)
        if e:
            if len(e) > 1:
                await edit(ctx, content='\N{HEAVY EXCLAMATION MARK SYMBOL} Only One Emote...', ttl=3)
            else:
                emo = utils.get(self.bot.emojis, id=int(e[0]))
                if emo:
                    em = discord.Embed(colour=discord.Color.purple())
                    em.set_image(url=emo.url)
                    await edit(ctx, embed=em)
        else:
            await edit(ctx, content='\N{HEAVY EXCLAMATION MARK SYMBOL} Only Emotes...', ttl=3)


def setup(bot):
    bot.add_cog(Tools(bot))
