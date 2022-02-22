import os
#imports
from bs4 import BeautifulSoup as soup
from dotenv import load_dotenv
load_dotenv()
import requests
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from dateutil.relativedelta import relativedelta
from datetime import date
import discord

def cleardota(name):
  #Loading username / password for Liquipedia
  headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
  
 


  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--window-size=1920,1080")
  driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
  name2 = name.lower()


  
  #driver = webdriver.Firefox(options=options)
  
  driver.get("https://www.hltv.org/")
  print("pushit")
  time.sleep(2)
  #Finds the username box and types the username in
  try:
    button = driver.find_element_by_name("query")
    button.click()
    button.send_keys(name)
    
    
    time.sleep(2)
    data = soup(driver.page_source)
    
    container = data.findAll("div", {"class":"box player expanded hoverable"})
    driver.close()
   
    tablestorage = container[0].find_all('a', href=True)
    
    value = tablestorage[0]['href']
    value2 = value[:7] + "s" + value[7:]
    
    link = 'https://www.hltv.org/stats' + str(value2)
    name = name
    
    today = date.today()

    if(name2=="niko"):
      if(name == "NiKo"):
        link = "https://www.hltv.org/stats/players/3741/niko"
      else:
        link = "https://www.hltv.org/stats/players/10264/niko"

    three_months_ago = today - relativedelta(months=1)
    url = link + f'?startDate={three_months_ago}&endDate={today}'
    player_page = requests.get(url, headers=headers)
    
    page_html = soup(player_page.text, "html.parser")
    rating_kast_row = page_html.find_all(
        "div", {"class": "summaryStatBreakdownRow"})[0]
    adr_kpr_impact_row = page_html.find_all(
        "div", {"class": "summaryStatBreakdownRow"})[1]
    
    # Get the Rating 2.0
    rating_container = rating_kast_row.find_all(
        "div", {"class": "summaryStatBreakdown"})[0]
    player_rating = rating_container.find(
        "div", {"class": "summaryStatBreakdownDataValue"}).text

    # Get the KAST
    kast_container = rating_kast_row.find_all(
        "div", {"class": "summaryStatBreakdown"})[2]
    player_kast = kast_container.find(
        "div", {"class": "summaryStatBreakdownDataValue"}).text

    # Get the impact
    impact_container = adr_kpr_impact_row.find_all(
        "div", {"class":"summaryStatBreakdown"})[0]
    player_impact = impact_container.find(
        "div", {"class": "summaryStatBreakdownDataValue"}).text
  
    # Get the ADR
    adr_container = adr_kpr_impact_row.find_all(
        "div", {"class": "summaryStatBreakdown"})[1]
    player_adr = adr_container.find(
        "div", {"class": "summaryStatBreakdownDataValue"}).text

    # Get the KPR
    kpr_container = adr_kpr_impact_row.find_all(
        "div", {"class": "summaryStatBreakdown"})[2]
    player_kpr = kpr_container.find(
        "div", {"class": "summaryStatBreakdownDataValue"}).text

    # Get the KDR
    kdr_container = page_html.find_all(
        "div", {"class": "col stats-rows standard-box"})[0].find_all("div", {"class": "stats-row"})[3]
    player_kdr = kdr_container.find_all("span")[1].text

    # Get the image
    image_container = page_html.find(
        "div", {"class": "summaryBodyshotContainer"})
    player_image = image_container.find(
        "img", {"class": "summaryBodyshot"})['src']

   

    player_stats = discord.Embed(
        title=f'{name} stats', url=url, color=0xff8800)
    player_stats.set_thumbnail(url=player_image)
    player_stats.add_field(
        name="Rating 2.0", value=player_rating, inline=False)
    player_stats.add_field(name="Impact", value=player_impact, inline=False)
    player_stats.add_field(name="ADR", value=player_adr, inline=False)
    player_stats.add_field(name="KAST", value=player_kast)
    player_stats.add_field(name="KPR", value=player_kpr)
    player_stats.add_field(name="KDR", value=player_kdr)
    

    return player_stats
    
  except Exception as e:
    embed = discord.Embed(title= "Error searching")
    embed.add_field(name="Error searching", value= "I was unable to find any players under that name, please try again!", inline=True)
    print(e)
    
    return(embed)

  