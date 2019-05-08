######################
# telegram bot functionality
######################
print("4")

from aiogram import Bot, Dispatcher, executor, types

import asyncio
import json
import io
import threading

# Array to collect all subscripted clients
chatids = []
privateids = []

endFunction = None

print("3")


# Load config
with open('config.json') as data_file:
    config = json.load(data_file)

loop = asyncio.get_event_loop()
bot = Bot(token=config['telegram']['bot_token'], loop=loop)
dp = Dispatcher(bot, loop=loop)

# LOGGING FOR TELEGRAM
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Start bot


print("below")

# FUNCTIONS

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    print("in")
    """
    This handler will be called when client send `/start` or `/help` commands.
    """
    if message.chat.id in chatids:
        await message.reply("You are aready subscribed!")
    else:
        await message.reply("You are now subscribed to updates!")
        chatids.append(message.chat.id)
        saveUsers()


async def sendBroadcast(message):
    # Sends message to everyone subscribed
    for uid in chatids:
        await bot.send_message(uid, message)

async def sendPrivate(message):
    # Sends message to everyone logged in private
    for uid in privateids:
        await bot.send_message(uid, message)

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

@dp.message_handler(commands=['private'])
async def setPrivate(message: types.Message):
    print("tries private")
    message = message.text
    message = message[9:]
    print(message)
    if message == (config['telegram']['bot_token'][-6:]):
        privateids.append(message.chat.id)
        saveUsers()
        await bot.send_message(message.chat.id, 'You are now subscribed to private!')

@dp.message_handler(commands=['stop'])
async def endBot(message: types.Message):
    if (message.chat.id in privateids):
        saveUsers()
        endFunction()
        await bot.send_message(message.chat.id, 'Bot is shutting down!')
        threading.Thread(target=shutdown).start()

@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)

def shutdown():
    bot.close()

def setEndFunction(function):
    global endFunction
    endFunction = function


chatids, privateids = loadUsers()

print(chatids)
print (privateids)  

# ----- SETUP BOT ------


def startBot(loop):
    asyncio.set_event_loop(loop)
    executor.start_polling(dp, loop=loop, skip_updates=True)
    loop.run_forever()


t = threading.Thread(target=startBot, args=(loop,))
t.start() 