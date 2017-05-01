[<img src="https://img.shields.io/badge/discord.py-rewrite-blue.svg?style=flat-square">](https://github.com/Rapptz/discord.py/tree/rewrite)
[<img src="https://img.shields.io/badge/python-3.6-brightgreen.svg?style=flat-square">](https://www.python.org/downloads/release/python-360/)
[<img src="https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square">](https://github.com/IgneelDxD/Discord-SelfBot/blob/master/LICENSE)
[<img src="https://canary.discordapp.com/api/guilds/266907735432495104/widget.png?style=shield">](https://discord.gg/DJK8h3n)
[![Twitter URL](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=I%20just%20found%20@IgneelDxD%27s%20awesome%20Discord%20SelfBot,%20check%20it%20out!%20https://igneeldxd.github.io/Discord-SelfBot/&source=webclient)


For any kind of suggestions, feedback, support or just to hang out, I'll gladly welcome you on my [Server](https://discord.gg/DJK8h3n).

If you encounter problems while setting up the SelfBot, come by and I am sure we'll find a solution.

[<img src="https://canary.discordapp.com/api/guilds/266907735432495104/widget.png?style=banner2">](https://discord.gg/DJK8h3n)

# IgneelDxD's Discord SelfBot
#### This Project uses the rewrite version of [discord.py](https://github.com/Rapptz/discord.py/tree/rewrite) as well as [Python 3.6](https://www.python.org/downloads/release/python-360/) or higher. Please keep this in mind when using the bot.

This SelfBot has a lot of useful features like a bunch of Moderation commands as well as fun commands or a Mention logger.

Disclaimer: Use this on your own risk. If you get banned somewhere because of using it I won't take responsibility.

> ### Table of Contents
> 1. [Features](#features)
> 2. [Setup](#setup)
> 3. [Running the Bot](#running-the-bot)
> 4. [Hosting](#hosting-on-a-linux-vps)
> 5. [Commands](#commands)
> 6. [Custom Commands](#custom-commands)
> 7. [Mention Logger](#mention-logger)
> 8. [Adding Your Own Stuff](#adding-your-own-stuff)
> 9. [Google API](#google-api)
> 10. [Acknowledgements](#acknowledgements)

## Features
- Moderation (Works only if you have the permissions to use it on a Server)
  - Add/Remove a role of a Server-Member.
  - Change Role-Colors without leaving the Chat.
  - Lock/Unlock a Channel in spammy situations to clean up a mess.
  - Kick/Ban Members if they misbehave.
  - Softban a Member if a kick would be necessary but you want to clean up the last messages they sent in one.
  - Mute/Unmute Members if they need a cool of phase.
  - Prune a Member's Messages of a certain type or your own if necessary.
  - Show Permissions of a Member.
- Mention Logging
  - Set a Channel on your own Server to log all your mentions and Keywords too.
  - Add Keywords to your logger to trigger it in whole Servers or specific Channels.
  - Don't like a user/channel? Simply add them to your blacklist and you'll never log them again.
- Information:
  - Love this SelfBot as much as I do? Use "About" to share it with others.
  - Display interesting information about Users, Servers, Roles, Channels or Emotes.
- Google
  - Search for information or images directly in the Chat.
- MyAnimeList
  - Display information about your favorite Anime/Manga within a nice looking embed.
- Custom Commands
  - Add quickly links per commands to a json and then use them like normal commands of the bot.
  - Show off those reaction gifs.
- Tools
  - Return the Ping or Uptime of your SelfBot.
  - Set a game so you will even have a status when you are on mobile.
  - Show several interesting Stats about your usage of the bot.
  - Quote Messages when you are replying to something.
  - Color command.
  - Display your favorite Emote larger than normal.
- Misc
  - 8ball / choose / learn to google command.
  - embed text or an image link.
  - Urban Dictionary
  - Giphy search
  - add reaction text with a command.
  - convert a message to Alphanumeric Emotes.
- Debug
  - Use Python within a channel.

## Setup
Clone this repo or download it as Zip and move/unpack it to the location where you wanna have it.

Go into the config folder and rename all three files by simply removing the ``.example`` ending and saving again.

Now after this is done, open the config file and start adding your information. Notepad should be enough to edit the file.

```json
{
  "token":"",
  "prefix":["/"],
  "gamestatus":"",
  "custom_search_engine":"",
  "google_api_key":"",
  "mal_username":"",
  "mal_password":"",
  "webhook_token":"",
  "log_channel": ,
  "setlog":"off",
  "embed_color":""
}
```

- ``token`` - On Discord hit ``Ctrl + Shift + I`` to open the Development Console. Then move to the tab ``Application`` and open the ``Local Storage`` on the left bar. Once that's done, get your token [here](https://i.imgur.com/dfb7nTt.png) and paste it into your config. Do not give this to *anyone* as they will be able to gain access to your account with it.
- ``prefix`` - This can be anything you like. You even can set multiple prefixes by doing something like ``["/", "self."]``. I'd suggest you to take a prefix which won't easily trigger common bots as it might get spammy.
- ``gamestatus`` - You can set this to whatever you want your game as. There is a command to change it while the bot is running so if you don't know what to choose you can skip this step.
- ``custom_search_engine`` and ``google_api_key`` - For this take a look at the [Google API](#google-api) section below.
- ``mal_username`` and ``mal_password`` - MyAnimeList username and password to use the Anime and Manga command. This will simply log into your account to obtain information about Anime or Manga. Your normal account is totally okay for it. If you don't own one till now, simply create a throwaway account.
- ``webhook_token``
  - Go to your private Server, create a logging channel and set it so only you see it.
  - Change the Notification settings to "All" Messages in that Channel
  - Open the Channel settings of the Server where you want to log your keywords and mentions.
  - Click on **Webhooks**, create a **New Webhook** (Give it a nice name an Avatar if you want eg: "Mention Bot", [Avi](https://i.imgur.com/BN4iLQt.png)) It should look like [this](https://i.imgur.com/cLABbvR.png).
  - Copy the **Webhook URL** at the bottom, add it to ``webhook_token`` and don't forget to **save**.
- ``log_channel``
  - For this you need to activate Developer Mode.
  - Go into **settings**, select **Appearance** and toggle **Developer Mode**
  - Then go to your log channel and right-click on the name in your channel selector.
  - Click the last point to copy the id and paste it to ``log_channel``. It should look like ``"log_channel": 123456789123456789,``. Do **not** use quotes here as we need it as number, not as Text.
- ``embed_color`` - This can be a lot of things. Even empty! If you leave it empty, every command that uses this will get a random color per call. You can insert several different values thought. A web color like ``purple`` or RGB values in the format of ``(155, 89, 182)`` or ``155, 89, 182`` or HEX values like ``9b59b6`` or ``#9b59b6`` or ``0x9b59b6``.


## Running the Bot
> Mind that this description is written for ``Windows``, it shouldn't differ too much on other Systems though.

> You can skip any step if your System already fulfills the step.

### Installing Python
As mentioned above we need to install Python 3.6 or higher, anything below won't work with this SelfBot.
1. Go and download anything above 3.6.0 [here](https://www.python.org/downloads/).
2. Once selected the Version you like/need, click onto ``Download`` and scroll down to ``Files``.
3. Select your System. You can find that in ``System Information`` or similar.
4. Then run the installer and pay attention to select ``Add Python ** to PATH`` like [here](https://i.imgur.com/sNW1jvG.png) and finish with ``Install Now``.
5. After finishing the install open your Command-Line (Windows + R, cmd.exe, enter) or PowerShell and type ``python -V``.
6. If you see the Version you just installed before you are set to go ([image](https://i.imgur.com/tDvZkKh.png)).

### Installing Git
1. Download the latest [Git](https://git-scm.com/downloads) Version for your System.
2. Once downloaded start the installation.
3. On [this](https://i.imgur.com/GBtdTav.png) step pay attention to select ``Windows Command Prompt``.
4. Go through the installation and adjust it to your likings. The default settings should be enough though.

### Starting the Bot Automatically
1. Go to the folder you unpacked in [Setup](#setup).
2. Click on the ``run.bat``
3. Logging in may take up to a minute or more, depending on your connection speed.
4. Have fun using the bot. Check [Commands](#commands), [Custom Commands](#custom-commands) and [Mention Logger](#mention-logger) to see what you can do.

### Starting the Bot Manually
1. Go to the folder you unpacked in [Setup](#setup).
2. Hold ``shift`` and right-click onto anything within the folder aside of the files
3. On [this](https://i.imgur.com/OPCZVDg.png) menu then select ``Open Command Prompt / PowerShell window here``
4. Type ``pip install -r .\requirements.txt`` into the console and let it install all dependencies we need.
5. Then type ``python loop.py`` and wait for it to login.
6. This may take up to a minute or more, depending on your connection speed.
7. Have fun using the bot. Check [Commands](#commands), [Custom Commands](#custom-commands) and [Mention Logger](#mention-logger) to see what you can do.

## Hosting on Linux
### Installing Python

## Commands

## Custom Commands

## Quick Commands
In the config folder you'll find the file ``quickcmds``. You can add there any quick command you want. This will react only if the exact key is said.

Like if I say ``flip`` in chat the SelfBot will edit the message to ``(╯°□°）╯︵ ┻━┻``.

![img](http://i.imgur.com/SCURead.gif)

Here you see the base commands I added, you can add anything you want here of course. (command to do it while the bot is running #SoonTM)

```json
{
  "shrug": "¯\\_(ツ)_/¯",
  "flip": "(╯°□°）╯︵ ┻━┻",
  "unflip": "┬─┬﻿ノ( ゜-゜ノ)",
  "lenny": "( ͡° ͜ʖ ͡°)",
  "fite": "(ง’̀-‘́)ง"
}
```

Keep in mind that if you have a ``\`` in your text you need to do 2 of them. like you can see with *shrug*.

## Mention Logger

## Adding Your Own Stuff

## Google API

In order to use the ``/i`` command to image search, you will need a Google API key and a Custom Search Engine ID.

Follow these steps to obtain them:

1. Visit the [Google API Console](https://console.developers.google.com/). Once you are in the Console, create a new project.
2. Go to ``Library`` and search ``Custom Search API``. Click it and enable it.
3. Go to ``Credentials`` and click ``create credentials`` and choose ``API Key`` (no need to restrict the key). The value under "Key" is your api key. Paste this into the config.json under ``google_api_key``.
4. Go [here](https://cse.google.com/cse/all) and click ``Add`` and then ``Create`` (if asked to specify a site, just do www.google.com)
5. On the home page of the Custom Search webpage, click on the newly created search engine and change the ``Sites to Search`` option to ``Search the entire web but emphasize included sites``.
6. Make sure the ``Image search`` option is enabled and make sure to click the ``Update`` button at the bottom when you are done with the changes!
6. Go to ``Details`` section and click ``Search Engine ID`` to grab the ID. Copy this and add it for ``custom_search_engine`` in the config.json.

**Note:** Google may take a little while to properly register your key so the search feature may not work right away. If it's still not working after a few hours, then you may have messed up somewhere.

## Acknowledgements
Thanks to
- [Appu](https://github.com/appu1232) for even getting me into doing this. As well as several ideas, suggestions and the Google API part.
- [Danny](https://github.com/Rapptz) for especially larger parts of the google and debug commands and now and there so minor improvements.
