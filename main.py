import discord
import logging
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

if not os.path.exists('.env'):
    print("Error: .env file not found.")
else:
    print(".env file loaded successfully.")
   # Access the variables
discord_token = os.getenv('DISCORD_TOKEN')
openai_key = os.getenv('OPENAI_API_KEY')


client = OpenAI(api_key=openai_key)

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')    


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    logging.info("-- updated at: 2024-10-18 13:40 -- ")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    res = await chat(message.content)
    await message.channel.send(res) 



async def chat(message):
    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]   
    )
    answer = response.choices[0].message.content
    return answer


bot.run(discord_token)
