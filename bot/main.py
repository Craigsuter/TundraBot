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
from tournamentchecker2 import DotaCheckTourni2
from dropboxUploader import upload_file
from dropboxUploader import download_file
import liquipediapy
from stream2 import DotaStreams2
from dtStreams import dtStreams
import random

#sets up command prefix
intents = discord.Intents().all()
client = commands.Bot(command_prefix = '!', intents=intents)



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
    try:
      scheduler.add_job(testingspam,CronTrigger(hour="7"))
      print("Daily announcement success")
    except:
      print("Daily announced schedule failed")
    #Opens the file checking the new member support to delete the old bot message
    try:
      scheduler.add_job(openingfile, CronTrigger(minute="0, 20, 40"))
      print("Opening file schedule success")
    except:
      print("Opening file to delete the last message failed")

    try:
      scheduler.add_job(cleanreminders, CronTrigger(minute= "0, 30"))
      print("Clean reminder file success")
    except:
      print("Clear reminders file schedule failed")
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


#Will delete the latest message from a user
@client.event
async def on_member_update(before, after):
  guild = after.guild.id
  info= ("<@" + str(after.id) + ">")
  #Only checks this guild
  if(guild == 689865753662455829):
    #If user gets given a new role
    if len(before.roles) < len(after.roles):
      newRole = next(role for role in after.roles if role not in before.roles)
      
      #If user gets added to 'Muted' role
      if (newRole.name == "Muted"):

        

        #channel to get messages from [so will be General in main server]
        c= client.get_channel(689865754354384996)
        messages = await c.history(limit=100).flatten()
        i=0
        if(i<1):
          #Will delete the latest message from the user
          for message in messages:
            user= message.author.id
            if user == after.id and i < 2:
              #channelID , messageid 
              await client.http.delete_message(689865754354384996, message.id)
              i=i+1
        channel = client.get_channel(847601410891841561)
        await channel.send(str(info) + " - user got muted in the main server, messages removed: " + str(i))

  



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
      
      

    messagetolower = introtomessage
    messagereceived = messagetolower.lower()
    mention = f'<@!{client.user.id}>'
    #Checks for a ping of the bot
    if ((mention in message.content) and (messagereceived[0] != '!')):
      await message.channel.send("Im up! Im up! Are you okay... cool... co... <:OGmonkaThink:821509791523930162> ")

    #Verifies that message is command usage
    if (first_char=="!"):
      if(messagereceived=="!spreadthegoose"):
        await message.channel.send(" <a:OGDuckoWiggle:745372475109408808> <a:OGDuckoWiggle:745372475109408808> <a:OGDuckoWiggle:745372475109408808> ")

      if(messagereceived=="!ping"):
        value = random.randint(1, 100)
        if value == 1:
          await message.channel.send("https://tenor.com/view/cat-ping-pong-funny-animals-cats-gif-8766860")
        else:
          await message.channel.send("Pong")

      if(messagereceived=="!dtstreams"):
        data = download_file('/dropdotatournament.txt', 'dotatournament.txt')
        f = open("dotatournament.txt","r")
        my_url=f.read()
        f.close()
        dtstreaminfo = dtStreams(my_url)
        streamlinks = dtstreaminfo[0]
        urloftourni = dtstreaminfo[1]

        embed=discord.Embed(title="Streams for the tournament" ,color=0x55a7f7)
        embed.add_field(name="Streams", value = streamlinks, inline= True)
        embed.add_field(name="Where I found the streams", value=urloftourni, inline=False)
        await message.channel.send(embed=embed)
      
      if(messagereceived=="!dtstreams2"):
        data = download_file('/dropdotatournament2.txt', 'dotatournament2.txt')
        f = open("dotatournament2.txt","r")
        my_url=f.read()
        f.close()
        dtstreaminfo = dtStreams(my_url)
        streamlinks = dtstreaminfo[0]
        urloftourni = dtstreaminfo[1]

        embed=discord.Embed(title="Streams for the tournament" ,color=0x55a7f7)
        embed.add_field(name="Streams", value = streamlinks, inline= True)
        embed.add_field(name="Where I found the streams", value=urloftourni, inline=False)
        await message.channel.send(embed=embed)


      
      
      if((messagereceived == "!teaminfo")):
        try:
          lenofmessage = len(sectionsofmessage) - 1
          team_name=""
          if (lenofmessage > 0):
            team_name = fullMessage.partition(' ')[2]
            team_name = team_name.replace(" ", "_")
            team_name =  ' '.join([w.title() if w.islower() and w[0].isdigit()==False else w[0].upper() + w[1:] for w in team_name.split()])
            team_name_for_text = team_name.replace("_", " ")
          else:
            team_name="OG"
            team_name_for_text = "OG"

          
          dota_obj = liquipediapy.dota("appname")
          team_details = dota_obj.get_team_info(team_name,False)
          image = team_details["cups"]
          generalinfo=""
          try:
            region = team_details["info"]["region"]
            generalinfo = generalinfo + "Region: " + region + "\n"
          except:
            pass
          
          try:
            coach=team_details["info"]["coach"]
            generalinfo = generalinfo + "Coach: " + coach + "\n"
          except:
            pass
          

          try:
            sponsorslist = team_details["info"]["sponsor"]
            i=0
            lenlist = len(sponsorslist) - 1
            sponsor=""
            
            while(i<len(sponsorslist)):
              try:
                if(i < lenlist):
                  sponsor = sponsor + sponsorslist[i] + ", "
                else:
                  sponsor = sponsor + sponsorslist[i]
              except:
                sponsor= sponsor
              i = i+1
            
            generalinfo = generalinfo + "Sponsors: " + sponsor + "\n"
          except:
            pass
          
        
          playerinfo=""
          try:
            player1 = team_details["team_roster"][0]
            
            pname1 = player1["Name"]
            pingame1 = player1["ID"]
            playerinfo = playerinfo  + "Pos1: " + pingame1 + "\n"

            
          except:
            player1 = "Could no find player 1"

          try:
            player2 = team_details["team_roster"][1]
            pname2 = player2["Name"]
            pingame2 = player2["ID"]
            playerinfo = playerinfo  + "Pos2: " + pingame2 + "\n"
          except:
            
            player2 = "Could no find player 1"

          try:
            player3 = team_details["team_roster"][2]
            pname3 = player3["Name"]
            pingame3 = player3["ID"]
            playerinfo = playerinfo  + "Pos3: " + pingame3 + "\n"
          except:
            player3 = "Could no find player 1"

          try:
            player4 = team_details["team_roster"][3]
            pname4 = player4["Name"]
            pingame4 = player4["ID"]
            playerinfo = playerinfo  + "Pos4: " + pingame4 + "\n"
          except:
            player4 = "Could no find player 1"

          try:
            player5 = team_details["team_roster"][4]
            pname5 = player5["Name"]
            pingame5 = player5["ID"]
            playerinfo = playerinfo  + "Pos5: " + pingame5 + "\n"
          except:
            player5 = "Could no find player 1"

          listlength = len(image) - 1
          i=0
          tournamentwins=""
          try:
            while(i < 3):
              try:
                value = image[listlength - i]
                
                if(i < 2):
                  tournamentwins = tournamentwins + value + ", "
                else:
                  tournamentwins = tournamentwins + value
              except:
                tournamentwins = "none"
              i = i+1
          except:
            tournamentwins="none"

          print(generalinfo)
          embed=discord.Embed(title="Team: " + team_name_for_text ,color=0x55a7f7)
          #embed.set_image(url="https://liquipedia.net/commons/images/thumb/7/70/OG_RB_allmode.png/600px-OG_RB_allmode.png")
          embed.add_field(name="Players", value = playerinfo, inline= True)
          if tournamentwins !="none":
            embed.add_field(name="Tournaments won", value= tournamentwins, inline=False)
          if generalinfo is not None:
            embed.add_field(name="General info", value=generalinfo, inline=False)
          await message.channel.send(embed=embed)
        except:
          embed=discord.Embed(title="Team info command usage",color=0x55a7f7)
          embed.add_field(name="Help", value = "I was uanble to find the team you specified sometimes this is caused by capital letters being needed, or could be spelling! Please try again", inline= True)
          await message.channel.send(embed=embed)

      #Gets the info for the next dota game
      if ((messagereceived =="!nextdota") or (messagereceived =="!nextdoto") or (messagereceived =="!nextdota2")):
        embed = DotaCheck(channelDataID)
        embed=embed[0]
        if((channelDataID == 689903856095723569) or (channelDataID == 690952309827698749)):
          userID = message.author.id
          userID = str(userID)
          await message.channel.send("<@" + userID + "> " + embed)
        else:
          await message.channel.send(embed=embed)

      #Gets the info for the next CSGO game   
      if ((messagereceived =="!nextcsgo")or (messagereceived=="!nextcs")):
        CSGOGame = CSGOCheck(channelDataID)
        embed = CSGOGame[6]
        if((channelDataID == 690952309827698749) or (channelDataID == 689903856095723569)):
          userID = message.author.id
          userID = str(userID)
          await message.channel.send("<@" + userID + "> " + embed)
        else:
          await message.channel.send(embed=embed)

      #Gets the info for the next Valo game
      if((messagereceived == "!nextvalo") or (messagereceived == "!nextvalorant") or (messagereceived == "!nextval")):
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

       #Used for checking the next game in Dota Tourni
      if (messagereceived=="!nextdt" or messagereceived=="!nextdtcis"):   
        embed = DotaCheckTourni(channelDataID)
        embed=embed[0]
        if((channelDataID == 689903856095723569) or (channelDataID == 690952309827698749)):
          userID = message.author.id
          userID = str(userID)
          await message.channel.send("<@" + userID + "> " + embed)
        else:
          await message.channel.send(embed=embed)

      if (messagereceived=="!nextdt2" or messagereceived=="!nextdtsa" ):   
        embed = DotaCheckTourni2(channelDataID)
        embed=embed[0]
        if((channelDataID == 689903856095723569) or (channelDataID == 690952309827698749)):
          userID = message.author.id
          userID = str(userID)
          await message.channel.send("<@" + userID + "> " + embed)
        else:
          await message.channel.send(embed=embed)
      
      
      #Gets the info for the last dota game
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

      #Gets the info for the last CSGO game
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


      #Gets the info for the last valo game
      if((messagereceived=="!lastvalo") or (messagereceived == "!lastvalorant")):
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



      if(messagereceived=="!playerinfo"):
        try:
          lenofmessage = len(sectionsofmessage) - 1
          team_name=""
          if (lenofmessage > 0):
            team_name = fullMessage.partition(' ')[2]
            team_name = team_name.replace(" ", "_")
            #team_name =  ' '.join([w.title() if w.islower() and w[0].isdigit()==False else w[0].upper() + w[1:] for w in team_name.split()])
            team_name_for_text = team_name.replace("_", " ")
          else:
            team_name="n0tail"
            team_name_for_text = "n0tail"
          dota_obj = liquipediapy.dota("appname")
          player_details = dota_obj.get_player_info(team_name,True)
          player = "n0tail"
          try:
            name = player_details["info"]["name"]
          except:
            name = "unknown"
          try:
            age = player_details["info"]["birth_details"]
          except:
            age = "unknown"

          try:
            currentteam = player_details["info"]["team"]
          except:
            currentteam = "unknown"

          try:
            currentlyplaying = player_details["info"]["status"]
            if(currentlyplaying == "Active"):
              currentlyplaying = "currently playing"
            else:
              currentlyplaying = "No longer playing"
          except:
            currentlyplaying = "unknown"

          try:
            sighero = player_details["info"]["signature_heros"]
            i=0
            signatureheros=""
            while(i < len(sighero)):
              if(i < len(sighero) - 1):
                signatureheros = signatureheros + sighero[i] + ", "
              else:
                signatureheros = signatureheros + sighero[i] 
              i=i+1
            
          except:
            signatureheros = "unknown"
          
          try:
            earnings = player_details["info"]["earnings"]
            earnings = ('{:,}'.format(earnings))
            earnings = "$" + str(earnings)
          except:
            earnings = "unknown"
        

          try:
            history=player_details["history"]
            history.reverse()
            playerhis =""
            if(len(history) > 2):
              j=0
              while(j < 3):
                playerhis = playerhis + history[j]["duration"] + " - " + history[j]["name"] + "\n"
                j=j+1

            else:
              k=0
              while(k < len(history)):
                playerhis = playerhis + history[k]["duration"] + " - " + history[k]["name"] + "\n"
              

          except:
            playerhis = "unknown"

          generalinfo=""
          if(name != "unknown"):
            generalinfo = generalinfo + "Name: " + name + "\n"
          if(age != "unknown"):
            generalinfo = generalinfo + "Age: " + age + "\n"
          if(currentlyplaying != "unknown"):
            generalinfo = generalinfo + "Activity: " + currentlyplaying + "\n"
          

          playerinfo =""
          if(currentteam != "unknown"):
            playerinfo = playerinfo + "Current team: " + currentteam + "\n"
          if(signatureheros != "unknown"):
            playerinfo = playerinfo + "Signature heroes: " + signatureheros + "\n"
          if(earnings != "unknown"):
            playerinfo = playerinfo + "Earnings: " + earnings + "\n"
          if(playerhis != "unknown"):
            playerinfo = playerinfo + "**__Team History__**\n" + playerhis + "\n"
          

          embed=discord.Embed(title="Player card for - " + team_name_for_text,color=0x55a7f7)
          counter1 = 0
          counter2 = 0
          playerinfotest = playerinfo.replace("\n", "")
          print(playerinfotest)
          if(generalinfo != ""):
            embed.add_field(name = "General information", value = generalinfo)
            counter1 = counter1 +1
          if(playerinfotest != "**__Team History__**"):
            embed.add_field(name = "Player information", value = playerinfo, inline= False)
            counter2 = counter2 +1
          
          if(counter1 > 0 or counter2 > 0):
            await message.channel.send(embed=embed)
          else:
            embed=discord.Embed(title="Player info command usage",color=0x55a7f7)
            embed.add_field(name="Help", value = "I was uanble to find the player you specified sometimes this is caused by capital letters being needed, or could be spelling! Please try again", inline= True)
            await message.channel.send(embed=embed)
        except:
          embed=discord.Embed(title="Player info command usage",color=0x55a7f7)
          embed.add_field(name="Help", value = "I was uanble to find the player you specified sometimes this is caused by capital letters being needed, or could be spelling! Please try again", inline= True)
          await message.channel.send(embed=embed)







      #None mod commands
      if (author.guild_permissions.administrator == False):
          
          #Commands that are Moderator only
          blockedcommands=["!deletedotabo1", "!deletedota2bo1", "!deletecsgoBo1", "!deletevalobo1", "!deletevalorantbo1", "!deletedotabo3", "!deletedota2bo3", "!deletecsgobo3", "!deletevalobo3", "!deletevalorantbo3", "!deletedotabo5", "!deletedota2bo5", "!deletecsgobo5", "!deletecsgobo5", "!deletevalobo5", "!deletevalorantbo5", "!dotabo1", "!dotabo3", "!dotabo5", "!csgobo1", "!csgobo3", "!csgobo5", "!valobo1", "!valobo3", "!valobo5", "!changedt", "!resetdt", "!verifydurl", "!changecst", "!changevt", "!resetvt", "!verifyvurl", "!resetcst", "!verifycsurl", "!copyover", "!gardenerhelp", "!cleardota"]

          if (messagereceived in blockedcommands):
            await message.channel.send("No role access")
          
         
          
          #Get CSGO streams list for next CS game
          if (messagereceived =="!csgostreams"):
            embed = CSGOStreams()
            embed = embed[0]
            await message.channel.send(embed=embed)

          #Checks if user tries using !nextmatch incorrectly
          if ((messagereceived == "!nextgame") or (messagereceived == "!game") or (messagereceived == "!nextmatch") or(messagereceived == "!match") or (messagereceived == "!next")):
            embed=discord.Embed(title="OGoose bot help",color=0xd57280)
            embed.set_thumbnail(url="https://i.imgur.com/YJfbFth.png")
            embed.add_field(name="Asking for game information", value="To get game information do be sure to use !nextdota / !nextcsgo / !nextvalo, you can get additional help using !goosehelp", inline=True)
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

          if(messagereceived =="!dotastreams2"):
              
              streaminfo = DotaStreams2()
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

            willshelp2 = "!dotastreams / !dotastreams2 [B-Streams listed for our team] - This will tell you the streams available for the next / current series of dota happening!\n!csgostreams - This will tell you the next / current CSGO games streams\n!valostreams - This will tell you the streams for the current / next Valorant series"
            willshelp3= "!nextdt - This will tell you the next game coming up in the currently tracked tournament"
            willshelp4 = "!teaminfo - Use this to get info on a dota team you're looking for\nE.G - !teaminfo EG, this will give the information on EG\n!playerinfo - Use this to get information on a player"
            willshelp5 = "!dtstreams / !dtstreams2 - This will collect the streams listed on the page of the tournaments being tracked for !nextdt / !nextdt2"

            embed=discord.Embed(title="The commands I work with", color=0xff8800)
            embed.add_field(name="The next OG games", value=willshelp1, inline=True)
            embed.add_field(name="The streams for games", value=willshelp2, inline=False)
            embed.add_field(name="The streams for tournament tracked", value=willshelp5, inline=False)
            embed.add_field(name="Next game in tournament", value =willshelp3, inline=False)
            embed.add_field(name="Team / player info", value=willshelp4, inline=False)
            await message.channel.send(embed=embed) 

          return













      #All gardener commands  
      else:

          if(messagereceived=="!snooze"):
            try:
              #time values
              timevaluechecker = ['d', 'h', 'm', 's']

              #downloads reminder file to local
              data=download_file('/dropreminders.txt','reminders.txt')
              a_file = open("reminders.txt", "r")
              list_of_lines = a_file.readlines()

              #Create current year / time values
              currentyear = "20" + str(currentyear)
              currentyear = int(currentyear)

              date_and_time = datetime.datetime(int(currentyear), int(currentmonth), int(currentd), int(currentH), int(currentM), int(currentsecond))


              #Start reminder embeds
              embed=discord.Embed(title="Snooze command initiated",color=0x55a7f7)
              embed2= discord.Embed(title="Your reminder... has arrived!",color=0x55a7f7)
              
              #counters for the command
              timechecker=0
              counter= 0
              i=0
              j=0

              #Get the 2nd part of message for time values
              reminder = secondPartOfMessage
              timevalue = reminder[-1]
              #Will collect the reminders and find the last sent reminder
              while(i < len(list_of_lines)):
                lineofinfo = list_of_lines[i].rsplit(", ")
                checkingsent = lineofinfo[4][0:2]
              
                #Will collect any sent reminders
                if(str(message.author.id) == lineofinfo[0] and checkingsent != "no"):
                  linetoresend = lineofinfo
                  j=j+1
                  
                i=i+1
              if(j>0):
                #The values used for sending + timing
                usertoping = linetoresend[0]
                channelToSend= str(linetoresend[1])
                remindertosave = linetoresend[2]
                textToSend = str(remindertosave)

                try:
                  #Creating the messafge
                  if reminder == "none" or (timevalue not in timevaluechecker) :
                    embed.add_field(name="Command used no time set", value="To set the time for this command, please set it using 'days' / 'hours' / 'minutes' / 'seconds'\n\nTo format this you use d / h / m / s, at the end of the time wanted\n\nExample - !reminder 10h This is a reminder\nThis will remind you in 10 hours!")
                  
                  timetoadd=""
                  new_time = date_and_time
                  i=0
                  #Generates time till reminder in a split way for if the user puts multiple values
                  if( reminder != "none" and (timevalue in timevaluechecker)):
                    while(i < len(reminder)):
                      if(reminder[i] == "s" or reminder[i] == "m" or reminder[i] == "h" or reminder[i] == "d"):
                        if (reminder[i] == "s"):
                          timetillremidningyou = timetoadd
                          timechecker = timechecker + int(timetoadd)
                          timetoadd=""
                          counter = counter + 1
                          if(i == len(reminder) - 1):
                            embed.add_field(name="Reminder set, reminding in - " + reminder , value=remindertosave, inline=True)
                            embed2.add_field(name="Your reminder!", value=remindertosave,inline=True)
                          #calculate time for reminder
                          time_change = datetime.timedelta(seconds=int(timetillremidningyou))
                          new_time = new_time + time_change
                        
                        if(reminder[i] == "m"):
                          timetillremidningyou = timetoadd
                          timechecker = timechecker + (int(timetoadd) * 60)
                          timetoadd=""
                          counter = counter + 1
                          if(i == len(reminder) - 1):
                            embed.add_field(name="Reminder set, reminding in - " + reminder, value=remindertosave, inline=True)
                            embed2.add_field(name=
                            "Your reminder!", value=remindertosave,inline=True)
                          timetillremidningyou = int(timetillremidningyou) * 60
                          #calculate time for reminder
                          time_change = datetime.timedelta(seconds=int(timetillremidningyou))
                          new_time = new_time + time_change

                        if(reminder[i] =="h"):
                          timetillremidningyou = timetoadd
                          timechecker = timechecker + (int(timetoadd) * 60 * 60)
                          timetoadd=""
                          counter = counter + 1
                          if(i == len(reminder) - 1):
                            embed.add_field(name="Reminder set, reminding in - " + reminder, value=remindertosave, inline=True)
                            embed2.add_field(name="Your reminder!", value=remindertosave,inline=True)
                          timetillremidningyou = int(timetillremidningyou) * 60 * 60
                          #calculate time for reminder
                          time_change = datetime.timedelta(seconds=int(timetillremidningyou))
                          new_time = new_time + time_change
                        
                        if(reminder[i]=="d"):
                          timetillremidningyou = timetoadd
                          timechecker = timechecker + (int(timetoadd) * 60 * 60 * 24)
                          timetoadd=""
                          counter = counter + 1
                          if(i == len(reminder) - 1):
                            embed.add_field(name="Reminder set, reminding in - " + reminder, value=remindertosave, inline=True)
                            embed2.add_field(name="Your reminder!", value=remindertosave,inline=True)
                          
                          timetillremidningyou = int(timetillremidningyou) * 60 * 60 * 24
                          #calculate time for reminder
                        
                          time_change = datetime.timedelta(seconds=int(timetillremidningyou))
                          
                          new_time = new_time + time_change
                      else:
                        timetoadd = timetoadd + str(reminder[i])
                      i=i+1

                  #Adding reminder to the text file
                  userID = message.author.id
                  userID = str(userID)

                  #For adding value to the file
                  if(counter > 0):
                    f=open("reminders.txt", "a")
                    f.write(userID + ", " + channelToSend + ", " + textToSend + ", " + str(new_time) + ", not\n")
                    f.close()
                    upload_file('/dropreminders.txt', 'reminders.txt' )
                  
                    LineOfReminder = sum(1 for line in open('reminders.txt'))
                  #sending embed for starting the command
                  await message.channel.send(embed=embed)


                except:
                  #Error catching
                  embed2=discord.Embed(title="Snooze command initiated",color=0x55a7f7)
                  embed2.add_field(name="Command used no time set", value="To set the time for this command, please set it using 'days' / 'hours' / 'minutes' / 'seconds'\n\nTo format this you use d / h / m / s, at the end of the time wanted\n\nExample - !reminder 10h This is a reminder\nThis will remind you in 10 hours!")
                  await message.channel.send(embed=embed2)
                

                try:
                  if(counter > 0):
                    timetosleep = int(timechecker)
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


              else:
                #If user has 0 reminders to snooze
                await message.channel.send("You currently have no messages available to snooze")


            except:
              print("error here")











          if(messagereceived=="!rolequal1"):
              i=0
              while(i<14):
                roletomake = "r1team-" + str(i)
                await guild.create_role(name=str(roletomake))
                i=i+1
                await message.channel.send("Created - " + str(roletomake))
          
          if(messagereceived=="!delrolequal1"):
            i=0
            while(i<14):
              roletodelete = "r1team-" + str(i)
              role_object = discord.utils.get(guild.roles, name=roletodelete)
              await role_object.delete()
              await message.channel.send("deleted - " + str(roletodelete))
              i=i+1

          if(messagereceived=="!rolequal2"):
              i=0
              while(i<12):
                roletomake = "r2team-" + str(i)
                await guild.create_role(name=str(roletomake))
                i=i+1
                await message.channel.send("Created - " + str(roletomake))
          
          if(messagereceived=="!delrolequal2"):
            i=0
            while(i<12):
              roletodelete = "r2team-" + str(i)
              role_object = discord.utils.get(guild.roles, name=roletodelete)
              await role_object.delete()
              await message.channel.send("deleted - " + str(roletodelete))
              i=i+1



          

          if(messagereceived =="!dotastreams2"):
              
              streaminfo = DotaStreams2()
              Teams1 = streaminfo[0]
              Teams2 = streaminfo[1]
              flagMessage= streaminfo[2]
              convertedURL = streaminfo[3]

              if(Teams1 == "No games found"):
                embed=discord.Embed(title="No Dota streams / games were found", color=0xf10909)
                embed.add_field(name="What you can try", value="You can try using !nextdota / !nextdota2 to see if there are any games coming up", inline=True)
                embed.add_field(name="Streams / Flags", value="```" + flagMessage + "```", inline=False)
                embed.add_field(name="Links", value="https://liquipedia.net/dota2/OG", inline=False)
                await message.channel.send(embed=embed)

              else:
                embed=discord.Embed(title="Dota streams found!", color=0xf10909)
                embed.add_field(name="The game found", value= Teams1 + " vs " + Teams2, inline=True)
                embed.add_field(name="Streams / Flags", value="```" + flagMessage + "```", inline=False)
                embed.add_field(name="Streams available", value=flagMessage, inline=False)
                embed.add_field(name="Where I found the streams", value= convertedURL, inline=False)
                await message.channel.send(embed=embed)

          if((messagereceived=="!discordstats")and (message.mentions.__len__()>0)):
            for user in message.mentions:
              createdon = user.created_at
              joinedon = user.joined_at
              cyear = createdon.year
              cmonth=createdon.month
              cday=createdon.day
              chour=createdon.hour
              cminute=createdon.minute
              csecond=createdon.second
              timecreation = str(cday) + "/" + str(cmonth) + "/" + str(cyear) + " - " + str(chour) + ":" + str(cminute) + ":" + str(csecond)

              jyear = joinedon.year
              jmonth= joinedon.month
              jday= joinedon.day
              jhour= joinedon.hour
              jminute= joinedon.minute
              jsecond= joinedon.second
              timejoining = str(jday) + "/" + str(jmonth) + "/" + str(jyear) + " - " + str(jhour) + ":" + str(jminute) + ":" + str(jsecond)

              embed=discord.Embed(title="Account information of - " + str(user.display_name),color=0x55a7f7)
              embed.add_field(name="Account details", value = "User account was created on - " + str(timecreation) + "\nJoined the server on- " + str(timejoining), inline= True)

              await message.channel.send(embed=embed)


              #await message.channel.send("<@" + str(user.id) + "> \nDiscord account created on - " + str(user.created_at) +"\nJoined the server on - " + str(user.joined_at))

          if ((messagereceived=="!discordstats")and (message.mentions.__len__()==0)):
            user=message.author
            createdon = user.created_at
            joinedon = user.joined_at
            cyear = createdon.year
            cmonth=createdon.month
            cday=createdon.day
            chour=createdon.hour
            cminute=createdon.minute
            csecond=createdon.second
            timecreation = str(cday) + "/" + str(cmonth) + "/" + str(cyear) + " - " + str(chour) + ":" + str(cminute) + ":" + str(csecond)

            jyear = joinedon.year
            jmonth= joinedon.month
            jday= joinedon.day
            jhour= joinedon.hour
            jminute= joinedon.minute
            jsecond= joinedon.second
            timejoining = str(jday) + "/" + str(jmonth) + "/" + str(jyear) + " - " + str(jhour) + ":" + str(jminute) + ":" + str(jsecond)

            embed=discord.Embed(title="Account information of - " + str(user.display_name),color=0x55a7f7)
            embed.add_field(name="Account details", value = "User account was created on - " + str(timecreation) + "\nJoined the server on- " + str(timejoining), inline= True)
            await message.channel.send(embed=embed)


          if(messagereceived=="!deletereminder"):
            data=download_file('/dropreminders.txt','reminders.txt')
            a_file = open("reminders.txt", "r")
            list_of_lines = a_file.readlines()
            
            remindertodelete = secondPartOfMessage
            author = message.author.id
            
            i=0
            j=1
            k=0
            datatosave=[]
            try:
              while(i< len(list_of_lines)):
                reminderdata = list_of_lines[i]
                remindersplitup = reminderdata.rsplit(", ")
                text = remindersplitup[0]
                text = text.strip()
                checksent = remindersplitup[len(remindersplitup) - 1]
                checksent = checksent.strip()
              
                if(text == str(author) and checksent != "sent"):
                  if(j == int(remindertodelete)):
                    print("we are here")
                    user = remindersplitup[0]
                    
                    channel = remindersplitup[1]
                    reminder = remindersplitup[2]
                    timetosend = remindersplitup[3]
                    issent = "sent"
                    remindersaved = reminder + ", to be sent on - " + timetosend
                    linetosave = user + ", " + channel + ", " + reminder + ", " + timetosend + ", " + issent +"\n"
                    embed=discord.Embed(title="Reminder removed",color=0x55a7f7)
                    embed.add_field(name="The deleted reminder", value = remindersaved, inline= True)
                    datatosave.append(linetosave)
                    j=j+1
                    k=k+1
                  else:
                    datatosave.append(reminderdata)
                    print(j)
                    j=j+1
                else:
                  datatosave.append(reminderdata)
                i=i+1
              
              a_file = open("reminders.txt", "w")
              a_file.writelines(datatosave)
              a_file.close()
              upload_file('/dropreminders.txt', 'reminders.txt')
              if(k != 0):
                await message.channel.send(embed=embed)
              else:
                embed=discord.Embed(title="Reminder deletion error",color=0x55a7f7)
                embed.add_field(name="Suggestion", value = "To use this find your reminders via !myreminders, and choose the reminder based on the value to the left of your reminder!\n E.G - !deletereminder 1", inline= True)
                await message.channel.send(embed=embed)
            except:
              embed=discord.Embed(title="Reminder deletion error",color=0x55a7f7)
              embed.add_field(name="Suggestion", value = "To use this find your reminders via !myreminders, and choose the reminder based on the value to the left of your reminder!\n E.G - !deletereminder 1", inline= True)
              await message.channel.send(embed=embed)










          
          if(messagereceived=="!deletetodo"):
           data=download_file('/droptodo.txt','ToDo.txt')
           try:
              todotoremove = secondPartOfMessage
              todotoremove = int(todotoremove)
              todotoremove = todotoremove - 1
                                
              a_file = open("ToDo.txt", "r")
              lines = a_file.readlines()
              a_file.close()
              #print(lines[1])
              #print(todotoremove)

              new_file = open("ToDo.txt", "w")
              i=0
              while( i < len(lines)):
                if(i != (todotoremove)):
                  new_file.write(lines[i])
                  
                else:
                  await message.channel.send(lines[i] + " - was removed")
                i=i+1

              new_file.close()
              upload_file('/droptodo.txt', 'ToDo.txt' )
              
           except:
              embed=discord.Embed(title="Trying to delete a To Do",color=0x55a7f7)
              embed.add_field(name="Usage", value = "To use this function use\n!deletetodo X\nX = The value of the Todo you would like to remove from !todolist", inline= True)
              await message.channel.send(embed=embed)
             
                               
            
            
                               
            
            
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
              valueofreminder = i + 1
              
              j=0
              lineoftext=""
              while (j < int(len(splitUpLine) - 1)):
                lineoftext = lineoftext + " " + splitUpLine[j]
                j=j+1
              
              savedToDo = savedToDo + str(valueofreminder) + "- " + lineoftext + " <@" + userofreminder + ">\n"


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
                textToSend = textToSend + str(j + 1) + " - " + reminders[j] + " - " + str(dayofreminding[j]) + "/" + str(monthofreminding[j]) + "/" + str(yearofreminding[j]) + " at " + str(timetosendreminder[j]) +" UTC - <#" + str(channeltosend[j]) + ">\n"
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
            timechecker=0
            counter=0
            

            
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
              timetoadd=""
              new_time = date_and_time
              i=0
              #Sets reminder if time value is set
              if( reminder != "none" and (timevalue in timevaluechecker)):
                while(i < len(reminder)):
                  if(reminder[i] == "s" or reminder[i] == "m" or reminder[i] == "h" or reminder[i] == "d"):
                    if (reminder[i] == "s"):
                      timetillremidningyou = timetoadd
                      timechecker = timechecker + int(timetoadd)
                      timetoadd=""
                      counter = counter + 1
                      if(i == len(reminder) - 1):
                        embed.add_field(name="Reminder set, reminding in - " + reminder , value=remindertosave, inline=True)
                        embed2.add_field(name="Your reminder!", value=remindertosave,inline=True)
                      #calculate time for reminder
                      time_change = datetime.timedelta(seconds=int(timetillremidningyou))
                      new_time = new_time + time_change
                    
                    if(reminder[i] == "m"):
                      timetillremidningyou = timetoadd
                      timechecker = timechecker + (int(timetoadd) * 60)
                      timetoadd=""
                      counter = counter + 1
                      if(i == len(reminder) - 1):
                        embed.add_field(name="Reminder set, reminding in - " + reminder, value=remindertosave, inline=True)
                        embed2.add_field(name=
                        "Your reminder!", value=remindertosave,inline=True)
                      timetillremidningyou = int(timetillremidningyou) * 60
                      #calculate time for reminder
                      time_change = datetime.timedelta(seconds=int(timetillremidningyou))
                      new_time = new_time + time_change

                    if(reminder[i] =="h"):
                      timetillremidningyou = timetoadd
                      timechecker = timechecker + (int(timetoadd) * 60 * 60)
                      timetoadd=""
                      counter = counter + 1
                      if(i == len(reminder) - 1):
                        embed.add_field(name="Reminder set, reminding in - " + reminder, value=remindertosave, inline=True)
                        embed2.add_field(name="Your reminder!", value=remindertosave,inline=True)
                      timetillremidningyou = int(timetillremidningyou) * 60 * 60
                      #calculate time for reminder
                      time_change = datetime.timedelta(seconds=int(timetillremidningyou))
                      new_time = new_time + time_change
                    
                    if(reminder[i]=="d"):
                      timetillremidningyou = timetoadd
                      timechecker = timechecker + (int(timetoadd) * 60 * 60 * 24)
                      timetoadd=""
                      counter = counter + 1
                      if(i == len(reminder) - 1):
                        embed.add_field(name="Reminder set, reminding in - " + reminder, value=remindertosave, inline=True)
                        embed2.add_field(name="Your reminder!", value=remindertosave,inline=True)
                      
                      timetillremidningyou = int(timetillremidningyou) * 60 * 60 * 24
                      #calculate time for reminder
                    
                      time_change = datetime.timedelta(seconds=int(timetillremidningyou))
                      
                      new_time = new_time + time_change
                  else:
                    timetoadd = timetoadd + str(reminder[i])
                  i=i+1
                  
                  

                  

              #Adding reminder to the text file
              userID = message.author.id
              userID = str(userID)
              channelToSend = str(channelDataID)
              textToSend = str(remindertosave)

              if(counter > 0):
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
              if(counter > 0):
                timetosleep = int(timechecker)
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

          if(messagereceived =="!resetdt2"):
            data = download_file('/dropdotatournament2.txt', 'dotatournament2.txt')
            f=open("dotatournament2.txt", "w")
            f.write("none")
            f.close()
            upload_file('/dropdotatournament2.txt', 'dotatournament2.txt')
            await message.channel.send("The tournament currently tracked has been removed")
          
          if(messagereceived=="!verifydturl2"):
            data = download_file('/dropdotatournament2.txt', 'dotatournament2.txt')
            f=open("dotatournament2.txt", "r")
            link = f.read()
            await message.channel.send("The link currently stored is - <" + link + ">")

          if(messagereceived=="!changedt2"):
            try:
              data = download_file('/dropdotatournament2.txt', 'dotatournament2.txt')
            except:
              print("lol")
            newlink = secondPartOfMessage
            f=open("dotatournament2.txt", "w")
            f.write(newlink)
            f.close()
            upload_file('/dropdotatournament2.txt', 'dotatournament2.txt')
            await message.channel.send("The tournament tracked has been updated to the link you have sent - <" + newlink + ">\n\nIf there is an error in your link, you are able to use !verifydturl to check the link or try changing again!")
            
            
              
          
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
            willshelp2 = "!dotastreams / !dotastreams2 [B-streams if we're on there]- This will tell you the streams available for the next / current series of dota happening!\n !csgostreams - This will tell you the next / current CSGO games streams\n !valostreams - This will tell you the streams for the current / next Valorant series"
            willshelp3= "!nextdt - This will tell you the next game coming up in the currently tracked tournament\n\nAs a gardener you also gain access to commands found in: '!gardenerhelp'"
            willshelp4 = "!teaminfo - Use this to get info on a dota team you're looking for\nE.G - !teaminfo EG, this will give the information on EG\n!playerinfo - Use this to get information on a player"
            willshelp5 = "!dtstreams / !dtstreams2 - This will collect the streams listed on the page of the tournaments being tracked for !nextdt / !nextdt2"

            embed=discord.Embed(title="The commands I work with", color=0xff8800)
            embed.add_field(name="The next OG games", value=willshelp1, inline=True)
            embed.add_field(name="The streams for games", value=willshelp2, inline=False)
            embed.add_field(name="The streams for tournament tracked", value=willshelp5, inline=False)
            embed.add_field(name="Next game in tournament", value =willshelp3, inline=False)
            embed.add_field(name="Team / player info", value=willshelp4, inline=False)
            await message.channel.send(embed=embed) 


          if ((messagereceived =="!gardenerhelp")):
            GardenerHelp9 = "!verifydturl / !resetdt / !changedt\n\n!verifydturl - This will tell you the currently tournament link being tracked\n!resetdt - This will the currently tracked tournament\n!changedt - This will change the tournament being tracked to the URL provided"
            GardenerHelp4 = "!DotaBo1 / Bo3 / Bo5 \n \n !CSGOBo1 / Bo3 / Bo5 \n \n !ValoBo1 / Bo3 / Bo5 \n \n These will create the roles required to host a predictions game, purely type the one required, e.g - \n !CSGOBo3 \n \n"

            GardenerHelp5 = "!deleteDotaBo1 / Bo3 / Bo5 \n \n !deleteCSGOBo1 / Bo3 / Bo5 \n \n !deleteValoBo1 / Bo3 / Bo5 \n \n These will delete the roles that were made for the prediction game e.g - \n !deleteCSGOBo3 will delete the CSGOBo3 roles \n \n"

            GardenerHelp6 = "!avatar - You're able to see the avatars of any user / yourself, if you ping nobody it'll show your own avatar, if you ping someone it will show theirs\n\n!server_badge - This will get your the icon used for the server icon"

            GardenerHelp7 = "!dotastreams / !csgostreams / !valostreams - these will tell you the streams available for the next match of OG Dota / CSGO / Valorant respectively\n\n"

            GardenerHelp8 = "!copyover [channel to copy from here] - use this command to copy the content of a channel from 1 to another, the command will send the last 100 messages from a channel to the channel the command is being used in\n\nE.G of usage - !copyover 847832196294115349\nThis will give you the value from a copy test, the bot must be in both servers if copying from a different server"

            GardenerHelp10 = "!reminder - This command will let you set reminders for future you, the bot will remind you in the channel it is used in after a set amount of time! Use !reminder to find more information!\n!myreminders - This command will tell you your currently saved reminders and when they are going to be sent\n!deletereminder - This will allow for you to remove a reminder of your choice, choose the reminder you want to delete by checking for it on !myreminders and then using it for example like - !deletereminder 1\n!snooze - This will let you reset the reminder you received last, you will need to specify a new time the same way you did for !reminder, example !snooze 5m - will remind you again in 5 minutes"

            GardenerHelp11 = "!todolist - This will list the current to do list for the bot\n!addtodo - This will add to the todolist the test following the command\n!deletetodo - This will delete the 'todo' that is attached to the number chosen, find the to-do values using !todolist"
            
            embed=discord.Embed(title="The commands you get as a Gardener!", color=0xff8800)
            embed.add_field(name="Getting game streams",value=GardenerHelp7, inline=True)
            embed.add_field(name="Creating the roles for prediction games", value=GardenerHelp4, inline=False)
            embed.add_field(name="Delete the roles that were used for a prediction game", value=GardenerHelp5, inline=False)
            embed.add_field(name="Viewing avatars of users", value=GardenerHelp6, inline=False)
            embed.add_field(name="Tracking a tournament", value=GardenerHelp9, inline=False)
            embed.add_field(name="Reminders", value=GardenerHelp10, inline=False)
            embed.add_field(name="Copying data", value=GardenerHelp8, inline=False)
            embed.add_field(name="To-Do / suggestion list", value=GardenerHelp11, inline=False)
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
  data = download_file('/droplastmessage.txt', 'lastmessage.txt')
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
    csgodata = CSGOCheck(720263155460079767)
    #return(teams, timeofgame, datep3, time2, matchlink, link4tourni, embed)
    timeToGame = csgodata[3]
    try:
      timeToGame = timeToGame.rsplit(":")
      timeToGame = timeToGame[0]
      if(timeToGame[-1] != "d"):
        embed = csgodata[6]
        channel2 = client.get_channel(847601411340501019)
        await channel2.send(embed=embed)

    except:
      print("No CSGO game")
  except:
    test = "test"

 
    
      


client.run(os.getenv('TOKEN'))
server.server()

