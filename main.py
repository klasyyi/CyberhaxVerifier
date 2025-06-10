import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# Securely fetch the token from environment variable
TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Set this in your cloud environment
GUILD_ID = 1302072773384077382  # Your server ID
ROLE_NAME = "Officer"  # Your target role name

intents = discord.Intents.default()
intents.members = True  # Needed to assign roles
intents.message_content = True  # Needed for reading message content

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def verify(ctx):
    try:
        user_id = str(ctx.author.id)
        
        # Google Sheets setup
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open("CYBERHAX Whitelist").sheet1

        ids = sheet.col_values(3)  # Ensure Discord IDs are in column 3

        if user_id in ids:
            role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)
            if role:
                await ctx.author.add_roles(role)
                await ctx.send(f"✅ {ctx.author.mention} verified as CYBERHAX member!")
            else:
                await ctx.send("❌ Role not found. Please check the role name.")
        else:
            await ctx.send(f"❌ {ctx.author.mention} not found in CYBERHAX whitelist.")
    except Exception as e:
        await ctx.send(f"⚠️ Error occurred: {e}")
        print(f"Error: {e}")

bot.run(TOKEN)
