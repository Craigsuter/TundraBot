import datetime

# imports
import discord
import requests
from bs4 import BeautifulSoup as soup
from dotenv import load_dotenv

from dropboxUploader import download_file, upload_file
load_dotenv()

def getcs_url():
  try:
    download_file('/dropcsgotournament.txt', 'csgotournament.txt')
    f = open('csgotournament.txt')
    tournament_url = f.read()
    f.close()
    return tournament_url

  except Exception as e:
    print(e)
    return "Error occured trying to execute this command"
    

def next_cst(channelDataID):
  try:    
    # Get the tournament
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
    tournament_url = getcs_url()
    #tournament_url = "https://www.hltv.org/events/6137/matches"
    tournament_page = requests.get(tournament_url, headers=headers)
    tournament_html = soup(tournament_page.text, "html.parser")
    tournament_name = tournament_html.find("div", {"class": "event-hub-title"}).string

    # Next match in the tourney
    match_info_container = tournament_html.find("a", {"class": "match a-reset"})
    match_time_mili = match_info_container.find("div", {"class": "matchTime"})['data-unix']
    match_time_second = int(int(match_time_mili) / 1000)
    match_time = datetime.datetime.fromtimestamp(match_time_second)
    time_now = datetime.datetime.now()
    time_remaining = match_time - time_now
    time_note = "This is local to your timezone"

    # Get the teams
    team1_html = match_info_container.find("div", {"class": "matchTeam team1"})
    team2_html = match_info_container.find("div", {"class": "matchTeam team2"})
    team1 = team1_html.find("div", {"class": "matchTeamName text-ellipsis"}).string
    team2 = team2_html.find("div", {"class": "matchTeamName text-ellipsis"}).string

    # Build the embed
    if int(channelDataID) != 926214194280419368 and int(channelDataID) != 690952309827698749:
      notice = "Please check HLTV by clicking the title of this embed for more information as the time might not be accurate"
      nextcst = discord.Embed(title=f'Next game in {tournament_name}', url=tournament_url, color=0xff8800)
      nextcst.add_field(name=f'{team1} vs {team2}', value=f'<t:{match_time_second}:F> - {time_note}', inline=False)
      nextcst.add_field(name="Time remaining", value=f'{str(time_remaining)[:-7]}', inline=False)
      nextcst.add_field(name="Notice", value=notice, inline=False)
      nextcst.add_field(name="Links", value=tournament_url)
    else:
      nextcst = f'{team1} vs {team2} - Starts in {str(time_remaining)[:-7]} / In your local time: <t:{match_time_second}:F> - For more information use !nextcst in <#721391448812945480>'
      
    return nextcst
  
  except Exception as e:
    if channelDataID != 926214194280419368 and channelDataID != 690952309827698749:
      error_message = discord.Embed(title="No tournament is currently being tracked")
      
    else:
      error_message = "No tournament is currently being tracked"
    return error_message


def change_cst(url):
  try:
    download_file('/dropcsgotournament.txt', 'csgotournament.txt')
    f = open('csgotournament.txt', 'w')
    f.write(url)
    f.close()
    upload_file('/dropcsgotournament.txt', 'csgotournament.txt')
    return (url) 
  except Exception as e: 
    print (e)
    return (e)