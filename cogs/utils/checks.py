import asyncio
import datetime
import json
import logging

from discord import utils

log = logging.getLogger('LOG')

with open('config/config.json', 'r') as f:
    config = json.load(f)


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
            await ctx.edit(content='\N{HEAVY EXCLAMATION MARK SYMBOL} No Perms for Embeds', delete_after=5)
    except:
        await ctx.send(content=content, embed=embed, delete_after=ttl, file=None)


# Check if me
def me(message):
    return message.author.id == config['me']


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
        return '{} minutes ago'.format(sec//60)
    elif 86400 > sec:
        return '{} hour ago'.format(sec//60//60) if 7200 > sec else '{} hours ago'.format(sec//60//60)
    else:
        return '{} day ago'.format(sec//60//60//24) if 7200 > sec else '{} days ago'.format(sec//60//60//24)


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
        return ctx.channel.id
    elif 1 == len(ctx.message.channel_mentions):
        return ctx.message.channel_mentions[0]
    elif msg.isdigit():
        return ctx.bot.get_channel(int(msg))
    elif utils.find(lambda c: msg.lower() in c.name.lower(), ctx.guild.text_channels):
        return utils.find(lambda c: msg.lower() in c.name.lower(), ctx.guild.text_channels)
    else:
        return utils.find(lambda c: msg.lower() in c.name.lower(), ctx.bot.get_all_channels)
    return None
