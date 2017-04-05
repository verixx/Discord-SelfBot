import asyncio
import logging
import os
import sys

from discord.ext import commands
from .utils import config
from .utils.checks import edit

log = logging.getLogger('LOG')


class Cogs:

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('config.json')

    # Loads a module
    @commands.command(aliases=["Load"])
    async def load(self, ctx, *, module: str):
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await edit(ctx, content='Not Loading\n``{}: {}``'.format(type(e).__name__, e), ttl=5)
            log.error('Loading {} faild!\n{}: {}'.format(module, type(e).__name__, e))
        else:
            await edit(ctx, content='Loaded %s' % module, ttl=5)
            log.info('Loaded %s' % module)

    # Unloads a module
    @commands.command(aliases=["Unload"])
    async def unload(self, ctx, *, module: str):
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await edit(ctx, content='Not unloading\n``{}: {}``'.format(type(e).__name__, e), ttl=5)
            log.error('Unloading {} faild!\n{}: {}'.format(module, type(e).__name__, e))
        else:
            await edit(ctx, content='Unloaded %s' % module, ttl=5)
            log.info('Unloaded %s' % module)

    # Reloads a module.
    @commands.command(aliases=["Reload"])
    async def reload(self, ctx, module: str = None):
        if not module:
            utils = []
            for i in self.bot.extensions:
                utils.append(i)
            fail = ''
            for i in utils:
                self.bot.unload_extension(i)
                try:
                    self.bot.load_extension(i)
                except Exception as e:
                    fail += 'Failed to reload extension ``{}``\n``{}: {}``'.format(i, type(e).__name__, e)
                    log.error('Reloading {} failed!\n{}: {}'.format(i, type(e).__name__, e))
            if fail != '':
                await edit(ctx, content='{}\nReloaded remaining extensions.'.format(fail), ttl=20)
            else:
                await edit(ctx, content='Reloaded all extensions.', ttl=5)
                log.info('Reloaded all extensions.')
        else:
            try:
                self.bot.unload_extension(module)
                self.bot.load_extension(module)
            except Exception as e:
                await edit(ctx, content='Not reloading\n``{}: {}``'.format(type(e).__name__, e), ttl=20)
                log.error('Reloading {} failed!\n{}: {}'.format(module, type(e).__name__, e))
            else:
                await edit(ctx, content='Reloaded %s' % module, ttl=5)
                log.info('Reloaded %s' % module)

    # Shutdown Bot
    @commands.command(aliases=["Quit"])
    async def quit(self, ctx):
        await edit(ctx, content='Bot has been killed.', ttl=2)
        log.warning('Bot has been killed.')
        with open('quit.txt', 'w') as re:
            re.write('quit')
        exit()

    # Restart selfbot
    @commands.command(aliases=["Restart"])
    async def restart(self, ctx):
        await self.config.put('restart', 'true')
        await self.config.put('restart_channel', ctx.message.channel.id)
        log.info('Restarting....')
        await ctx.message.edit(content='Good Bye :wave:')
        await asyncio.sleep(.5)
        await ctx.message.delete()
        python = sys.executable
        os.execl(python, python, *sys.argv)


def setup(bot):
    bot.add_cog(Cogs(bot))
