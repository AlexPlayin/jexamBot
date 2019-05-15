import telebot

import json
import io
import threading

chatids = []
privateids = []
queue = []
config = {}

not_stopped = True

def saveConfig(config_temp):
    # param: config object
    # Writes into config.json file
    with open("config.json", "w") as outfile:
        json.dump(config_temp, outfile)


def loadConfig():
    # Reads from config.json file
    # Returns config as object
    with open("config.json") as data_file:
        config_temp = json.load(data_file)

    return config_temp



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

def listener (messages):
    for m in messages:
        chatid = m.chat.id
        if m.text == "/start":
            if chatids.count(chatid) == 1:
                tb.send_message(chatid, "You are already subscribed!")
            else:
                tb.send_message(chatid, "You are now subscribed!")
                chatids.append(chatid)
                saveUsers()

def sendBroadcast (message):
    for uid in chatids:
        tb.send_message(uid, message)

def sendPrivate (message):
    for uid in privateids:
        tb.send_message(uid, message)

config = loadConfig()

TOKEN = config['telegram']['bot_token']

chatids, privateids = loadUsers()

tb = telebot.TeleBot(TOKEN)

tb.set_update_listener(listener)

def toPoll():
    tb.polling()
    tb.polling(none_stop=True)
    tb.polling(interval=3)

t = threading.Thread(target=toPoll)
t.start()
