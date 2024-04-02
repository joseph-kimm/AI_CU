import pychrome
import subprocess
import os
from selenium import webdriver
import time

def pychr():

    #os.system("Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222")
    browser = pychrome.Browser(url="http://127.0.0.1:9222")
    
    # Get the list of tabs
    print(len(browser.list_tab()))
    
    #close the connection
    browser.close_tab()


# seleniu is more of an automation tool, but not good for tabs that are already open
def selen():
    driver = webdriver.Chrome()

    driver.execute_script("window.open('');")
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[0])
    driver.get("https://www.youtube.com/watch?v=IgEXWRSJbi4")

    time.sleep(20)
    video_element.pause()

    print(len(driver.window_handles))
    
selen()

#pychr()