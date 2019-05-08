# JExamWatcher

## Requirements
    selenium
    python-telegram-bot
    pyvirtualdisplay

## Setup

Requires a `config.json`:

    {"login_credentials": {"username": "jexam_Username", "password": "jExam_Password"}, "telegram": {"bot_token": "telegram bot token"}, "known_exams": [""], "classes": {"semesterid": "3362686", "watch": [3392553, 3362770, 3363080, 3362748], "classes": {}, "name": {"3392553": "Test 1", "3362770": "Test 2", "3363080": "Formale Systeme", "3362748": "Test 3"}}}

and a `users.json`:

    {"sub": [], "private": []}

in the same directory as the `main.py`

### Additional setup

JexamBot requires a multitude of other system installations in order to work

- Firefox browser
- Geckodriver installation
- [Compatibillity](https://firefox-source-docs.mozilla.org/testing/geckodriver/geckodriver/Support.html)


## Features

1. Login into jExam
2. Read exam results
3. Read newly released lesson times
4. Send new notifications via Telegram Bot

## 1. Login into jExam

Login happens on url

`
https://jexam.inf.tu-dresden.de/de.jexam.web.v4.5/spring/welcome
`

Field data consists of:

- username field `//*[@id="username"]`
- password field `//*[@id="password"]`
- submit button `//*[@id="cntntwrpr"]/div[1]/div/div[2]/div/div/form/ol/li[3]/input`

Login to receive login token in session 
--> Nothing has to be changed as it is in Seleniums Driver

TODO: Possible timeout after X Minutes ???
EDIT: I


## 2. Read exam results

Endpoint :

`https://jexam.inf.tu-dresden.de/de.jexam.web.v4.5/spring/exams/results`


HOWTO:
- Save old results and check every so often for new entries
- entries are inside of table that *might* need to be expanded before

X-Path to check table: `//*[@id="tab1"]/tbody`

in this there are tr's with ids `node*i*i*`

theory:
always node0i*i0 is important 

## 3. Read newly released lesson times

Endpoint :

`https://jexam.inf.tu-dresden.de/de.jexam.web.v4.5/spring/scheduler?semesterId={semesterID}`

2 Parts to succeed:

- Open important lessons in table 1
    - find lessons with wanted ID in table
    - click on < a> in tr
- Wait 20 s to let jexam load
- Check table 2 for group with ID
- check if elements below has class `empty` or ID that wasn't seen yet
- do this until new div with `group_*` has been found below


X-Path to selector table : `//*[@id="to-list"]/tbody`

X-Path to lesson table: `//*[@id="lecture-list"]/tbody`

Class name in table 1: `item_*`, * = ID

Class name in table 2: `group_*`, * = ID

Tag is `tr` for both

Conditions for table 2:

- If group has 2 `tr` with class `empty` below it, no lessons are out yet
- if `tr` below that has a class `item_*` then lessons are out
- there may be n many `item_*` until a new `group_*` has been found or < /tbody> is hit

        * = unique for each lesson (for item_*)

## 4. Send new notifications via Telegram Bot

Use Telegram bot API for python to send message to configured phone numbers with update of changes made on the website

TODO: Further information needs to be found