import asyncio
import datetime
import json
import logging

from colour import Color
from discord import utils

log = logging.getLogger('LOG')
loop = asyncio.get_event_loop()
lock = asyncio.Lock()


def read_config(searched):
    with open('config/config.json', 'r') as f:
        cont = json.load(f)
        try:
            return cont[searched]
        except:
            return None


def read_log(searched):
    with open('config/log.json', 'r') as f:
        cont = json.load(f)
        try:
            return cont[searched]
        except:
            return None


def saving(file_name, field, value):
    with open('config/' + file_name, 'r') as q:
        content = json.load(q)
        secure_content = content
        with open('config/' + file_name, 'w') as f:
            try:
                content[field] = value
                f.seek(0)
                f.truncate()
                json.dump(content, f, indent=4, separators=(',', ':'))
                return True
            except:
                f.seek(0)
                f.truncate()
                json.dump(secure_content, f, indent=4, separators=(',', ':'))
                log.error("An Error occurd while saving")
                return False


async def save_config(field, value):
    with await lock:
        await loop.run_in_executor(None, saving, 'config.json', field, value)


async def save_log(field, value):
    with await lock:
        await loop.run_in_executor(None, saving, 'log.json', field, value)


# Edit thingy
async def edit(ctx, content=None, embed=None, ttl=None):
    perms = ctx.channel.permissions_for(ctx.me).embed_links
    try:
        if ttl and perms:
            await ctx.message.edit(content=content, embed=embed)
            await asyncio.sleep(ttl)
            try:
                await ctx.message.delete()
            except:
                log.error('Failed to delete Message in {}, #{}'.format(ctx.guild.name, ctx.channel.name))
                pass
        elif ttl is None and perms:
            await ctx.message.edit(content=content, embed=embed)
        elif embed is None:
            await ctx.message.edit(content=content, embed=embed)
        elif embed and not perms:
            await ctx.message.edit(content='\N{HEAVY EXCLAMATION MARK SYMBOL} No Perms for Embeds', delete_after=5)
    except:
        if embed and not perms:
            await ctx.message.edit(content='\N{HEAVY EXCLAMATION MARK SYMBOL} No Perms for Embeds', delete_after=5)
        else:
            await ctx.send(content=content, embed=embed, delete_after=ttl, file=None)


# Check if me
def me(self, message):
    return message.author.id == self.bot.user.id


# Check for perms of links and attached files
def permFile(message):
    return message.channel.permissions_for(message.author).attach_files


# Check for perms of links and attached files
def permEmbed(message):
    return message.channel.permissions_for(message.author).embed_links


# Get Message without inokation prefix and space after invokation
def getwithoutInvoke(ctx):
    message = ctx.message.content
    if message.endswith(' stay'):
        return message[len(ctx.prefix + ctx.command.qualified_name + ' '):-5]
    else:
        return message[len(ctx.prefix + ctx.command.qualified_name + ' '):]


# Get time difference obviously
def getTimeDiff(t, now=None):
    if now is None:
        now = datetime.datetime.utcnow()
    delta = now - t
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    return '{d}:{h}:{m}:{s}'.format(d=days, h=hours, m=minutes, s=seconds)


# Returns time that has passed since the given time(datetime) in seconds, minuts, hours or days
# Fuck Years, who cars, days is more intersting for comparison.
def getAgo(time):
    sec = int((datetime.datetime.utcnow() - time).total_seconds())
    if 120 > sec:
        return f'{sec} seconds ago'
    elif 3600 > sec:
        return '{} minutes ago'.format(sec // 60)
    elif 86400 > sec:
        return '{} hour ago'.format(sec // 60 // 60) if 7200 > sec else '{} hours ago'.format(sec // 60 // 60)
    else:
        return '{} day ago'.format(sec // 60 // 60 // 24) if 7200 > sec else '{} days ago'.format(sec // 60 // 60 // 24)


# Find User on server
def getUser(ctx, msg):
    if '' is msg:
        return ctx.message.author
    elif 1 == len(ctx.message.mentions):
        return ctx.message.mentions[0]
    elif not ctx.guild:
        return utils.find(lambda m: msg.lower() in m.name.lower(), ctx.bot.users)
    elif msg.isdigit():
        return ctx.guild.get_member(int(msg))
    elif ctx.message.guild.get_member_named(msg):
        return ctx.message.guild.get_member_named(msg)
    elif utils.find(lambda m: msg.lower() in m.name.lower(), ctx.message.guild.members):
        return utils.find(lambda m: msg.lower() in m.name.lower(), ctx.message.guild.members)
    else:
        for member in ctx.message.guild.members:
            if member.nick:
                if msg.lower() in member.nick.lower():
                    return member
                    break
    return None


# Find Guild
def getGuild(ctx, msg):
    if msg == '':
        return ctx.guild
    elif msg.isdigit():
        return ctx.bot.get_guild(int(msg))
    else:
        return utils.find(lambda g: msg.lower() in g.name.lower(), ctx.bot.guilds)
    return None


# Find Channel
def getChannel(ctx, msg):
    if msg == '':
        return ctx.channel
    elif 1 == len(ctx.message.channel_mentions):
        return ctx.message.channel_mentions[0]
    elif msg.isdigit():
        return ctx.bot.get_channel(int(msg))
    elif utils.find(lambda c: msg.lower() in c.name.lower(), ctx.guild.text_channels):
        return utils.find(lambda c: msg.lower() in c.name.lower(), ctx.guild.text_channels)
    else:
        return utils.find(lambda c: msg.lower() in c.name.lower(), ctx.bot.get_all_channels())
    return None


# Find Role
def getRole(ctx, msg):
    if msg == '':
        return ctx.guild.default_role
    if 1 == len(ctx.message.role_mentions):
        return ctx.message.role_mentions[0]
    elif msg.isdigit():
        return utils.find(lambda r: msg.strip() == r.id, ctx.guild.roles)
    else:
        return utils.find(lambda r: msg.strip().lower() in r.name.lower(), ctx.guild.roles)
    return None


# Find Color
def getColor(incolor):
    if len(incolor.split(',')) == 3:
        try:
            incolor = incolor.split(',')
            if float(incolor[0]) > 1.0 or float(incolor[1]) > 1.0 or float(incolor[2]) > 1.0:
                red = float(int(incolor[0]) / 255)
                blue = float(int(incolor[1]) / 255)
                green = float(int(incolor[2]) / 255)
            else:
                red = incolor[0]
                blue = incolor[1]
                green = incolor[2]
            outcolor = Color(rgb=(float(red), float(green), float(blue)))
        except:
            outcolor = None
    else:
        try:
            outcolor = Color(incolor)
        except:
            outcolor = None

        if outcolor is None:
            try:
                outcolor = Color('#' + incolor)
            except:
                outcolor = None
    return outcolor
