import aiohttp
import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
from sys import platform
import asyncio

load_dotenv()

API_KEY = os.getenv('API_KEY')
APOD_URL = f'https://api.nasa.gov/planetary/apod?api_key={API_KEY}' 

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

async def image_download(result, token, rpath, name):
    image_url = result[token]
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as image_response:
            if image_response.status == 200:
                image_data = await image_response.read()
                if platform == 'linux':
                    slash = '/'
                elif platform == 'win64' or platform == 'win32':
                    slash = '\\'
                with open(f'{rpath}{slash}{name}.jpg', 'wb') as file:
                    file.write(image_data)
                print('Successful download')
            else:
                print(f'Failed to download image, HTTP Status Code = {image_response.status}')

@bot.event
async def on_ready():
    print(f'{bot.user} is ready')
    await bot.tree.sync()

@bot.tree.command(name='apod', description="Get NASA's Astronomy Picture of the Day")
async def apod(interaction: discord.Interaction):
    async with aiohttp.ClientSession() as session:
        async with session.get(APOD_URL) as response:
            if response.status == 200:
                print('Access granted\n')
                result = await response.json()
                print(result)
                msg = f"On **{result['date']}** NASA uploaded **{result['title']}** in **Astronomy Picture of the Day**\n{result['hdurl']}\n{result['explanation']}"
                await interaction.response.send_message(msg)
                await image_download(result, 'hdurl', 'Apod_photos', str(result['date']))
            else:
                print(f'Failed to access API, HTTP Status Code = {response.status}')

@bot.tree.command(name='mars', description="Get Curiosity Rover images")
async def mars(interaction: discord.Interaction):
    mars_url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={int(random.random() * 1000)}&api_key={API_KEY}'
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(mars_url) as response:
            if response.status == 200:
                print('Access granted\n')
                result = await response.json()
                random_element = random.choice(result["photos"])
                msg = f'Camera: {random_element["camera"]["full_name"]}\nSolar day: {random_element["sol"]}\n{random_element["img_src"]}'
                print(msg)
                await asyncio.sleep(2)
                await interaction.followup.send(msg)
                await image_download(random_element, 'img_src', 'Mars_photos', str(random_element['id']))
            else:
                print(f'Failed to access API, HTTP Status Code = {response.status}')

if __name__ == '__main__':
    bot.run(os.getenv('TOKEN'))
