import os
#imports
from bs4 import BeautifulSoup as soup
from dotenv import load_dotenv
load_dotenv()
import requests
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time

def cleardota():
  try:
    #Loading username / password for Liquipedia
    LiquiUser =  os.getenv('liquiUser')
    liquiPass = os.getenv('liquiPass')
    print("hi")
    #Opening web browser / logging on
    #options = Options()
    #options.add_arugment('--headless')
    options = webdriver.FirefoxOptions()  
    options.add_argument('-disable-gpu')
    options.add_argument('-no-sandbox') 
    #options.headless = True
    options.add_argument('-headless')
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override","user-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36")
    binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))
    driver = webdriver.Firefox(firefox_profile= profile, firefox_binary=binary, executable_path=os.environ.get('GECKODRIVER_PATH'), options=options)
  
    print("hi2")
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

  
    
    driver.get("https://liquipedia.net/dota2/index.php?title=Special:UserLogin&returnto=OG&returntoquery=action%3Dedit")
    print("hi2")
    #Finds the username box and types the username in
    button = driver.find_element_by_id('wpName1')
    button.click()
    button.send_keys(LiquiUser)
    print("hi3")

    #Finds the password box and types the password in
    button=driver.find_element_by_id('wpPassword1')
    button.click()
    button.send_keys(liquiPass)

    button.submit()

    #Going to OG's Liquipedia page

    time.sleep(5)
    text = driver.get('https://liquipedia.net/dota2/OG')
    time.sleep(10)
    print(text)
    button=driver.find_element_by_id('ca-purge')
    button.click()

    time.sleep(17)
    #Finding the clear cache button and then logging out
    button=driver.find_element_by_class_name('fas.fa-fw.fa-user-circle')
    button.click()

    button=driver.find_element_by_id('pt-logout')
    button.click()

    driver.close()
  except Exception as e: print(e)