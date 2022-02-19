# imports
import requests
from bs4 import BeautifulSoup as soup
import discord
from dotenv import load_dotenv
load_dotenv()


def playerstats(name, url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        player_page = requests.get(url, headers=headers)
        page_html = soup(player_page.text, "html.parser")
        wl_record = page_html.find("div", {"class": "player_stats"}).find("span").text
        player_picks = page_html.find_all("div", {"class": "meta-hero-card"})
        top5_picks_container = player_picks[:5]

        top5_picks_info = ""

        for pick_container in top5_picks_container[:-1]:
            pick_info = pick_container.find_all("div", {"class": "meta-pick-info-block"})
            pick_name = pick_container.find("div", {"class": "meta-pick-title"}).text
            pick_matchcount = pick_info[0].next_element.strip()
            pick_winrate = pick_info[1].next_element.strip()
            top5_picks_info = top5_picks_info + f'{pick_name}: {pick_matchcount} ({pick_winrate} Winrate) \n'

        top5_picks_info = top5_picks_info + f'{pick_name}: {pick_matchcount} ({pick_winrate} Winrate)'
        player_stats = discord.Embed(title=f'{name} stats', url=url, color=0x55a7f7)
        player_stats.add_field(name="Win Lose", value=wl_record, inline=False)
        player_stats.add_field(name="Top 5 picks", value=top5_picks_info, inline=False)
        return player_stats
    except Exception as e:
        print(e)
        return "No Data found for this player"
