import discord
#from discord.ui import Button, View
from discord.ext import commands
from youtube_dl import YoutubeDL

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True',
               'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
#FFMPEG_OPTIONS_LOCAL = {'before_options': '-f dshow', 'options': ''}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# проверка запуска бота + его статус
@bot.event
async def on_ready():
    print('Bot connected')
    await bot.change_presence(status = discord.Status.online, activity = discord.Game('захват мира'))

# команда (!ping) для проверки работы бота в дс
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

# команда (!join) для присоединения бота к голосовому каналу
@bot.command()
async def join(ctx, url):
    vc = await ctx.message.author.voice.channel.connect()

    with YoutubeDL(YDL_OPTIONS) as ydl:
        if 'https://' in url:
            info = ydl.extract_info(url, download=False)
        else:
            info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
 
    link = info['formats'][0]['url']
 
    vc.play(discord.FFmpegPCMAudio(executable="C:/FFmpeg/bin/ffmpeg.exe", source=link, **FFMPEG_OPTIONS))

    #src = "audio=CABLE Output (VB-Audio Virtual Cable)"

    #vc.play(discord.FFmpegPCMAudio(executable = "C:/FFmpeg/bin/ffmpeg.exe", source=src, **FFMPEG_OPTIONS_LOCAL))

# команда (!leave) для отсоединения бота от голосового канала
@bot.command()
async def leave(ctx):
    await ctx.message.guild.voice_client.disconnect()

bot.run('MTA3MzM0MjkyODE0NTEwMDkwMA.Gs5DA7.0D4g4JgJeFHe2kQZICH757LkCQfXgZcG_KPZNA')
