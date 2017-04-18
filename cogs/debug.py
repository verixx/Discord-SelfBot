import discord
import inspect
import io
import textwrap
import traceback

from .utils.checks import getUser, edit
from contextlib import redirect_stdout
from discord.ext import commands
from PythonGists import PythonGists


class Debug:

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    # DEBUG
    @commands.command(aliases=["Debug", "d", "D"])
    async def debug(self, ctx, *, code: str):
        code = code.strip('` ')
        python = '```ocaml\n>>> Input: {}\n{}\n```'
        result = None
        env = {
            'bot': self.bot,
            'say': ctx.send,
            'edit': ctx.message.edit,
            'ctx': ctx,
            'message': ctx.message,
            'guild': ctx.message.guild,
            'server': ctx.message.guild,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'me': ctx.message.author,
            'self': self,
            'user': getUser,
            'discord': discord
            }
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
            await edit(ctx, content=python.format(code, '>>> Output: See link below..')+'\n<{}>'.format(link))
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
        env = {
            'bot': self.bot,
            'say': ctx.send,
            'edit': ctx.message.edit,
            'ctx': ctx,
            'message': ctx.message,
            'guild': ctx.message.guild,
            'server': ctx.message.guild,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'me': ctx.message.author,
            'self': self,
            'user': getUser,
            '_': self._last_result
        }

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
                if len(str(value)+str(ret)) > 1985:
                    link = PythonGists.Gist(description='SelfBot Python Eval', content=str(value)+'\n'+str(ret), name='eval.py')
                    await ctx.send(content='\N{ROBOT FACE} I uploaded that for you!\n<{}>'.format(link))
                else:
                    await ctx.send('```py\n%s%s\n```' % (value, ret))


def setup(bot):
    bot.add_cog(Debug(bot))
