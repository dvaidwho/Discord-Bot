import discord
from discord.ext import commands
import logging #log content of whats happening 
from dotenv import load_dotenv #load enviorment variable files 
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

secret_role = "joemama"

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print(f"Activated and ready to go, {bot.user.name}.")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "fuck" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention}, thats a bad word!")

    if "aluc" in message.content.lower():
        await message.channel.send(f"{message.author.mention}, we dont like that Aluc guy")

    await bot.process_commands(message)

# .hello
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

# .joemama
@bot.command()
async def joemama(ctx):
    await ctx.send(f"Joemama.")

# .assign
@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
    else:
        await ctx.send("Role doesn't exist")

# .remove
@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} removed")
    else:
        await ctx.send("Role doesn't exist")

# .dm joemama
@bot.command()
async def dm (ctx, *, msg):
    await ctx.author.send(f"You said {msg}")

# .reply
@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

# .secret
@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("Welcome to the big leauges!")

@secret.error
async def secret_error(ctx, error):
    await ctx.send("You do not have permission to do that!")
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to do that!")

bot.run(token, log_handler=handler, log_level=logging.DEBUG) #debug info is logged into discord.log file