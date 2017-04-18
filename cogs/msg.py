import discord
import logging
import re

from .utils.allmsgs import quickcmds, custom
from .utils.checks import permEmbed, me
from datetime import datetime
from discord_webhooks import Webhook

log = logging.getLogger('LOG')


class OnMessage:
    def __init__(self, bot):
        self.bot = bot
        self.webhook_class = Webhook(self.bot)
        self.request_webhook = self.webhook_class.request_webhook

    async def on_message(self, message):
        if self.bot.is_ready():
            # Increase Message Count
            if hasattr(self.bot, 'message_count'):
                self.bot.message_count += 1
            # Custom commands
            if me(self, message):
                if hasattr(self.bot, 'icount'):
                    self.bot.icount += 1
                prefix = ''
                for i in self.bot.prefix:
                    if message.content.startswith(i):
                        prefix = i
                        break
                if prefix is not '':
                    response = custom(prefix, message.content)
                    if response is None:
                        pass
                    else:
                        self.bot.commands_triggered[response[3]] += 1
                        destination = 'DM with {0.channel.recipient}'.format(message) if isinstance(message.channel, discord.DMChannel) else '#{0.channel.name},({0.guild.name})'.format(message)
                        log.info('In {1}:{0.content}'.format(message, destination))
                        if response[0] == 'embed':
                            if permEmbed(message):
                                await message.edit(content=response[2], embed=discord.Embed(colour=discord.Color.purple()).set_image(url=response[1]))
                            else:
                                await message.edit(content='{0}\n{1}'.format(response[2], response[1]))
                        else:
                            await message.edit(content='{0}\n{1}'.format(response[2], response[1]))
                else:
                    response = quickcmds(message.content.lower().strip())
                    if response:
                        self.bot.commands_triggered[response[1]] += 1
                        destination = 'DM with {0.channel.recipient}'.format(message) if isinstance(message.channel, discord.DMChannel) else '#{0.channel.name},({0.guild.name})'.format(message)
                        log.info('In {1}:{0.content}'.format(message, destination))
                        await message.edit(content=response[0])
            elif (message.guild is not None) and (self.bot.setlog == 'on'):
                if message.author.id in self.bot.log_block_user:
                    return
                if message.channel.id in self.bot.log_block_channel:
                    return
                if message.author.is_blocked():
                    return
                if message.guild.id in self.bot.log_guild or message.channel.id in self.bot.log_channel:
                    msg = re.sub('[,.!?-_"^()/]', ' ', message.content.lower())
                    if any(map(lambda v: v in msg.split(), self.bot.log_block_key)):
                        return
                    notify = False
                    if (message.guild.get_member(self.bot.user.id).mentioned_in(message)):
                        notify = mention = True
                        if message.role_mentions != [] or message.mention_everyone:
                            em = discord.Embed(title='\N{SPEAKER WITH THREE SOUND WAVES} ROLE MENTION', colour=discord.Color.dark_blue())
                            log.info("Role Mention from #%s, %s" % (message.channel, message.guild))
                        else:
                            em = discord.Embed(title='\N{BELL} MENTION', colour=discord.Color.dark_gold())
                            log.info("Mention from #%s, %s" % (message.channel, message.guild))
                        if hasattr(self.bot, 'mention_count'):
                            self.bot.mention_count += 1
                    else:
                        for word in self.bot.log_key:
                            if word in msg.split():
                                notify = True
                                mention = False
                                em = discord.Embed(title='\N{HEAVY EXCLAMATION MARK SYMBOL} %s MENTION' % word.upper(), colour=discord.Color.dark_red())
                                log.info("%s Mention in #%s, %s" % (word.title(), message.channel, message.guild))
                                if hasattr(self.bot, 'mention_count_name'):
                                    self.bot.mention_count_name += 1
                                break
                    if notify:
                        content = message.clean_content if len(message.clean_content) < 1020 else message.clean_content[:1020] + '...'
                        em.set_author(name=message.author, icon_url=message.author.avatar_url)
                        em.add_field(name='In',
                                     value="#%s, ``%s``" % (message.channel, message.guild), inline=False)
                        em.add_field(name='At',
                                     value=datetime.now().__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
                        em.add_field(name='Message',
                                     value=content, inline=False)
                        em.set_thumbnail(url=message.author.avatar_url)
                        token = self.bot.webhook_token[42:]
                        if token and not mention:
                            try:
                                await self.request_webhook(token, embeds=[em.to_dict()])
                            except:
                                await self.bot.get_channel(self.bot.log_channel).send(embed=em)
                        else:
                            await self.bot.get_channel(self.bot.log_channel).send(embed=em)

    async def on_message_edit(self, before, after):
        if me(self, before):
            if before.content != after.content:
                del before
                await self.on_message(after)
                await self.bot.process_commands(after)


def setup(bot):
    bot.add_cog(OnMessage(bot))
