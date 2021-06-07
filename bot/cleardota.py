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
  #Loading username / password for Liquipedia
  LiquiUser =  os.getenv('liquiUser')
  liquiPass = os.getenv('liquiPass')
  print("hi")
  
  FF_options = webdriver.FirefoxOptions()
  FF_profile = webdriver.FirefoxProfile()
  FF_options.add_argument("-headless")
  FF_profile.update_preferences()


  
  driver = webdriver.Firefox(options=FF_options, firefox_profile=FF_profile, executable_path=os.environ.get("GECKODRIVER_PATH"), firefox_binary=FirefoxBinary(os.environ.get("FIREFOX_BIN")))


  print("hi2")
  #driver = webdriver.Firefox(options=options)
  
  driver.get("https://liquipedia.net/dota2/index.php?title=Special:UserLogin&returnto=OG&returntoquery=action%3Dedit")
  print("hi2")
  #Finds the username box and types the username in
  try:
    button = driver.find_element_by_id('wpName1')
    button.click()
    button.send_keys(LiquiUser)
    print("hi3")

    #Finds the password box and types the password in
    button=driver.find_element_by_id('wpPassword1')
    button.click()
    button.send_keys(liquiPass)

    button.submit()
  except:
    print("Error logging in")

  #Going to OG's Liquipedia page

  time.sleep(5)
  driver.get('https://liquipedia.net/dota2/OG')
  print("hi4")
  print(driver.page_source)
  time.sleep(10)
  button=driver.find_element_by_id('ca-purge')
  print("hi5")
  button.click()

  time.sleep(17)
  #Finding the clear cache button and then logging out
  print("hi6")
  button=driver.find_element_by_class_name('fas.fa-fw.fa-user-circle')
  button.click()

  button=driver.find_element_by_id('pt-logout')
  button.click()

  driver.close()
