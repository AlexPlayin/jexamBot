######################
# telegram bot functionality
######################

import __main__

import telegram 
from telegram.ext import Updater

import json
import io
import threading

# Array to collect all subscripted clients
chatids = []
privateids = []

endFunction = None

# Load config
with open('config.json') as data_file:
    config = json.load(data_file)


# FUNCTIONS
def start(bot, update):
    # Will be called when somebody writes /start to the bot
    if (update.message.chat_id in chatids):
        bot.send_message(chat_id=update.message.chat_id, text="You are already subscribed to grade updates")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="You are now subscribed to grade updates")
        chatids.append(update.message.chat_id)
        saveUsers()

def sendBroadcast(message):
    # Sends message to everyone subscribed
    for uid in chatids:
        bot.send_message(chat_id=uid, text=message)

def sendPrivate(message):
    # Sends message to everyone logged in private
    for uid in privateids:
        bot.send_message(chat_id=uid, text=message)

def loadUsers ():
    with open('users.json') as data_file:
        users = json.load(data_file)
    return users['sub'], users['private']
    

def saveUsers ():
    data = {}
    data['sub'] = chatids
    data['private'] = privateids
    with open('users.json', 'w') as outfile: 
      json.dump(data, outfile)

def setPrivate(bot, update):
    print("tries private")
    message = update.message.text
    message = message[9:]
    print(message)
    if message == (config['telegram']['bot_token'][-6:]):
        privateids.append(update.message.chat_id)
        saveUsers()
        bot.send_message(chat_id=update.message.chat_id, text='You are now subscribed to private!')

def endBot(bot, update):
    if (update.message.chat_id in privateids):
        saveUsers()
        endFunction()
        bot.send_message(chat_id=update.message.chat_id, text='Bot is shutting down!')
        threading.Thread(target=shutdown).start()

def shutdown():
    updater.stop()
    updater.is_idle = False

def setEndFunction(function):
    global endFunction
    endFunction = function


chatids, privateids = loadUsers()

print(chatids)
print (privateids)
# ----- SETUP BOT ------
bot = telegram.Bot(token=config['telegram']['bot_token'])

updater = Updater(token=config['telegram']['bot_token'])

dispatcher = updater.dispatcher

# LOGGING FOR TELEGRAM
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# Initiates easier handling of bot
from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
private_handler = CommandHandler('private', setPrivate)
stop_handler = CommandHandler('stop', endBot)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(private_handler)
dispatcher.add_handler(stop_handler)

# Start bot
updater.start_polling()
print("Starting bot")


