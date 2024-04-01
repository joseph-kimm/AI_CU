import pychrome
import subprocess
import os

def init():

    os.system("Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222")
    browser = pychrome.Browser(url="http://127.0.0.1:9222")
    
    # Get the list of tabs
    print(len(browser.list_tab()))
    
    #close the connection
    browser.close_tab()

init()