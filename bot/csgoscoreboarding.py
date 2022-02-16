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

#resetting the boards
def scoreboarding():
  #This is purely for creating a CSV file that is empty
  
  
  
  f = open('Scoreboard.csv', 'w+')
  
 
  f.close()
  upload_file('/csgoscoreboard.csv', 'Scoreboard.csv')
  



def scoreboardreader():
  #opens the scoreboard file + generates a file to store a sorted list for leaderboard
  download_file('/csgoscoreboard.csv', 'scoreboard2.csv')
  f = open('scoreboard2.csv', 'r') 
  f2 = open('scoreboard3.csv', 'w') 

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
  #reads in all lines from CSV - useful for generating the scoreboard
  i=1
  j=1
  for line2 in csv_reader2:
    if (i < 11):
      messagetosend= messagetosend + str(i) + " - " + line2[0] +  " - " + line2[2] + "\n"
      i = i+1
    
 
  f3.close()
    
  
  
  return(messagetosend)
    
  
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
  



  
    
def scoreboardadder(usersname, userID, scoretoadd):
  i=0
  filenames = ["accountname", "userIDs", "score"]
  
  #downloads CSV file from dropbox 
  download_file('/csgoscoreboard.csv', 'scoreboard2.csv')

  #opening files
  f=open('scoreboard2.csv', 'r')
  f2=open('scoreboard3.csv', "w")
  
  reader = csv.DictReader(f, fieldnames=filenames)
  writer = csv.writer(f2)
  
  #updating values if finding matching adding the new score to it
  for row in reader:
    if(str(row['userIDs']) == str(userID)):
      score = int(row['score']) + int(scoretoadd)
      i= 1
      values=[row['accountname'], row['userIDs'], str(score)]
      writer.writerow(values)
    else:
      values=[row['accountname'], row['userIDs'], row['score']]
      writer.writerow(values)
  
  f2.close()
  #if a new member is being added then it appends to end
  if (i == 0):
    f3 =open('scoreboard3.csv', "a")
    writer2 = csv.writer(f3)
    addingscore = [usersname, userID, scoretoadd]
    writer2.writerow(addingscore)
    f3.close()
  
 
  #reuploads the file
  upload_file('/csgoscoreboard.csv', 'scoreboard3.csv')

    
   

