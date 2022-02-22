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

def csgoplayerstat(name):
  #Loading username / password for Liquipedia
  headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
  
 


  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--window-size=1920,1080")
  # you need executable path for heroku (aka production) - but remove it for using replit 
  # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
  
  # Use this for testing
  driver = webdriver.Chrome(chrome_options=chrome_options)
  name2 = name.lower()


  
  #driver = webdriver.Firefox(options=options)
  
  driver.get("https://www.hltv.org/")
  
  #time.sleep(2)
  #Finds the username box and types the username in
  try:
    button = driver.find_element_by_name("query")
    button.click()
    button.send_keys(name)
    
    
    time.sleep(2)
    data = soup(driver.page_source, "html.parser")

    # Use this is if the search uses the photo
    container = data.findAll("div", {"class":"box player expanded hoverable"})
    if not container:
      container = data.findAll("div", {"class": "box compact player hoverable"})
    print(container)
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
    embed.add_field(name="Error searching", value= "I was unable to find any players under that name, please try again!\nE.G: !csgostats flamez", inline=True)
    print(e)
    
    return(embed)


def dotaplayerstats(name):
  headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless") 
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--window-size=2560,1440")
  user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
  chrome_options.add_argument(f'user-agent={user_agent}')

  # you need executable path for heroku (aka production) - but remove it for using replit 
  driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
  
  # Use this for testing
  #driver = webdriver.Chrome(chrome_options=chrome_options)
  name2 = name.lower()
  if(name2 == "ammar" or name2 == "ammar_the_fucker"):
    name = "atf"

  driver.get("https://dota2protracker.com/")
  #time.sleep(2)
  try:
    button = driver.find_element_by_id("autocomplete")
    button.click()
    button.send_keys(name)


    time.sleep(2)
    data = soup(driver.page_source, "html.parser")
    container = data.findAll("ul", {"class": "players"})
    link = container[0].find("a")['href']
    link = "https://dota2protracker.com" + link
    if name2 == "ceb":
      link = "https://dota2protracker.com/player/Ceb"
    driver.close()
    player_page = requests.get(link, headers=headers)
    page_html = soup(player_page.text, "html.parser")


    wl_record = page_html.find("div", {"class": "player_stats"}).find("span").text
    if(int(wl_record[0]) > 0):
      player_picks = page_html.find_all("div", {"class": "meta-hero-card"})
      top5_picks_container = player_picks[:5]

      top5_picks_info = ""

      for pick_container in top5_picks_container:
          pick_info = pick_container.find_all("div", {"class": "meta-pick-info-block"})
          pick_name = pick_container.find("div", {"class": "meta-pick-title"}).text
          pick_matchcount = pick_info[0].next_element.strip()
          pick_winrate = pick_info[1].next_element.strip()
          top5_picks_info = top5_picks_info + \
              f'{pick_name}: {pick_matchcount} matches ({pick_winrate} Winrate) \n'

      player_stats = discord.Embed(title=f'{name} stats', url=link, color=0x55a7f7)
      player_stats.add_field(name="Win Lose", value=wl_record, inline=False)
      player_stats.add_field(name="Top 5 picks", value=top5_picks_info, inline=False)
    else:
      player_stats = discord.Embed(title=f'{name} stats', url=link, color=0x55a7f7)
      player_stats.add_field(name="Win Lose", value=wl_record, inline=False)
      
    
    return player_stats
  except Exception as e:
    print(e)
    embed = discord.Embed(title= "Error searching")
    embed.add_field(name="Error searching", value= "I was unable to find any players under that name, please try again!\nE.G: !dotastats atf", inline=True)
    return embed
    

def valoplayerstats(name):
  headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless") 
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--window-size=2560,1440")
  user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
  chrome_options.add_argument(f'user-agent={user_agent}')

  # you need executable path for heroku (aka production) - but remove it for using replit 
  driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
  
  # Use this for testing
  #driver = webdriver.Chrome(chrome_options=chrome_options)
  name2 = name.lower()


  driver.get("https://www.vlr.gg/")
  
  try:
    button = driver.find_element_by_name("q")
    button.click()
    
    button.send_keys(name)
    time.sleep(2)
    data = soup(driver.page_source, "html.parser")

    container = data.findAll("a", {"class": "auto-item"})
    
    i=0
    for a in container:
      if i == 0:
        link = a['href']
        i = 1
    driver.close()
    
    link = "https://www.vlr.gg" + link + "/?timespan=60d"
    if (str(name2).lower() == "leeeeeen" or str(name2).lower() == "leeeeen" or str(name2).lower() == "leeeen" or str(name2).lower() == "leeen"):   
      link = "https://www.vlr.gg/player/14607/leeeeeen/?timespan=60d"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
    player_page = requests.get(link, headers=headers)
    page_html = soup(player_page.text, "html.parser")
    image_container = page_html.find("div", {"class": "wf-avatar mod-player"})
    stats_table = page_html.find("table", {"class": "wf-table"})
    stats_per_agent = stats_table.find("tbody").find_all("tr")

    player_image = image_container.find("img")['src']
    if player_image == "/img/base/ph/sil.png":
        player_image = "https://vlr.gg" + player_image
    else:
        player_image = "https:" + player_image

    count = 0
    player_agents = ""
    player_acs = 0
    player_kdr = 0
    player_adr = 0
    player_kast = 0
    player_kpr = 0
    # Get the stats involved
    for agent_stats in stats_per_agent:
        if count == 0:
            player_agents += agent_stats.find("img")['src'].split("agents/", 1)[1].split(".", 1)[0].capitalize()
        else:
            player_agents += ", " + agent_stats.find("img")['src'].split("agents/", 1)[1].split(".", 1)[0].capitalize()
        player_acs += float(agent_stats.find_all("td")[3].text.strip())
        player_kdr += float(agent_stats.find_all("td")[4].text.strip())
        player_adr += float(agent_stats.find_all("td")[5].text.strip())
        player_kast += float(agent_stats.find_all("td")[6].text.strip().rstrip("%"))
        player_kpr += float(agent_stats.find_all("td")[7].text.strip())
        count += 1

    player_acs /= count
    player_kdr /= count
    player_adr /= count
    player_kast /= count
    player_kpr /= count
    
    if len(str(player_kpr)) > 4:
      player_kpr = str(player_kpr)
      player_kpr = player_kpr[0:5]
    if(len(str(player_kdr))) > 4:
      player_kdr = str(player_kdr)
      player_kdr = player_kdr[0:5]

    player_stats = discord.Embed(title=f'{name} stats', url=link, color=0xd57280)
    player_stats.set_thumbnail(url=player_image)
    player_stats.add_field(name="Top agents", value=player_agents, inline=False)
    player_stats.add_field(name="ACS", value=player_acs, inline=False)
    player_stats.add_field(name="ADR", value=player_adr, inline=False)
    player_stats.add_field(name="KAST", value=player_kast)
    player_stats.add_field(name="KPR", value=player_kpr)
    player_stats.add_field(name="KDR", value=player_kdr)

    return player_stats

      
    
  except Exception as e:
    print(e)
    embed = discord.Embed(title= "Error searching")
    embed.add_field(name="Error searching", value= "I was unable to find any players under that name, please try again!\nE.G: !valostats laaw", inline=True)
    return embed
