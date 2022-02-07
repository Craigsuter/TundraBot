# imports
from bs4 import BeautifulSoup as soup
import discord
from dotenv import load_dotenv
load_dotenv()
import requests

def dotaevents():
  try:
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    OGPage = "https://liquipedia.net/dota2/OG"
    r2 = requests.get(OGPage, headers=headers)

    page_soup2 = soup(r2.text, "html.parser")
    data_of_events = page_soup2.find_all("div", attrs={"class": "fo-nttax-infobox wiki-bordercolor-light"})
    event_containers = data_of_events[2]("table")
    event_names = []
    event_links = []
    event_dates = []
    for event_container in event_containers:
      event_names.append(event_container.find("a")['title'])
      event_links.append("https://liquipedia.net" + event_container.find("a")['href'])
      event_dates.append(event_container.find("div").text)
  
    info = ""
    n = 0
    if (len(event_names) > 0):
      embed = discord.Embed(title="Upcoming Dota events for OG", color=0x55a7f7)
      while(n < len(event_names)):
        info = info + "" + str([event_names[n]]) + "(" + str(event_links[n]) + ") - " + str(event_dates[n]) + "\n"
        n+=1
      
      embed.add_field(name="Events Found", value=info, inline=True)
    else:
      embed = discord.Embed(title="There are currently no planned tournaments for OG")
    
    
    return(embed)

  except Exception as e:
    print(e)
    
    return("There are currently no planned tournaments for OG")
