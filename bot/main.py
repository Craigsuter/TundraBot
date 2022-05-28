import discord
import os
#import pynacl
#import dnspython
import server
from discord.ext import commands
#imports
import csv
from urllib.request import urlopen as uReq
#from bs4 import BeautifulSoup as soup
import os
from playerstats import csgoplayerstat, dotaplayerstats, valoplayerstats
import ffmpeg
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from dotenv import load_dotenv
from discord.utils import get
load_dotenv()
import datetime
from time import strptime
import asyncio
import youtube_dl
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
from tournamentcheckers import DotaCheckTourni
from tournamentchecker2 import DotaCheckTourni2
from dropboxUploader import upload_file
from dropboxUploader import download_file
import liquipediapy
from stream2 import DotaStreams2
from dtStreams import dtStreams
import random
from csmap import csgomap
from valomaps import valomaps
from lastcs import lastcsgo
from lastvalo import lastvalo
from CSEvents import csgoevents
from dota_events import dotaevents
from csgoscoreboarding import scoreboarding
from csgoscoreboarding import scoreboardreader
from csgoscoreboarding import scoreboardadder
from csgoscoreboarding import scoreboardsingle
from dotascoreboarding import dotascoreboarding
from dotascoreboarding import dotascoreboardreader
from dotascoreboarding import dotascoreboardadder
from dotascoreboarding import dotascoreboardsingle
from valoscoreboarding import valoscoreboarding
from valoscoreboarding import valoscoreboardreader
from valoscoreboarding import valoscoreboardadder
from valoscoreboarding import valoscoreboardsingle
from testscoreboarding import testscoreboarding
from testscoreboarding import testscoreboardreader
from testscoreboarding import testscoreboardsingle
from testscoreboarding import testscoreboardadder
from cstour import next_cst
from cstour import change_cst
from cstour import getcs_url

#sets up command prefix
intents = discord.Intents().all()
client = commands.Bot(command_prefix='!', intents=intents)

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
    await client.change_presence(activity=discord.Game(
        name="catching snowflakes on my tongue"))

    #Starts schedule
    scheduler = AsyncIOScheduler()
    #Post on the day of a game
    try:
        scheduler.add_job(testingspam, CronTrigger(minute="10, 20, 30, 35, 40, 50"))
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
        #scheduler.add_job(cleanreminders, CronTrigger(minute="0, 30"))
        print("Clean reminder file success")
    except:
        print("Clear reminders file schedule failed")
    scheduler.start()

    data = download_file('/dropreminders.txt', 'reminders.txt')
    a_file = open("reminders.txt", "r")
    list_of_lines = a_file.readlines()
    i = 0

    reminders = []
    while (i < len(list_of_lines)):

        base_reminder = list_of_lines[i]
        splitUpValues = base_reminder.rsplit(", ")

        checkIfSent = splitUpValues[4]
        checkIfSent = checkIfSent[0:2]

        if (checkIfSent == "no"):
            reminders.append(base_reminder + ", " + str(i))

        i = i + 1

    i = 0

    tasks = []

    while i < len(reminders):
        tasks.append(asyncio.create_task(reminder(reminders[i])))

        i = i + 1
    print("There were: " + str(i) + " reminders started up")
    await asyncio.gather(*tasks)


#Will delete the latest message from a user
@client.event
async def on_member_update(before, after):
    guild = after.guild.id
    guild2 = after.guild
    info = ("<@" + str(after.id) + ">")
    #Only checks this guild

    if (guild == 798487245920141322 or guild == 731631689826041878):

        #If user gets given a new role
        if len(before.roles) < len(after.roles):
            newRole = next(role for role in after.roles
                           if role not in before.roles)

            #If user gets added to 'Muted' role
            if (newRole.name == "Muted"):

                #channel to get messages from [so will be General in main server]
                c = client.get_channel(689865754354384996)

                i = 0
                counter = 0
                if (i < 1):
                    for channel in guild2.text_channels:
                        try:
                            c = client.get_channel(channel.id)
                            messages = [messhis async for messhis in c.history(limit=100)]
                            i = 0

                            #Will delete the latest message from the user
                            for message in messages:
                                user = message.author.id

                                if user == after.id and i < 1:
                                    #channelID , messageid
                                    try:
                                        channelofdel = client.get_channel(
                                            channel.id)
                                        msgtodelete = await channelofdel.fetch_message(
                                            message.id)
                                        await client.http.delete_message(
                                            channel.id, message.id)
                                        counter = counter + 1
                                        i = i + 1
                                    except:
                                        i = i + 1
                                        print("No access to channel")
                        except:
                            i = i + 1

                channel = client.get_channel(867689528667144232)

                if guild == 798487245920141322 and counter == 0:
                    guildofdel = client.get_guild(798487245920141322)
                    member = guildofdel.get_member(after.id)
                    await member.ban(reason="Spam bot")
                    bannedlist = [
                        'https://cdn.discordapp.com/emojis/704664998307168297.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/853134498631647262.webp?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/666320711266205717.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/760839234243395595.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/838414946320515142.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/740935957972254873.webp?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/627835162910261269.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/746678657493237760.webp?size=96&quality=lossless'
                    ]
                    embed = discord.Embed(title="User was banned: " +
                                          str(info),
                                          color=0xff8800)
                    embed.set_thumbnail(url=random.choice(bannedlist))
                    embed.add_field(name="The action that happened",
                                    value="**Banned**",
                                    inline=False)
                    await channel.send(embed=embed)

                elif guild == 798487245920141322 and counter == 1:

                    mutelist = [
                        'https://cdn.discordapp.com/emojis/754439381703589958.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/734030265248382986.webp?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/827576073382264862.webp?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/517470041856540685.webp?size=96&quality=lossless'
                    ]
                    embed = discord.Embed(title="User was Muted: " + str(info),
                                          color=0xff8800)
                    embed.set_thumbnail(url=random.choice(mutelist))
                    embed.add_field(name="The action that happened",
                                    value="**Muted**",
                                    inline=False)
                    embed.add_field(name="We have removed - " + str(counter) +
                                    " message[s] - with the following text",
                                    value= "```" + msgtodelete.content + "```" ,
                                    inline=False)
                    await channel.send(embed=embed)

                else:
                    await channel.send(
                        str(info) +
                        " - user got muted in the main server, messages removed: "
                        + str(counter))

            #Deletes messages when user gets Seeds role
            if (newRole.name == "Tribe Gatherer"):
                c = client.get_channel(980144504000626698)
                messages = [messhis async for messhis in c.history(limit=30)]
                i = 0
                #creates a collection of messahes
                for message in messages:
                    user = message.author.id
                    #checks if message and the person who got Seeds is the same person deleting the messages
                    if user == after.id:
                        await client.http.delete_message(
                            980144504000626698, message.id)
                        i = i + 1


#Starts the bot up to check for messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.bot:
        if message.channel.id == 892880084111855620:
            dictionary = message.embeds[0].to_dict()
            #dict2 = dictionary.get('author').get('name')
            #print(dict2)
            return
        else:
            return

    guild = message.guild

    #All commands that are blocked to none admins are found in here
    global currenttime
    global currentH
    global currentM
    global currentd
    global dotadailypost
    global csgodailypost
    global valodailypost
    currenttime = datetime.datetime.now()
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
    author = message.author
    areadmin = author.guild_permissions.administrator

    global my_url5
    global my_url6
    global my_url7

    #Gets segments of every message - full message found in 'fullMEssage to avoid over use of Discord API'
    fullMessage = message.content
    nexttrans = fullMessage
    sectionsofmessage = fullMessage.rsplit(" ")
    introtomessage = sectionsofmessage[0]
    first_char = introtomessage[0]
    channelDataID = message.channel.id

    #Getting the 2nd part of a message
    try:
        secondPartOfMessage = sectionsofmessage[1]
        url = secondPartOfMessage
    except:
        url = "none"
        secondPartOfMessage = "none"

    try:
        thirdPartOfMessage = sectionsofmessage[2]
        
    except:
        thirdPartOfMessage = "none"
        

    messagetolower = introtomessage
    messagereceived = messagetolower.lower()
    mention = f'<@!{client.user.id}>'
    #Checks for a ping of the bot
    if ((mention in message.content) and (messagereceived[0] != '!')):
        await message.channel.send(
            "Im up! Im up! Are you okay... cool... co... <:OGmonkaThink:821509791523930162> "
        )

    #if(channelDataID == 926219724868681749):
    #member = message.author
    #role = discord.utils.get(member.guild.roles, name="2021celebration")
    #await member.add_roles(role)

    #Verifies that message is command usage
    if (first_char == "!"):


        if (messagereceived == "!dtstreams"):
            data = download_file('/dropdotatournament.txt',
                                 'dotatournament.txt')
            f = open("dotatournament.txt", "r")
            my_url = f.read()
            f.close()
            dtstreaminfo = dtStreams(my_url)
            streamlinks = dtstreaminfo[0]
            urloftourni = dtstreaminfo[1]

            embed = discord.Embed(title="Streams for the tournament",
                                  color=0x55a7f7)
            embed.add_field(name="Streams", value=streamlinks, inline=True)
            embed.add_field(name="Where I found the streams",
                            value=urloftourni,
                            inline=False)
            await message.channel.send(embed=embed)


        if (messagereceived == "!show"
                  and (str(secondPartOfMessage).lower() == "dota"
                       or str(secondPartOfMessage).lower() == "dota2")
                  and message.mentions.__len__() == 0):
              test = dotascoreboardreader(thirdPartOfMessage)
              embed = discord.Embed(title="Dota 2 prediction leaderboard",
                                    color=0x55a7f7)
              embed.add_field(name="Dota 2 Prediction - page: " + str(test[2]) + "/" + str(test[1]),
                              value="```\n" + test[0] + "\n```",
                              inline=True)
              embed.add_field(
                  name="Can't see yourself?",
                  value=
                  "Can't see yourself on the table? use !show dota @*yourself* to see where you stand!",
                  inline=False)
              await message.channel.send(embed=embed)

        if ((messagereceived == "!show")
                  and (str(secondPartOfMessage).lower() == "dota"
                       or str(secondPartOfMessage).lower() == "dota2")
                  and (message.mentions.__len__() > 0)):
              for user in message.mentions:
                  test = dotascoreboardsingle(user.id)
                  await message.channel.send(test)




        #Gets the info for the next dota game
        if ((messagereceived == "!nextdota")
                or (messagereceived == "!nextdoto")
                or (messagereceived == "!nextdota2") or (messagereceived == "!nextdotes")):
            try:
              embed = DotaCheck(channelDataID)
              embed = embed[0]
              if ((channelDataID ==867690069981003807)):
                  userID = message.author.id
                  userID = str(userID)
                  await message.reply("<@" + userID + "> " + embed)
              else:
                  await message.reply(embed=embed)
            except:
              if ((channelDataID == 867690069981003807)):
                await message.reply("No games planned currently - For more information use !nextdota in <#721391448812945480>")
              else:
                embed=discord.Embed(title="Tundra Dota's next game", url="https://liquipedia.net/dota2/Tundra_Esports", color=0xf10909)
                embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/7/7d/Tundra_Esports_2020_allmode_full.png/600px-Tundra_Esports_2020_allmode_full.png")
                embed.add_field(name="Time remaining", value = "No games currently planned" , inline=False)
                embed.add_field(name="Notice",value="Please check Liquipedia by clicking the title of this embed for more information as the time might not be accurate", inline=False)
                embed.add_field(name="Links", value="Tundra Liquipedia: https://liquipedia.net/dota2/Tundra_Esports", inline=False)
                await message.reply(embed=embed)
              


        #Used for checking the next game in Dota Tourni
        if (messagereceived == "!nextdt" or messagereceived == "!nextdteuw"):
            embed = DotaCheckTourni(channelDataID)
            embed = embed[0]
            if ((channelDataID == 867690069981003807)
                    or (channelDataID == 867690069981003807)):
                userID = message.author.id
                userID = str(userID)
                await message.reply("<@" + userID + "> " + embed)
            else:
                await message.reply(embed=embed)



        if messagereceived == "!dotastats":
          embed = dotaplayerstats(secondPartOfMessage)
          await message.reply(embed=embed)


        
        #None mod commands
        if (author.guild_permissions.administrator == False):

            #Commands that are Moderator only
            blockedcommands = [
                "!deletedotabo1", "!deletedota2bo1", "!deletecsgoBo1",
                "!deletevalobo1", "!deletevalorantbo1", "!deletedotabo3",
                "!deletedota2bo3", "!deletecsgobo3", "!deletevalobo3",
                "!deletevalorantbo3", "!deletedotabo5", "!deletedota2bo5",
                "!deletecsgobo5", "!deletecsgobo5", "!deletevalobo5",
                "!deletevalorantbo5", "!dotabo1", "!dotabo3", "!dotabo5",
                "!csgobo1", "!csgobo3", "!csgobo5", "!valobo1", "!valobo3",
                "!valobo5", "!changedt", "!resetdt", "!verifydurl",
                "!changecst", "!changevt", "!resetvt", "!verifyvurl",
                "!resetcst", "!verifycsurl", "!copyover", "!gardenerhelp",
                "!cleardota"
            ]

            if (messagereceived in blockedcommands):
                await message.channel.send("No role access")

            

            #Checks if user tries using !nextmatch incorrectly
            if ((messagereceived == "!nextgame")
                    or (messagereceived == "!game")
                    or (messagereceived == "!nextmatch")
                    or (messagereceived == "!match")
                    or (messagereceived == "!next")):
                embed = discord.Embed(title="Tundra Snowflake", color=0xd57280)
                embed.set_thumbnail(url="https://i.imgur.com/YJfbFth.png")
                embed.add_field(
                    name="Asking for game information",
                    value=
                    "To get game information do be sure to use !nextdota",
                    inline=True)
                await message.channel.send(embed=embed)

            


            

            if (messagereceived == "!dotastreams"):
                streaminfo = DotaStreams()
                Teams1 = streaminfo[0]
                Teams2 = streaminfo[1]
                flagMessage = streaminfo[2]
                convertedURL = streaminfo[3]

                if (Teams1 == "No games found"):
                    embed = discord.Embed(
                        title="No Dota streams / games were found",
                        color=0xf10909)
                    embed.add_field(
                        name="What you can try",
                        value=
                        "You can try using !nextdota / !nextdota2 to see if there are any games coming up",
                        inline=True)
                    embed.add_field(name="Links",
                                    value="https://liquipedia.net/dota2/Tundra_Esports",
                                    inline=False)
                    await message.reply(embed=embed)

                else:
                    embed = discord.Embed(title="Dota streams found!",
                                          color=0xf10909)
                    embed.add_field(name="The game found",
                                    value=Teams1 + " vs " + Teams2,
                                    inline=True)
                    embed.add_field(name="Streams available",
                                    value=flagMessage,
                                    inline=False)
                    embed.add_field(name="Where I found the streams",
                                    value=convertedURL,
                                    inline=False)
                    await message.reply(embed=embed)

            if ((messagereceived == "!discordstats")
                    and (message.mentions.__len__() == 0)):
                user = message.author
                createdon = user.created_at
                joinedon = user.joined_at
                cyear = createdon.year
                cmonth = createdon.month
                cday = createdon.day
                chour = createdon.hour
                cminute = createdon.minute
                csecond = createdon.second
                timecreation = str(cday) + "/" + str(cmonth) + "/" + str(
                    cyear) + " - " + str(chour) + ":" + str(
                        cminute) + ":" + str(csecond)

                jyear = joinedon.year
                jmonth = joinedon.month
                jday = joinedon.day
                jhour = joinedon.hour
                jminute = joinedon.minute
                jsecond = joinedon.second

                if (str(message.author.id) == "733626039002988574"):
                    timejoining = " 11/12/2020 - 16:54"
                else:
                    timejoining = str(jday) + "/" + str(jmonth) + "/" + str(
                        jyear) + " - " + str(jhour) + ":" + str(
                            jminute) + ":" + str(jsecond)

                embed = discord.Embed(title="Account information of - " +
                                      str(user.display_name),
                                      color=0x55a7f7)
                embed.add_field(name="Account details",
                                value="User account was created on - " +
                                str(timecreation) +
                                "\nJoined the server on- " + str(timejoining),
                                inline=True)
                await message.channel.send(embed=embed)

            

            return

        # All gardener commands
        else:
            


            if(messagereceived=="!cleardotaevent"):
              f = open("dotaevent.txt", "w")
              f.write("empty")
              f.close()
              upload_file('/dotaevent.txt', 'dotaevent.txt')
              await message.channel.send("Event cleared")

            
            if(messagereceived=="!dotadiscordevent"):
              try:
                value = DotaCheck(0)
                Teams = value[1]
                name = "Dota 2 game: " + Teams
                time=datetime.datetime.now().astimezone() + value[3]
                end_time=time+datetime.timedelta(minutes=10)
                linktogame = value[7]
                tourniname = value[6]
                streaminfo = DotaStreams()
                
                flagMessage = streaminfo[2]
                description = tourniname +"\n" + flagMessage + "\n:mega: https://twitter.com/TundraEsports\n"
                
                linetocheck = Teams+","+linktogame

                try:
                  download_file('/dotaevent.txt', 'dotaevent.txt')
                  f=open('dotaevent.txt', 'r')
                  lines=f.readlines()
                  f.close()
                except:
                  lines="empty"

                try:
                  if lines[0] == linetocheck:
                    await message.channel.send("Event has already been added")
                    pass
                  else:
                    await guild.create_scheduled_event(name=name, description=description, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=linktogame)
                    f = open("dotaevent.txt", "w")
                    f.write(linetocheck)
                    f.close()
                    upload_file('/dotaevent.txt', 'dotaevent.txt')
                    await message.channel.send("Event made - you will need to share this in the event channel")
                    
                except:
                  await guild.create_scheduled_event(name=name, description=description, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=linktogame)
                  f = open("dotaevent.txt", "w")
                  f.write(linetocheck)
                  f.close()
                  upload_file('/dotaevent.txt', 'dotaevent.txt')
                  await message.channel.send("Event made - you will need to share this in the event channel")
                  pass
                
              
                
              except Exception as e:
                await message.channel.send("An error was hit during this process")
                print(e)



            if (messagereceived == "!dotawinners"):
              try:
                server = message.guild
                role_name = "Tribe Prophet"
                i = 0
                role_id = server.roles[0]
                display_names = []
                member_ids = []
                for role in server.roles:
                    if role_name == role.name:
                        role_id = role
                        break
                else:
                    await message.channel.send("Role doesn't exist")
                    return

                for member in server.members:
                    if role_id in member.roles:
                        i = i + 1
                        display_names.append(member.display_name)
                        member_ids.append(member.id)
                
                j=0
                for id in member_ids:
                  user = message.guild.get_member(id)
                  role = discord.utils.get(user.guild.roles, id=966648883813965864)
                  await user.remove_roles(role)
                  j=j+1
                print(j)
                await message.channel.send("I have removed the Tribe Prophet role from - " + str(j) + " people")
              except Exception as e:
                
                print(e)

              try:
                download_file('/dotascoreboard.csv', 'scoreboard14.csv')
                f = open('scoreboard14.csv', 'r')
                reader = csv.reader(f, delimiter=',')
                scorecheck = int(secondPartOfMessage)
                i=0
                additionalmessage=""
                for lines in reader:
                  if( int(lines[2]) == scorecheck or int(lines[2]) > scorecheck):
                    
                    try:
                      
                      i=i+1
                      user = message.guild.get_member(int(lines[1]))
                      additionalmessage = additionalmessage + "<@" + str(lines[1]) + "> / "
                      role = discord.utils.get(user.guild.roles, id=966648883813965864)
                      await user.add_roles(role)
                    except:
                      print("User no longer in server")
                  
                await message.channel.send("I have added the Tribe Prophet role to - " + str(i) + " people - you can use !getuserlist @ Tribe Prophet, to get a list of users with the role")
                await message.channel.send("This includes:\n```" + additionalmessage + "```")
              except Exception as e: 
                print(e)
                await message.channel.send("There was an error in command usage, to use command use !dotawinners X, replacing X with the score you want people to have minimum to be rewarded the role, using '5', would mean all people with 5 and more will get the role")



          
            

            if ((messagereceived == "!dotaadd")):
                download_file('/dotascoreboard.csv', 'scoreboard5.csv')
                if (len(sectionsofmessage) > 1):
                    await message.channel.send(
                        "Starting adding results this might take a while")
                    try:
                        server = message.guild
                        role_name = sectionsofmessage[1]
                        role_name = role_name[3:-1]
                        role_name = discord.utils.get(guild.roles,
                                                      id=int(role_name))
                        role_name = str(role_name)
                        i = 0
                        role_id = server.roles[0]
                        display_names = []
                        member_ids = []
                        file = open("filetosend.txt", "w")
                        file.close()
                        for role in server.roles:
                            if role_name == role.name:
                                role_id = role
                                break
                        else:
                            await message.channel.send("Role doesn't exist")
                            return
                        for member in server.members:
                            if role_id in member.roles:
                                i = i + 1
                                dotascoreboardadder(member.display_name,
                                                    member.id, 1, i)
                                display_names.append(member.display_name)
                                member_ids.append(member.id)
                        if (i == 0):
                            await message.channel.send(
                                "No one was found in that role!")
                        else:
                          upload_file('/dotascoreboard.csv', 'scoreboard6.csv')
                          await message.channel.send(
                              "I have added the results! This affected: " +
                              str(i) + " users")
                    except:
                        await message.channel.send(
                            "You need to tag the winning role: example !dotaadd @D9-0"
                        )
                else:
                    await message.channel.send(
                        "You need to tag the winning role: example !dotaadd @D9-0"
                    )

           
            if ((messagereceived == "!dotaremove")):
                if (len(sectionsofmessage) > 1):
                    download_file('/dotascoreboard.csv', 'scoreboard5.csv')
                    await message.channel.send(
                        "Starting adding results this might take a while")
                    try:
                        server = message.guild
                        role_name = sectionsofmessage[1]
                        role_name = role_name[3:-1]
                        role_name = discord.utils.get(guild.roles,
                                                      id=int(role_name))
                        role_name = str(role_name)
                        i = 0
                        role_id = server.roles[0]
                        display_names = []
                        member_ids = []
                        file = open("filetosend.txt", "w")
                        file.close()
                        for role in server.roles:
                            if role_name == role.name:
                                role_id = role
                                break
                        else:
                            await message.channel.send("Role doesn't exist")
                            return
                        for member in server.members:
                            if role_id in member.roles:
                                i = i + 1
                                dotascoreboardadder(member.display_name,
                                                    member.id, -1, i)
                                display_names.append(member.display_name)
                                member_ids.append(member.id)
                        if (i == 0):
                            await message.channel.send(
                                "No one was found in that role!")
                        else:
                            upload_file('/dotascoreboard.csv', 'scoreboard6.csv')
                            await message.channel.send(
                                "I have added the results! This affected: " +
                                str(i) + " users")
                    except:
                        await message.channel.send(
                            "You need to tag the winning role: example !dotaremove @D9-0"
                        )
                else:
                    await message.channel.send(
                        "You need to tag the winning role: example !dotaremove @D9-0"
                    )

            

  
            if (messagereceived == "!cleardotaboard"):
                dotascoreboarding()
                await message.channel.send("The Dota Leaderboard is reset")


            if ((messagereceived == "!gettingrolelist")):
                if (len(sectionsofmessage) > 1):
                    try:
                        server = message.guild
                        role_name = sectionsofmessage[1]
                        role_name = role_name[3:-1]
                        role_name = discord.utils.get(guild.roles,
                                                      id=int(role_name))
                        role_name = str(role_name)

                        role_id = server.roles[0]
                        display_names = []
                        member_ids = []
                        file = open("filetosend.txt", "w")
                        file.close()
                        for role in server.roles:
                            if role_name == role.name:
                                role_id = role
                                break
                        else:
                            await message.channel.send("Role doesn't exist")
                            return
                        for member in server.members:
                            if role_id in member.roles:
                                display_names.append(member.display_name)
                                member_ids.append(member.id)

                        print(member_ids)
                    except:
                        print("lol")

            if (messagereceived == "!getuserlist"):
                if (len(sectionsofmessage) > 1):
                    try:
                        server = message.guild
                        role_name = sectionsofmessage[1]
                        role_name = role_name[3:-1]
                        role_name = discord.utils.get(guild.roles,
                                                      id=int(role_name))
                        role_name = str(role_name)

                        role_id = server.roles[0]
                        display_names = []
                        member_ids = []
                        file = open("filetosend.txt", "w")
                        file.close()
                        for role in server.roles:
                            if role_name == role.name:
                                role_id = role
                                break
                        else:
                            await message.channel.send("Role doesn't exist")
                            return
                        for member in server.members:
                            if role_id in member.roles:
                                display_names.append(member.display_name)
                                member_ids.append(member.id)

                        i = 0
                        while (i < len(display_names)):
                            f = open("filetosend.txt", "a")
                            f.write("name: " + display_names[i] +
                                    " - their id number: " +
                                    str(member_ids[i]) + "\n")
                            f.close
                            i = i + 1

                        f = open("filetosend.txt", "r")
                        print(f.read())
                        await message.channel.send(
                            "Role returned: " + role_name + '!',
                            file=discord.File("filetosend.txt"))
                    except Exception as e:
                        await message.channel.send(
                            "Error in command usage please use !getuserlist @testingrole\nWhere the role is pinged with a space between it and the command name"
                        )
                else:
                    await message.channel.send(
                        "Please ping a role you wish to get a list for, example - !getuserlist @testingrole"
                    )




            if ((messagereceived == "!discordstats")
                    and (message.mentions.__len__() > 0)):
                for user in message.mentions:
                    createdon = user.created_at
                    joinedon = user.joined_at
                    cyear = createdon.year
                    cmonth = createdon.month
                    cday = createdon.day
                    chour = createdon.hour
                    cminute = createdon.minute
                    csecond = createdon.second
                    timecreation = str(cday) + "/" + str(cmonth) + "/" + str(
                        cyear) + " - " + str(chour) + ":" + str(
                            cminute) + ":" + str(csecond)

                    jyear = joinedon.year
                    jmonth = joinedon.month
                    jday = joinedon.day
                    jhour = joinedon.hour
                    jminute = joinedon.minute
                    jsecond = joinedon.second
                    timejoining = str(jday) + "/" + str(jmonth) + "/" + str(
                        jyear) + " - " + str(jhour) + ":" + str(
                            jminute) + ":" + str(jsecond)
                    if (str(user.id) == "733626039002988574"):
                        timejoining = " 11/12/2020 - 16:54"

                    embed = discord.Embed(title="Account information of - " +
                                          str(user.display_name),
                                          color=0x55a7f7)
                    embed.add_field(name="Account details",
                                    value="User account was created on - " +
                                    str(timecreation) +
                                    "\nJoined the server on- " +
                                    str(timejoining),
                                    inline=True)

                    await message.channel.send(embed=embed)

                    #await message.channel.send("<@" + str(user.id) + "> \nDiscord account created on - " + str(user.created_at) +"\nJoined the server on - " + str(user.joined_at))

            if ((messagereceived == "!discordstats")
                    and (message.mentions.__len__() == 0)):
                user = message.author
                createdon = user.created_at
                joinedon = user.joined_at
                cyear = createdon.year
                cmonth = createdon.month
                cday = createdon.day
                chour = createdon.hour
                cminute = createdon.minute
                csecond = createdon.second
                timecreation = str(cday) + "/" + str(cmonth) + "/" + str(
                    cyear) + " - " + str(chour) + ":" + str(
                        cminute) + ":" + str(csecond)

                jyear = joinedon.year
                jmonth = joinedon.month
                jday = joinedon.day
                jhour = joinedon.hour
                jminute = joinedon.minute
                jsecond = joinedon.second
                timejoining = str(jday) + "/" + str(jmonth) + "/" + str(
                    jyear) + " - " + str(jhour) + ":" + str(
                        jminute) + ":" + str(jsecond)
                if (str(message.author.id) == "733626039002988574"):
                    timejoining = " 11/12/2020 - 16:54"

                embed = discord.Embed(title="Account information of - " +
                                      str(user.display_name),
                                      color=0x55a7f7)
                embed.add_field(name="Account details",
                                value="User account was created on - " +
                                str(timecreation) +
                                "\nJoined the server on- " + str(timejoining),
                                inline=True)
                await message.channel.send(embed=embed)

            

            if (messagereceived == "!resetdt"):
                data = download_file('/dropdotatournament.txt',
                                     'dotatournament.txt')
                f = open("dotatournament.txt", "w")
                f.write("none")
                f.close()
                upload_file('/dropdotatournament.txt', 'dotatournament.txt')
                await message.channel.send(
                    "The tournament currently tracked has been removed")

            if (messagereceived == "!verifydturl"):
                data = download_file('/dropdotatournament.txt',
                                     'dotatournament.txt')
                f = open("dotatournament.txt", "r")
                link = f.read()
                await message.channel.send("The link currently stored is - <" +
                                           link + ">")

            if (messagereceived == "!changedt"):
                #data = download_file('/dropdotatournament.txt',
                                     #'dotatournament.txt')
                newlink = secondPartOfMessage
                f = open("dotatournament.txt", "w")
                f.write(newlink)
                f.close()
                upload_file('/dropdotatournament.txt', 'dotatournament.txt')
                await message.channel.send(
                    "The tournament tracked has been updated to the link you have sent - <"
                    + newlink +
                    ">\n\nIf there is an error in your link, you are able to use !verifydturl to check the link or try changing again!"
                )

        

            
            if ((messagereceived == "!nextgame")
                    or (messagereceived == "!game")
                    or (messagereceived == "!nextmatch")
                    or (messagereceived == "!next")):
                embed = discord.Embed(title="Tundra Snowflake Help", color=0xd57280)
                embed.set_thumbnail(url="https://i.imgur.com/YJfbFth.png")
                embed.add_field(
                    name="Asking for game information",
                    value=
                    "To get game information do be sure to use !nextdota / !nextcsgo / !nextvalo, you can get additional help using !goosehelp",
                    inline=True)
                await message.channel.send(embed=embed)


            if ((messagereceived == "!avatar")
                    and (message.mentions.__len__() > 0)):
                for user in message.mentions:
                    await message.channel.send(user.avatar)

            elif ((messagereceived == "!avatar")
                  and (message.mentions.__len__() == 0)):
                await message.channel.send(message.author.avatar)

            if ((messagereceived == "!deletedotabo1")
                    or (messagereceived == "!deletedota2bo1")):
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

            

            if ((messagereceived == "!deletedotabo3")
                    or (messagereceived == "!deletedota2bo3")):
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

            

            if ((messagereceived == "!deletedotabo5")
                    or (messagereceived == "!deletedota2bo5")):
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

            

            if ((messagereceived == "!deletedotabo2")
                    or (messagereceived == "!deletedota2bo2")):
                guild = message.guild
                try:
                    role_object = discord.utils.get(guild.roles, name="D2-0")
                    await role_object.delete()
                    await message.channel.send("D2-0 deleted")
                except:
                    await message.channel.send("D2-0 not found")

                try:
                    role_object = discord.utils.get(guild.roles, name="D1-1")
                    await role_object.delete()
                    await message.channel.send("D1-1 deleted")
                except:
                    await message.channel.send("D1-1 not found")

                try:
                    role_object = discord.utils.get(guild.roles, name="D0-2")
                    await role_object.delete()
                    await message.channel.send("D0-2 deleted")
                except:
                    await message.channel.send("D0-2 not found")

           
            if (messagereceived == "!dotabo1"):
                guild = message.guild
                await guild.create_role(name="D1-0")
                await message.channel.send("D1-0 created")
                await guild.create_role(name="D0-1")
                await message.channel.send("D0-1 created")

            if (messagereceived == "!dotabo3"):
                guild = message.guild
                await guild.create_role(name="D2-0")
                await message.channel.send("D2-0 created")
                await guild.create_role(name="D2-1")
                await message.channel.send("D2-1 created")
                await guild.create_role(name="D1-2")
                await message.channel.send("D1-2 created")
                await guild.create_role(name="D0-2")
                await message.channel.send("D0-2 created")

            if (messagereceived == "!dotabo2"):
                guild = message.guild
                await guild.create_role(name="D2-0")
                await message.channel.send("D2-0 created")
                await guild.create_role(name="D1-1")
                await message.channel.send("D1-1 created")
                await guild.create_role(name="D0-2")
                await message.channel.send("D0-2 created")

            

            if (messagereceived == "!dotabo5"):
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

            
            if (messagereceived == "!dotastreams"):
                streaminfo = DotaStreams()
                Teams1 = streaminfo[0]
                Teams2 = streaminfo[1]
                flagMessage = streaminfo[2]
                convertedURL = streaminfo[3]

                if (Teams1 == "No games found"):
                    embed = discord.Embed(
                        title="No Dota streams / games were found",
                        color=0xf10909)
                    embed.add_field(
                        name="What you can try",
                        value=
                        "You can try using !nextdota / !nextdota2 to see if there are any games coming up",
                        inline=True)
                    embed.add_field(name="Links",
                                    value="https://liquipedia.net/dota2/Tundra_Esports",
                                    inline=False)
                    await message.reply(embed=embed)

                else:
                    embed = discord.Embed(title="Dota streams found!",
                                          color=0xf10909)
                    embed.add_field(name="The game found",
                                    value=Teams1 + " vs " + Teams2,
                                    inline=True)
                    if(message.channel.id != 867690069981003807):
                      embed.add_field(name="Streams / Flags",
                                      value="```" + flagMessage + "```",
                                      inline=False)
                    embed.add_field(name="Streams available",
                                    value=flagMessage,
                                    inline=False)
                    embed.add_field(name="Where I found the streams",
                                    value=convertedURL,
                                    inline=False)
                    await message.reply(embed=embed)

            


    #new-member-support OG Main Discord
    if (channelDataID == 980144504000626698):
        embed = discord.Embed(title="Welcome to the Tundra Tribe!",
                              color=0xff8800)
        embed.add_field(
            name="You seem to be lost, let me help",
            value=
            "Do be sure to go through <#867689566572118036> to check out the rules of the server! Follow this up in <#935744075670360064> to get access to the rest of the server! See you in there!",
            inline=True)
        embed.set_image(url="https://i.imgur.com/uiNH28L.png")
        
        data = download_file('/droplastmessage.txt', 'lastmessage.txt')
        g = open("lastmessage.txt", "r")
        g2 = g.read()
        g.close()

        try:
            print("Tried to delete message: " + g2)

        except:
            print("Failed to delete any message")
        try:
            await client.http.delete_message(980144504000626698, g2)
        except:
            print("Failed to delete any message")
        message = await message.reply(embed=embed)
        f = open("lastmessage.txt", "w")
        f.write(str(message.id))
        f.close()
        upload_file('/droplastmessage.txt', 'lastmessage.txt')

    if (message.author == discord.Permissions.administrator):
        print("nice")



#Opening the file with last message every 5 mins
async def openingfile():
    data = download_file('/droplastmessage.txt', 'lastmessage.txt')
    g = open("lastmessage.txt", "r")
    g2 = g.read()
    g.close()
    print("File opened, value = " + g2)


#Daily posts
async def testingspam():
    
    c = client.get_channel(839466348970639391)
    currenttime = datetime.datetime.now()
   
    #Dota daily
    try:
      channel = client.get_channel(980148345030987806)
      value = DotaCheck(0)
      Teams = value[1]
      name = "Dota 2 game: " + Teams
      time=datetime.datetime.now().astimezone() + value[3]
      end_time=time+datetime.timedelta(minutes=10)
      linktogame = value[7]
      tourniname = value[6]
      streaminfo = DotaStreams()
      
      flagMessage = streaminfo[2]
      description = tourniname +"\n" + flagMessage + "\n:mega: https://twitter.com/TundraEsports\n"
      guild = client.get_guild(798487245920141322)
      linetocheck = Teams+","+linktogame

      try:
        download_file('/dotaevent.txt', 'dotaevent.txt')
        f=open('dotaevent.txt', 'r')
        lines=f.readlines()
        f.close()
      except:
        lines="empty"

      try:
        if lines[0] == linetocheck:
          
          pass
        else:
          eventdata = await guild.create_scheduled_event(name=name, description=description, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=linktogame)
          f = open("dotaevent.txt", "w")
          f.write(linetocheck)
          f.close()
          upload_file('/dotaevent.txt', 'dotaevent.txt')
          data2= await guild.fetch_scheduled_event(eventdata.id)
          await channel.send(data2.url)
          
      except:
        eventdata = await guild.create_scheduled_event(name=name, description=description, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=linktogame)
        f = open("dotaevent.txt", "w")
        f.write(linetocheck)
        f.close()
        upload_file('/dotaevent.txt', 'dotaevent.txt')
        data2= await guild.fetch_scheduled_event(eventdata.id)
        await channel.send(data2.url)
        pass

      
    
      
    except Exception as e:
      print(e)

    



  

client.run(os.getenv('TOKEN'))
server.server()
