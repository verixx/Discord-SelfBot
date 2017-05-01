import itertools
import logging

from discord.ext import commands
from .utils.helper import edit
from .utils.save import delete_key, read_json, save_commands

log = logging.getLogger('LOG')


class CustomCommands:

    def __init__(self, bot):
        self.bot = bot

    # List all custom commands without links
    @commands.group(aliases=["Cmds"])
    async def cmds(self, ctx):
        """Show all custom commands."""
        if ctx.invoked_subcommand is None:
            ttl = None if ctx.message.content.endswith(' stay') else 20
            p = commands.Paginator(prefix='```css')
            cmds = read_json("commands")
            p.add_line('[List of Custom Commands]')
            msg = []
            for cmd in sorted(cmds):
                msg.append(cmd)
                if cmd == list(sorted(cmds))[-1] or len(msg) % 5 == 0 and len(msg) != 0:
                    p.add_line(', '.join(x for x in msg))
                    msg = []
            for page in p.pages:
                await ctx.send(page, delete_after=ttl)
            await ctx.message.delete()

    # List all custom commands with Links
    @cmds.command(aliases=["Long"])
    async def long(self, ctx):
        """Display also their content"""
        ttl = None if ctx.message.content.endswith(' stay') else 20
        p = commands.Paginator(prefix='```css')
        cmds = read_json("commands")
        p.add_line('[List of Custom Commands]')
        width = len(max(cmds, key=len))
        for cmd in sorted(cmds):
            p.add_line('{0:<{width}}| {1}'.format(cmd, cmds.get(cmd), width=width))
        for page in p.pages:
            await ctx.send(page, delete_after=ttl)
        await ctx.message.delete()

    @commands.group(aliases=["Cmd"])
    async def cmd(self, ctx, key: str):
        """Display content of a command."""
        cmds = read_json("commands")
        if key in cmds:
            await edit(ctx, content="``{}`` content:\n{}".format(key, cmds.get(key)), ttl=20)
        else:
            await edit(ctx, content=f"\N{HEAVY EXCLAMATION MARK SYMBOL} Couldn't find ``{key}`` in Custom Commands", ttl=5)

    # Add a custom command
    @commands.command(aliases=["Add"])
    async def add(self, ctx, *, msg: str):
        """Add a Custom Command."""
        words = msg.strip('"').split(' ', 1)
        cmds = read_json("commands")
        if len(words) == 2:
            if words[0].lower() not in cmds:
                builtin = list(itertools.chain.from_iterable([x.aliases for x in self.bot.commands])) + [x.name for x in self.bot.commands]
                if words[0] not in builtin:
                    save = await save_commands(words[0].lower(), words[1])
                    if save is True:
                        await edit(ctx, content="\N{HEAVY CHECK MARK} Successfully added ``{}`` to ``{}``".format(words[1], words[0].lower()), ttl=5)
                    else:
                        await edit(ctx, content=f"\N{HEAVY EXCLAMATION MARK SYMBOL} Something went wrong.Exception: ``{save}``", ttl=20)
                else:
                    await edit(ctx, content=f"\N{HEAVY EXCLAMATION MARK SYMBOL} ``{words[0]}`` is already a command and can't be used because of that.", ttl=5)
            else:
                await edit(ctx, content=f"\N{HEAVY EXCLAMATION MARK SYMBOL} Key ``{words[0]}`` already in use.", ttl=5)
        else:
            await edit(ctx, content="\N{HEAVY EXCLAMATION MARK SYMBOL} You need a Key and a Value eg. ``add testkey testvalue``", ttl=5)

    # Remove a custom command
    @commands.command(aliases=["Remove"])
    async def remove(self, ctx, key: str):
        """Remove a Custom Command."""
        key = key.strip('"')
        cmds = read_json("commands")
        builtin = list(itertools.chain.from_iterable([x.aliases for x in self.bot.commands])) + [x.name for x in self.bot.commands]
        if key in builtin:
            await edit(ctx, content=f"\N{HEAVY EXCLAMATION MARK SYMBOL} You can't remove the builtin command ``{key}``", ttl=5)
        else:
            if key.lower() in cmds:
                value = cmds[key.lower()]
                delete = await delete_key("commands", key.lower())
                if delete is True:
                    await edit(ctx, content=f"\N{HEAVY CHECK MARK} Successfully removed ``{key}`` with value ``{value}``", ttl=5)
                else:
                    await edit(ctx, content=f"\N{HEAVY EXCLAMATION MARK SYMBOL} Something went wrong.Exception: ``{delete}``", ttl=20)
            else:
                await edit(ctx, content=f"\N{HEAVY EXCLAMATION MARK SYMBOL} Couldn't find ``{key}`` in Custom Commands", ttl=5)


def setup(bot):
    bot.add_cog(CustomCommands(bot))
