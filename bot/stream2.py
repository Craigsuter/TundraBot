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
import asyncio
from itertools import cycle
import asyncio
import requests
import time
#Gets the streams from OG's Liquipedia
def DotaStreams2():
  headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
  try:
    my_url10 = "https://liquipedia.net/dota2/OG"
    print("Im here")

    my_url10 = str(my_url10)
    uClient10 = uReq(my_url10)
    page_html10 = uClient10.read()
    uClient10.close()
    page_soup10 = soup(page_html10, "html.parser")

    #Web scrapes for the first game and finds its url
    v_table = page_soup10.find("table", attrs={"class": "wikitable wikitable-striped infobox_matches_content"})
    tabledata = v_table.tbody.find_all("tr")
    #for td in tabledata[1].find_all('a', href=True):
      #print ("Found the URL:", td['href'])

    #puts that URL into the new webscraping
    tablestorage = tabledata[1].find_all('a', href=True)
    URL = tablestorage[0]['href']
    extendedURL = "https://liquipedia.net" + URL

    print("hi")
    #Parses the HTML data - Dota
    containers = page_soup10.findAll(
        "span", {"class": "team-template-team2-short"})
    containers2 = page_soup10.findAll(
        "span", {"class": "team-template-team-short"})

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

  
    print("test2")


    #Opens the new page, and checks for the stream table
    page=extendedURL
    r3 = requests.get(page,headers=headers)
    try:
      print("test2")
      page_soup2 = soup(r3.text,"html.parser")
      streamtable = page_soup2.findAll("table",{"style": "text-align:center;margin:0;margin-bottom:1em"})
      

      print("lol2")
      testingtable = streamtable[1]
      print(testingtable)
      print("lol")

      test=[]
      for tr in testingtable.findAll('tr'):
        for td in tr.findAll('td'):
          #print(td)
          test.append(td)
          
      #appends flags / links to their array to match up
      i=0
      streamlinks=[]
      flags=[]
      while (i < len(test)):
        if (i < (len(test) / 2)):
          test2 = test[i].find_all(href=True)
          flag = test2[0].get('href')
          flag2 = flag.rsplit(":")
          flags.append(flag2[(len(flag2)-1)])
        else:
          test2 = test[i].find_all(href=True)
          streamlinks.append(test2[0].get('href'))
        
        i=i+1
      
      #Creates the flags into versions that Discord can use
      flagsToSend=[]
      counter3=0
      if (len(streamlinks) == len(flags)):
        while counter3 < (len(flags)):
          if (flags[counter3] == "Indonesia"):
            flagsToSend.append(':flag_id:')
          elif (flags[counter3] == "UsGb_hd.png"):
            flagsToSend.append(':flag_gb:')
          elif (flags[counter3] == 'Russia'):
            flagsToSend.append(':flag_ru:')
          elif (flags[counter3] == 'Spain'):
            flagsToSend.append(':flag_es:')
          elif (flags[counter3] == 'France'):
            flagsToSend.append(':flag_fr:')
          elif (flags[counter3]=='Pl_hd.png'):
            flagsToSend.append(':flag_pl:')
          elif(flags[counter3]=='Cn_hd.png'):
            flagsToSend.append(':flag_cn:')
          elif(flags[counter3]=='China'):
            flagsToSend.append(':flag_cn:')
          elif(flags[counter3]=='EsMx_hd.png'):
            flagsToSend.append(':flag_es:')
          elif(flags[counter3]=='PtBr_hd.png'):
            flagsToSend.append(':flag_br:')
          elif(flags[counter3]=='Ph_hd.png'):
            flagsToSend.append(':flag_ph:')
          elif(flags[counter3]=='Germany'):
            flagsToSend.append(':flag_de:')
          elif(flags[counter3]=='Thailand'):
            flagsToSend.append(':flag_th:')
          elif(flags[counter3]=='Serbia'):
            flagsToSend.append(':flag_rs:')
          elif(flags[counter3]=='Vietnam'):
            flagsToSend.append(':flag_vn:')
          else:
            flagsToSend.append(':pirate_flag:')
          counter3 += 1

        #Creates the text that goes into the message attached the flags + streams together 
        counter4=0
        flagMessage=""
        while counter4 < (len(flagsToSend)):
          flagadd = str(flagsToSend[counter4])
          streamsAdd = str(streamlinks[counter4])
          flagMessage = flagMessage + flagadd + " <" + streamsAdd + ">\n"
          counter4 += 1  

    except:
        flagMessage="No streams were found for this game"
      
    convertedURL = "<" + extendedURL + ">"


    return(Teams1, Teams2, flagMessage, convertedURL)
    #embed=discord.Embed(title="Dota streams found!", color=0xf10909)
    #embed.add_field(name="The game found", value= Teams1 + " vs " + Teams2, inline=True)
    #embed.add_field(name="Streams available", value=flagMessage, inline=False)
    #embed.add_field(name="Where I found the streams", value= convertedURL, inline=False)
    #await message.channel.send(embed=embed)


  except:
    return("No games found","No games found","No games found","No games found")




#CSGO Stream collection starts here
def CSGOStreams():
  try:
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    OGpage = 'https://www.hltv.org/team/10503/og#tab-matchesBox'
    r2 = requests.get(OGpage, headers=headers)

    page_soup2 = soup(r2.text, "html.parser")
    dataofpage = page_soup2.findAll("td", {"class":"matchpage-button-cell"})

    #finds the link to the game page on HLTV, checking if there is a game at all
    linkinfo = []
    for a in dataofpage[0].findAll('a', href=True):

      linkinfo.append(a['href'])

    matchlink = "https://www.hltv.org" + linkinfo[0]  
    r = requests.get(matchlink , headers=headers)
    try:
      #Opens the page for the game and gets the values from it that are needed
      page_soup = soup(r.text, "html.parser")
      tabledata = page_soup.findAll("div",{"class":"external-stream"})
      test = page_soup.findAll("div", {"class":"teamName"})
      team1= test[0].text
      team2 = test[1].text
      headings=[]
      headings2=[]

      links=''

      #for note - we need to use a i / i++ loop to get all the links out of tabledata using an array catch of len-1
      lenrot = len(tabledata)
      i=0
      print(lenrot)
      while(i < (lenrot)):
        for a in tabledata[i].findAll('a', href=True):
          headings.append(a['href'])
        i = i+1
      j=0

      try:
        testingdata = page_soup.findAll("div",{"class":"stream-box-embed"})
        
        #Checks for streams 
        while(j < len(testingdata)):
        
          value = testingdata[j]
          testsplit = str(value).rsplit("=")
          
          splitlink = testsplit[5].rsplit(".")
          splitsecond = splitlink[1]
          link = testsplit[5]
          link2 = link[1:]
          if(splitsecond[0] == "y"):
            headings.insert(j, link2)
          
          j+=1

      except:
        print(":(")
        pass
      
      print(headings)
      print(len(headings))

      

      #This finds the stream table
      moredata = page_soup.findAll("div", {"class":"stream-box-embed"})

      flagdata=[]
      k=0
      #Finds all of the flag images and appends them to the flag table
      while (k < len(moredata)):
        moredata2 = moredata[k].findAll('img')

        for img in moredata2:
          if img.has_attr('src'):
            #print(img['src'])
            flagdata.append(img['src'])
        k= k+1


      flags=[]
      l=0
      #converts flag names into usable flag emotes that discord can use and appends them to the the links to the stream
      while (l<len(flagdata)):
        flag = flagdata[l].rsplit("/")
        flags.append(flag[(len(flag)-1)])
        l=l+1
      #print(flags)

      flags2=[]
      m=0
      while (m<len(flags)):
        test = flags[m].rsplit(".")
        test2 = test[0].lower()
        if (test2 == "world"):
          test2 = "gb"
        flags2.append(test2)
        m=m+1
      #print(flags2)
      j=0
      while(j<len(headings)):
        links=links + ":flag_"+flags2[j]+": " "<" + headings[j] + ">" +"\n"
        j = j+1
    except:
      links = "No streams were found"
      

    
    print(len(flags2))
    print(team1)
    print(team2)
    print(links)
    print(matchlink)
    if links=="":
      links = "No streams were found"


    embed=discord.Embed(title="CSGO Stream links", color=0xff8800)
    embed.add_field(name="The game found", value=team1 + " vs " + team2, inline=True)
    embed.add_field(name="Streams available", value = links, inline=False)
    embed.add_field(name="Game page info", value=matchlink, inline=False)

   
    
    

    return(embed, team1, team2, links, matchlink)

  except:
    embed=discord.Embed(title="No CSGO streams / games were found", color=0xff8800)
    embed.add_field(name="What you can try", value="You can try using !nextcsgo to see if there are any games coming up", inline=True)
    embed.add_field(name="Links", value="OG Liquipedia:  https://liquipedia.net/counterstrike/OG\nOG HLTV: https://www.hltv.org/team/10503/og#tab-matchesBox" , inline=False)
    
    return(embed, "No games found","No games found","No games found","No games found")







def ValoStreams():
  headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

  page='https://www.vlr.gg/team/2965/og'
  r3 = requests.get(page,headers=headers)

  page_soup2 = soup(r3.text,"html.parser")
  dataofpage =  page_soup2.findAll("a", {"class":"wf-module-item mod-flex rm-item mod-first mod-tbd"})
  

  valoenemyteam  = page_soup2.find("div", attrs={"class":"rm-item-opponent"}).text
  valoenemyteam = valoenemyteam.strip()   
  tags = page_soup2.findAll("a", {"class":"wf-module-item mod-flex rm-item mod-first mod-tbd", 'href':True })
  games=[]
  for tag in tags:
    games.append(tag['href'])
    #print(tag['href'])


  try:
    matchlink = 'https://www.vlr.gg' + games[0]
    
    r = requests.get(matchlink , headers=headers)

    try:
      page_soup = soup(r.text, "html.parser")
      test = page_soup.findAll("div", {"class":"wf-card mod-dark noselect match-streams-btn mod-embed"})


      headings=[]
      i = 0
      lenrot = len(test)
      #Gets stream links
      while(i < (lenrot)):
        for a in test[i].findAll('a', href=True):
          headings.append(a['href'])

          
        i =i+1



      #Getting flag data
      flags=[]
      j = 0
      while (j < (lenrot)):
        try:
          for element in test[j].find_all('i', class_=True):
            flags.append(element["class"])
        except:
          pass
        j = j+1


      flaglen = len(flags)

      flagdata=[]
      k=0
      while (k < (flaglen - 1)):
        try:

          data = flags[k][1]
          datasplit = data.rsplit("-")
          flagdata.append(datasplit[1])

        except:
          pass
        k=k+2

      actualflags=[]
      o=0
      while ((o < len(flagdata)) or (o == 0)):
        try:
          if (flagdata[o]== "un"):
            actualflags.append(":flag_eu:")
          else:
            actualflags.append(":flag_" + flagdata[o] + ":") 
        except:
          pass
        o = o+1


      m=0
      streams=""
      while (m < len(headings)):
        streams = str(streams) + actualflags[m] + " <" + headings[m] + ">\n"
        m=m+1
    except:
      streams = "No streams found"

    
    return(valoenemyteam,streams,matchlink)
    

    #embed=discord.Embed(title="Valorant streams coming up!", color=0xd57280)
    #embed.add_field(name="The game found", value="OG vs " + valoenemyteam, inline=True)
    #embed.add_field(name="Streams available", value=streams,inline=False)
    #embed.add_field(name="Game page info", value=matchlink, inline=False)
    #await message.channel.send(embed=embed)


  except:
    return("No games found", "No games found", "No games found")
    #embed=discord.Embed(title="No Valorant streams / games were found", color=0xd57280)

    #embed.add_field(name="What you can try", value="You can try using !nextvalo / !nextvalorant to see if there are any games coming up", inline=True)
    #embed.add_field(name="Links", value="https://www.vlr.gg/team/2965/og / https://liquipedia.net/valorant/OG", inline=False)
    #await message.channel.send(embed=embed)