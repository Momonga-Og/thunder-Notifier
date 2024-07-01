import discord
import os
from discord.ext import commands
from discord import app_commands

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Add this to avoid warnings

# Create the bot instance with desired intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Use the existing command tree from the bot
tree = bot.tree


@tree.command(name='hello', description='Replies with Hello!')
async def hello_command(interaction: discord.Interaction):
    await interaction.response.send_message('Hello!')


@tree.command(name='pm_all', description='Send a private message to all users in the server')
@app_commands.describe(message='The message to send')
async def pm_all(interaction: discord.Interaction, message: str):
    try:
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return

        # Defer response to prevent timeout
        await interaction.response.defer(ephemeral=True)

        sent_count = 0
        failed_count = 0
        guild = interaction.guild

        for member in guild.members:
            if member.bot or member == interaction.user:
                continue

            try:
                await member.send(message)  # Send a private message
                sent_count += 1
            except Exception:
                failed_count += 1  # Log or handle errors during sending

        await interaction.followup.send(
            f"Sent messages to {sent_count} users. Failed to send to {failed_count} users."
        )
    except Exception as e:
        await interaction.followup.send(f"Error: {e}", ephemeral=True)


# Start the bot
bot.run(DISCORD_BOT_TOKEN)