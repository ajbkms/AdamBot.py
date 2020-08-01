# Standard libraries
import os
import logging
import time
import asyncio
import random
import platform
from discord.ext import tasks

# Third party libraries
import discord
import datetime
from pathlib import Path
from discord.ext import commands
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown) 
from discord.errors import HTTPException, Forbidden

bot = commands.Bot(command_prefix = "~")
bot.remove_command('help')

IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

filtered_words = ["Nigger", 
                "nigger",
                "nigg3r",
                "nIgger",
                "niGger",
                "NIGGER",
                "cunt",
                "CUNT",
                "CuNt",
                "NiGgEr",
                "Kill YourSelf",
                "kill your self",
                "KYS",
                "Kys",
                "kys",
                "Kill Your Self",
                "KILL YOURSELF",
                "KILL YOUR SELF",
                "kill your s3lf",
                "i hope your mother dies",
                "i hope your father dies",
                "i hope you killyourself",
                "hang yourself",
                "Hang yourself",
                "Hang Yourself",
                "Hang Your Self",
                "HaNg YoUrSeLf",
                "jsbjsbfiusgfduisgfbdsudsi cfsufvi ds",
                "Cunt",
                "Cunt",
                "Cunt",]

@tasks.loop(seconds=172800)
async def online():
    # Message that Shows when bot comes online #
    channel = bot.get_channel(716087338379247626)
    embed = discord.Embed(
        description="All Systems Online", color=discord.Color.green())

    embed.set_author(name="Online", icon_url=bot.user.avatar_url)
    embed.set_footer(text=f"{round(bot.latency * 10000)}ms | {bot.user.name}")

    await channel.send(embed=embed)

@tasks.loop(seconds=15)
async def change_status():
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Streaming(name = "~help", url = "https://twitch.tv/ajbkmss"))
    await asyncio.sleep(15)
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Streaming(name = "discord.gg/QaNBSzG", url = "https://twitch.tv/ajbkmss"))
    await asyncio.sleep(15)

#---------------------------------------------------------------------------------------------------------------------

@bot.event
async def on_ready():
    #online.start()
    change_status.start()
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: ~\n-----")
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Streaming(name = "~help", url = "https://twitch.tv/ajbkmss"))

#@bot.event
#async def on_message(message):
#    for word in filtered_words:
#        if word in message.content:
##            await message.delete()
 #           Log = discord.utils.get(message.guild.text_channels, name='warn-log')
#
#            embed = discord.Embed(description=f"**Reason:** Bad Word Usage", color=discord.Color.red(), timestamp=message.created_at)
#
 #           embed.set_author(name=f"{message.author} Auto Warned", icon_url=message.author.avatar_url)
  #          embed.set_footer(text="Case: Coming Soon")
   #         
    #        await message.channel.send(embed=embed)
     #       await Log.send(embed=embed)
      #      await bot.process_commands(message)
       #     pass

@bot.event
async def on_message_delete(message=None):
    guild = discord.utils.get(bot.guilds, name=f'{message.guild.name}')
    if guild is not None:
        channel = discord.utils.get(guild.text_channels, name='mod-log')

    embed = discord.Embed(description=f"**User:** <@{message.author.id}> `{message.author}`\n**Channel:** <#{message.channel.id}> `#{message.channel}`\n **Message:** {message.content}", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
    embed.set_author(name="Message Deleted", icon_url="https://cdn.discordapp.com/emojis/314068430787706880.png?v=1")

    await channel.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None, amount=0):
    await ctx.guild.kick(user=member, reason=reason)
    guild = discord.utils.get(bot.guilds, name=f'{ctx.guild.name}')
    if guild is not None:
        channel = discord.utils.get(guild.text_channels, name='mod-log')

    embed = discord.Embed(
        title=f"**Member Kicked**", description=f"**User:** <@{member.id}>\n**Reason:** {reason}", color=discord.Color.red(), timestamp=ctx.message.created_at)

    embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    
#    await ctx.channel.purge(limit=amount + 1)
    await channel.send(embed=embed)
@kick.error
async def kick_error(ctx, error):
    await ctx.send("There was an Error with this command. Make sure I have what I need to use this command.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None, amount=0):
    await ctx.guild.ban(user=member, reason=reason)
    guild = discord.utils.get(bot.guilds, name=f'{ctx.guild.name}')
    if guild is not None:
        channel = discord.utils.get(guild.text_channels, name='mod-log')

    embed = discord.Embed(
        title=f"**Member Banned**", description=f"**User:** <@{member.id}>\n**Reason:** {reason}", color=discord.Color.red(), timestamp=ctx.message.created_at)

    embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)

    await channel.send(embed=embed)
@ban.error
async def ban_error(ctx, error):
    await ctx.send("There was an Error with this command. Make sure I have what I need to use this command.")

@bot.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member=None, *, reason=None, amount=0):
    if not member:
        await ctx.send("~mute @user reason")
        return
    muterole = discord.utils.get(ctx.guild.roles, name="Muted")
    #roletwo = discord.utils.get(ctx.guild.roles, name="MEMBER")
    #rolethree = discord.utils.get(ctx.guild.roles, name="Member")
    await member.add_roles(muterole)
    #await member.remove_roles(roletwo)
    #await member.remove_roles(rolethree)
    channel = discord.utils.get(ctx.guild.text_channels, name='mod-log')

    embed = discord.Embed(
        title=f"**Member Muted**", description=f"**User:** <@{member.id}>\n**Reason:** {reason}", color=discord.Color.red(), timestamp=ctx.message.created_at)

    embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
#    await ctx.channel.purge(limit=amount + 1)
    await channel.send(embed=embed)
    await ctx.send(embed=embed)
@mute.error
async def mute_error(ctx, error):
    await ctx.send("There was an Error with this command. Make sure I have what I need to use this command.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unmute(ctx, member: discord.Member=None, amount=0):
    if not member:
        await ctx.send("~unmute @user reason")
        return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
#    roletwo = discord.utils.get(ctx.guild.roles, name="MEMBER")
#    rolethree = discord.utils.get(ctx.guild.roles, name="Member")
    await member.remove_roles(role)
#    await member.add_roles(roletwo)
#    await member.add_roles(rolethree)
    guild = discord.utils.get(bot.guilds, name=f'{ctx.guild.name}')
    channel = discord.utils.get(guild.text_channels, name='mod-log')

    embed = discord.Embed(
        title=f"**Member Unmuted**", description=f"**User:** <@{member.id}>\n**Admin:** <@{ctx.message.author.id}>", color=discord.Color.green(), timestamp=ctx.message.created_at)

    embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)

#    await ctx.channel.purge(limit=amount + 1)
    await channel.send(embed=embed)
    await ctx.send(embed=embed)
@unmute.error
async def unmute_error(ctx, error):
    await ctx.send("There was an Error with this command. Make sure I have what I need to use this command.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def nuke(ctx, amount=25):
    await ctx.channel.purge(limit=amount + 1)
    guild = discord.utils.get(bot.guilds, name=f'{ctx.guild.name}')
    if guild is not None:
        channel = discord.utils.get(guild.text_channels, name='mod-log')

    embed = discord.Embed(
        title=f"Nuked: {ctx.channel.name}",
        description=f"{amount} messages were cleared", color=discord.Color.orange(), timestamp=ctx.message.created_at)
    embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)

    await channel.send(embed=embed)
@nuke.error
async def nuke_error(ctx, error):
        await ctx.send("There was an Error with this command")

@bot.command()
async def channel_stats(ctx):
        channel = ctx.channel

        embed = discord.Embed(
            title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}", color=0xc42bc5)

        embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
        embed.add_field(name="Channel Id", value=channel.id, inline=False)
        embed.add_field(
            name="Channel Topic",
            value=f"{channel.topic if channel.topic else 'No topic.'}",
            inline=False,
        )
        embed.add_field(name="Channel Position", value=channel.position, inline=False)
        embed.add_field(
            name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False
        )
        embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=False)
        embed.add_field(name="Channel is news?", value=channel.is_news(), inline=False)
        embed.add_field(
            name="Channel Creation Time", value=channel.created_at, inline=False
        )
        embed.add_field(
            name="Channel Permissions Synced",
            value=channel.permissions_synced,
            inline=False,
        )
        embed.add_field(name="Channel Hash", value=hash(channel), inline=False)

        await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="**Bot Commands**", description="**–– INFO ––**\n\nping | Returns bot ping\nhelp | Shows Commands\npfp | Returns user you @ pfp\nserver_stats | Gets info on Current server\nchannel_stats | Gets info about the current channel your in\nbot_stats | Returns bot status\n\n **–– MODERATION ––** \n\nban | Bans mentioned user\nunban | UnBans user ID from server\nkick | Kicks mentioned user\nwarn | Warns mentioned user\nmute | Mutes mentioned user\nunmute | unMutes mentioned user\nnuke | Clears specific number of messages\n\n **–– GENERAL ––** \n\nfact | Sends random fact\nfbi | ;)\nkill | shows a random way you kill mentioned user\nslap | Slaps mentioned user\nrate | Rates mentioned user out of 5 stars\nflipoff | Flips off mentioned user\nkiss | Kisses mentioned user\ncuddle | Cuddles real close into bed with mentioned user\n8ball | Answers all your questions… not very well however\njoke | Give you something so you can laugh\nlaugh | …what do u think it does\nstare | stalk a user you @\ndice | rolls a set of dice", colour=ctx.author.color)

    await ctx.send(embed=embed)
    await ctx.author.send("if you need more help with AdamBot, join the Support Discord.\nhttps://discord.gg/QaNBSzG")

@bot.command()
async def server_stats(ctx):
		embed = discord.Embed(title=f'Server Stats <:settings:585767366743293952>', colour=ctx.author.colour)

		embed.set_thumbnail(url=ctx.guild.icon_url)

		statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

		fields = [("ID", ctx.guild.id, True),
				  ("Owner  <:owner:585789630800986114>", ctx.guild.owner, True),
				  ("Region", ctx.guild.region, True),
				  ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Members", len(ctx.guild.members), True),
				  ("Humans<:authorized:585790083161128980> ", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
				  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
				  ("Banned members", len(await ctx.guild.bans()), True),
				  ("Text channels<:channel:585783907841212418>", len(ctx.guild.text_channels), True),
				  ("Voice channels <:voice:585783907673440266>", len(ctx.guild.voice_channels), True),
				  ("Categories", len(ctx.guild.categories), True),
				  ("Roles", len(ctx.guild.roles), True),
				  ("Invites", len(await ctx.guild.invites()), True),
				  ("Member's Status:", f"Online <:online:313956277808005120> {statuses[0]}\nIdle <:away:313956277220802560> {statuses[1]}\nDND <:dnd:313956276893646850> {statuses[2]}\nOffline <:offline:313956277237710868> {statuses[3]}", True),
				  ("\u200b", "\u200b", True)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def lockdown(ctx, channel: discord.TextChannel=None, amount=0):
    channel = channel or ctx.channel
    if ctx.guild.default_role not in channel.overwrites:
        overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
        }
        await channel.edit(overwrites=overwrites)
    #    await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🔒 **Lockdown on** <#{channel.id}> **has been activated.**")
    elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
        overwrites = channel.overwrites[ctx.guild.default_role]
        overwrites.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
    #    await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🔒 **Lockdown on** <#{channel.id}> **has been activated.**")
    else:
        overwrites = channel.overwrites[ctx.guild.default_role]
        overwrites.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
    #    await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🔓 **Lockdown on** <#{channel.id}> **has been removed.**")
@lockdown.error
async def lockdown_error(ctx, error):
        await ctx.send("There was an error with this command")

@bot.command(name='eightball', help='Ask the magic bot that AJB made')
async def eightball(ctx, *, question):
    Responses = [" It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes – definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "No... just.. no.",
                "Outlook good.",
                "Yes.",
                "ERROR 404.",
                "kdshvbhsdvbd h",
                "Im getting tired of everyone asking me things",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Do not count on it.",
                "My reply is no.",
                "Ask again later, im on break",
                "Ask an admin im just code.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful.",
                "Idk idiot lmao.",
                "Why are you even askin me.",
                "Its not like i can read ur question",
                "LMAOOOOOOO NAH."]
    await ctx.send(f'Question: **{question}**\nAnswer: {random.choice(Responses)}')

@bot.command()
async def bot_stats(ctx):
    """
    A usefull command that displays bot statistics.
    """
    pythonVersion = platform.python_version()
    dpyVersion = discord.__version__
    serverCount = len(bot.guilds)
    memberCount = len(set(bot.get_all_members()))

    embed = discord.Embed(colour=bot.user.colour, timestamp=ctx.message.created_at)

    embed.add_field(name='Bot Version:', value='1.0.9')
    embed.add_field(name='Python Version:', value=pythonVersion)
    embed.add_field(name='Discord.Py Version', value=dpyVersion)
    embed.add_field(name='Total Servers:', value=serverCount)
    embed.add_field(name='Total Users<:authorized:585790083161128980>', value=memberCount)
    embed.add_field(name='<:owner:585789630800986114>Bot Developer:', value="<@542483477640249354>")
    embed.add_field(name='Support Server<:verified:585790522677919749>', value="https://discord.gg/QaNBSzG")

    embed.set_author(name=f"{bot.user.name} Stats", icon_url=bot.user.avatar_url)


    await ctx.send(embed=embed)

@bot.command()
async def pfp(ctx, member: discord.Member=None):  
    if not member:
        member = ctx.message.author
    show_avatar = discord.Embed(description="[Click Here For URL](%s)" % member.avatar_url)
    show_avatar.set_image(url="{}".format(member.avatar_url))
    show_avatar.set_footer(text=f'{member}')
    await ctx.send(embed=show_avatar)

@bot.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def say(ctx, *args, amount=0):
    mesg = ' '.join(args)
#    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'{mesg}')

@bot.command()
@commands.has_permissions(kick_members=True)
async def guilds(ctx):
    """Check guilds the bot is in"""
    botGuilds = bot.guilds
    string = "**Current Server's Im In:**\n"
    for guild in botGuilds:
        string = string + f"{guild.name}\n"
    await ctx.send(f"{string}")

@bot.command(alieses = ["r"])
@commands.has_permissions(kick_members=True)
async def restart(ctx):
    channel = bot.get_channel(716087338379247626)
    embed = discord.Embed(description=f"Restart requested by <@{ctx.author.id}>", colour=discord.Color.greyple())

    embed.set_author(name="Restarting...", icon_url=bot.user.avatar_url)

    await channel.send(embed=embed)
    await bot.close()
@restart.error
async def restart_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ **You cant turn the bot off. LMAO**")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def embed(ctx, *, adminMessage, amount=0):
    embed = discord.Embed(description=f"{adminMessage}", colour=ctx.author.colour)

#    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(embed=embed)

@bot.command()
async def warn(ctx, member : discord.Member=None, *, reason=None, amount=0):
    guild = discord.utils.get(bot.guilds, name=f'{ctx.guild.name}')
    if guild is not None:
        channel = discord.utils.get(guild.text_channels, name='warn-log')

    if not member:
    #    await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"<@{ctx.author.id}> Please @ a Member when using that command")
        await asyncio.sleep(10)
    #    await ctx.channel.purge(limit=amount + 1)

#    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'<@{member.id}> Was Warned for {reason}.')
    embed = discord.Embed(
        title=f"**Member Warned**", description=f"**User:** <@{member.id}>\n**Reason:** {reason}", color=discord.Color.red(), timestamp=ctx.message.created_at)

    embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"{round(bot.latency * 10000)}ms | Case: WIP")

    await channel.send(embed=embed)
@warn.error
async def warn_error(ctx, error):
    await ctx.send("There was an Error with this command. Make sure I have what I need to use this command.")


#------------------New Updated Commands------------------------------------

@bot.command()
async def hug(ctx, member : discord.Member):
    await ctx.send(f'<@{ctx.author.id}> sent a biggggg hug to <@{member.id}>')

@bot.command()
async def kill(ctx, member : discord.Member=None, amount=0):
    if not member:
    #    await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"<@{ctx.author.id}> Please @ a Member when using that command")
        await asyncio.sleep(10)
    #    await ctx.channel.purge(limit=amount + 1)
        return
    Deaths = [f"Gets in their car and goes to kill <@{member.id}>, they run them over while they are walking to work",
                f"Kills <@{member.id}> while they were breaking into their house",
                f"Hired a Hitman to kill <@{member.id}>, the Hitman drops a building on top of them... ouch",
                f"Tried to kill <@{member.id}> with a bomb but ended up blowing themself up.... maybe next time look up how to make a bomb insted of just doing it"]
    await ctx.send(f'<@{ctx.author.id}> {random.choice(Deaths)}')

@bot.command()
async def stare(ctx, member : discord.Member=None, amount=0):
    if not member:
    #    await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"<@{ctx.author.id}> Please @ a Member when using that command")
        await asyncio.sleep(10)
    #    await ctx.channel.purge(limit=amount + 1)
        return
    await ctx.send(f'Someone is looking at <@{member.id}> and they dont even know....\n\nWell... I guess they know now')

@bot.command()
async def flipoff(ctx, member : discord.Member=None, amount=0):
    if not member:
    #    await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"<@{ctx.author.id}> Please @ a Member when using that command")
        await asyncio.sleep(10)
    #    await ctx.channel.purge(limit=amount + 1)
        return
    await ctx.send(f'<@{ctx.author.id}> flipped off <@{member.id}>.... dang.. kinda harsh')

@bot.command()
async def rate(ctx, member : discord.Member=None, amount=0):
    if not member:
    #    await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"<@{ctx.author.id}> Please @ a Member when using that command")
        await asyncio.sleep(10)
    #    await ctx.channel.purge(limit=amount + 1)
        return
    Deaths = [f"wants us to rate <@{member.id}> were gonna give them ⭐ out of 5 stars",
                f"wants us to rate <@{member.id}> were gonna give them ⭐⭐ out of 5 stars",
                f"wants us to rate <@{member.id}> were gonna give them ⭐⭐⭐ out of 5 stars",                
                f"wants us to rate <@{member.id}> were gonna give them ⭐⭐⭐⭐ out of 5 stars.... not bad!",
                f"wants us to rate <@{member.id}> were gonna give them ⭐⭐⭐⭐⭐ out of 5 starts!!!"]
#    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'<@{ctx.author.id}> {random.choice(Deaths)}')

@bot.command()
async def dog(ctx):
    Dogs = [f"https://media0.giphy.com/media/DvyLQztQwmyAM/giphy.gif?cid=ecf05e476euoa2qa8xb4zkomckn7i7oyc2x05e8b78hmsfti&rid=giphy.gif",
                f"https://media1.giphy.com/media/Y4pAQv58ETJgRwoLxj/giphy.gif?cid=ecf05e476euoa2qa8xb4zkomckn7i7oyc2x05e8b78hmsfti&rid=giphy.gif",
                f"https://media2.giphy.com/media/1fj7LPAGBMiCfxqtQy/giphy.gif?cid=ecf05e472r2jgt00v11tu6t0nvqhxxyai4slvmu8cfvknvv9&rid=giphy.gif",
                f"https://media3.giphy.com/media/oDK8A6xUNjD2M/giphy.gif?cid=ecf05e4718nx590tdzbn41fsrdo3i90xwmqx8opdg1jh6z7r&rid=giphy.gif",
                f"https://media0.giphy.com/media/2bUqez1VlOCInOZLTp/giphy.webp?cid=ecf05e474ovd1k4vxrenddazhvobfq6u0xxsbl3038bkszzw&rid=giphy.webp",
                f"https://media3.giphy.com/media/zkcXND5kY4POU/giphy.webp?cid=ecf05e474ovd1k4vxrenddazhvobfq6u0xxsbl3038bkszzw&rid=giphy.webp",
                f"https://media1.giphy.com/media/1kkxWqT5nvLXupUTwK/200w.webp?cid=ecf05e47ba6r97vf5h8u6vxwosm4dund9qn9m9386pfdnoqt&rid=200w.webp",
                f"https://media2.giphy.com/media/LfCt1sR1VweBy/giphy.webp?cid=ecf05e47ba6r97vf5h8u6vxwosm4dund9qn9m9386pfdnoqt&rid=giphy.webp",
                f"https://media1.giphy.com/media/cLcxtL1z8t8oo/giphy.webp?cid=ecf05e473v2gtez69uy4uvfdcu73eo6j0umy7wkcqwxffjo8&rid=giphy.webp",
                f"https://media1.giphy.com/media/VgIH2PYoS0ICY/giphy.gif?cid=ecf05e47zr6o4ra9w5txtsysxx51z9ei8cifmwbixmlmsi6e&rid=giphy.gif",
                f"https://media2.giphy.com/media/LYRT0ChB4CGnm/200w.webp?cid=ecf05e47orledpsm4olslcd31jsn02qttu86zarwcdbwftws&rid=200w.webp",
                f"https://media1.giphy.com/media/J546wv1ja2LkrAwRBm/giphy.webp?cid=ecf05e47dw2ggo1t1chndp0tvz3tz37pebs2qmhazglg1qex&rid=giphy.webp",
                f"https://media0.giphy.com/media/z66wZincEFYYg/200.webp?cid=ecf05e47hblqq7rwfsnxbp0i1jdoqwhkgplqq5xxwlomk62l&rid=200.webp",
                f"https://media0.giphy.com/media/3o7budU9s3Gjo5Mqt2/200.webp?cid=ecf05e47hblqq7rwfsnxbp0i1jdoqwhkgplqq5xxwlomk62l&rid=200.webp",
                f"https://media1.giphy.com/media/l3vR4Ell5crP9nYR2/giphy.webp?cid=ecf05e47nz8ugc6u8gfz9zqogecwdr6b7gatl86tyd8oikey&rid=giphy.webp",
                f"https://media3.giphy.com/media/yLZQKurQvmIAo/200.webp?cid=ecf05e47soozbyqok1skeobf9qiyi9iscq2wn82tuptll7uq&rid=200.webp",
                f"https://media3.giphy.com/media/bl7QswROIbauI/giphy.gif?cid=ecf05e470j965vchqnvymq13yq0o71ggskq0ixc1es4esxjm&rid=giphy.gif",
                f"https://media1.giphy.com/media/naXyAp2VYMR4k/giphy.gif?cid=ecf05e47r827xjjknb3e4borqczsb49xgbt815t6swia3xje&rid=giphy.gif"]
    await ctx.send(f'{random.choice(Dogs)}')

@bot.command()
async def ping(ctx):
    await ctx.send(f'My Current Ping: {round(bot.latency * 10000)}ms')

@bot.command()
async def fbi(ctx):
    await ctx.send("https://media0.giphy.com/media/QUY2pzDAKVpX3QacCg/giphy.gif?cid=ecf05e47dnzxyz13w259cjcv4rovxjwyk0z478guwng3lyh7&rid=giphy.gif")

@bot.command()
async def laugh(ctx):
    await ctx.send(f'{ctx.author} says: "ha...ha..haha..ha" while trying not to cringe')

@bot.command()
async def fact(ctx):
    Facts = [f"McDonald’s once made bubblegum-flavored broccoli",
                f"Some fungi create zombies, then control their minds",
                f"The first oranges weren’t orange",
                f"There’s only one letter that doesn’t appear in any U.S. state name... its **Q**",
                f"A cow-bison hybrid is called a beefalo",
                f"Scotland has 421 words for snow",
                f"Samsung tests phone durability with a butt-shaped robot",
                f"The “Windy City” name has nothing to do with Chicago weather",
                f"Peanuts aren’t technically nuts",
                f"Armadillo shells are bulletproof",
                f"Firefighters use wetting agents to make water wetter",
                f"The longest English word is 189,819 letters long",
                f"Octopuses lay 56,000 eggs at a time",
                f"Cats have fewer toes on their back paws",
                f"Kleenex tissues were originally intended for gas masks",
                f"That tiny pocket in jeans was designed to store pocket watches",
                f"Most Disney characters wear gloves to keep animation simple",
                f"The man with the world’s deepest voice can make sounds humans can’t hear",
                f"The current American flag was designed by a high school student",
                f"Cows don’t have upper front teeth",
                f"Thanks to 3D printing, NASA can basically “email” tools to astronauts",
                f"Bananas grow upside-down",
                f"There were active volcanoes on the moon when dinosaurs were alive",
                f"Dogs sniff good smells with their left nostril",
                f"Avocados were named after reproductive organs",
                f"The word “fizzle” started as a type of fart",
                f"No number before 1,000 contains the letter A",
                f"The # symbol isn’t officially called hashtag or pound",
                f"The French have their own name for a “French kiss”",
                f"You can thank the Greeks for calling Christmas “Xmas”",
                f"Movie trailers originally played after the movie",
                f"Mercedes invented a car controlled by joystick",
                f"The U.S. government saved every public tweet from 2006 through 2017",
                f"Theodore Roosevelt had a pet hyena",
                f"Fact: Cap’n Crunch’s full name is Horatio Magellan Crunch",
                f"The CIA headquarters has its own Starbucks, but baristas don’t write names on the cups",
                f"There’s only one U.S. state capital without a McDonald’s... Vermont",
                f"Europeans were scared of eating tomatoes when they were introduced",
                f"Humans aren’t the only animals that dream",
                f"The Eiffel Tower can grow more than six inches during the summer",
                f"Medical errors are a top cause of death",
                f"Bees can fly higher than Mount Everest",
                f"Ancient Egyptians used dead mice to ease toothaches",
                f"Humans have jumped further than horses in the Olympics",
                f"Pigeon poop is the property of the British Crown",
                f"Onions were found in the eyes of an Egyptian mummy... yummm",
                f"Abraham Lincoln was a bartender",
                f"Beethoven never knew how to multiply or divide",
                f"The word aquarium means “watering place for cattle” in Latin",
                f"An espresso maker was sent into space in 2015",
                f"An employee at Pixar accidentally deleted a sequence of Toy Story 2 during production... lol how do u even do this on accident?"]
    await ctx.send(f'Fun Fact: {random.choice(Facts)}')

@bot.command()
async def joke(ctx):
    Jokes = [f"What’s the tallest building in the world?\n\n||The library, cause it has the most stories.||",
                f"How do trees get online?\n\n||They log in.||",
                f"Why did the scarecrow keep getting promoted?\n\n ||Because he was outstanding in his field.||",
                f"What does a grape say after it’s stepped on?\n\n ||Nothing. It just lets out a little wine||",
                f"Why don’t teddy bears ever order dessert.\n\n ||Because they’re always stuffed.||",
                f"What do you say to a drunk who walks into a bar with jumper cables around his neck?\n\n ||“You can stay. Just don’t try to start anything.”||",
                f"What’s the difference between snowmen and snow women?\n\n ||Snowballs.||"]
    await ctx.send(f'Heres a Joke: {random.choice(Jokes)}')

@bot.command()
async def kiss(ctx, member : discord.Member=None, amount=0):
    if not member:
    #    await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"<@{ctx.author.id}> Please @ a Member when using that command")
        await asyncio.sleep(10)
    #    await ctx.channel.purge(limit=amount + 1)
        return
    await ctx.send(f'<@{ctx.author.id}> gave <@{member.id}> a smooch 😳😳')

@bot.command()
async def cuddle(ctx, member : discord.Member=None, amount=0):
    if not member:
    #    await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"<@{ctx.author.id}> Please @ a Member when using that command")
        await asyncio.sleep(10)
    #    await ctx.channel.purge(limit=amount + 1)
        return
    await ctx.send(f'Woahhhhh...<@{ctx.author.id}> snuggled a little to close to <@{member.id}>... or maybe they didnt ;)')

@bot.command()
async def slap(ctx, member : discord.Member=None, amount=0):
    if not member:
    #    await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"<@{ctx.author.id}> Please @ a Member when using that command")
        await asyncio.sleep(10)
    #    await ctx.channel.purge(limit=amount + 1)
        return
    await ctx.send(f'Yooooo!!! <@{ctx.author.id}> just slapped the life out of <@{member.id}>')

@bot.command(name='roll', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: 1, number_of_sides: int, amount=0):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
#    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(', '.join(dice))

@bot.command()
async def whois(ctx, target : discord.Member=None):
    target = target or ctx.author

    embed = discord.Embed(title="Users Info", colour=target.colour)

    fields = [("Name", str(target), True),
                ("ID", target.id, True),
                ("Bot?", target.bot, True),
                ("Top role", target.top_role.mention, True),
                ("Status", str(target.status).title(), True),
                ("Activity", f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", True),
                ("Mobile?", target.is_on_mobile(), True),
                ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                ("Boosted", bool(target.premium_since), True)]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    await ctx.send(embed=embed)
@whois.error
async def whois_error(ctx, error):
    await ctx.send("Error: Member not found in Guild Members")











bot.run("TOKEN")


   # guild = discord.utils.get(bot.guilds, name=f'{guild.name}')
    #if guild is not None:
     #   channel = discord.utils.get(guild.text_channels, name='mod-log')
    #
    #embed = discord.Embed(
     #   title=f"**Message Deleted: **", description=f"Channel: #{message.channel} -> user {message.author} deleted: **{message.content}**")

   # embed.set_footer(text=f"{round(bot.latency * 10000)}ms | {bot.user.name}")

    #await channel.send(embed=embed)
