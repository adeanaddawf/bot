import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

# Get the bot token securely
TOKEN = os.getenv("MTM0NTM0ODk0OTQxODA1MzY0Mw.GYPEwY.n9BNyDYcIoFIws2b0ub1jx0t7uuLYBM1nqVUuk")

# Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Admin User IDs (Replace with actual Roblox Admin IDs)
ADMIN_USER_IDS = [4158494426, 2335100844]

# Function to send requests to Roblox backend
def send_to_roblox(action, user_id, reason=None, amount=None, item=None):
    url = "https://your-roblox-server.com/admin"
    headers = {"Authorization": "your_secret_key", "Content-Type": "application/json"}
    payload = {
        "action": action,
        "user_id": user_id,
        "reason": reason,
        "amount": amount,
        "item": item
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json() if response.status_code == 200 else {"success": False, "error": "Server error"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}

# Kick Command
@bot.command()
async def kick(ctx, user_id: int, *, reason="No reason provided"):
    if ctx.author.id in ADMIN_USER_IDS:
        response = send_to_roblox("kick", user_id, reason)
        message = f"✅ Kicked **{user_id}** for **{reason}**" if response.get("success") else f"❌ Failed: {response.get('error', 'Unknown error')}"
        await ctx.send(message)
    else:
        await ctx.send("❌ You don't have permission.")

# Ban Command
@bot.command()
async def ban(ctx, user_id: int, *, reason="No reason provided"):
    if ctx.author.id in ADMIN_USER_IDS:
        response = send_to_roblox("ban", user_id, reason)
        message = f"✅ Banned **{user_id}** for **{reason}**" if response.get("success") else f"❌ Failed: {response.get('error', 'Unknown error')}"
        await ctx.send(message)
    else:
        await ctx.send("❌ You don't have permission.")

# Unban Command
@bot.command()
async def unban(ctx, user_id: int):
    if ctx.author.id in ADMIN_USER_IDS:
        response = send_to_roblox("unban", user_id)
        message = f"✅ Unbanned **{user_id}**" if response.get("success") else f"❌ Failed: {response.get('error', 'Unknown error')}"
        await ctx.send(message)
    else:
        await ctx.send("❌ You don't have permission.")

# Give Item Command
@bot.command()
async def giveitem(ctx, user_id: int, item: str, amount: int):
    if ctx.author.id in ADMIN_USER_IDS:
        response = send_to_roblox("give_item", user_id, amount=amount, item=item)
        message = f"✅ Given **{amount}x {item}** to **{user_id}**" if response.get("success") else f"❌ Failed: {response.get('error', 'Unknown error')}"
        await ctx.send(message)
    else:
        await ctx.send("❌ You don't have permission.")

# Bot Ready Event
@bot.event
async def on_ready():
    print(f"Bot is online! Logged in as {bot.user}")

# Run the bot
bot.run(TOKEN)
