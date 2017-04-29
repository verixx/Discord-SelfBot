import discord
import inspect
import io
import textwrap
import traceback

from contextlib import redirect_stdout
from discord.ext import commands
from PythonGists import PythonGists
from .utils.gets import getAgo, getChannel, getColor, getGuild, getRole, getTimeDiff, getUser, getWithoutInvoke
from .utils.helper import edit, permEmbed
from .utils.save import read_config, read_log, save_config, save_log

###############
# Imports for Eval/Debug, I hate errors.
##############
import asyncio
import datetime
import gc
import json
import psutil
import random
import re
import time
import urllib

from bs4 import BeautifulSoup


class Debug:

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        # I don't allow those errors to trigger me lol
        self.env = {
                    "asyncio": asyncio,
                    "datetime": datetime,
                    "gc": gc,
                    "json": json,
                    "psutil": psutil,
                    "random": random,
                    "re": re,
                    "time": time,
                    "urllib": urllib,
                    "BeautifulSoup": BeautifulSoup,
                    "discord": discord,
                    "edit": edit,
                    "getAgo": getAgo,
                    "getChannel": getChannel,
                    "getColor": getColor,
                    "getGuild": getGuild,
                    "getRole": getRole,
                    "getTimeDiff": getTimeDiff,
                    "getUser": getUser,
                    "getWithoutInvoke": getWithoutInvoke,
                    "permEmbed": permEmbed,
                    "read_config": read_config,
                    "read_log": read_log,
                    "save_config": save_config,
                    "save_log": save_log
                   }

    # DEBUG
    @commands.command(aliases=["Debug", "d", "D"])
    async def debug(self, ctx, *, code: str):
        """Single line Python debug.."""
        code = code.strip('` ')
        python = '```ocaml\n>>> Input: {}\n{}\n```'
        result = None
        env = {
            'bot': self.bot,
            'say': ctx.send,
            'ctx': ctx,
            'message': ctx.message,
            'guild': ctx.guild,
            'server': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.message.author,
            'me': ctx.message.author,
            'self': self
        }

        env.update(self.env)
        env.update(globals())
        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await edit(ctx, content=python.format(code, '>>> %s' % type(e).__name__ + ': ' + str(e)))
            return
        if len(str(code) + '>>> Output:' + str(result)) > 2000:
            link = PythonGists.Gist(description='SelfBot Python Debug', content=str(result), name='debug.py')
            await edit(ctx, content=python.format(code, '>>> Output: See link below..') + '\n<{}>'.format(link))
        else:
            await edit(ctx, content=python.format(code, '>>> Output: %s' % result))

    def cleanup_code(self, content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

    # Eval Command
    @commands.command(name='eval', aliases=["Eval", "e", "E"])
    async def _eval(self, ctx, *, body: str):
        """Multiline Python Eval."""
        env = {
            'bot': self.bot,
            'say': ctx.send,
            'ctx': ctx,
            'message': ctx.message,
            'guild': ctx.guild,
            'server': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.message.author,
            'me': ctx.message.author,
            'self': self,
            '_': self._last_result
        }

        env.update(self.env)
        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = 'async def func():\n%s' % textwrap.indent(body, '  ')

        try:
            exec(to_compile, env)
        except SyntaxError as e:
            return await ctx.send(self.get_syntax_error(e))

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send('```py\n{}{}\n```'.format(value, traceback.format_exc()))
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    if len(value) > 1985:
                        link = PythonGists.Gist(description='SelfBot Python Eval', content=str(value), name='eval.py')
                        await ctx.send(content='\N{ROBOT FACE} I uploaded that for you!\n<{}>'.format(link))
                    else:
                        await ctx.send('```py\n%s\n```' % value)
            else:
                self._last_result = ret
                if len(str(value) + str(ret)) > 1985:
                    link = PythonGists.Gist(description='SelfBot Python Eval', content=str(value) + '\n' + str(ret), name='eval.py')
                    await ctx.send(content='\N{ROBOT FACE} I uploaded that for you!\n<{}>'.format(link))
                else:
                    await ctx.send('```py\n%s%s\n```' % (value, ret))


def setup(bot):
    bot.add_cog(Debug(bot))
