import asyncio
import logging

log = logging.getLogger('LOG')


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


# Check for perms of links and attached files
def permFile(message):
    return message.channel.permissions_for(message.author).attach_files


# Check for perms of links and attached files
def permEmbed(message):
    return message.channel.permissions_for(message.author).embed_links
