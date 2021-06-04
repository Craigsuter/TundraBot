import discord
import os
#import pynacl
#import dnspython
import server
from discord.ext import commands
#imports
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import discord
import os
from cleardota import cleardota
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from dotenv import load_dotenv
load_dotenv()
import datetime
from time import strptime
import asyncio
import time
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from translation import translations
from gamecheckers import DotaCheck
from gamecheckers import CSGOCheck
from gamecheckers import ValoCheck
from streamcollection import DotaStreams
from streamcollection import CSGOStreams
from streamcollection import ValoStreams
from lastgames import LastDota
from lastgames import LastCSGO
from tournamentcheckers import DotaCheckTourni 
from dropboxUploader import upload_file
from dropboxUploader import download_file

#sets up command prefix
client = commands.Bot(command_prefix = '!')



#This is the OG URL for Dota 2 / CSGO / Valo
my_url = 'https://liquipedia.net/dota2/OG'
my_url2 = 'https://liquipedia.net/counterstrike/OG'
my_url3 = 'https://liquipedia.net/valorant/OG'
global my_url5
global my_url6
global my_url7
global dotadailypost
global csgodailypost
global valodailypost

dotadailypost = True
csgodailypost = True
valodailypost = True

#Posts once bot has started up
startup = datetime.datetime.now()

print("Bot started up at: ", startup)



#Logs the discord bot on
@client.event
async def on_ready():
    print("We have logged in as {0.user}.format(client)")
    #Sets presence
    await client.change_presence(activity=discord.Game(name="with ducks (use !goosehelp)"))

    #Starts schedule
    scheduler = AsyncIOScheduler()
    #Post on the day of a game
    scheduler.add_job(testingspam,CronTrigger(hour="7"))
    #Opens the file checking the new member support to delete the old bot message
    scheduler.add_job(openingfile, CronTrigger(minute="5, 10, 15,20, 25, 30, 35, 40, 45, 50,55, 0"))
    scheduler.add_job(cleanreminders, CronTrigger(minute= "0, 30"))
    scheduler.start()

    data = download_file('/dropreminders.txt', 'reminders.txt')
    a_file = open("reminders.txt", "r")
    list_of_lines = a_file.readlines()
    i=0
  
    reminders=[]
    while (i < len(list_of_lines)):
      
      base_reminder = list_of_lines[i]
      splitUpValues = base_reminder.rsplit(", ")

      checkIfSent = splitUpValues[4]
      checkIfSent= checkIfSent[0:2]
      
      if(checkIfSent == "no"):
        reminders.append(base_reminder + ", " + str(i))


      i=i+1

    i=0
   
    tasks=[]

    while i < len(reminders):
      tasks.append(asyncio.create_task(reminder(reminders[i])))
      
      i = i +1
    print("There were: " + str(i) + " reminders started up")
    await asyncio.gather(*tasks)



#Starts the bot up to check for messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.bot:
      return
    
    guild=message.guild
    
    
#All commands that are blocked to none admins are found in here
    global currenttime
    global currentH
    global currentM
    global currentd
    global dotadailypost
    global csgodailypost
    global valodailypost
    currenttime =  datetime.datetime.now()
    #day
    currentd = currenttime.strftime("%d")
    #hour [UK time - 1]
    currentH = currenttime.strftime("%H")
    #Minute
    currentM = currenttime.strftime("%M")
    #Month
    currentmonth = currenttime.strftime("%m")
    #year
    currentyear = currenttime.strftime("%y")
    #second
    currentsecond = currenttime.strftime("%S")
    

    currentH = int(currentH)
    currentM = int(currentM)
    author=message.author
    areadmin = author.guild_permissions.administrator



    global my_url5
    global my_url6
    global my_url7

    #Gets segments of every message - full message found in 'fullMEssage to avoid over use of Discord API'
    fullMessage = message.content
    nexttrans= fullMessage
    sectionsofmessage = fullMessage.rsplit(" ")
    introtomessage = sectionsofmessage[0]
    first_char = introtomessage[0]
    channelDataID = message.channel.id

    #Getting the 2nd part of a message
    try:
      secondPartOfMessage= sectionsofmessage[1]
    except:
      secondPartOfMessage = "none"
      pass

    messagetolower = introtomessage
    messagereceived = messagetolower.lower()
    mention = f'<@!{client.user.id}>'
    #Checks for a ping of the bot
    if ((mention in message.content) and (messagereceived[0] != '!')):
      await message.channel.send("Im up! Im up! Are you okay... cool... co... <:OGmonkaThink:821509791523930162> ")

    #Verifies that message is command usage
    if (first_char=="!"):

      #None mod commands
      if (author.guild_permissions.administrator == False):
          
          #Commands that are Moderator only
          blockedcommands=["!deletedotabo1", "!deletedota2bo1", "!deletecsgoBo1", "!deletevalobo1", "!deletevalorantbo1", "!deletedotabo3", "!deletedota2bo3", "!deletecsgobo3", "!deletevalobo3", "!deletevalorantbo3", "!deletedotabo5", "!deletedota2bo5", "!deletecsgobo5", "!deletecsgobo5", "!deletevalobo5", "!deletevalorantbo5", "!dotabo1", "!dotabo3", "!dotabo5", "!csgobo1", "!csgobo3", "!csgobo5", "!valobo1", "!valobo3", "!valobo5", "!changedt", "!resetdt", "!verifydurl", "!changecst", "!changevt", "!resetvt", "!verifyvurl", "!resetcst", "!verifycsurl", "!copyover", "!gardenerhelp", "!cleardota"]

          if (messagereceived in blockedcommands):
            await message.channel.send("No role access")
          
          #Used for checking the next game in Dota Tourni
          if (messagereceived=="!nextdt"):   
            embed = DotaCheckTourni(channelDataID)
            embed=embed[0]
            if((channelDataID == 689903856095723569) or (channelDataID == 690952309827698749)):
              userID = message.author.id
              userID = str(userID)
              await message.channel.send("<@" + userID + "> " + embed)
            else:
              await message.channel.send(embed=embed)
          
          #Get CSGO streams list for next CS game
          if (messagereceived =="!csgostreams"):
            embed = CSGOStreams()
            embed = embed[0]
            await message.channel.send(embed=embed)

          #Checks if user tries using !nextmatch incorrectly
          if ((messagereceived == "!nextgame") or (messagereceived == "!game") or (messagereceived == "!nextmatch") or (messagereceived == "!next")):
            embed=discord.Embed(title="OGoose bot help",color=0xd57280)
            embed.set_thumbnail(url="https://i.imgur.com/YJfbFth.png")
            embed.add_field(name="Asking for game information", value="To get game information do be sure to use !nextdota / !nextcsgo / !nextvalo, you can get additional help using !goosehelp", inline=True)
            await message.channel.send(embed=embed)

          
          if((messagereceived == "!nextvalo") or (messagereceived == "!nextvalorant")):
            Valogame = ValoCheck(channelDataID)
            valorantTeams = Valogame[0]
            valorantTeamTime = Valogame[1]
            timeremaining = Valogame[2]

            if(valorantTeams == "No games planned"):
              embed=discord.Embed(title="OG Valorant's next game", url="https://www.vlr.gg/team/2965/og",color=0xd57280)
              embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
              embed.add_field(name="No games planned", value="No games planned", inline=True)
              embed.add_field(name="Links", value="https://www.vlr.gg/team/2965/og / https://liquipedia.net/valorant/OG", inline=False)
              await message.channel.send(embed=embed)
            else:
              embed=discord.Embed(title="OG Valorant's next game", url="https://www.vlr.gg/team/2965/og",color=0xd57280)
              embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
              embed.add_field(name=valorantTeams, value=valorantTeamTime, inline=True)
              embed.add_field(name="Time remaining", value= timeremaining, inline = False)
              embed.add_field(name="Notice", value="Please check Liquipedia by clicking the title of this embed for more information as the time might not be accurate", inline=False)
              embed.add_field(name="Links", value="https://www.vlr.gg/team/2965/og / https://liquipedia.net/valorant/OG", inline=False)
              await message.channel.send(embed=embed)


          if ((messagereceived =="!lastdota")):
            lastinfo = LastDota()
            Dateandtime1 = lastinfo[0]
            Dateandtime2 = lastinfo[1]
            Dateandtime3 = lastinfo[2]
            LastGameScore1 = lastinfo[3]
            LastGameEnemy1 = lastinfo[6]
            LastGameScore2 = lastinfo[4]
            LastGameEnemy2 = lastinfo[7]
            LastGameScore3 = lastinfo[5]
            LastGameEnemy3 = lastinfo[8]
            
            embed=discord.Embed(title="The last game OG Dota played",url='https://liquipedia.net/dota2/OG/Played_Matches', color=0xf10909)
            embed.add_field(name="Date / tournament",value=(Dateandtime1 + "\n" + Dateandtime2 + "\n" + Dateandtime3), inline=True)
            embed.add_field(name="Score", value=(("OG " + LastGameScore1 + " " + LastGameEnemy1) +"\n"+("OG " + LastGameScore2 + " " + LastGameEnemy2) + "\n" +("OG " + LastGameScore3 + " " + LastGameEnemy3)), inline=True)
            await message.channel.send(embed=embed)

          if ((messagereceived =="!lastcsgo")):
            lastinfo = LastCSGO()
            Dateandtime1 = lastinfo[0]
            Dateandtime2 = lastinfo[1]
            Dateandtime3 = lastinfo[2]
            LastGameScore1 = lastinfo[3]
            LastGameEnemy1 = lastinfo[6]
            LastGameScore2 = lastinfo[4]
            LastGameEnemy2 = lastinfo[7]
            LastGameScore3 = lastinfo[5]
            LastGameEnemy3 = lastinfo[8]


            embed=discord.Embed(title="The last OG CSGO games played",url='https://liquipedia.net/counterstrike/OG/Matches', color=0xff8800)
            embed.add_field(name="Date / tournament",value=(Dateandtime1 + "\n" + Dateandtime2 + "\n" + Dateandtime3), inline=True)
            embed.add_field(name="Score", value=(("OG " + LastGameScore1 + " " + LastGameEnemy1) +"\n"+("OG " + LastGameScore2 + " " + LastGameEnemy2) + "\n" +("OG " + LastGameScore3 + " " + LastGameEnemy3)), inline=True)
            await message.channel.send(embed=embed)

              

          if((messagereceived=="!lastvalo") or (messagereceived == "!lastvalorant")) :
            testurl = "https://liquipedia.net/valorant/OG/Matches"
            uClient = uReq(testurl)
            page_html = uClient.read()
            uClient.close()
            page_soup = soup(page_html,"html.parser")

            tabledata = page_soup.find("div", attrs ={"class": "table-responsive recent-matches"})
            #print(tabledata)
            tabledata2 = tabledata.tbody.find_all("tr")
            tabledata3 = tabledata2[1].find_all("td")
            try:
              LastGameOG1 = "OG "
              LastgameDate1 = tabledata3[0].text
              LastGameTime1 = tabledata3[1].text
              LastGameTier1 = tabledata3[2].text
              LastGameTourni1 = tabledata3[3].text
              LastGameScore1 = tabledata3[5].text
              LastGameEnemy1 = tabledata3[6].text             
              Dateandtime1 = LastgameDate1 +  " - " + LastGameTourni1
             
              
              
            except:
              print("kek")
              
            
            
            try:
              tabledata4 = tabledata2[2].find_all("td")
              LastGameOG1 ="OG "
              LastgameDate2 = tabledata4[0].text
              LastGameTime2 = tabledata4[1].text
              LastGameTier2 = tabledata4[2].text
              LastGameTourni2 = tabledata4[3].text
              LastGameScore2 = tabledata4[5].text
              LastGameEnemy2 = tabledata4[6].text
              Dateandtime2 = LastgameDate2 +  " - " + LastGameTourni2
            except:
              print("kek2")
              
            try:
              tabledata5 = tabledata2[3].find_all("td")
              LastGameOG1 = "OG "
              LastgameDate3 = tabledata5[0].text
              LastGameTime3 = tabledata5[1].text
              LastGameTier3 = tabledata5[2].text
              LastGameTourni3 = tabledata5[3].text
              LastGameScore3 = tabledata5[5].text
              LastGameEnemy3 = tabledata5[6].text
              Dateandtime3 = LastgameDate3 +  " - " + LastGameTourni3
            except:
              LastGameOG3 = " "
              LastgameDate3 = " "
              LastGameTime3 = " "
              LastGameTier3 =" "
              LastGameType3 = " "
              LastGameTourni3 = " "
              LastGameScore3 =" "
              LastGameEnemy3 =" "
              Dateandtime3 = " "
              print("kek3")

            embed=discord.Embed(title="The last OG Valo games played",url='https://liquipedia.net/dota2/OG/Played_Matches', color=0xd57280)
            embed.add_field(name="Date / tournament",value=(Dateandtime1 + "\n" + Dateandtime2 + "\n" + Dateandtime3), inline=True)
            embed.add_field(name="Score", value=(("OG " + LastGameScore1 + " " + LastGameEnemy1) +"\n"+("OG " + LastGameScore2 + " " + LastGameEnemy2) + "\n" +(LastGameOG3 + LastGameScore3 + " " + LastGameEnemy3)), inline=True)
            await message.channel.send(embed=embed)


          if ((messagereceived =="!nextdota")  or (messagereceived =="!nextdota2")):
              embed = DotaCheck(channelDataID)
              embed=embed[0]
              if((channelDataID == 689903856095723569) or (channelDataID == 690952309827698749)):
                userID = message.author.id
                userID = str(userID)
                await message.channel.send("<@" + userID + "> " + embed)
              else:
                await message.channel.send(embed=embed)


          if ((messagereceived =="!nextcsgo")or (messagereceived=="!nextcs")):
            CSGOGame = CSGOCheck(channelDataID)
            embed = CSGOGame[6]
            if((channelDataID == 690952309827698749) or (channelDataID == 689903856095723569)):
              userID = message.author.id
              userID = str(userID)
              await message.channel.send("<@" + userID + "> " + embed)
            else:
              await message.channel.send(embed=embed)


          if (messagereceived=="!valostreams" or messagereceived=="!valorantstreams"):
            streaminfo = ValoStreams()
            valoenemyteam= streaminfo[0]
            streams = streaminfo[1]
            matchlink= streaminfo[2]

            if(matchlink == "No games found"):
              embed=discord.Embed(title="No Valorant streams / games were found", color=0xd57280)
              embed.add_field(name="What you can try", value="You can try using !nextvalo / !nextvalorant to see if there are any games coming up", inline=True)
              embed.add_field(name="Links", value="https://www.vlr.gg/team/2965/og / https://liquipedia.net/valorant/OG", inline=False)
              await message.channel.send(embed=embed)

            else:
              embed=discord.Embed(title="Valorant streams coming up!", color=0xd57280)
              embed.add_field(name="The game found", value= "OG vs " + valoenemyteam, inline=True)
              embed.add_field(name="Streams for copying", value ="```" + streams + "```", inline=False)
              embed.add_field(name="Streams with flags", value=streams,inline=False)
              embed.add_field(name="Game page info", value=matchlink, inline=False)
              await message.channel.send(embed=embed)

            
          if(messagereceived=="!dotastreams"):
            streaminfo = DotaStreams()
            Teams1 = streaminfo[0]
            Teams2 = streaminfo[1]
            flagMessage= streaminfo[2]
            convertedURL = streaminfo[3]

            if(Teams1 == "No games found"):
              embed=discord.Embed(title="No Dota streams / games were found", color=0xf10909)
              embed.add_field(name="What you can try", value="You can try using !nextdota / !nextdota2 to see if there are any games coming up", inline=True)
              embed.add_field(name="Links", value="https://liquipedia.net/dota2/OG", inline=False)
              await message.channel.send(embed=embed)

            else:
              embed=discord.Embed(title="Dota streams found!", color=0xf10909)
              embed.add_field(name="The game found", value= Teams1 + " vs " + Teams2, inline=True)
              embed.add_field(name="Streams available", value=flagMessage, inline=False)
              embed.add_field(name="Where I found the streams", value= convertedURL, inline=False)
              await message.channel.send(embed=embed)




          if (messagereceived =="!goosehelp"):
            willshelp1 = "!nextdota - This will tell you the next OG Dota 2 game coming up \n!nextcsgo - This will tell you the next OG CSGO game coming up \n!nextvalo - This will tell you the next OG Valorant  game coming up \n \n"

            willshelp2 = "!dotastreams - This will tell you the streams available for the next / current series of dota happening!\n!csgostreams - This will tell you the next / current CSGO games streams\n!valostreams - This will tell you the streams for the current / next Valorant series"
            willshelp3= "!nextdt - This will tell you the next game coming up in the currently tracked tournament"
 

            embed=discord.Embed(title="The commands I work with", color=0xff8800)
            embed.add_field(name="The next OG games", value=willshelp1, inline=True)
            embed.add_field(name="The streams for games", value=willshelp2, inline=False)
            embed.add_field(name="Next game in tournament", value =willshelp3, inline=False)
            await message.channel.send(embed=embed) 

          return













      #All gardener commands  
      else:

          if(messagereceived=="!addtodo"):
            try:
              userRequesting = message.author.id
              todotoadd=""
              breaking="throw error"
              i=1
              if (len(sectionsofmessage) == 1):
                breaking + 1
              while(i < len(sectionsofmessage)):
                todotoadd = todotoadd + sectionsofmessage[i] + " "
                i = i+1
              data = download_file('/droptodo.txt', 'ToDo.txt')
              f=open("ToDo.txt", "a")
              f.write(str(todotoadd) + " - Requested by: " + str(userRequesting) + "\n")
              f.close()
              upload_file('/droptodo.txt', 'ToDo.txt' )

              embed=discord.Embed(title="You have added the following suggestion",color=0x55a7f7)
              embed.add_field(name="Suggestion", value = todotoadd, inline= True)
              await message.channel.send(embed=embed)
            except:
              embed=discord.Embed(title="Adding a suggestion",color=0x55a7f7)
              embed.add_field(name="Adding a suggestion", value = "You can add a suggestion using: \n!addtodo *suggestion following*", inline= True)
              await message.channel.send(embed=embed)
              pass

          if(messagereceived=="!todolist"):
            data = download_file('/droptodo.txt', 'ToDo.txt')
            a_file = open("ToDo.txt", "r")
            list_of_lines = a_file.readlines()
            i=0
            savedToDo=""
            while(i<len(list_of_lines)):
              currentline = list_of_lines[i]
              splitUpLine = currentline.rsplit(" ")
              userofreminder = splitUpLine[len(splitUpLine) - 1]
              userofreminder = userofreminder.strip()
              
              j=0
              lineoftext=""
              while (j < int(len(splitUpLine) - 1)):
                lineoftext = lineoftext + " " + splitUpLine[j]
                j=j+1
              
              savedToDo = savedToDo + lineoftext + " <@" + userofreminder + ">\n"


              i=i+1
            embed=discord.Embed(title="Current list of things to work on",color=0x55a7f7)
            embed.add_field(name="List of projects", value = savedToDo, inline=True)
            embed.add_field(name="Adding a suggestion", value = "You can add a suggestion using: \n!addtodo *suggestion following*", inline= False)
            await message.channel.send(embed=embed)

          if(messagereceived=="!myreminders"):
            data = download_file('/dropreminders.txt', 'reminders.txt')
            a_file = open("reminders.txt", "r")
            list_of_lines = a_file.readlines()
            i=0
            userID = message.author.id
            userID = str(userID)

            reminders=[]
            timeofreminders=[]
            dayofreminding =[]
            monthofreminding=[]
            yearofreminding=[]
            timetosendreminder=[]
            channeltosend =[]
            while(i<len(list_of_lines)):
              base_reminder = list_of_lines[i]
              splitUpValues = base_reminder.rsplit(", ")
              checkIfSent = splitUpValues[4]
              dateOfSend = splitUpValues[3]
              textofreminder = splitUpValues[2]
              channelToSend = splitUpValues[1]
              userToSend = splitUpValues[0]
              checkifSent = checkIfSent[0:2]
              

              dateofremindbsplit = dateOfSend.rsplit(" ")
              datesplitup = dateofremindbsplit[0].rsplit("-")
              dayofreminder = datesplitup[2]
              monthofsend = datesplitup[1]
              yearofsend = datesplitup[0]
              timeofsend = dateofremindbsplit[1]

              if(checkifSent=="no"):
                if(userID == str(userToSend)):
                  reminders.append(textofreminder)
                  timeofreminders.append(dateOfSend)
                  dayofreminding.append(dayofreminder)
                  monthofreminding.append(monthofsend)
                  yearofreminding.append(yearofsend)
                  timetosendreminder.append(timeofsend)
                  channeltosend.append(channelToSend)
                

              i=i+1
            j=0
            textToSend = ""
            if (len(reminders) > 0):
              while(j < len(reminders)):
                textToSend = textToSend + reminders[j] + " - " + str(dayofreminding[j]) + "/" + str(monthofreminding[j]) + "/" + str(yearofreminding[j]) + " at " + str(timetosendreminder[j]) +" UTC - <#" + str(channeltosend[j]) + ">\n"
                #textToSend = textToSend + reminders[j] + " - " + timeofreminders[j] + "\n"
                j = j+1
            
              embed=discord.Embed(title="Your currently saved reminders",color=0x55a7f7)
              embed.add_field(name="Reminders", value = textToSend, inline= True)
              
              embed.add_field(name="Note", value= "If you see #deleted-channel, you are unable to access the channel tagged / or it is deleted", inline=False)

              await message.channel.send(embed=embed)
              
            else:
              await message.channel.send("You currently have no saved reminders")


          


          if(messagereceived=="!reminder"):
            data = download_file('/dropreminders.txt', 'reminders.txt')
            
            #value checkers
            reminder = secondPartOfMessage 
            timevalue = reminder[-1]
            remindertosave=""
            #Saves user info for pinging
            userID = message.author.id
            userID = str(userID)
            #Create embed
            embed=discord.Embed(title="Reminder command initiated",color=0x55a7f7)
            embed2= discord.Embed(title="Your reminder... has arrived!",color=0x55a7f7)
            currentyear = "20" + str(currentyear)
            currentyear = int(currentyear)
            date_and_time = datetime.datetime(int(currentyear), int(currentmonth), int(currentd), int(currentH), int(currentM), int(currentsecond))
            

            
            i=2
            #Gets the reminder to save
            while(i < len(sectionsofmessage)):
              remindertosave = remindertosave + sectionsofmessage[i] + " "
              i = i+1
           
            try:
              timevaluechecker = ['d', 'h', 'm', 's']

              #Tells user how to set a reminder if tiem value not given
              if reminder == "none" or (timevalue not in timevaluechecker) :
                embed.add_field(name="Command used no time set", value="To set the time for this command, please set it using 'days' / 'hours' / 'minutes' / 'seconds'\n\nTo format this you use d / h / m / s, at the end of the time wanted\n\nExample - !reminder 10h This is a reminder\nThis will remind you in 10 hours!")

              #Sets reminder if time value is set
              if( reminder != "none" and (timevalue in timevaluechecker)):

                if (timevalue == "s"):
                  timetillremidningyou = reminder[:-1]
                  
                  embed.add_field(name="Reminder set, reminding in - " + timetillremidningyou + "s", value=remindertosave, inline=True)
                  embed2.add_field(name="Your reminder!", value=remindertosave,inline=True)
                  #calculate time for reminder
                  time_change = datetime.timedelta(seconds=int(timetillremidningyou))
                  new_time = date_and_time + time_change
                
                if(timevalue == "m"):
                  timetillremidningyou = reminder[:-1]
                  embed.add_field(name="Reminder set, reminding in - " + timetillremidningyou + "m", value=remindertosave, inline=True)
                  embed2.add_field(name=
                  "Your reminder!", value=remindertosave,inline=True)
                  timetillremidningyou = int(timetillremidningyou) * 60
                  #calculate time for reminder
                  time_change = datetime.timedelta(seconds=int(timetillremidningyou))
                  new_time = date_and_time + time_change

                if(timevalue =="h"):
                  timetillremidningyou = reminder[:-1]
                  embed.add_field(name="Reminder set, reminding in - " + timetillremidningyou + "h", value=remindertosave, inline=True)
                  embed2.add_field(name="Your reminder!", value=remindertosave,inline=True)
                  timetillremidningyou = int(timetillremidningyou) * 60 * 60
                  #calculate time for reminder
                  time_change = datetime.timedelta(seconds=int(timetillremidningyou))
                  new_time = date_and_time + time_change
                
                if(timevalue=="d"):
                  timetillremidningyou = reminder[:-1]
                  

                  embed.add_field(name="Reminder set, reminding in - " + timetillremidningyou + "d", value=remindertosave, inline=True)
                  embed2.add_field(name="Your reminder!", value=remindertosave,inline=True)
                  
                  timetillremidningyou = int(timetillremidningyou) * 60 * 60 * 24
                  #calculate time for reminder
                 
                  time_change = datetime.timedelta(seconds=int(timetillremidningyou))
                  
                  new_time = date_and_time + time_change
                  
                  

              #Adding reminder to the text file
              userID = message.author.id
              userID = str(userID)
              channelToSend = str(channelDataID)
              textToSend = str(remindertosave)

             
              f=open("reminders.txt", "a")
              f.write(userID + ", " + channelToSend + ", " + textToSend + ", " + str(new_time) + ", not\n")
              f.close()
              upload_file('/dropreminders.txt', 'reminders.txt' )
              
              LineOfReminder = sum(1 for line in open('reminders.txt'))
              
              await message.channel.send(embed=embed)
            
            #catches time error 
            except:
              embed2=discord.Embed(title="Reminder command initiated",color=0x55a7f7)
              embed2.add_field(name="Command used no time set", value="To set the time for this command, please set it using 'days' / 'hours' / 'minutes' / 'seconds'\n\nTo format this you use d / h / m / s, at the end of the time wanted\n\nExample - !reminder 10h This is a reminder\nThis will remind you in 10 hours!")
              await message.channel.send(embed=embed2)

            try:
              timetosleep = int(timetillremidningyou)
              await asyncio.sleep(timetosleep)
              
              #Will update the file to make sure reminders get saved
              data = download_file('/dropreminders.txt', 'reminders.txt')
              a_file = open("reminders.txt", "r")
              list_of_lines = a_file.readlines()
              list_of_lines[int(LineOfReminder) - 1] = (userID + ", " + channelToSend + ", " + textToSend + ", " + str(new_time) + ", sent\n")

              a_file = open("reminders.txt", "w")
              a_file.writelines(list_of_lines)
              a_file.close()
              upload_file('/dropreminders.txt', 'reminders.txt' )

              await message.channel.send("<@" + userID + ">")
              await message.channel.send(embed=embed2)
            except:
              pass
            
            
              
          
          if(messagereceived =="!resetdt"):
            data = download_file('/dropdotatournament.txt', 'dotatournament.txt')
            f=open("dotatournament.txt", "w")
            f.write("none")
            f.close()
            upload_file('/dropdotatournament.txt', 'dotatournament.txt')
            await message.channel.send("The tournament currently tracked has been removed")
          
          if(messagereceived=="!verifydturl"):
            data = download_file('/dropdotatournament.txt', 'dotatournament.txt')
            f=open("dotatournament.txt", "r")
            link = f.read()
            await message.channel.send("The link currently stored is - <" + link + ">")

          if(messagereceived=="!changedt"):
            data = download_file('/dropdotatournament.txt', 'dotatournament.txt')
            newlink = secondPartOfMessage
            f=open("dotatournament.txt", "w")
            f.write(newlink)
            f.close()
            upload_file('/dropdotatournament.txt', 'dotatournament.txt')
            await message.channel.send("The tournament tracked has been updated to the link you have sent - <" + newlink + ">\n\nIf there is an error in your link, you are able to use !verifydturl to check the link or try changing again!")
        
          

          if (messagereceived=="!nextdt"):   
            embed = DotaCheckTourni(channelDataID)
            embed=embed[0]
            if((channelDataID == 689903856095723569) or (channelDataID == 690952309827698749)):
              userID = message.author.id
              userID = str(userID)
              await message.channel.send("<@" + userID + "> " + embed)
            else:
              await message.channel.send(embed=embed)

          #copies 100 messages from 1 channel to another

          if (messagereceived=="!copyover"):
            try:
              #channel to copy from
              channeltosendtoo = int(secondPartOfMessage)
              c= client.get_channel(channeltosendtoo)
              messages = await c.history(limit=100).flatten()
              messages.reverse()
              
              
              for message in messages:
                
                user = message.author.name
                messageToSend = user + ": "+ message.content
                #channel to copy to
                c2= client.get_channel(channelDataID)
                #print(messageToSend)
                await c2.send(messageToSend)
            except:
              ErrorChannel = client.get_channel(channelDataID)
              embed=discord.Embed(title="Using the copyover command / error hit")
              embed.add_field(name="Help", value="An error was hit while using the command!\nDo try using it again and find the example below of usage - it will copy over the last 100 messages in the channel chosen to the channel the command is used in\n\n!copyover *channelid*\n\nE.G: !copyover 847832196294115349", inline=True)
              await ErrorChannel.send(embed=embed)
              



          if (messagereceived == "!server_badge"):
            icon_url = message.guild.icon_url
            await message.channel.send(icon_url)

          

          if (messagereceived=="!cleardota"):
            embed1 = discord.Embed(title="Clearing of cache has begun")
            embed1.add_field(name="This can take roughly 20s", value="This will update once complete", inline=True)
            message = await message.channel.send(embed=embed1)
            try:
              cleardota()
              embed=discord.Embed(title="Clearing the dota page cache complete")
              embed.add_field(name="Clearing of liquipedia complete!", value="This usually takes 5 minutes to take effect!", inline= True)
              embed.add_field(name="Where to check", value="https://liquipedia.net/dota2/OG", inline=False)
              await message.edit(embed=embed)
            except:
              embed=discord.Embed(title="Clearing hit an error")
              embed.add_field(name="Help", value="You're able to visit - https://liquipedia.net/dota2/OG or you're able to try using the command again", inline=True)
              await message.edit(embed=embed)
              pass
            



          if ((messagereceived == "!nextgame") or (messagereceived == "!game") or (messagereceived == "!nextmatch") or (messagereceived == "!next")):
            embed=discord.Embed(title="OGoose bot help",color=0xd57280)
            embed.set_thumbnail(url="https://i.imgur.com/YJfbFth.png")
            embed.add_field(name="Asking for game information", value="To get game information do be sure to use !nextdota / !nextcsgo / !nextvalo, you can get additional help using !goosehelp", inline=True)
            await message.channel.send(embed=embed)


          if(messagereceived=="!lastdota"):
            lastinfo = LastDota()
            Dateandtime1 = lastinfo[0]
            Dateandtime2 = lastinfo[1]
            Dateandtime3 = lastinfo[2]
            LastGameScore1 = lastinfo[3]
            LastGameEnemy1 = lastinfo[6]
            LastGameScore2 = lastinfo[4]
            LastGameEnemy2 = lastinfo[7]
            LastGameScore3 = lastinfo[5]
            LastGameEnemy3 = lastinfo[8]
            
            embed=discord.Embed(title="The last game OG Dota played",url='https://liquipedia.net/dota2/OG/Played_Matches', color=0xf10909)
            embed.add_field(name="Date / tournament",value=(Dateandtime1 + "\n" + Dateandtime2 + "\n" + Dateandtime3), inline=True)
            embed.add_field(name="Score", value=(("OG " + LastGameScore1 + " " + LastGameEnemy1) +"\n"+("OG " + LastGameScore2 + " " + LastGameEnemy2) + "\n" +("OG " + LastGameScore3 + " " + LastGameEnemy3)), inline=True)
            await message.channel.send(embed=embed)

          if ((messagereceived =="!lastcsgo")):
            lastinfo = LastCSGO()
            Dateandtime1 = lastinfo[0]
            Dateandtime2 = lastinfo[1]
            Dateandtime3 = lastinfo[2]
            LastGameScore1 = lastinfo[3]
            LastGameEnemy1 = lastinfo[6]
            LastGameScore2 = lastinfo[4]
            LastGameEnemy2 = lastinfo[7]
            LastGameScore3 = lastinfo[5]
            LastGameEnemy3 = lastinfo[8]


            embed=discord.Embed(title="The last OG CSGO games played",url='https://liquipedia.net/counterstrike/OG/Matches', color=0xff8800)
            embed.add_field(name="Date / tournament",value=(Dateandtime1 + "\n" + Dateandtime2 + "\n" + Dateandtime3), inline=True)
            embed.add_field(name="Score", value=(("OG " + LastGameScore1 + " " + LastGameEnemy1) +"\n"+("OG " + LastGameScore2 + " " + LastGameEnemy2) + "\n" +("OG " + LastGameScore3 + " " + LastGameEnemy3)), inline=True)
            await message.channel.send(embed=embed)

          


          if((messagereceived=="!lastvalo") or (messagereceived == "!lastvalorant")) :
            testurl = "https://liquipedia.net/valorant/OG/Matches"
            uClient = uReq(testurl)
            page_html = uClient.read()
            uClient.close()
            page_soup = soup(page_html,"html.parser")

            tabledata = page_soup.find("div", attrs ={"class": "table-responsive recent-matches"})
            #print(tabledata)
            tabledata2 = tabledata.tbody.find_all("tr")
            tabledata3 = tabledata2[1].find_all("td")
            try:
              LastGameOG1 = "OG "
              LastgameDate1 = tabledata3[0].text
              LastGameTime1 = tabledata3[1].text
              LastGameTier1 = tabledata3[2].text
              LastGameTourni1 = tabledata3[3].text
              LastGameScore1 = tabledata3[5].text
              LastGameEnemy1 = tabledata3[6].text             
              Dateandtime1 = LastgameDate1 +  " - " + LastGameTourni1
             
              
              
            except:
              print("kek")
              
            
            
            try:
              tabledata4 = tabledata2[2].find_all("td")
              LastGameOG1 ="OG "
              LastgameDate2 = tabledata4[0].text
              LastGameTime2 = tabledata4[1].text
              LastGameTier2 = tabledata4[2].text
              LastGameTourni2 = tabledata4[3].text
              LastGameScore2 = tabledata4[5].text
              LastGameEnemy2 = tabledata4[6].text
              Dateandtime2 = LastgameDate2 +  " - " + LastGameTourni2
            except:
              print("kek2")
              
            try:
              tabledata5 = tabledata2[3].find_all("td")
              LastGameOG1 = "OG "
              LastgameDate3 = tabledata5[0].text
              LastGameTime3 = tabledata5[1].text
              LastGameTier3 = tabledata5[2].text
              LastGameTourni3 = tabledata5[3].text
              LastGameScore3 = tabledata5[5].text
              LastGameEnemy3 = tabledata5[6].text
              Dateandtime3 = LastgameDate3 +  " - " + LastGameTourni3
            except:
              LastGameOG3 = " "
              LastgameDate3 = " "
              LastGameTime3 = " "
              LastGameTier3 =" "
              LastGameType3 = " "
              LastGameTourni3 = " "
              LastGameScore3 =" "
              LastGameEnemy3 =" "
              Dateandtime3 = " "
              print("kek3")

            embed=discord.Embed(title="The last OG Valo games played",url='https://liquipedia.net/dota2/OG/Played_Matches', color=0xd57280)
            embed.add_field(name="Date / tournament",value=(Dateandtime1 + "\n" + Dateandtime2 + "\n" + Dateandtime3), inline=True)
            embed.add_field(name="Score", value=(("OG " + LastGameScore1 + " " + LastGameEnemy1) +"\n"+("OG " + LastGameScore2 + " " + LastGameEnemy2) + "\n" +(LastGameOG3 + LastGameScore3 + " " + LastGameEnemy3)), inline=True)
            await message.channel.send(embed=embed)

          if (messagereceived =="!csgostreams"):
            streaminfo = CSGOStreams()
            team1 = streaminfo[1]
            team2 = streaminfo[2]
            links = streaminfo[3]
            matchlink = streaminfo[4]

            if(team1 == "No games found"):
              embed=discord.Embed(title="No CSGO streams / games were found", color=0xff8800)
              embed.add_field(name="What you can try", value="You can try using !nextcsgo to see if there are any games coming up", inline=True)
              embed.add_field(name="Links", value="OG Liquipedia:  https://liquipedia.net/counterstrike/OG\nOG HLTV: https://www.hltv.org/team/10503/og#tab-matchesBox" , inline=False)
              await message.channel.send(embed=embed)
            else:
              embed=discord.Embed(title="CSGO Stream links", color=0xff8800)
              embed.add_field(name="The game found", value=team1 + " vs " + team2, inline=True)
              embed.add_field(name="Streams", value="```" + links + "```", inline=False)
              embed.add_field(name="Streams available", value = links, inline=False)
              embed.add_field(name="Game page info", value=matchlink, inline=False)
              await message.channel.send(embed=embed)



          if ((messagereceived == "!avatar") and (message.mentions.__len__()>0)):
            for user in message.mentions:
                await message.channel.send(user.avatar_url)
                      
          elif ((messagereceived=="!avatar") and (message.mentions.__len__()==0)):
            await message.channel.send(message.author.avatar_url)


          if ((messagereceived == "!deletedotabo1") or (messagereceived =="!deletedota2bo1")):
              guild = message.guild
              #global my_url5
              
              try:
                  role_object = discord.utils.get(guild.roles, name="D1-0")
                  await role_object.delete()
                  await message.channel.send("D1-0 deleted")
              except:
                  await message.channel.send("D1-0 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="D0-1")
                  await role_object.delete()
                  await message.channel.send("D0-1 deleted")
              except:
                  await message.channel.send("D0-1 not found")

          if ((messagereceived =="!deletecsgobo1") or (messagereceived =="!deletecsgobo1")):
              guild = message.guild
              try:
                  role_object = discord.utils.get(guild.roles, name="CS1-0")
                  await role_object.delete()
                  await message.channel.send("CS1-0 deleted")
              except:
                  await message.channel.send("CS1-0 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="CS0-1")
                  await role_object.delete()
                  await message.channel.send("CS0-1 deleted")
              except:
                  await message.channel.send("CS0-1 not found")

          if ((messagereceived == "!deletevalobo1") or (messagereceived =="!deletevalorantbo1")):
              guild = message.guild
              try:
                  role_object = discord.utils.get(guild.roles, name="V1-0")
                  await role_object.delete()
                  await message.channel.send("V1-0 deleted")
              except:
                  await message.channel.send("V1-0 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="V0-1")
                  await role_object.delete()
                  await message.channel.send("V0-1 deleted")
              except:
                  await message.channel.send("V0-1 not found")

          if ((messagereceived =="!deletedotabo3") or (messagereceived == "!deletedota2bo3")):
              guild = message.guild
              try:
                  role_object = discord.utils.get(guild.roles, name="D2-0")
                  await role_object.delete()
                  await message.channel.send("D2-0 deleted")
              except:
                  await message.channel.send("D2-0 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="D2-1")
                  await role_object.delete()
                  await message.channel.send("D2-1 deleted")
              except:
                  await message.channel.send("D2-1 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="D1-2")
                  await role_object.delete()
                  await message.channel.send("D1-2 deleted")
              except:
                  await message.channel.send("D1-2 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="D0-2")
                  await role_object.delete()
                  await message.channel.send("D0-2 deleted")
              except:
                  await message.channel.send("D0-2 not found")

          if ((messagereceived =="!deletecsgobo3") or (messagereceived == "!deletecsgobo3")):
              guild = message.guild
              try:
                  role_object = discord.utils.get(guild.roles, name="CS2-0")
                  await role_object.delete()
                  await message.channel.send("CS2-0 deleted")
              except:
                  await message.channel.send("CS2-0 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="CS2-1")
                  await role_object.delete()
                  await message.channel.send("CS2-1 deleted")
              except:
                  await message.channel.send("CS2-1 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="CS1-2")
                  await role_object.delete()
                  await message.channel.send("CS1-2 deleted")
              except:
                  await message.channel.send("CS1-2 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="CS0-2")
                  await role_object.delete()
                  await message.channel.send("CS0-2 deleted")
              except:
                  await message.channel.send("CS0-2 not found")

          if ((messagereceived =="!deletevalobo3") or (messagereceived =="!deletevalorantbo3")):
              guild = message.guild
              try:
                  role_object = discord.utils.get(guild.roles, name="V2-0")
                  await role_object.delete()
                  await message.channel.send("V2-0 deleted")
              except:
                  await message.channel.send("V2-0 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="V2-1")
                  await role_object.delete()
                  await message.channel.send("V2-1 deleted")
              except:
                  await message.channel.send("V2-1 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="V1-2")
                  await role_object.delete()
                  await message.channel.send("V1-2 deleted")
              except:
                  await message.channel.send("V1-2 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="V0-2")
                  await role_object.delete()
                  await message.channel.send("V0-2 deleted")
              except:
                  await message.channel.send("V0-2 not found")

          if ((messagereceived =="!deletedotabo5") or (messagereceived =="!deletedota2bo5")):
              guild = message.guild
              try:
                  role_object = discord.utils.get(guild.roles, name="D3-0")
                  await role_object.delete()
                  await message.channel.send("D3-0 deleted")
              except:
                  await message.channel.send("D3-0 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="D3-1")
                  await role_object.delete()
                  await message.channel.send("D3-1 deleted")
              except:
                  await message.channel.send("D3-1 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="D3-2")
                  await role_object.delete()
                  await message.channel.send("D3-2 deleted")
              except:
                  await message.channel.send("D3-2 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="D2-3")
                  await role_object.delete()
                  await message.channel.send("D2-3 deleted")
              except:
                  await message.channel.send("D2-3 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="D1-3")
                  await role_object.delete()
                  await message.channel.send("D1-3 deleted")
              except:
                  await message.channel.send("D1-3 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="D0-3")
                  await role_object.delete()
                  await message.channel.send("D0-3 deleted")
              except:
                  await message.channel.send("D0-3 not found")

          if ((messagereceived =="!deletecsgobo5") or (messagereceived =="!deletecsgobo5")):
              guild = message.guild
              try:
                  role_object = discord.utils.get(guild.roles, name="CS3-0")
                  await role_object.delete()
                  await message.channel.send("CS3-0 deleted")
              except:
                  await message.channel.send("CS3-0 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="CS3-1")
                  await role_object.delete()
                  await message.channel.send("CS3-1 deleted")
              except:
                  await message.channel.send("CS3-1 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="CS3-2")
                  await role_object.delete()
                  await message.channel.send("CS3-2 deleted")
              except:
                  await message.channel.send("CS3-2 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="CS2-3")
                  await role_object.delete()
                  await message.channel.send("CS2-3 deleted")
              except:
                  await message.channel.send("CS2-3 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="CS1-3")
                  await role_object.delete()
                  await message.channel.send("CS1-3 deleted")
              except:
                  await message.channel.send("CS1-3 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="CS0-3")
                  await role_object.delete()
                  await message.channel.send("CS0-3 deleted")
              except:
                  await message.channel.send("CS0-3 not found")

          if ((messagereceived =="!deletevalobo5") or (messagereceived =="!deletevalorantbo5")):
              guild = message.guild
              try:
                  role_object = discord.utils.get(guild.roles, name="V3-0")
                  await role_object.delete()
                  await message.channel.send("V3-0 deleted")
              except:
                  await message.channel.send("V3-0 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="V3-1")
                  await role_object.delete()
                  await message.channel.send("V3-1 deleted")
              except:
                  await message.channel.send("V3-1 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="V3-2")
                  await role_object.delete()
                  await message.channel.send("V3-2 deleted")
              except:
                  await message.channel.send("V3-2 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="V2-3")
                  await role_object.delete()
                  await message.channel.send("V2-3 deleted")
              except:
                  await message.channel.send("V2-3 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="V1-3")
                  await role_object.delete()
                  await message.channel.send("V1-3 deleted")
              except:
                  await message.channel.send("V1-3 not found")

              try:
                  role_object = discord.utils.get(guild.roles, name="V0-3")
                  await role_object.delete()
                  await message.channel.send("V0-3 deleted")
              except:
                  await message.channel.send("V0-3 not found")

          if (messagereceived =="!dotabo1"):
              guild = message.guild
              await guild.create_role(name="D1-0")
              await message.channel.send("D1-0 created")
              await guild.create_role(name="D0-1")
              await message.channel.send("D0-1 created")
          

          if (messagereceived =="!dotabo3"):
              guild = message.guild
              await guild.create_role(name="D2-0")
              await message.channel.send("D2-0 created")
              await guild.create_role(name="D2-1")
              await message.channel.send("D2-1 created")
              await guild.create_role(name="D1-2")
              await message.channel.send("D1-2 created")
              await guild.create_role(name="D0-2")
              await message.channel.send("D0-2 created")

          if (messagereceived =="!dotabo5"):
              guild = message.guild
              await guild.create_role(name="D3-0")
              await message.channel.send("D3-0 created")
              await guild.create_role(name="D3-1")
              await message.channel.send("D3-1 created")
              await guild.create_role(name="D3-2")
              await message.channel.send("D3-2 created")
              await guild.create_role(name="D2-3")
              await message.channel.send("D2-3 created")
              await guild.create_role(name="D1-3")
              await message.channel.send("D1-3 created")
              await guild.create_role(name="D0-3")
              await message.channel.send("D0-3 created")

          if (messagereceived =="!csgobo1"):
              guild = message.guild
              await guild.create_role(name="CS1-0")
              await message.channel.send("CS1-0 created")
              await guild.create_role(name="CS0-1")
              await message.channel.send("CS0-1 created")

          if (messagereceived =="!csgobo3"):
              guild = message.guild
              await guild.create_role(name="CS2-0")
              await message.channel.send("CS2-0 created")
              await guild.create_role(name="CS2-1")
              await message.channel.send("CS2-1created")
              await guild.create_role(name="CS1-2")
              await message.channel.send("CS1-2 created")
              await guild.create_role(name="CS0-2")
              await message.channel.send("CS0-2 created")

          if (messagereceived =="!csgobo5"):
              guild = message.guild
              await guild.create_role(name="CS3-0")
              await message.channel.send("CS3-0 created")
              await guild.create_role(name="CS3-1")
              await message.channel.send("CS3-1 created")
              await guild.create_role(name="CS3-2")
              await message.channel.send("CS3-2 created")
              await guild.create_role(name="CS2-3")
              await message.channel.send("CS2-3 created")
              await guild.create_role(name="CS1-3")
              await message.channel.send("CS1-3 created")
              await guild.create_role(name="CS0-3")
              await message.channel.send("CS0-3 created")

          if (messagereceived =="!valobo1"):
              guild = message.guild
              await guild.create_role(name="V1-0")
              await message.channel.send("V1-0 created")
              await guild.create_role(name="V0-1")
              await message.channel.send("V0-1 created")

          if (messagereceived =="!valobo3"):
              guild = message.guild
              await guild.create_role(name="V2-0")
              await message.channel.send("V2-0 created")
              await guild.create_role(name="V2-1")
              await message.channel.send("V2-1 created")
              await guild.create_role(name="V1-2")
              await message.channel.send("V1-2 created")
              await guild.create_role(name="V0-2")
              await message.channel.send("V0-2 created")

          if (messagereceived =="!valobo5"):
              guild = message.guild
              await guild.create_role(name="V3-0")
              await message.channel.send("V3-0 created")
              await guild.create_role(name="V3-1")
              await message.channel.send("V3-1 created")
              await guild.create_role(name="V3-2")
              await message.channel.send("V3-2 created")
              await guild.create_role(name="V2-3")
              await message.channel.send("V2-3 created")
              await guild.create_role(name="V1-3")
              await message.channel.send("V1-3 created")
              await guild.create_role(name="V0-3")
              await message.channel.send("V0-3 created")
          
         

          if ((messagereceived =="!nextdota") or (messagereceived =="!nextdota2")):
            embed = DotaCheck(channelDataID)
            embed=embed[0]

            
            if((channelDataID == 690952309827698749) or (channelDataID == 689903856095723569)):
              userID = message.author.id
              userID = str(userID)
              await message.channel.send("<@" + userID + "> " + embed)
            else:
              await message.channel.send(embed=embed)

          if ((messagereceived =="!nextcsgo")or (messagereceived=="!nextcs")):
            CSGOGame = CSGOCheck(channelDataID)
            embed = CSGOGame[6]
            if((channelDataID == 690952309827698749) or (channelDataID == 689903856095723569)):
              userID = message.author.id
              userID = str(userID)
              await message.channel.send("<@" + userID + "> " + embed)
            else:
              await message.channel.send(embed=embed)


          if((messagereceived == "!nextvalo") or (messagereceived == "!nextvalorant")):
            Valogame = ValoCheck(channelDataID)
            valorantTeams = Valogame[0]
            valorantTeamTime = Valogame[1]
            timeremaining = Valogame[2]

            if(valorantTeams == "No games planned"):
              embed=discord.Embed(title="OG Valorant's next game", url="https://www.vlr.gg/team/2965/og",color=0xd57280)
              embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
              embed.add_field(name="No games planned", value="No games planned", inline=True)
              embed.add_field(name="Links", value="https://www.vlr.gg/team/2965/og / https://liquipedia.net/valorant/OG", inline=False)
              await message.channel.send(embed=embed)
            else:
              embed=discord.Embed(title="OG Valorant's next game", url="https://www.vlr.gg/team/2965/og",color=0xd57280)
              embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
              embed.add_field(name=valorantTeams, value=valorantTeamTime, inline=True)
              embed.add_field(name="Time remaining", value= timeremaining, inline = False)
              embed.add_field(name="Notice", value="Please check Liquipedia by clicking the title of this embed for more information as the time might not be accurate", inline=False)
              embed.add_field(name="Links", value="https://www.vlr.gg/team/2965/og / https://liquipedia.net/valorant/OG", inline=False)
              await message.channel.send(embed=embed)


          if(messagereceived=="!dotastreams"):
            streaminfo = DotaStreams()
            Teams1 = streaminfo[0]
            Teams2 = streaminfo[1]
            flagMessage= streaminfo[2]
            convertedURL = streaminfo[3]

            if(Teams1 == "No games found"):
              embed=discord.Embed(title="No Dota streams / games were found", color=0xf10909)
              embed.add_field(name="What you can try", value="You can try using !nextdota / !nextdota2 to see if there are any games coming up", inline=True)
              embed.add_field(name="Links", value="https://liquipedia.net/dota2/OG", inline=False)
              await message.channel.send(embed=embed)

            else:
              embed=discord.Embed(title="Dota streams found!", color=0xf10909)
              embed.add_field(name="The game found", value= Teams1 + " vs " + Teams2, inline=True)
              embed.add_field(name="Streams / Flags", value="```" + flagMessage + "```", inline=False)
              embed.add_field(name="Streams available", value=flagMessage, inline=False)
              embed.add_field(name="Where I found the streams", value= convertedURL, inline=False)
              await message.channel.send(embed=embed)



          if ((messagereceived=="!valostreams")or (messagereceived=="!valorantstreams")):
            streaminfo = ValoStreams()
            valoenemyteam= streaminfo[0]
            streams = streaminfo[1]
            matchlink= streaminfo[2]

            if(matchlink == "No games found"):
              embed=discord.Embed(title="No Valorant streams / games were found", color=0xd57280)
              embed.add_field(name="What you can try", value="You can try using !nextvalo / !nextvalorant to see if there are any games coming up", inline=True)
              embed.add_field(name="Links", value="https://www.vlr.gg/team/2965/og / https://liquipedia.net/valorant/OG", inline=False)
              await message.channel.send(embed=embed)

            else:
              embed=discord.Embed(title="Valorant streams coming up!", color=0xd57280)
              embed.add_field(name="The game found", value= "OG vs " + valoenemyteam, inline=True)
              embed.add_field(name="Streams for copying", value ="```" + streams + "```", inline=False)
              embed.add_field(name="Streams with flags", value=streams,inline=False)
              embed.add_field(name="Game page info", value=matchlink, inline=False)
              await message.channel.send(embed=embed)



          if (messagereceived =="!goosehelp"):
            willshelp1 = "!nextdota - This will tell you the next OG Dota 2 game coming up \n !nextcsgo - This will tell you the next OG CSGO game coming up \n !nextvalo - This will tell you the next OG Valorant  game coming up"
            willshelp2 = "!dotastreams - This will tell you the streams available for the next / current series of dota happening!\n !csgostreams - This will tell you the next / current CSGO games streams\n !valostreams - This will tell you the streams for the current / next Valorant series"
            willshelp3= "!nextdt - This will tell you the next game coming up in the currently tracked tournament\n\nAs a gardener you also gain access to commands found in: '!gardenerhelp'"

            embed=discord.Embed(title="The commands I work with", color=0xff8800)
            embed.add_field(name="The next OG games", value=willshelp1, inline=True)
            embed.add_field(name="The streams for games", value=willshelp2, inline=False)
            embed.add_field(name="Next game in tournament", value =willshelp3, inline=False)
            await message.channel.send(embed=embed) 


          if ((messagereceived =="!gardenerhelp")):
            GardenerHelp9 = "!verifydturl / !resetdt / !changedt\n\n!verifydturl - This will tell you the currently tournament link being tracked\n!resetdt - This will the currently tracked tournament\n!changedt - This will change the tournament being tracked to the URL provided"
            GardenerHelp4 = "!DotaBo1 / Bo3 / Bo5 \n \n !CSGOBo1 / Bo3 / Bo5 \n \n !ValoBo1 / Bo3 / Bo5 \n \n These will create the roles required to host a predictions game, purely type the one required, e.g - \n !CSGOBo3 \n \n"

            GardenerHelp5 = "!deleteDotaBo1 / Bo3 / Bo5 \n \n !deleteCSGOBo1 / Bo3 / Bo5 \n \n !deleteValoBo1 / Bo3 / Bo5 \n \n These will delete the roles that were made for the prediction game e.g - \n !deleteCSGOBo3 will delete the CSGOBo3 roles \n \n"

            GardenerHelp6 = "!avatar - You're able to see the avatars of any user / yourself, if you ping nobody it'll show your own avatar, if you ping someone it will show theirs\n\n!server_badge - This will get your the icon used for the server icon"

            GardenerHelp7 = "!dotastreams / !csgostreams / !valostreams - these will tell you the streams available for the next match of OG Dota / CSGO / Valorant respectively\n\n"

            GardenerHelp8 = "!copyover [channel to copy from here] - use this command to copy the content of a channel from 1 to another, the command will send the last 100 messages from a channel to the channel the command is being used in\n\nE.G of usage - !copyover 847832196294115349\nThis will give you the value from a copy test, the bot must be in both servers if copying from a different server"

            GardenerHelp10 = "!reminder - This command will let you set reminders for future you, the bot will remind you in the channel it is used in after a set amount of time! Use !reminder to find more information!\n!myreminders - This command will tell you your currently saved reminders and when they are going to be sent"
            
            embed=discord.Embed(title="The commands you get as a Gardener!", color=0xff8800)
            embed.add_field(name="Getting game streams",value=GardenerHelp7, inline=True)
            embed.add_field(name="Creating the roles for prediction games", value=GardenerHelp4, inline=False)
            embed.add_field(name="Delete the roles that were used for a prediction game", value=GardenerHelp5, inline=False)
            embed.add_field(name="Viewing avatars of users", value=GardenerHelp6, inline=False)
            embed.add_field(name="Tracking a tournament", value=GardenerHelp9, inline=False)
            embed.add_field(name="Reminders", value=GardenerHelp10, inline=False)
            embed.add_field(name="Copying data", value=GardenerHelp8, inline=False)
            await message.channel.send(embed=embed)










    #if message.author.guild_permissions.administrator == True:
            #print("SMILE")
    #TRANSLATIONS / specific channel messages

    #new-member-support OG Main Discord
    if(channelDataID == 736505679354921092):
      embed=discord.Embed(title="Welcome to the Flowerhouse!",color=0xff8800)
      embed.add_field(name="You seem to be lost, let me help", value = "Do be sure to go through <#829738571010277406> to check out the rules of the server! Follow this up in <#832198110204919848> to get access to the rest of the server! See you in there!", inline=True)
      embed.set_image(url="https://i.imgur.com/zr9Hp7C.png")
      
        
      data = download_file('/droplastmessage.txt', 'lastmessage.txt')
      g = open("lastmessage.txt", "r")
      g2 = g.read()
      g.close()
      

      try:
        print("Tried to delete message: " + g2 )
       
      except:
        print("Failed to delete any message")
      try:
        await client.http.delete_message(736505679354921092, g2)
      except:
        print("Failed to delete any message")
      message = await message.channel.send(embed=embed)
      f = open("lastmessage.txt", "w")
      f.write(str(message.id))
      f.close()
      upload_file('/droplastmessage.txt', 'lastmessage.txt' )

    if(message.author == discord.Permissions.administrator):
      print("nice")


    #Spanish Translations - Main OG Discord
    if(channelDataID == 818793950965006357):
      channel = message.guild.get_channel(832296821119647755)
      msgID = message.jump_url
      author = message.author
      data = translations(nexttrans, author, msgID)
      #Getting translation data
      embed=data
      await channel.send(embed=embed)
    

    #Finnis Translations - Jerax Discord
    if(channelDataID == 825328809854238731):
      channel = message.guild.get_channel(835434616000872448)
      msgID = message.jump_url
      author = message.author
      data = translations(nexttrans, author, msgID)
      #Getting translation data
      embed=data
      await channel.send(embed=embed)



    #Testing translation - test channel personal discord
    if(channelDataID == 810893610496426024):
      #Channel to send too
      channel = message.guild.get_channel(810893610496426024)
      msgID = message.jump_url
      author = message.author
      data = translations(nexttrans, author, msgID)
      #Getting translation data
      embed=data
      await channel.send(embed=embed)
      
    #Rus translation - N0tail Discord
    if(channelDataID == 808362012849340416):
      channel = message.guild.get_channel(834445890235138133)
      msgID = message.jump_url
      author = message.author
      data = translations(nexttrans, author, msgID)
      #Getting translation data
      embed=data
      await channel.send(embed=embed)

    #Russain Translation - Main Discord
    if(channelDataID == 697447277647626297):
      channel = message.guild.get_channel(832296883887407146)
      msgID = message.jump_url
      author = message.author
      data = translations(nexttrans, author, msgID)
      #Getting translation data
      embed=data
      await channel.send(embed=embed)




#if previously created reminders haven't ran it'll start them back up
async def reminder(reminderData):
  #Time Values for checking difference
  currenttime =  datetime.datetime.now()
  #day
  currentd = currenttime.strftime("%d")
  #hour [UK time - 1]
  currentH = currenttime.strftime("%H")
  #Minute
  currentM = currenttime.strftime("%M")
  #Month
  currentmonth = currenttime.strftime("%m")
  #year
  currentyear = currenttime.strftime("%y")
  currentyear = "20" + str(currentyear)
  currentyear = int(currentyear)
  #second
  currentsecond = currenttime.strftime("%S")
  currentDandT = datetime.datetime(int(currentyear), int(currentmonth), int(currentd), int(currentH), int(currentM), int(currentsecond))
  
  #reminder data
  reminderinfo = reminderData
  #Splitting up the reminder
  splitUpValues = reminderinfo.rsplit(", ")
  userID = splitUpValues[0]
  channelToSend = splitUpValues[1]
  textToSend = splitUpValues[2]
  timeToSend = splitUpValues[3]
  lineOfFile = splitUpValues[5]

  #Splitting date values 
  timesplitting = timeToSend.rsplit(" ")
  dateToSend = timesplitting[0]
  timeToSend = timesplitting[1]
  #Date splitting
  datesplitting = dateToSend.rsplit("-")
  timesplitting = timeToSend.rsplit(":")
  #day values
  yearToSend = datesplitting[0]
  monthToSend = datesplitting[1]
  dayToSend = datesplitting[2]
  #time values
  hourToSend = timesplitting[0]
  minuteToSend = timesplitting[1]
  secondToSend = timesplitting[2]
  
  sendonDandT = datetime.datetime(int(yearToSend), int(monthToSend), int(dayToSend), int(hourToSend), int(minuteToSend), int(secondToSend))
  time_delta = (sendonDandT - currentDandT)

  timeLeftInSeconds = time_delta.total_seconds()
  channel = client.get_channel(int(channelToSend))
  if timeLeftInSeconds < 0:
    #Creating the embed
    embed=discord.Embed(title="Your reminder time had already arrived! - While I was offline",color=0x55a7f7)
    embed.add_field(name="Your reminder, scheduled at - " + str(sendonDandT), value=textToSend, inline=True)

    #Overwrites the file with tagging the line as sent
    a_file = open("reminders.txt", "r")
    list_of_lines = a_file.readlines()
    list_of_lines[int(lineOfFile)] = (userID + ", " + channelToSend + ", " + textToSend + ", " + str(sendonDandT) + ", sent\n")

    a_file = open("reminders.txt", "w")
    a_file.writelines(list_of_lines)
    a_file.close()
    upload_file('/dropreminders.txt', 'reminders.txt' )
    #Sends to user
    await channel.send("<@" + userID + ">")
    await channel.send(embed=embed)
    

  else:
    #Forces bot to wait till the reminder is set
    await asyncio.sleep(timeLeftInSeconds)
    embed=discord.Embed(title="Your reminder time has arrived!",color=0x55a7f7)
    embed.add_field(name="Your reminder, scheduled at - " + str(sendonDandT), value=textToSend, inline=True)

    #Overwrites the file with tagging the line as sent
    a_file = open("reminders.txt", "r")
    list_of_lines = a_file.readlines()
    list_of_lines[int(lineOfFile)] = (userID + ", " + channelToSend + ", " + textToSend + ", " + str(sendonDandT) + ", sent\n")

    a_file = open("reminders.txt", "w")
    a_file.writelines(list_of_lines)
    a_file.close()
    upload_file('/dropreminders.txt', 'reminders.txt' )
    #Sends to user
    await channel.send("<@" + userID + ">")
    await channel.send(embed=embed)




#Cleans out reminder file if no reminders are left
async def cleanreminders():
  data = download_file('/dropreminders.txt', 'reminders.txt')
  a_file = open("reminders.txt", "r")
  list_of_lines = a_file.readlines()
  i=0

  reminders=[]
  while (i < len(list_of_lines)):
    
    base_reminder = list_of_lines[i]
    splitUpValues = base_reminder.rsplit(", ")

    checkIfSent = splitUpValues[4]
    checkIfSent= checkIfSent[0:2]
    
    if(checkIfSent == "no"):
      reminders.append(base_reminder + ", " + str(i))


    i=i+1
  
  print(len(reminders))
  if(len(reminders) == 0):
    file = open("reminders.txt", "r+")
    file.truncate(0)
    file.close()
    upload_file('/dropreminders.txt', 'reminders.txt' )






#Opening the file with last message every 5 mins
async def openingfile():
  g = open("lastmessage.txt", "r")
  g2 = g.read()
  g.close()
  print("File opened, value = " + g2)



  

#Daily posts
async def testingspam():
  global currentd
  print("testing: " + currentd)
  c= client.get_channel(839466348970639391)
  currenttime = datetime.datetime.now()
  message = "its working" + str(currenttime)
  await c.send(message)
  #Dota daily
  try:
    DotaGame = DotaCheck(720263155460079767)
    Teams = DotaGame[1]
    nextgametime = DotaGame[2]
    c = DotaGame[3]
    links= DotaGame[4]
    dayofgame2 = DotaGame[5]

    if((currentd[0]== "0")):
      currentd = currentd[1]

    if(dayofgame2 == currentd):
      embed=discord.Embed(title="There is an OG Dota game today!", url="https://liquipedia.net/dota2/OG", color=0xf10909)
      embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
      embed.add_field(name=Teams, value=nextgametime, inline=True)
      embed.add_field(name="Time remaining", value = c, inline=False)
      embed.add_field(name="Notice", value = "Please check Liquipedia by clicking the title of this embed for more information as the time might not be accurate", inline=False)
      embed.add_field(name="Links", value="OG Liquipedia: https://liquipedia.net/dota2/OG\nTournament: " + links, inline=False)
      #await message.channel.send(embed=embed)
      print("e")
      channel = client.get_channel(720263155460079767)
      print ("e2")
      channel2 = client.get_channel(847601411340501019)
      await channel2.send(embed=embed)
      await channel.send(embed=embed)
  except:
    print("no dota games today")



#Valo daily
  try:
    ValoGame = ValoCheck()
    valorantTeams = ValoGame[0]
    valorantTeamTime = ValoGame[1]
    c = ValoGame[2]
    dayofgame2 = ValoGame[3]
    

    if((currentd[0]== "0")):
      currentd = currentd[1]

    if(dayofgame2 == currentd):
      embed=discord.Embed(title="There is an OG Valo game today!", url="https://www.vlr.gg/team/2965/og",color=0xd57280)
      embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
      embed.add_field(name=valorantTeams, value=valorantTeamTime, inline=True)
      embed.add_field(name="Time remaining", value= c, inline = False)
      embed.add_field(name="Notice", value="Please check Liquipedia by clicking the title of this embed for more information as the time might not be accurate", inline=False)
      embed.add_field(name="Links", value="https://www.vlr.gg/team/2965/og / https://liquipedia.net/valorant/OG", inline=False)
      channel = client.get_channel(720263155460079767)
      channel2 = client.get_channel(847601411340501019)
      await channel2.send(embed=embed)
      await channel.send(embed=embed)
  except:
     print("No valo games today")

#CSGO daily
  try:
    uClient2 = uReq(my_url2)
    page_html2 = uClient2.read()
    uClient2.close()
    page_soup2 = soup(page_html2, "html.parser")

    now = datetime.datetime.now()

    dt_string_day = now.strftime("%d")
    dt_string_month = now.strftime("%m")
    dt_string_year= now.strftime("%y")
    dt_string_hour= now.strftime("%H")
    dt_string_minute= now.strftime("%M")
    dt_string_second= now.strftime("%S")

    #Parses the HTML data - csgo
    csgocontainers = page_soup2.findAll(
        "span", {"class": "team-template-team2-short"})
    csgocontainers2 = page_soup2.findAll(
        "span", {"class": "team-template-team-short"})
    csgocontainers3 = page_soup2.findAll(
        "span", {"class": "timer-object timer-object-countdown-only"})

    #This finds the next match time - csgo
    try:
        csgonextgametime = csgocontainers3[0].text
    except:
        pass

    #Adds game to containers - csgo
    try:
        csgoteam1 = csgocontainers[0]
        csgoteam2 = csgocontainers2[0]
    except:
        pass

    #Grabbing 1st team - CSGO
    try:
        print(csgoteam1.a["title"])
        csgoTeams1 = csgoteam1.a["title"]
    except:
        try:
            print(csgoteam1["data-highlightingclass"])
            csgoTeams1 = csgoteam1["data-highlightingclass"]

        except:
            pass

    #Grabbing 2nd team - CSGO
    try:
        print(csgoteam2.a["title"])
        csgoTeams2 = csgoteam2.a["title"]

    except:
        try:
            print(csgoteam2["data-highlightingclass"])
            csgoTeams2 = csgoteam2["data-highlightingclass"]

        except:
            pass

    #prints next CSGO game
    try:
        csgoTeams = (csgoTeams1 + " vs " + csgoTeams2)
        nextcsgogame = ("<:OGpeepoThumbsUp:734000712169553951> " + csgoTeams1 + " vs " + csgoTeams2 + " on " +
                        csgonextgametime +
                        ", more information can be found at - " +
                        my_url2)
        datetimesplit = csgonextgametime.rsplit(" ")
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
        
        a = datetime.datetime(int(yearofgame), int(monthnumber), int(dayofgame2), int(hourofgame), int(minuteofgame), 0)

        b = datetime.datetime(int(dt_string_year), int(dt_string_month), int(dt_string_day), int(dt_string_hour), int(dt_string_minute), int(dt_string_second))

        c = a-b
        if (c.days < 0):
          c = "The game is meant to have begun!"
        if((currentd[0]== "0")):
          currentd = currentd[1]
        
        if (dayofgame2 == currentd):
          embed=discord.Embed(title="There is an OG CSGO game today!", url="https://liquipedia.net/counterstrike/OG", color=0xff8800)
          embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
          embed.add_field(name=csgoTeams, value=csgonextgametime, inline=True)
          embed.add_field(name="Time remaining", value= c, inline = False)
          embed.add_field(name="Notice", value="Please check Liquipedia by clicking the title of this embed for more information as the time might not be accurate", inline=False)
          embed.add_field(name="Links", value="https://www.hltv.org/team/10503/og#tab-matchesBox / https://liquipedia.net/counterstrike/OG", inline=False)
          print("CS1")
          channel = client.get_channel(720263155460079767)
          print ("cs2")
          channel2 = client.get_channel(847601411340501019)
          await channel2.send(embed=embed)
          await channel.send(embed=embed)
    except:
      print("tried")
     
  except:
    print("no csgo games today")

 
    
      


client.run(os.getenv('TOKEN'))
server.server()

