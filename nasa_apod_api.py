import requests
import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
import asyncio

load_dotenv()

API_KEY = os.getenv('API_KEY')
APOD_URL = f'https://api.nasa.gov/planetary/apod?api_key={API_KEY}' 

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

async def image_download(result, token, rpath, name):
    image_url = result[token]
    image_response = requests.get(image_url)
    
    with open(f'{rpath}\\{name}.jpg', 'wb') as file:
        file.write(image_response.content)
    print('Successful download')

@bot.event
async def on_ready():
    print(f'{bot.user} is ready')
    await bot.tree.sync()

@bot.tree.command(name='apod', description="Get NASA's Astronomy Picture of the Day")
async def apod(interaction: discord.Interaction):
    response = requests.get(APOD_URL)
    result = response.json()
    print(result)
    msg = f"On **{result['date']}** NASA uploaded **{result['title']}** in **Astronomy Picture of the Day**\n{result['hdurl']}\n{result['explanation']}"
    await interaction.response.send_message(msg)
  ##  await image_download(result, 'hdurl', 'Apod_photos', str(result['date']))

@bot.tree.command(name='mars', description="Get Curiosity Rover images")
async def mars(interaction: discord.Interaction):
    await interaction.response.defer()
    mars_url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={int(random.random() * 1000)}&api_key={API_KEY}'
    response = requests.get(mars_url)
    result = response.json()
    random_element = random.choice(result["photos"])
    msg = f'Camera: {random_element["camera"]["full_name"]}\nSolar day: {random_element["sol"]}\n{random_element["img_src"]}'
    print(msg)
    await asyncio.sleep(2)
    await interaction.followup.send(msg)
   ## await image_download(random_element, 'img_src', 'Mars_photos', str(random_element['id']))

if __name__ == '__main__':
    bot.run(os.getenv('TOKEN'))
