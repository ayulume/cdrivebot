print(f'Starting...')
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from datetime import timedelta
import asyncio
import config

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user.name}')
    bot.loop.create_task(beemoviescript())

status_task = None
# status
async def beemoviescript():
    while True:
        await bot.change_presence(activity=discord.Game(name="around with a VM"))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name="https://seqyusphere.eu/"))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name="y'all"))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Game(name="with foxes!"))
        await asyncio.sleep(30)

@bot.event
async def on_message(message):
    if bot.user in message.mentions and not message.author.bot:
        embed = discord.Embed(
            title="Did someone ping me?",
            description="Run $help to see my commands",
            color=discord.Color.blurple()
        )
        await message.channel.send(embed=embed)
    await bot.process_commands(message)    

# kick
@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.send(f"You have been kicked from **{ctx.guild.name}**.\n**Reason:** {reason}")
    await member.kick(reason=reason)
    embed = discord.Embed(
        title="👢 Member Kicked",
        description=f"{member.mention} has been kicked.\n**Reason:** {reason}",
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed)

# ban
@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    await member.send(f"You have been banned from **{ctx.guild.name}**.\n**Reason:** {reason}")
    await member.ban(reason=reason)
    embed = discord.Embed(
        title="⛔ Member Banned",
        description=f"{member.mention} has been banned.\n**Reason:** {reason}",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

# clear
@bot.command()
@has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(
        title="🧹 Messages Deleted",
        description=f"{amount} messages were deleted.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, delete_after=5)

# mute
@bot.command()
@has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int, *, reason="No reason"):
    try:
        duration = timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await member.send(f"You have been muted in **{ctx.guild.name}** for {minutes} minute(s).\n**Reason:** {reason}")
        embed = discord.Embed(
            title="🔇 Member Muted",
            description=f"{member.mention} has been muted for {minutes} minute(s).\n**Reason:** {reason}",
            color=discord.Color.dark_purple()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="❌ Error",
            description=f"Unable to mute this member.\n`{str(e)}`",
            color=discord.Color.dark_red()
        )
        await ctx.send(embed=embed)

# unmute
@bot.command()
@has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    try:
        await member.timeout(None)
        await member.send(f"You have been unmuted in **{ctx.guild.name}**.")
        embed = discord.Embed(
            title="🔊 Member Unmuted",
            description=f"{member.mention} has been unmuted.",
            color=discord.Color.teal()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="❌ Error",
            description=f"Unable to unmute this member.\n`{str(e)}`",
            color=discord.Color.dark_red()
        )
        await ctx.send(embed=embed)

# Permission errors
@kick.error
@ban.error
@clear.error
@mute.error
@unmute.error
async def mod_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            title="🚫 Missing Permission",
            description="You don't have permission to run this command.\nThis incident will be reported.",
            color=discord.Color.dark_red()
        )
        await ctx.send(embed=embed)

# Help command
@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title="📖 Help",
        description="Here are all the available commands:",
        color=discord.Color.blurple()
    )
    
    embed.add_field(
        name="🔨 Moderation",
        value=(
            "`$kick @member [reason]` - Kick a member\n"
            "`$ban @member [reason]` - Ban a member\n"
            "`$clear [number]` - Deletes a specified number of messages\n"
            "`$mute @member [minutes] [reason]` - Timeout a member for a specific number of minutes\n"
            "`$unmute @member` - Remove timeout from a member"
        ),
        inline=False
    )

    embed.add_field(
        name="ℹ️ Misc",
        value="`There aren't any fun commands for now. So 1984`",
        inline=False
    )

    embed.set_footer(text="Prefix: $")

    await ctx.send(embed=embed)

# Starting the bot
bot.run(config.TOKEN)
