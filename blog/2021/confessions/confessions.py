import requests
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
import time

browser = RoboBrowser(history=True)
def login(username, password):
    browser.open("https://www.facebook.com/")
    login_form = browser.get_form(id="login_form")
    login_form['email'] = username
    login_form['pass'] = password
    browser.submit_form(login_form)

def get_confession(number):
    url = "https://www.facebook.com/page/462508190484900/search/?q=" + str(number)
    browser.open(url)
    spans = browser.find_all('span')
    print(spans)

if __name__ == "__main__":
    username = args[0]
    password = args[1]
    login(username, password)
    for i in range(46263, 46240, -1):
        get_confession(i)
        # time.sleep(10)
        input()