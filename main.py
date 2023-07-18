import os
import subprocess
import logging
from telegram.ext import Updater, CommandHandler
from pydub import AudioSegment
import yt_dlp
from youtube_search import YoutubeSearch
import json

with open("config.json", "r") as f:
	data = json.load(f)
	bot_token = data["token"]



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

def start(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Hi I'm Clara developed by @shambo04\nI can convert download music from youtube\ntry `/a jaded by sadeyes`")

def convert(update, context):
	try:
		# Extract the YouTube link from the user's message
		youtube_link = update.message.text.split(' ')[1]

		# Download the YouTube video as an MP4 file using youtube-dl
		def duration_checker(info, *, incomplete):
			"""Download only videos shorter than 2 minutes (or with unknown duration)"""
			duration = info.get('duration')
			if duration and duration > 1800:
				return 'The video is too long'

		ydl_opts = {
			'match_filter': duration_checker,
			'format': 'bestaudio[ext=m4a]'
		}
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			info_dict = ydl.extract_info(youtube_link, download=False)
			audio_file = ydl.prepare_filename(info_dict)
			ydl.process_info(info_dict)


		# Send the converted MP3 file to the user
		try:
			context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(audio_file, "rb"))
		except:
			context.bot.send_message(
				chat_id=update.effective_chat.id, 
				text="Video lenght exceeded 30 mins"
			)

		# Clean up temporary files
		try:
			os.remove(audio_file)
		except:
			pass

	except Exception as e:
		logging.error(str(e))
		context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred while converting the video.")

def a(update, context):
	query = update.message.text[3:]
	context.bot.send_message(
		chat_id=update.effective_chat.id, 
		text="🔎 Searching the song..."
	)
	def duration_checker(info, *, incomplete):
		"""Download only videos shorter than 2 minutes (or with unknown duration)"""
		duration = info.get('duration')
		if duration and duration > 1800:
			return 'The video is too long'

	ydl_opts = {
		'match_filter': duration_checker,
		'format': 'bestaudio[ext=m4a]'
	}

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
	
			title = results[0]["title"]
			thumbnail = results[0]["thumbnails"][0]
			duration = results[0]["duration"]
			views = results[0]["views"]

		except Exception as e:
			print(e)
			context.bot.send_message(
				chat_id=update.effective_chat.id, 
				text="Found Nothing!\nTry checking the spelling!"
			)
	except Exception as e:
		context.bot.send_message(
			chat_id=update.effective_chat.id, 
			text="Found Nothing!\nTry checking the spelling!"
		)
		print(str(e))

	context.bot.send_message(
		chat_id=update.effective_chat.id, 
		text="Downloading..."
	)
	try:
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			info_dict = ydl.extract_info(link, download=False)
			audio_file = ydl.prepare_filename(info_dict)
			ydl.process_info(info_dict)


		# Send the converted MP3 file to the user
		try:
			context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(audio_file, "rb"))
		except:
			context.bot.send_message(
				chat_id=update.effective_chat.id, 
				text="Video lenght exceeded 30 mins"
			)

		# Clean up temporary files
		try:
			os.remove(audio_file)
		except:
			pass
	except Exception as e:
		print(e)
	try:
		os.remove(audio_file)

	except Exception as e:
		print(e)






def main():
	# Create an instance of the Updater class
	updater = Updater(token=bot_token, use_context=True)

	# Get the dispatcher to register handlers
	dispatcher = updater.dispatcher

	# Register command handlers
	dispatcher.add_handler(CommandHandler("start", start))
	dispatcher.add_handler(CommandHandler("convert", convert))
	dispatcher.add_handler(CommandHandler("a", a))

	# Start the bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C to stop it
	updater.idle()

if __name__ == '__main__':
	main()

