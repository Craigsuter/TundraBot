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
def dtStreams(tourniURL):
  headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
  try:
    extendedURL = tourniURL
    page=extendedURL
    r3 = requests.get(page,headers=headers)
    try:
      page_soup2 = soup(r3.text,"html.parser")
      streamtable = page_soup2.find("table",{"style": "text-align:center;margin:0;margin-bottom:1em"})
      table_body = streamtable.find('tbody')
      


      test=[]
      for tr in streamtable.findAll('tr'):
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
          elif(flags[counter3] == "Philippines"):
            flagsToSend.append(':flag_ph:')
          elif(flags[counter3]=="DeAt_hd.png"):
            flagsToSend.append(':flag_de:')
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


    return(flagMessage, convertedURL)
    #embed=discord.Embed(title="Dota streams found!", color=0xf10909)
    #embed.add_field(name="The game found", value= Teams1 + " vs " + Teams2, inline=True)
    #embed.add_field(name="Streams available", value=flagMessage, inline=False)
    #embed.add_field(name="Where I found the streams", value= convertedURL, inline=False)
    #await message.channel.send(embed=embed)


  except:
    return("No games found","No games found","No games found","No games found")



