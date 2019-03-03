#!/usr/local/bin/python3

# Required for server application as selenium works in firefox window
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
display.start()

from selenium import webdriver
from selenium.common import exceptions

import json
import io
import requests
import time



def closeFunction():
    # function to connect telegrambot with main module
    global noEnd
    noEnd = False


def login(driver):

    driver.get("https://jexam.inf.tu-dresden.de/de.jexam.web.v4.5/spring/welcome")

    # ------ LOGIN PROGRESS ------
    # Fills forms with info and presses login button

    userName_input = driver.find_element_by_xpath('//*[@id="username"]')
    userName_input.send_keys(config["login_credentials"]["username"])

    password_input = driver.find_element_by_xpath('//*[@id="password"]')
    password_input.send_keys(config["login_credentials"]["password"])

    driver.find_element_by_xpath(
        '//*[@id="cntntwrpr"]/div[1]/div/div[2]/div/div/form/ol/li[3]/input'
    ).click()


def logout(driver):
    # Presses logout link on jExam
    # Can be called anytime
    driver.implicitly_wait(15)
    driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div[2]/div[2]/a").click()
    time.sleep(10)

    # Closes firefox when EVERYTHING on DOM is loaded --> sleep is required so that it waits until
    # logout has happened
    driver.close()
    return


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


def checkNewGrades():

    # Start firefox
    driver = webdriver.Firefox()

    login(driver)

    # ------ MOVE TO RESULTS PAGE -----

    driver.find_element_by_xpath(
        "/html/body/div/div[2]/div[3]/div[1]/div/div[1]/div/div[2]/ul/li[5]/a"
    ).click()
    driver.find_element_by_xpath(
        "/html/body/div/div[2]/div[3]/div[1]/div/div/div/form/ol/li[3]/input"
    ).click()

    # ------ ON RESULTS PAGE ------

    i = 0
    flag = 0

    while flag == 0:

        # Appears to be the syntax for columns
        # TODO: Needs confirmation
        identifier = "node0i" + str(i) + "i0"

        try:
            # Find a fitting column to search within
            parent = driver.find_element_by_id(identifier)

            # Collect data from childs
            name = (
                parent.find_elements_by_tag_name("td")[2]
                .find_elements_by_tag_name("span")[0]
                .get_attribute("innerHTML")
            )
            grade = (
                parent.find_elements_by_tag_name("td")[5]
                .find_elements_by_tag_name("span")[0]
                .get_attribute("innerHTML")
            )

            # Remove whitespaces from grade
            grade = grade.strip()

            if name not in knownExams:
                telegrambot.sendBroadcast(name + " ist raus!")
                telegrambot.sendPrivate("Note ist " + grade)
                knownExams.append(name)
                saveConfig(config)

            print("Name: " + name + "\n")
            print("Note: " + grade + "\n")

            # Advance inside of table
            i = i + 1

        except exceptions.NoSuchElementException:
            # Catch when we reach bottom of the table
            print("No more items")
            flag = 1

    # Logout to avoid timeout
    logout(driver)


def selectClasses(driver, ids):
    # Selects wanted lessons from left table
    table = driver.find_element_by_xpath('//*[@id="to-list"]/tbody')
    classes = table.find_elements_by_tag_name('tr')
    print(classes)
    print(ids)
     
    for c in classes:
        # Loops through all available lessons
        print("in c")
        css = c.get_attribute("class").split()[0]
        itemID = (css[5:])
        print(itemID)
        
        # int() is needed as the trimed class is a string
        if int(itemID) in ids:
            # if id is one of the ones we watch --> click
            c.find_elements_by_tag_name('a')[0].click()
            print("Clicked " + itemID)
    
    return


def checkClass(driver, id):
    # Checks selected classes in right table and return ids of classes or 0
    table = driver.find_element_by_xpath('//*[@id="lecture-list"]/tbody')

    # Get complete content of the table
    alltr = table.find_elements_by_tag_name('tr')
    content = []

    # make id a string as comparision would not work otherwise
    id = str(id)
    print("ID is "+ id)

    for tr in alltr:
        # loop through content of table and find ids
        trid = tr.get_attribute("class").split()[1][6:]
        index = 0
        print("TRID is "+ trid)

        if trid == id:
             # If the id of the searched element is the one of the parameter
            print("found it")

            # Get current position inside of table
            index = alltr.index(tr)

            # Check special case --> see readme
            if alltr[index + 1].get_attribute("class").split()[1] == "empty":
                print(trid + " is empty")
                return [0]

            print(alltr[index + 1].get_attribute("class").split()[1])
            
            # to initiate search for following events
            index = index + 1
            
            # loop through all available events until at bottom or new lesson begins
            while index < len(alltr) and alltr[index].get_attribute("class").split()[0] != "group":
                content.append(alltr[index].get_attribute("class").split()[0][5:])
                print("Found something")

                index = index + 1

    return content



def checkNewReleases():
    # Function that does part 3 of the bot
    print("releaseCheck")
    driver = webdriver.Firefox()

    login(driver)

    driver.get(
        "https://jexam.inf.tu-dresden.de/de.jexam.web.v4.5/spring/scheduler?semesterId="
        + config["classes"]["semesterid"]
    )

    selectClasses(driver, config["classes"]["watch"])

    time.sleep(10)

    for classID in config["classes"]["watch"]:

        classID = str(classID)

        value = checkClass(driver, classID)
        print(value)

        if not classID in config["classes"]["classes"]:
            print("doesnt exist")
            config["classes"]["classes"][classID] = [0]
        print(config["classes"]["classes"][classID])
        if value != config["classes"]["classes"][classID]:
            print("There has been a change in ")
            print(classID)
            config["classes"]["classes"][classID] = value
            print(" " + config["classes"]["name"][classID])
            telegrambot.sendBroadcast("Einträge in " + config["classes"]["name"][classID] + " haben sich verändert")

    saveConfig(config)
    logout(driver)
    return

import telegrambot

telegrambot.setEndFunction(closeFunction)


config = loadConfig()

# Provide config to telegram bot
telegrambot.config = config

# Firefox Instance for visiting jExam

knownExams = config["known_exams"]

# checkNewGrades()

noEnd = True

print("start2")

#time.sleep(120)
while noEnd:
    checkNewReleases()
    time.sleep(900)
    checkNewGrades()
    time.sleep(900)
    