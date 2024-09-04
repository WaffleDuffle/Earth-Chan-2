import requests
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
URL = f'https://api.nasa.gov/planetary/apod?api_key={API_KEY}' 

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is ready')
    await bot.tree.sync()  


@bot.tree.command(name="apod", description="Get NASA's Astronomy Picture of the Day")
async def apod(interaction: discord.Interaction):
    response = requests.get(URL)
    result = response.json()

    msg = f'On **{result['date']}** NASA uploaded **{result['title']}** in **Astronomy Picture of the Day**\n{result['hdurl']}\n{result['explanation']}'
    await interaction.response.send_message(msg)

    image_url = result['url']
    image_response = requests.get(image_url)
    with open (str(result['date']) + '.jpg', 'wb') as file:
        file.write(image_response.content)
    print('Successfull download')


if __name__ == '__main__':
    bot.run(os.getenv('TOKEN'))
