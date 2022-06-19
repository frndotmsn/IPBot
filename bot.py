from discord.ext import commands
from requests import get
import json

class Data:
    def __init__(self, _dict):
        if _dict is None:
            raise Exception('No data.json file in env found')
        self.allowed_users = [] if _dict['allowed_users'] is None else _dict['allowed_users']
        if _dict['owner'] is None:
            raise Exception('No owner provided')
        else: self.owner = _dict['owner']

bot = commands.Bot(command_prefix='!')

data = None
with open('data.json', 'r') as f:
    data = Data(json.load(f))

@bot.command()
async def ip(ctx):
    if (str(ctx.message.author) in data.allowed_users or str(ctx.message.author) == data.owner):
        ip = get('https://api.ipify.org').text
        await ctx.send(ip)
    else: await ctx.send('You are not allowed to use this command')

@bot.command()
async def add(ctx, name):
    if (str(ctx.message.author) == data.owner):
        data.allowed_users.append(name)
        with open('data.json', 'w') as f:
            json.dump(data.__dict__, f)
        await ctx.send(f'Added {name} to the allowed users')
    else: await ctx.send('You are not allowed to use this command')

@bot.command()
async def remove(ctx, name):
    if (str(ctx.message.author) == data.owner):
        data.allowed_users.pop(name)
        with open('data.json', 'w') as f:
            json.dump(data.__dict__, f)
        await ctx.send(f'Removed {name} from the allowed users')
    else: await ctx.send('You are not allowed to use this command')