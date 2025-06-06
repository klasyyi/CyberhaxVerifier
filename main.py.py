import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# Securely fetch the token from environment variable
TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Set this in Railway under Variables
GUILD_ID = 1302072773384077382  # Replace with your server's ID
ROLE_NAME = "Officer"  # Must match your Discord role name exactly

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Setup Google Sheets access
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
client = gspread.authorize(creds)
sheet = client.open("CYBERHAX Whitelist").sheet1

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def verify(ctx):
    user_id = str(ctx.author.id)
    ids = sheet.col_values(3)  # Make sure this is the column with Discord IDs

    if user_id in ids:
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=ROLE_NAME)
        await ctx.author.add_roles(role)
        await ctx.send(f"✅ {ctx.author.mention} verified as CYBERHAX member!")
    else:
        await ctx.send(f"❌ {ctx.author.mention} not found in CYBERHAX whitelist.")

bot.run(TOKEN)
