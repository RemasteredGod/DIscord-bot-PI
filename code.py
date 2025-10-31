import discord
from discord.ext import commands, tasks
import subprocess
import psutil
import time
import humanize
from datetime import datetime
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
TOKEN = os.getenv("DISCORD_TOKEN")  # Load from environment variable
DEFAULT_CHANNEL_ID = int(os.getenv("DEFAULT_CHANNEL_ID", "0"))  # Load from environment variable
DEFAULT_INTERVAL = int(os.getenv("DEFAULT_INTERVAL", "60"))  # Default logging interval in seconds

# Validate configuration
if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables. Please create a .env file based on .env.example")
if DEFAULT_CHANNEL_ID == 0:
    print("WARNING: DEFAULT_CHANNEL_ID not set. Use !setchannel command to configure.")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Global variables for logging configuration
log_channel_id = DEFAULT_CHANNEL_ID
log_interval = DEFAULT_INTERVAL

# Function to get system stats
def get_system_stats():
    try:
        # CPU Temperature (Raspberry Pi specific)
        temp_output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
        cpu_temp = temp_output.strip().replace("temp=", "")
    except:
        cpu_temp = "N/A"

    # CPU Usage
    cpu_usage = psutil.cpu_percent(interval=1)

    # RAM Usage
    ram = psutil.virtual_memory()
    ram_total = humanize.naturalsize(ram.total)
    ram_used = humanize.naturalsize(ram.used)
    ram_percent = ram.percent

    # Disk Usage
    disk = psutil.disk_usage('/')
    disk_total = humanize.naturalsize(disk.total)
    disk_used = humanize.naturalsize(disk.used)
    disk_percent = disk.percent

    return {
        "cpu_temp": cpu_temp,
        "cpu_usage": cpu_usage,
        "ram_total": ram_total,
        "ram_used": ram_used,
        "ram_percent": ram_percent,
        "disk_total": disk_total,
        "disk_used": disk_used,
        "disk_percent": disk_percent
    }

# Custom help command
class CustomHelpCommand(commands.MinimalHelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="📚 System Monitor Bot Help",
            description="Commands for monitoring and controlling the bot.",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else "")
        embed.set_footer(text="Use !help <command> for more details.")

        for cog, commands in mapping.items():
            command_list = [cmd for cmd in commands if not cmd.hidden]
            if command_list:
                command_descriptions = []
                for cmd in command_list:
                    command_descriptions.append(
                        f"`!{cmd.name}`: {cmd.short_doc or 'No description'}"
                    )
                embed.add_field(
                    name="Commands",
                    value="\n".join(command_descriptions),
                    inline=False
                )

        channel = self.get_destination()
        await channel.send(embed=embed)

# Set custom help command
bot.help_command = CustomHelpCommand()

# Select Menu for Set Channel
class ChannelSelect(discord.ui.Select):
    def __init__(self, guild):
        options = [
            discord.SelectOption(label=channel.name, value=str(channel.id))
            for channel in guild.text_channels
            if channel.permissions_for(guild.me).send_messages
        ]
        super().__init__(
            placeholder="Select a channel for logging...",
            options=options[:25],  # Discord limits to 25 options
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        global log_channel_id
        new_channel_id = int(self.values[0])
        channel = bot.get_channel(new_channel_id)

        if not channel:
            embed = discord.Embed(
                title="Error: Set Logging Channel",
                description="Selected channel not found.",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text="Configuration failed")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        permissions = channel.permissions_for(interaction.guild.me)
        if not permissions.send_messages:
            embed = discord.Embed(
                title="Error: Set Logging Channel",
                description=f"I don't have permission to send messages in {channel.mention}.",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text="Configuration failed")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        log_channel_id = new_channel_id
        print(f"Logging channel updated to: {channel.name} (ID: {log_channel_id})")
        embed = discord.Embed(
            title="Set Logging Channel",
            description=f"System stats will now be logged to {channel.mention}.",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="Configuration updated")
        await interaction.response.send_message(embed=embed)

# Select Menu for Set Interval
class IntervalSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="30 seconds", value="30"),
            discord.SelectOption(label="60 seconds", value="60"),
            discord.SelectOption(label="120 seconds", value="120"),
            discord.SelectOption(label="300 seconds", value="300"),
            discord.SelectOption(label="600 seconds", value="600")
        ]
        super().__init__(
            placeholder="Select logging interval...",
            options=options,
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        global log_interval
        interval = int(self.values[0])
        log_interval = interval
        log_stats.change_interval(seconds=log_interval)
        embed = discord.Embed(
            title="Set Logging Interval",
            description=f"Logging interval set to {interval} seconds.",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="Configuration updated")
        await interaction.response.send_message(embed=embed)

# Button for Get Channel
class GetChannelButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Show Current Channel", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        channel = bot.get_channel(log_channel_id)
        embed = discord.Embed(
            title="Current Logging Channel",
            description=f"Logging to: {channel.mention if channel else 'Unknown channel (ID: ' + str(log_channel_id) + ')'}",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="Channel info")
        await interaction.response.send_message(embed=embed, ephemeral=True)

# View for Set Channel
class ChannelView(discord.ui.View):
    def __init__(self, guild, timeout=60):
        super().__init__(timeout=timeout)
        self.add_item(ChannelSelect(guild))

# View for Set Interval
class IntervalView(discord.ui.View):
    def __init__(self, timeout=60):
        super().__init__(timeout=timeout)
        self.add_item(IntervalSelect())

# View for Get Channel
class GetChannelView(discord.ui.View):
    def __init__(self, timeout=60):
        super().__init__(timeout=timeout)
        self.add_item(GetChannelButton())

# Command to set logging channel (with dropdown)
@bot.command(name="setchannel", brief="Change logging channel")
async def set_channel(ctx):
    """Set the logging channel using a dropdown menu."""
    embed = discord.Embed(
        title="Select Logging Channel",
        description="Choose a channel from the dropdown below.",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text="Select within 60 seconds")
    view = ChannelView(ctx.guild)
    await ctx.send(embed=embed, view=view)

# Command to set logging interval (with dropdown)
@bot.command(name="setinterval", brief="Change logging interval")
async def set_interval(ctx):
    """Set the logging interval using a dropdown menu."""
    embed = discord.Embed(
        title="Select Logging Interval",
        description="Choose an interval from the dropdown below.",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text="Select within 60 seconds")
    view = IntervalView()
    await ctx.send(embed=embed, view=view)

# Command to get current logging channel (with button)
@bot.command(name="getchannel", brief="Show current logging channel")
async def get_channel(ctx):
    """Show the current logging channel with a button."""
    embed = discord.Embed(
        title="Current Logging Channel",
        description="Click the button to view the current logging channel.",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text="Click within 60 seconds")
    view = GetChannelView()
    await ctx.send(embed=embed, view=view)

# Command to run shell commands
@bot.command(name="run", brief="Run a shell command")
async def run_command_discord(ctx, *, command: str):
    """Execute a shell command and return the output."""
    embed = discord.Embed(title="Shell Command", color=discord.Color.green())
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=10)
        output = output.decode()
        embed.add_field(name="Output", value=f"```\n{output[:1000]}\n```", inline=False)
        embed.set_footer(text="Command executed successfully")
    except subprocess.CalledProcessError as e:
        embed.color = discord.Color.red()
        embed.add_field(name="Error", value=f"```\n{e.output.decode()[:1000]}\n```", inline=False)
        embed.set_footer(text="Command failed")
    except subprocess.TimeoutExpired:
        embed.color = discord.Color.red()
        embed.add_field(name="Error", value="Command timed out after 10 seconds.", inline=False)
        embed.set_footer(text="Command failed")
    await ctx.send(embed=embed)

# Task to log system stats
@tasks.loop(seconds=DEFAULT_INTERVAL)
async def log_stats():
    stats = get_system_stats()
    channel = bot.get_channel(log_channel_id)
    if not channel:
        print(f"Error: Channel with ID {log_channel_id} not found or inaccessible.")
        return

    permissions = channel.permissions_for(channel.guild.me)
    if not permissions.send_messages:
        print(f"Error: No permission to send messages in channel {channel.name} (ID: {log_channel_id})")
        return

    embed = discord.Embed(
        title="🖥️ System Monitor",
        color=discord.Color.purple(),
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else "")
    
    embed.add_field(
        name="🌡️ CPU Temperature",
        value=stats["cpu_temp"],
        inline=True
    )
    embed.add_field(
        name="📊 CPU Usage",
        value=f"{stats['cpu_usage']}%",
        inline=True
    )
    embed.add_field(
        name="🧠 RAM Usage",
        value=f"{stats['ram_used']} / {stats['ram_total']} ({stats['ram_percent']}%)",
        inline=False
    )
    embed.add_field(
        name="💾 Disk Usage",
        value=f"{stats['disk_used']} / {stats['disk_total']} ({stats['disk_percent']}%)",
        inline=False
    )
    embed.set_footer(text="System stats updated")

    try:
        await channel.send(embed=embed)
    except discord.errors.Forbidden:
        print(f"Error: Forbidden to send messages in channel {channel.name} (ID: {log_channel_id})")
    except Exception as e:
        print(f"Error sending stats to channel {channel.name} (ID: {log_channel_id}): {str(e)}")

# Bot startup
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    if not log_stats.is_running():
        log_stats.start()

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
