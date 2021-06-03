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
  LiquiUser =  os.environ['liquiUser']
  liquiPass = os.environ['liquiPass']

  #Opening web browser / logging on
  driver = webdriver.Firefox()
  driver.get("https://liquipedia.net/dota2/index.php?title=Special:UserLogin&returnto=OG&returntoquery=action%3Dedit")
  #Finds the username box and types the username in
  button = driver.find_element_by_id('wpName1')
  button.click()
  button.send_keys(LiquiUser)

  #Finds the password box and types the password in
  button=driver.find_element_by_id('wpPassword1')
  button.click()
  button.send_keys(liquiPass)

  button.submit()

  #Going to OG's Liquipedia page

  time.sleep(5)
  driver.get('https://liquipedia.net/dota2/OG')
  time.sleep(10)
  button=driver.find_element_by_id('ca-purge')
  button.click()

  time.sleep(17)
  #Finding the clear cache button and then logging out
  button=driver.find_element_by_class_name('fas.fa-fw.fa-user-circle')
  button.click()

  button=driver.find_element_by_id('pt-logout')
  button.click()

  driver.close()
