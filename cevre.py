import discord
from discord.ext import commands
import requests
import matplotlib.pyplot as plt
from io import BytesIO

TOKEN = 'YOUR_BOT_TOKEN_HERE'  # Buraya kendi bot token'inizi koyun
WAQI_API_TOKEN = 'fa32a9c5dbf36436d38c235864ad9a91da90ee24'  # World Air Quality Index API token

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı')

@bot.command(name='kirlilik')
async def pollution_info(ctx, city: str):
    url = f'https://api.waqi.info/feed/{city}/?token={WAQI_API_TOKEN}'
    response = requests.get(url).json()
    
    if response['status'] == 'ok':
        data = response['data']
        aqi = data['aqi']
        iaqi = data['iaqi']
        
        description = f"{city} için hava kalitesi indeksi (AQI): {aqi}\n"
        description += "\n".join([f"{key}: {value['v']}" for key, value in iaqi.items()])
        
        await ctx.send(description)
    else:
        await ctx.send(f"{city} için hava kalitesi bilgisi alınamadı.")

@bot.command(name='grafik')
async def pollution_chart(ctx, city: str):
    url = f'https://api.waqi.info/feed/{city}/?token={WAQI_API_TOKEN}'
    response = requests.get(url).json()
    
    if response['status'] == 'ok':
        data = response['data']
        iaqi = data['iaqi']
        
        pollutants = list(iaqi.keys())
        values = [value['v'] for value in iaqi.values()]
        
        plt.figure(figsize=(10, 5))
        plt.bar(pollutants, values, color='green')
        plt.title(f"{city} için Hava Kalitesi İndeksi")
        plt.xlabel('Kirletici')
        plt.ylabel('Değer')
        
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        await ctx.send(file=discord.File(buf, 'pollution_chart.png'))
    else:
        await ctx.send(f"{city} için hava kalitesi bilgisi alınamadı.")

@bot.command(name='yardım')
async def help_command(ctx):
    help_text = """
    Komutlar:
    !kirlilik <şehir> - Belirtilen şehir için hava kalitesi bilgisi verir.
    !grafik <şehir> - Belirtilen şehir için hava kalitesi grafiği oluşturur.
    !yardım - Bu mesajı gösterir.
    """
    await ctx.send(help_text)

bot.run(TOKEN)
