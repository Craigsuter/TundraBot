#imports
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import discord
import os
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
from datetime import timedelta



def DotaCheck(channelDataID):
    #Opening OG's Liquipedia page
      
      headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}


      OGpage = 'https://liquipedia.net/dota2/OG'
      my_url = OGpage
      r2 = requests.get(OGpage, headers=headers)

      page_soup2 = soup(r2.text, "html.parser")



      
      links = '[OG Liquipedia Page](https://liquipedia.net/dota2/OG)'

      now = datetime.datetime.now()
      #Getting current date / time values
      dt_string_day = now.strftime("%d")
      dt_string_month = now.strftime("%m")
      dt_string_year= now.strftime("%y")
      dt_string_hour= now.strftime("%H")
      dt_string_minute= now.strftime("%M")
      dt_string_second= now.strftime("%S")



      #Parses the HTML data - Dota - grabbing time / both team HTML
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
        links = links + "\n [Tournament](" + extendedURL +")"
      except:
        pass



      try:
        testlink = extendedURL
        uClient = uReq(testlink)
        page_html2 = uClient.read()
        uClient.close()
        page_soup2 = soup(page_html2, "html.parser")
  
        tabledata2 = page_soup2.findAll("div", {"class":"infobox-header wiki-backgroundcolor-light"})
        tourniname = tabledata2[0].text.strip().replace("[e]","").replace("[h]","")
        
        
      
      except:
        tourniname="No tourni found"
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
          
          #Compares the time between current  time and when game starts 
          a = datetime.datetime(int(yearofgame), int(monthnumber), int(dayofgame2), int(hourofgame), int(minuteofgame), 0)

          b = datetime.datetime(int(dt_string_year), int(dt_string_month), int(dt_string_day), int(dt_string_hour), int(dt_string_minute), int(dt_string_second))

          epochtest = datetime.datetime(int(yearofgame), int(monthnumber), int(dayofgame2), int(hourofgame), int(minuteofgame), 0).timestamp()
          
          lenofepoch = len(str(epochtest))
          epoch = str(epochtest)[:lenofepoch - 2]
          

          c = a-b
               
          #Verifies if the game has begun
          if (c.days < 0):
            
            c = "The game is meant to have begun!"

  



      except:
        #If no game available - will tell user
          Teams = 'No games planned'
          nextgametime = 'No games planned'
          dayofgame2 = 'no games planned'
          epoch = 'No games planned'
          c = "No games planned"

      #Verifies the channels if in pro-match 
      if((channelDataID == 689903856095723569) or (channelDataID == 972571026066141204) or (channelDataID == 972946124161835078) or (channelDataID == 972570634196512798) or (channelDataID == 690952309827698749)or (channelDataID == 697447277647626297) or (channelDataID == 818793950965006357)):
        c= str(c)
        if (c == "No games planned"):
          embed = "No games planned currently - For more information use !nextdota in <#721391448812945480>"
        else:
          embed= Teams + " - Starts in: " + c + " / In your local time: <t:" + str(epoch) + "> - For more information use !nextdota in <#721391448812945480>"

      #Creates the embed with all the details
      else:
        print(c)
        embed=discord.Embed(title="OG Dota's next game", url="https://liquipedia.net/dota2/OG", color=0xf10909)
        embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
        if(str(epoch) != "No games planned"):
          embed.add_field(name=Teams, value="<t:" + str(epoch) + "> - this is local to your timezone", inline=True)
       

        embed.add_field(name="Time remaining", value = str(c) , inline=False)
        embed.add_field(name="Notice",value="Please check Liquipedia by clicking the title of this embed for more information as the time might not be accurate", inline=False)
        embed.add_field(name="Links", value=links, inline=False)

      return(embed, Teams,nextgametime, c, links,dayofgame2, tourniname, extendedURL)






def CSGOCheck(channelDataID):
  try:
    #Loading HLTV of OG
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    #change url
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
    print("hi")
    time1 = test4[0].text
    time2 = time1.replace(" ","")

    try:
      testlink = matchlink
      r3 = requests.get(testlink, headers=headers)
  
      page_soup2 = soup(r3.text, "html.parser")

      tabledata2 = page_soup2.findAll("div", {"class":"event text-ellipsis"})
      tourniname= tabledata2[0].text
      
      
    
    except Exception as e:
      print(e)
      tourniname="No tourni found"
      pass

    
    try:
      x= time2.split(":")
    
      timetoadd = 0
      while len(x) > 1:
        ValueCheck = x[0]
        timevalue = ValueCheck[-1]
        if(timevalue == "s"):
          if (int(ValueCheck[:-1]) != 0):
            timetoadd = timetoadd + int(ValueCheck[:-1])
          x.pop(0)
        if(timevalue =="m"):
          if (int(ValueCheck[:-1]) != 0):
            timetoadd = timetoadd + (int(ValueCheck[:-1])*60)
          x.pop(0)
        if(timevalue =="h"):
          if (int(ValueCheck[:-1]) != 0):
            timetoadd = timetoadd + (int(ValueCheck[:-1])*60*60)
          x.pop(0)
        if(timevalue =="d"):
          if (int(ValueCheck[:-1]) != 0):
            timetoadd = timetoadd + (int(ValueCheck[:-1])*60*60*24)
          x.pop(0)
      if len(x) == 1:

        ValueCheck = x[0]
        timevalue = ValueCheck[-1]

        if(timevalue == "s"):
          if (int(ValueCheck[:-1]) != 0):
            timetoadd = timetoadd + int(ValueCheck[:-1])
          x.pop(0)
       
        else:
          
          del x[:]

    except Exception as e: print(e)
  
    if(timetoadd > 0):
      
      timeforstuff = datetime.datetime.now() + timedelta(seconds = int(timetoadd))
      test = int(timeforstuff.timestamp())
 
      
    else:
       timeforstuff = "Game should be live now!"
       test="Game should be live now!"
    
    
    
    print("hi2")
    #Link to the tournament page
    link4tourni = page_soup.findAll("div", {"class":"event text-ellipsis"})

    for a in link4tourni[0].findAll('a', href=True):
        link4tourni = "https://www.hltv.org" + a['href']
  
    teams = team1 + " vs " + team2
    dateofgame = test2[0].text
    timeofgame = test3[0].text
    

    datep1 = dateofgame.rsplit(":")
    #change datep2 on the -1 to fit timezone, since scan is based off UK timezone, once UK is behind UTC make -2
    datep2 = int(datep1[0]) - 1
    if(datep2 < 10):
      print("help")
      datep3 = "0" + str(datep2) + ":" + datep1[1]
      

    else:
      print("hello")
      datep3 = str(datep2) + ":" + datep1[1]
      

    #Prints based on pro-match channel - will give a more chat friendly version
    if((channelDataID == 690952309827698749) or (channelDataID == 972571026066141204) or (channelDataID == 972946124161835078) or (channelDataID == 972570634196512798) or (channelDataID == 689903856095723569) or (channelDataID == 697447277647626297) or (channelDataID == 818793950965006357)):
      if(timetoadd > 0 ):
        embed=teams + " - Starts in: " + time2 + " /  <t:" + str(test) + "> - For more information use !nextcsgo in <#721391448812945480>"
      else:
        embed=teams + " should be live now - For more information use !nextcsgo in <#721391448812945480>"
    else:
      embed=discord.Embed(title="OG CSGO's next game", url="https://www.hltv.org/team/10503/og#tab-matchesBox",color=0xff8800)
      embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
      if(timetoadd > 0 ):
        embed.add_field(name=teams, value= "<t:" + str(test) + "> - this is in local timezone to you" , inline=True)
      else:
        embed.add_field(name=teams, value= "Game should be live now" , inline=True)
      embed.add_field(name="Time till game", value=time2, inline=False)
      embed.add_field(name="Notice", value="Please check HLTV by clicking the title of this embed for more information as the time might not be accurate", inline=False)
      embed.add_field(name="Links", value="[OG Liquipedia](https://liquipedia.net/counterstrike/OG)\n[OG HLTV](https://www.hltv.org/team/10503/og#tab-matchesBox)\n[Game page](" + matchlink +")\n[Tournament](" + link4tourni+")", inline=False)

    if timetoadd >0:
      return(teams, timeofgame, datep3, time2, matchlink, link4tourni, embed, timetoadd, tourniname)
    else:
      timetoadd=0
      return(teams, timeofgame, datep3, time2, matchlink, link4tourni, embed, timetoadd, tourniname)



  except Exception as e: 
    print(e)
    if((channelDataID == 690952309827698749) or (channelDataID == 972571026066141204) or (channelDataID == 972946124161835078) or (channelDataID == 972570634196512798) or (channelDataID == 689903856095723569) or (channelDataID == 697447277647626297) or (channelDataID == 818793950965006357)):
      embed= "There is currently no games planned for OG, for more information use !nextcsgo in <#721391448812945480>"
    else:
      embed=discord.Embed(title="OG CSGO's next game", url="https://www.hltv.org/team/10503/og#tab-matchesBox",color=0xff8800)
      embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
      embed.add_field(name="No games planned", value="No games planned", inline=True)
      embed.add_field(name="Links", value="[OG HLTV](https://www.hltv.org/team/10503/og#tab-matchesBox/) \n [OG CSGO Liquipedia](https://liquipedia.net/counterstrike/OG)", inline=False)
    
    return("No games planned","No games planned","No games planned","No games planned","No games planned","No games planned", embed)
    




def ValoCheck(channelDataID, pageURL):
  try:
    #Loads OG VLR page
    testv = str(pageURL)
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
    tabledata3 = page_soup.findAll("div", {"class":"rm-item-datze"})
    carrot = "carrot"
    #Gets the enemy team's name
    valoenemyteam  = page_soup.find("div", attrs={"style":"font-size: 11px; min-width: 0; font-weight: 700; width: 120px;"}).text
    random = page_soup.find("span", {"class": "rm-item-score-eta"})
    random2 = str(random)
    #This will error out of the check if the score value is null [catching if the game found has already happened / started]
    if random2 == "None":
      carrot = carrot  + 1
      print(carrot)
      

    nameOfEnemy = valoenemyteam.strip() 

    valotimeofgame = tabledata3[0].text
    datebeforesplit = valotimeofgame.strip()
    datesplit = datebeforesplit.rsplit(" ")
    actualdatebeforeclean = datesplit[0]
    testing = actualdatebeforeclean.split()
    #Creating date / time from all values from VLR
    dateOfGame = testing[0]
    timeOfGame = testing[1]
    prefixOfTime = datesplit[1]
    
    timeOfGame = timeOfGame.rsplit(":")
    hourofgame = timeOfGame[0]
    hourofgame = int(hourofgame)
    minuteofgame = timeOfGame[1]


    hourofgame = hourofgame
    
    
    
    timeOfGame = str(hourofgame) + ":" + str(minuteofgame)
    
   
    datesections = dateOfGame.rsplit("/")
    datep1 = datesections[0]
    datep2 = datesections[1]
    datep3 = datesections[2]
    dateOfGame = datep3 + "/" + datep2 + "/" + datep1
    #Splitting out the date vlaues
    yearofgame = datep1
    monthnumber = datep2
    dayofgame2 = datep3



    try:
      tags = page_soup.findAll("a", {"class":"wf-card fc-flex m-item", 'href':True })
      games=[]
      for tag in tags:
        games.append(tag['href'])
        #print(tag['href'])

      matchlink = 'https://www.vlr.gg' + games[0]
      
    except:
      pass

    try:
      testlink = matchlink
      uClient = uReq(testlink)
      page_html2 = uClient.read()
      uClient.close()
      page_soup2 = soup(page_html2, "html.parser")

      tabledata2 = page_soup2.findAll("div", {"class":"match-header-event-series"})
      gameposition = tabledata2[0].text.strip()
      gameposition = gameposition.replace("\t", "").replace("\n","")
      
      
    except:
      gameposition="No game found"
      pass

    try:
      testlink = matchlink
      uClient = uReq(testlink)
      page_html3 = uClient.read()
      uClient.close()
      page_soup3 = soup(page_html3, "html.parser")

      tabledata3 = page_soup2.findAll("div", {"style":"font-weight: 700;"})
      tourniname = tabledata3[0].text.replace("\n","").replace("\t","")
         
    except:
      
      tourniname = "No game found"
      pass
    

    UTCTime = timeOfGame.rsplit(":")
    UTCTime2 = timeOfGame.rsplit(":")
    UTCBC = int(UTCTime[0]) - 1
    
    if UTCBC > 12:
      if prefixOfTime == "am":
        prefixOfTime = "pm"
        
      else:
        prefixOfTime = "am"
    if UTCBC > 12:
      hourofvalo = str(UTCBC-12)
      UTCTime = str(UTCBC - 12) + ":" + UTCTime[1] + prefixOfTime
    else:
      hourofvalo= UTCBC
      UTCTime = str(UTCBC) + ":" + UTCTime[1] + prefixOfTime
    
    #date/time comparisions to get a countdown
    

    
    if prefixOfTime == "pm" and hourofvalo != 12:
      hourofvalo = int(hourofvalo) + 12
      
      
    minuteofgame = UTCTime2[1]
    dt_string_year = "20" + str(dt_string_year)
    a = datetime.datetime(int(yearofgame), int(monthnumber), int(dayofgame2), (int(hourofvalo)) , int(minuteofgame), 0)
    
    b = datetime.datetime(int(dt_string_year), int(dt_string_month), int(dt_string_day), int(dt_string_hour), int(dt_string_minute), int(dt_string_second))


    epochtest = datetime.datetime(int(yearofgame), int(monthnumber), int(dayofgame2), int(hourofvalo), int(minuteofgame), 0).timestamp()
    
    lenofepoch = len(str(epochtest))
    epoch = str(epochtest)[:lenofepoch - 2]
    

    
    c = a-b
    
    #Will check if the game has already begun
    if (str(pageURL) == "https://www.vlr.gg/team/2965/og"):
        valorantTeams = "OG vs " + nameOfEnemy
    else:
        valorantTeams = "OG LDN UTD vs " + nameOfEnemy
    valorantTeamTime = dateOfGame + " - " + UTCTime + " UTC"
    if (c.days < 0):
      c = "The game is meant to have begun!"
    
    

    if(channelDataID == 810939258222936094 or (channelDataID == 972571026066141204) or (channelDataID == 972946124161835078) or (channelDataID == 972570634196512798) or channelDataID == 690952309827698749 or channelDataID == 689903856095723569 or channelDataID == 926214194280419368):
      
      c= str(c)
      embed = valorantTeams + " - Starts in: " + c  + " / In your local time: <t:" + str(epoch) + "> - For more information use !nextvalo / !nextldnvalo in <#721391448812945480>"
      



      
    else:
      if (str(pageURL) == "https://www.vlr.gg/team/2965/og"):
        embed=discord.Embed(title="OG Valorant's next game", url=str(pageURL),color=0xd57280)
      else:
        embed=discord.Embed(title="OG LDN UTD Valorant's next game", url=str(pageURL),color=0xd57280)
      embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
      embed.add_field(name=valorantTeams, value= "In your local timezone - <t:" + str(epoch) + ">", inline=True)
      embed.add_field(name="Time remaining", value= c , inline = False)
      embed.add_field(name="Notice", value="Please check Liquipedia by clicking the title of this embed for more information as the time might not be accurate", inline=False)
      if (str(pageURL) == "https://www.vlr.gg/team/2965/og"):
          try:
            embed.add_field(name="Links", value="[OG VLR](str(pageURL)) / [OG Valorant Liquipedia](https://liquipedia.net/valorant/OG)\n[Matchlink](" + str(matchlink) + ")", inline=False)
          except:
            embed.add_field(name="Links", value="[OG VLR](str(pageURL)) / [OG Valorant Liquipedia](https://liquipedia.net/valorant/OG)", inline=False)
      else:
        try:
            embed.add_field(name="Links", value="[OG VLR](str(pageURL)) / [OG LDN UTD Valorant Liquipedia](https://liquipedia.net/valorant/OG_LDN_UTD\n[Matchlink](" + str(matchlink) + ")", inline=False)
        except:
            embed.add_field(name="Links", value="[OG VLR](str(pageURL)) / [OG LDN UTD Valorant Liquipedia](https://liquipedia.net/valorant/OG_LDN_UTD)", inline=False)
        
    #return(embed)
    return (embed, valorantTeams, valorantTeamTime, c, matchlink, dayofgame2, gameposition, tourniname)

  except Exception as e:
    print(e)
    return("No games planned")
   
