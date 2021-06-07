import os
#imports
from bs4 import BeautifulSoup as soup
from dotenv import load_dotenv
load_dotenv()
import requests
from selenium import webdriver
import time

def cleardota():
  #Loading username / password for Liquipedia
  LiquiUser =  os.getenv('liquiUser')
  liquiPass = os.getenv('liquiPass')
  print("hi")
  
  


  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--no-sandbox")
  driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

  print("hi2")
  #driver = webdriver.Firefox(options=options)
  
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
  driver.get('https://liquipedia.net/dota2/OG')
  print("hi4")
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
  
