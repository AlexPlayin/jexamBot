import telebot

import json
import io
import threading

chatids = []
privateids = []
queue = []
config = {}

not_stopped = True

TOKEN = config['telegram']['bot_token']

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

def sendBroadcast (message):
    for uid in privateids:
        tb.send_message(uid, message)

print("4")

chatids, privateids = loadUsers()
print("5")

tb = telebot.TeleBot(TOKEN)
print("6")

tb.set_update_listener(listener)
print("8")
def toPoll():
    tb.polling()
    tb.polling(none_stop=True)
    tb.polling(interval=3)

t = threading.Thread(target=toPoll)
t.start()
print("9")
