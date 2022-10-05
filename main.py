from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
import yt_dlp
from youtube_search import YoutubeSearch
import requests
import os
import keep_alive



bot_token = os.environ['token']
api_id = os.environ['api_id']
api_hash = os.environ['api_hash']


bot = Client(
    'Clara',
    bot_token = bot_token,
    api_id = api_id,
    api_hash = api_hash
)



# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))



@bot.on_message(filters.command(['start']))
def start(client, message):
    darkprince = f'👋 Hello @{message.from_user.username}\n I\'m Clara, developed by Shambo, I can download songs from YouTube. Type /a song name\n e.g - `/a talking to the moon`'
    message.reply_text(
        text=darkprince, 
        quote=False,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Github', url='https://github.com/typhonshambo/Clara-Music-Bot-Telegram'),  
                ]
            ]
        )
    )

@bot.on_message(filters.command(['a']))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('🔎 Searching the song...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                os.times.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            if time_to_seconds(duration) >= 1800:  # duration limit
                m.edit("Exceeded video duration limit : 30 mins")
                return

            views = results[0]["views"]

        except Exception as e:
            print(e)
            m.edit('Found nothing. Try changing the spelling a little.')
            return
    except Exception as e:
        m.edit(
            "✖️ Found Nothing. Sorry.\n\nTry another keywork or maybe spell it properly."
        )
        print(str(e))
        return
    m.edit("⏬ Downloading...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎧 **Title**: [{title[:35]}]({link})\n⏳ **Duration**: `{duration}`\n👁‍🗨 **Views**: `{views}`'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file,caption=rep,quote=False, title=title, duration=dur)
        m.delete()
    except Exception as e:
        m.edit('❌ Error')
        print(e)
    try:
        os.remove(audio_file)
        #os.remove(thumb_name)
    except Exception as e:
        print(e)

keep_alive.keep_alive()
bot.run()
