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
import csv
from dropboxUploader import upload_file
from dropboxUploader import download_file
import random
import operator
from beautifultable import BeautifulTable

#resetting the boards
def scoreboarding():
  #This is purely for creating a CSV file that is empty
  
  
  
  f = open('Scoreboard.csv', 'w+')
  
 
  f.close()
  upload_file('/csgoscoreboard.csv', 'Scoreboard.csv')
  



def scoreboardreader(pagenumber):
  #opens the scoreboard file + generates a file to store a sorted list for leaderboard
  download_file('/csgoscoreboard.csv', 'scoreboard2.csv')
  f = open('scoreboard2.csv', 'r') 
  f2 = open('scoreboard3.csv', 'w') 

  table = BeautifulTable()
  table.set_style(BeautifulTable.STYLE_MARKDOWN)
  table.columns.header = ["Rank", "Name", "Score"]
  

  #reads in the current scoreboard and then sorts it
  reader = csv.reader(f, delimiter=',')
  sortedList = sorted(reader, key=lambda row: int(row[2]), reverse = True)

  #starts write for sorted list
  writer = csv.writer(f2)
 
  
  #writes row on the CSV file in sorted way
  for row in sortedList:
    writer.writerow(row)
  f2.close()
  f3 = open('scoreboard3.csv', 'r')

  messagetosend=""
  csv_reader2 = csv.reader(f3)


  try:
    if(str(pagenumber) == "none"):
      k=11
      pagenumber=1
    if(int(pagenumber) < 2):
      k=11
    else: 
      k = 11*int(pagenumber)
  except:
     k=11
  #reads in all lines from CSV - useful for generating the scoreboard
  i=1
  j=1
  for line2 in csv_reader2:
    if (i < int(k)):
      if(int(pagenumber)>1):
        if(i < (int(k)-(int(pagenumber)) + 1) and i > 10 * ((int(pagenumber)-1))):
          table.rows.append([str(i), line2[0], line2[2]])
      else:
        if(i < int(k) and i > int(k) - (11*(int(pagenumber)))):
          table.rows.append([str(i), line2[0], line2[2]])
      i = i+1
  
 
  f3.close()
  if(i==1):
    table= "There are currently no users on the table!"
  
  return(str(table))
    
  
def scoreboardsingle(userID):
  filenames = ["accountname", "userIDs", "score"]
  
  #downloads CSV file from dropbox 
  download_file('/csgoscoreboard.csv', 'scoreboard2.csv')
  f=open('scoreboard2.csv', 'r')
  reader = csv.DictReader(f, fieldnames=filenames)
  i=0
  j=0
  for row in reader:
    j=j+1
    if(str(row['userIDs']) == str(userID)):
      score = "The CSGO Prediction score for : " + str(row['accountname']) + "  -  " + str(row['score']) + ", giving them rank - " + str(j)
      i=1


      
  if(i==0):
    
    score = "The user is not currently on the leaderboard"
  return(score)
  



  
    
def scoreboardadder(usersname, userID, scoretoadd, counter):
  i=0
  filenames = ["accountname", "userIDs", "score"]

  try:
    if(counter == 1):
      table = BeautifulTable().from_csv('scoreboard2.csv', header=False)
    else:
      table = BeautifulTable().from_csv('scoreboard3.csv', header=False)
      
  except Exception as e:
    print(e)

  
  arrayofusers = list(table.columns[1])
  
  z=0
  try:
    for i, item in enumerate(arrayofusers):
      
      if item == str(userID):
        table.rows[i] = [usersname, userID, int(table.rows[i][2]) + 1]
        z=z+1

    if(z == 0):
      table.rows.append([usersname, userID, 1])
  except Exception as e:
    print(e)
      
 
  
  try:
    table.to_csv('scoreboard3.csv')
  except Exception as e:
    print(e)

    
   

