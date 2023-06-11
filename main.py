import os
import random
import configparser
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config['BOT']['TOKEN']

def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    for file_name in os.listdir('.'):  # replace '.' with your directory path
        if file_name.endswith('.png'):
            with open(file_name, 'rb') as photo:
                context.bot.send_photo(chat_id, photo, caption = f"Here's a photo: {file_name}")

def special(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    special_folder = 'special'  # replace with your special directory path
    png_files = [f for f in os.listdir(special_folder) if f.endswith('.png') and not f.startswith('d_')]
    
    if not png_files:  # if there are no files without 'd_' at the beginning
        png_files = [f for f in os.listdir(special_folder) if f.endswith('.png')]  # consider all .png files
    
    if png_files:
        file_name = random.choice(png_files)
        with open(os.path.join(special_folder, file_name), 'rb') as photo:
            context.bot.send_photo(chat_id, photo, caption = f"Here's a special photo :)")
        os.rename(os.path.join(special_folder, file_name), os.path.join(special_folder, f"d_{file_name}"))


def main():    
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    special_handler = CommandHandler('special', special)
    dispatcher.add_handler(special_handler)

    updater.start_polling()

if __name__ == '__main__':
    main()
