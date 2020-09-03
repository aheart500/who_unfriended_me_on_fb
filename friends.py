from selenium import webdriver
import time
import os
import re
from selenium.webdriver.common.keys import Keys
import pickle

creditintials = {
    'email': 'your@email.com',
    'password': 'yourpassword',
    'username': 'your_fb_username'  ''' the part after facebook.com/ that leads to your personal profile '''
}
friends = []


def getLastListNumber():
    maxFile = 0
    files = os.listdir('Lists')
    for file in files:
        fileNumber = re.search(r'\d+', file).group()
        if int(fileNumber) > maxFile:
            maxFile = int(fileNumber)
    return maxFile


def saveList():
    main()
    fileName = os.path.join(
        'Lists', 'list{}.pickle'.format(getLastListNumber()+1))
    with open(fileName, 'wb') as myFile:
        pickle.dump(friends, myFile)


def loadList(listNumber):
    fileName = os.path.join('Lists', 'list{}.pickle'.format(listNumber))
    with open(fileName, 'rb') as Myfile:
        return pickle.load(Myfile)


def main():

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(
        executable_path='./webdrivers/chromedriver', options=chrome_options)
    driver.get('http://www.facebook.com')
    emailBox = driver.find_element_by_name('email')
    passBox = driver.find_element_by_name('pass')
    emailBox.send_keys(creditintials['email'])
    passBox.send_keys(creditintials['password'])
    passBox.send_keys(Keys.RETURN)
    time.sleep(5)
    driver.get(
        'http://www.facebook.com/{}/friends'.format(creditintials['username']))

    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    friendsList = driver.find_elements_by_xpath(
        '//div[contains(@class, "uiProfileBlockContent")]//div[contains(@class, "fsl")]')
    for friend in friendsList:
        friends.append(friend.text)
    driver.close()


def getUserOrder():
    print('What do you want?')
    print('If you want to save a new list enter 1')
    print('If you wanna get the last list enter 2')
    print('If you want to compare between the last two lists enter 3')
    print('If you want to exit enter 4')
    uI = input()
    if uI == '1':
        saveList()
        print('saved')
        exit()
    elif uI == '2':
        print(loadList(getLastListNumber()))
        exit()
    elif uI == '3':
        lastList = loadList(getLastListNumber())
        try:
            secondToLastList = loadList(getLastListNumber() - 1)
        except:
            print(
                'You only have one list and you can\'t compare. Please save a new list ')
            getUserOrder()
        unfriended = []
        for name in secondToLastList:
            if name not in lastList:
                unfriended.append(name)
        print(unfriended)
        exit()
    elif uI == '4':
        exit()


getUserOrder()
