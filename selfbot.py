import asyncio
import datetime
import discord
import logging
import os
import traceback

from cogs.utils.helper import edit
from cogs.utils.save import read_config, read_log
from collections import Counter
from discord.ext import commands

# Logging
log = logging.getLogger('LOG')
log.setLevel(logging.INFO)

fileFormatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
consoleFormatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%H:%M:%S')

selfFile = logging.FileHandler(filename='Logs/SelfBot/SelfBot' + datetime.datetime.now().strftime("%Y-%m-%d") + '.log', encoding='utf-8', mode='a')
selfFile.setFormatter(fileFormatter)
log.addHandler(selfFile)

selfConsole = logging.StreamHandler()
selfConsole.setFormatter(consoleFormatter)
log.addHandler(selfConsole)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

discordFile = logging.FileHandler(filename='Logs/Discord/Discord' + datetime.datetime.now().strftime("%Y-%m-%d") + '.log', encoding='utf-8', mode='a')
discordFile.setFormatter(fileFormatter)
logger.addHandler(discordFile)

discordConsole = logging.StreamHandler()
discordConsole.setLevel(logging.ERROR)
discordConsole.setFormatter(consoleFormatter)
logger.addHandler(discordConsole)

bot = commands.Bot(command_prefix=read_config('prefix'), description='''IgneelDxD's Selfbot''', self_bot=True)


# Startup
@bot.event
async def on_ready():
    log.info('------')
    log.info('Logged in as')
    log.info(str(bot.user) + '(' + str(bot.user.id) + ')')
    log.info('------')
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()
    if not hasattr(bot, 'message_count'):
        bot.message_count = 0
    if not hasattr(bot, 'commands_triggered'):
        bot.commands_triggered = Counter()
    if not hasattr(bot, 'socket_stats'):
        bot.socket_stats = Counter()
    if not hasattr(bot, 'icount'):
        bot.icount = 0
    if not hasattr(bot, 'mention_count'):
        bot.mention_count = 0
    if not hasattr(bot, 'mention_count_name'):
        bot.mention_count_name = 0

    bot.gamename = read_config('gamestatus')
    bot.mal_un = read_config('mal_username')
    bot.mal_pw = read_config('mal_password')
    bot.mention_channel = read_config('log_channel')
    bot.webhook_token = read_config('webhook_token')
    bot.google_api_key = read_config('google_api_key')
    bot.custom_search_engine = read_config('custom_search_engine')
    bot.prefix = read_config('prefix')

    bot.setlog = read_config('setlog')
    bot.log_guild = read_log('guild')
    bot.log_block_user = read_log('block-user')
    bot.log_block_channel = read_log('block-channel')
    bot.log_key = read_log('key')
    bot.log_block_key = read_log('block-key')
    bot.log_channel = read_log('channel')

    if os.path.isfile('restart.txt'):
        with open('restart.txt', 'r') as re:
            await bot.get_channel(int(re.readline())).send(':wave: Back Running!', delete_after=2)
        os.remove('restart.txt')


# Command Errors
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await edit(ctx, content='\N{HEAVY EXCLAMATION MARK SYMBOL} Only usable on Servers', ttl=5)
    elif isinstance(error, commands.CheckFailure):
        await edit(ctx, content='\N{HEAVY EXCLAMATION MARK SYMBOL} No Permissions to use this command', ttl=5)
    elif isinstance(error, commands.CommandInvokeError):
        log.error('In {0.command.qualified_name}:\n{1}'.format(ctx, ''.join(traceback.format_list(traceback.extract_tb(error.original.__traceback__)))))
        log.error('{0.__class__.__name__}: {0}'.format(error.original))


# Increase use count and log to logger
@bot.event
async def on_command(ctx):
    bot.commands_triggered[ctx.command.qualified_name] += 1
    message = ctx.message
    if isinstance(message.channel, discord.DMChannel):
        destination = 'DM with {0.channel.recipient}'.format(message)
    else:
        destination = '#{0.channel.name},({0.guild.name})'.format(message)
    log.info('In {1}:{0.content}'.format(message, destination))


@bot.event
async def on_socket_response(msg):
    if bot.is_ready():
        bot.socket_stats[msg.get('t')] += 1


# Gamestatus
async def status(bot):
    gamename = ''
    while not bot.is_closed():
        if bot.is_ready():
            if bot.gamename:
                if bot.gamename != gamename:
                    log.info('Game changed to playing {}'.format(bot.gamename))
                    gamename = bot.gamename
                game = discord.Game(name=bot.gamename)
            else:
                if bot.gamename != gamename:
                    log.info('Removed Game Status')
                    gamename = bot.gamename
                game = None
            await bot.change_presence(game=game, status=discord.Status.invisible, afk=True)
        await asyncio.sleep(20)

# Load Extensions / Logger / Runbot
if __name__ == '__main__':
    try:
        bot.load_extension("cogs.cogs")
    except Exception as e:
        log.error('Failed to load extension cogs.cogs\n{}: {}'.format(type(e).__name__, e))
        log.error("Bot automatically shut down. Cogs extension is needed!")
        with open('quit.txt', 'w') as re:
            re.write('quit')
        os._exit(0)
    for extension in os.listdir("cogs"):
        if extension.endswith('.py') and not extension == "cogs.py":
            try:
                bot.load_extension("cogs." + extension.rstrip(".py"))
            except Exception as e:
                log.warning('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))
    bot.loop.create_task(status(bot))
    bot.run(read_config('token'), bot=False)
