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



def DotaCheck(channelDataID):
    #Opening OG's Liquipedia page
      my_url = 'https://liquipedia.net/dota2/OG'  
      uClient = uReq(my_url)
      page_html = uClient.read()
      uClient.close()
      page_soup = soup(page_html, "html.parser")
      links = 'OG Liquipedia: https://liquipedia.net/dota2/OG'

      now = datetime.datetime.now()
      #Getting current date / time values
      dt_string_day = now.strftime("%d")
      dt_string_month = now.strftime("%m")
      dt_string_year= now.strftime("%y")
      dt_string_hour= now.strftime("%H")
      dt_string_minute= now.strftime("%M")
      dt_string_second= now.strftime("%S")



      #Parses the HTML data - Dota - grabbing time / both team HTML
      containers = page_soup.findAll(
          "span", {"class": "team-template-team2-short"})
      containers2 = page_soup.findAll(
          "span", {"class": "team-template-team-short"})
      containers3 = page_soup.findAll(
          "span", {"class": "timer-object timer-object-countdown-only"})

      try:
        v_table = page_soup.find("table", attrs={"class": "wikitable wikitable-striped infobox_matches_content"})
        tabledata = v_table.tbody.find_all("tr")


        tablestorage = tabledata[1].find_all('a', href=True)
        URL = tablestorage[0]['href']
        extendedURL = "https://liquipedia.net" + URL
        links = links + "\n Tournament: " + extendedURL
      except:
        pass

      #This finds the next match time - Dota
      try:
          nextgametime = containers3[0].text
          print(nextgametime)
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
          
          #Compares the time between current  time and when game starts 
          a = datetime.datetime(int(yearofgame), int(monthnumber), int(dayofgame2), int(hourofgame), int(minuteofgame), 0)

          b = datetime.datetime(int(dt_string_year), int(dt_string_month), int(dt_string_day), int(dt_string_hour), int(dt_string_minute), int(dt_string_second))

          c = a-b
          print(c)       
          #Verifies if the game has begun
          if (c.days < 0):
            
            c = "The game is meant to have begun!"

  



      except:
        #If no game available - will tell user
          Teams = 'No games planned'
          nextgametime = 'No games planned'
          dayofgame2 = 'no games planned'
          
          c = "No games planned"

      #Verifies the channels if in pro-match 
      if((channelDataID == 689903856095723569) or (channelDataID == 690952309827698749)):
        c= str(c)
        if (c == "No games planned"):
          embed = "No games planned currently - For more information use !nextdota in <#721391448812945480>"
        else:
          embed= Teams + " - Starts in: " + c + " - For more information use !nextdota in <#721391448812945480>"

      #Creates the embed with all the details
      else:
        embed=discord.Embed(title="OG Dota's next game", url="https://liquipedia.net/dota2/OG", color=0xf10909)
        embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
        embed.add_field(name=Teams, value=nextgametime, inline=True)
        embed.add_field(name="Time remaining", value = c, inline=False)
        embed.add_field(name="Notice",value="Please check Liquipedia by clicking the title of this embed for more information as the time might not be accurate", inline=False)
        embed.add_field(name="Links", value=links, inline=False)

      return(embed, Teams,nextgametime, c, links,dayofgame2)






def CSGOCheck(channelDataID):
  try:
    #Loading HLTV of OG
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}


    OGpage = 'https://www.hltv.org/team/10503/og#tab-matchesBox'
    r2 = requests.get(OGpage, headers=headers)

    page_soup2 = soup(r2.text, "html.parser")
    dataofpage = page_soup2.findAll("td", {"class":"matchpage-button-cell"})


    linkinfo = []
    #If game found - open the page via the href / link info
    for a in dataofpage[0].findAll('a', href=True):

      linkinfo.append(a['href'])

    matchlink = "https://www.hltv.org" + linkinfo[0]


   
    
    r = requests.get(matchlink , headers=headers)
    
    #Load the page of the match
    page_soup = soup(r.text, "html.parser")
    test = page_soup.findAll("div", {"class":"teamName"})
    team1= test[0].text
    team2 = test[1].text
    
    #Grab time / date
    test2 = page_soup.findAll("div", {"class":"time"})
    
    test3 = page_soup.findAll("div",{"class":"date"})
    
    #Time till game count down via HLTV value
    test4 = page_soup.findAll("div", {"class":"countdown"})
    time1 = test4[0].text
    time2 = time1.replace(" ","")
    
    #Link to the tournament page
    link4tourni = page_soup.findAll("div", {"class":"event text-ellipsis"})

    for a in link4tourni[0].findAll('a', href=True):
        link4tourni = "https://www.hltv.org" + a['href']
  
    teams = team1 + " vs " + team2
    dateofgame = test2[0].text
    timeofgame = test3[0].text
    

    datep1 = dateofgame.rsplit(":")
    datep2 = int(datep1[0]) - 2
    if(datep2 < 10):
      datep3 = "0" + str(datep2) + ":" + datep1[1]

    else:
      datep3 = str(datep2) + ":" + datep1[1]

    #Prints based on pro-match channel - will give a more chat friendly version
    if((channelDataID == 690952309827698749) or (channelDataID == 689903856095723569)):
      embed=teams + " - Starts in: " + time2 + " - For more information use !nextcsgo in <#721391448812945480>"
    else:
      embed=discord.Embed(title="OG CSGO's next game", url="https://www.hltv.org/team/10503/og#tab-matchesBox",color=0xff8800)
      embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
      embed.add_field(name=teams, value= timeofgame + " - " + datep3 + " UTC", inline=True)
      embed.add_field(name="Time till game", value=time2, inline=False)
      embed.add_field(name="Notice", value="Please check HLTV by clicking the title of this embed for more information as the time might not be accurate", inline=False)
      embed.add_field(name="Links", value="OG Liquipedia: https://liquipedia.net/counterstrike/OG\nOG HLTV: https://www.hltv.org/team/10503/og#tab-matchesBox\nGame page: " + matchlink +"\nTournament: " + link4tourni, inline=False)


    return(teams, timeofgame, datep3, time2, matchlink, link4tourni, embed)



  except:
    if((channelDataID == 690952309827698749) or (channelDataID == 689903856095723569)):
      embed= "There is currently no games planned for OG, for more information use !nextcsgo in <#721391448812945480>"
    else:
      embed=discord.Embed(title="OG CSGO's next game", url="https://www.hltv.org/team/10503/og#tab-matchesBox",color=0xff8800)
      embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
      embed.add_field(name="No games planned", value="No games planned", inline=True)
      embed.add_field(name="Links", value="https://www.hltv.org/team/10503/og#tab-matchesBox/ https://liquipedia.net/counterstrike/OG", inline=False)
    
    return("No games planned","No games planned","No games planned","No games planned","No games planned","No games planned", embed)
    




def ValoCheck(channelDataID):
  try:
    #Loads OG VLR page
    testv = "https://www.vlr.gg/team/2965/og"
    uClient = uReq(testv)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")

    now = datetime.datetime.now()
    #Gets current time for later comparisons
    dt_string_day = now.strftime("%d")
    dt_string_month = now.strftime("%m")
    dt_string_year= now.strftime("%y")
    dt_string_hour= now.strftime("%H")
    dt_string_minute= now.strftime("%M")
    dt_string_second= now.strftime("%S")


    tabledata = page_soup.find("div", attrs = {"class":"wf-card "})
    tabledata2 = page_soup.findAll("div", {"class":"text-of"})
    tabledata3 = page_soup.findAll("div", {"class":"rm-item-date"})
    carrot = "carrot"
    #Gets the enemy team's name
    valoenemyteam  = page_soup.find("div", attrs={"class":"rm-item-opponent"}).text
    random = page_soup.find("span", {"class": "rm-item-score-eta"})
    random2 = str(random)
    #This will error out of the check if the score value is null [catching if the game found has already happened / started]
    if random2 == "None":
      carrot = carrot  + 1
      print(carrot)
      print("test")

    
    valotimeofgame = tabledata3[0].text
    datebeforesplit = valotimeofgame.strip()
    datesplit = datebeforesplit.rsplit(" ")
    actualdatebeforeclean = datesplit[1]
    testing = actualdatebeforeclean.split()
    #Creating date / time from all values from VLR
    dateOfGame = testing[1]
    timeOfGame = datesplit[0]
    prefixOfTime = testing[0]
    nameOfEnemy = valoenemyteam.strip() 
    datesections = dateOfGame.rsplit("/")
    datep1 = datesections[0]
    datep2 = datesections[1]
    datep3 = datesections[2]
    dateOfGame = datep3 + "/" + datep2 + "/" + datep1
    #Splitting out the date vlaues
    yearofgame = datep1
    monthnumber = datep2
    dayofgame2 = datep3
  


    

    UTCTime = timeOfGame.rsplit(":")
    UTCTime2 = timeOfGame.rsplit(":")
    UTCBC = int(UTCTime[0]) + 4
    if UTCBC > 12:
      if prefixOfTime == "AM":
        prefixOfTime = "PM"
      else:
        prefixOfTime = "AM"
    if UTCBC > 12:
      hourofvalo = str(UTCBC-12)
      UTCTime = str(UTCBC - 12) + UTCTime[1] + prefixOfTime
    else:
      hourofvalo= UTCBC
      UTCTime = str(UTCBC) + ":" + UTCTime[1] + prefixOfTime
    
    #date/time comparisions to get a countdown
    minuteofgame = UTCTime2[1]
    dt_string_year = "20" + str(dt_string_year)
    a = datetime.datetime(int(yearofgame), int(monthnumber), int(dayofgame2), int(hourofvalo), int(minuteofgame), 0)
    b = datetime.datetime(int(dt_string_year), int(dt_string_month), int(dt_string_day), int(dt_string_hour), int(dt_string_minute), int(dt_string_second))

    c = a-b
    print(c) 
    #Will check if the game has already begun
    if (c.days < 0):
      c = "The game is meant to have begun!"
    



    valorantTeams = "OG vs " + nameOfEnemy
    valorantTeamTime = dateOfGame + " - " + UTCTime + " UTC"


    return(valorantTeams, valorantTeamTime, c, dayofgame2)

  except:
    return("No games planned", "No games planned", "No games planned")
   
