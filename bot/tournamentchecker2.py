#imports
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import discord
import os
from cleardota import cleardota
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
from discord.utils import get
#from datetime import date
#from datetime import datetime
import datetime
from time import strptime
from googletrans import Translator, LANGUAGES
import asyncio
from itertools import cycle
import asyncio
import requests
import time
from dropboxUploader import upload_file
from dropboxUploader import download_file


def DotaCheckTourni2(channelDataID):
  try:
    #Gets the URL for the tourni
      data = download_file('/dropdotatournament2.txt', 'dotatournament2.txt')
      print("smile")
      f = open("dotatournament2.txt","r")
      my_url=f.read()
      f.close()
      print(str(my_url))

      


      
     

      if (my_url=="test" or my_url=="none"):
        #If incorrect - it will return an embed telling the user
        embed=discord.Embed(title="NextDT usage - no tournament set currently!", url="https://liquipedia.net/dota2/OG", color=0xf10909)
        embed.add_field(name="Notice",value="There are currently no tournaments set for the command - please ask a Gardener to update this if there is a tournament that you think should be tracked!", inline=False)
        randomval = 0
        return(embed, randomval)

      #Starts webscraping for the game info
      headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

      OGpage = my_url
      r2 = requests.get(OGpage, headers=headers)

      page_soup2 = soup(r2.text, "html.parser")

      
      links = "Where to find the game: " + my_url

      now = datetime.datetime.now()

      dt_string_day = now.strftime("%d")
      dt_string_month = now.strftime("%m")
      dt_string_year= now.strftime("%y")
      dt_string_hour= now.strftime("%H")
      dt_string_minute= now.strftime("%M")
      dt_string_second= now.strftime("%S")

      #Gets the title of the tournament
      DTtitle = page_soup2.find('title')
      DTtitledata = DTtitle.string
      DTtitleinfo = DTtitledata.rsplit("-")
      DTtourniname = DTtitleinfo[0]
      
     

      #Parses the HTML data - Dota
      containers = page_soup2.findAll(
          "span", {"class": "team-template-team2-short"})
      containers2 = page_soup2.findAll(
          "span", {"class": "team-template-team-short"})
      containers3 = page_soup2.findAll(
          "span", {"class": "timer-object timer-object-countdown-only"})

      try:
        v_table = page_soup2.find("table", attrs={"class": "wikitable wikitable-striped infobox_matches_content"})
        tabledata = v_table.tbody.find_all("tr")


        tablestorage = tabledata[1].find_all('a', href=True)
        URL = tablestorage[0]['href']
        extendedURL = "https://liquipedia.net" + URL
        #links = links + "\n Where to find game: " + extendedURL
      except:
        pass

      #This finds the next match time - Dota
      try:
          nextgametime = containers3[0].text
          
      except:
          pass

      #Adds game to containers - dota
      try:
          team1 = containers[0]
          team2 = containers2[0]
          
      except:
          pass

      #Grabbing 1st team - Dota 2
      try:

          Teams1 = team1.a["title"]
      except:
          try:

              Teams1 = team1["data-highlightingclass"]

          except:
              pass

      #Grabbing 2nd team - Dota 2
      try:

          Teams2 = team2.a["title"]

      except:
          try:

              Teams2 = team2["data-highlightingclass"]

          except:
              pass

      #prints next dota 2 game
      try:
          Teams = (Teams1 + " vs " + Teams2)
          nextdotagame = ("<:OGpeepoThumbsUp:734000712169553951> " + Teams1 + " vs " + Teams2 + " on " +
                          nextgametime +
                          ", more information can be found at - " +
                          my_url)
          datetimesplit = nextgametime.rsplit(" ")
          monthofgame = datetimesplit[0]
          dayofgame1 = datetimesplit[1]
          dayofgame2 = dayofgame1[:-1]
          yearofgame = datetimesplit[2]
          timeofgame = datetimesplit[4]
          timesplit = timeofgame.rsplit(":")
          hourofgame = timesplit[0]
          minuteofgame = timesplit[1]
          dt_string_year = "20" + str(dt_string_year)

          try:
            monthnumber = strptime(monthofgame,'%B').tm_mon
          except:
            monthnumber = strptime(monthofgame,'%b').tm_mon
          
          #Checks / compares when the game is meant to start vs current time
          a = datetime.datetime(int(yearofgame), int(monthnumber), int(dayofgame2), int(hourofgame), int(minuteofgame), 0)

          b = datetime.datetime(int(dt_string_year), int(dt_string_month), int(dt_string_day), int(dt_string_hour), int(dt_string_minute), int(dt_string_second))

          c = a-b
                 
          if (c.days < 0):
            
            c = "The game is meant to have begun!"
          

  



      except:
          Teams = 'No games planned'
          nextgametime = 'No games planned'
          dayofgame2 = 'no games planned'
          links= 'Tournament page: ' + str(my_url)
          c = "No games planned"

      #Verifies if this is a pro-match channel if so it will send a none embed version of the message
      if((channelDataID == 689903856095723569) or (channelDataID == 690952309827698749)):
        c= str(c)
        print(c)
        if (c == "No games planned"):
          embed = "No games planned currently in the tournament tracked"
        else:
          embed= Teams + " - Starts in: " + c + " - this is in: "+ DTtourniname + " - For more information use !nextdt in <#721391448812945480>"
      else:
        embed=discord.Embed(title="Next game in - "+ DTtourniname, url=my_url, color=0xf10909)
        embed.add_field(name=Teams, value=nextgametime, inline=True)
        embed.add_field(name="Time remaining", value = c, inline=False)
        embed.add_field(name="Notice",value="Please check Liquipedia by clicking the title of this embed for more information as the time might not be accurate", inline=False)
        embed.add_field(name="Links", value=links, inline=False)
      
      return(embed, Teams,nextgametime, c, links,dayofgame2)
      
  except:
    embed=discord.Embed(title="NextDT usage - no tournament set correctly!!", url="https://liquipedia.net/dota2/OG", color=0xf10909)
    embed.add_field(name="Notice",value="An error was hit during the scan, likely caused by incorrect url, please ask a Gardener to check this", inline=False)
    randomval = 0
    

    return(embed, randomval)    
