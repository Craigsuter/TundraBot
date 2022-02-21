# imports
import discord
import requests
from bs4 import BeautifulSoup as soup
from datetime import date
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

load_dotenv()


def dotastats(name, url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        player_page = requests.get(url, headers=headers)
        page_html = soup(player_page.text, "html.parser")
        wl_record = page_html.find(
            "div", {"class": "player_stats"}).find("span").text
        player_picks = page_html.find_all("div", {"class": "meta-hero-card"})
        top5_picks_container = player_picks[:5]

        top5_picks_info = ""

        for pick_container in top5_picks_container:
            pick_info = pick_container.find_all(
                "div", {"class": "meta-pick-info-block"})
            pick_name = pick_container.find(
                "div", {"class": "meta-pick-title"}).text
            pick_matchcount = pick_info[0].next_element.strip()
            pick_winrate = pick_info[1].next_element.strip()
            top5_picks_info = top5_picks_info + \
                f'{pick_name}: {pick_matchcount} matches ({pick_winrate} Winrate) \n'

        player_stats = discord.Embed(
            title=f'{name} stats', url=url, color=0x55a7f7)
        player_stats.add_field(name="Win Lose", value=wl_record, inline=False)
        player_stats.add_field(
            name="Top 5 picks", value=top5_picks_info, inline=False)
        return player_stats
    except Exception as e:
        print(e)
        return "No Data found for this player"


def csstats(name, url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        today = date.today()
        three_months_ago = today - relativedelta(months=3)
        url = url + f'?startDate={three_months_ago}&endDate={today}'
        player_page = requests.get(url, headers=headers)
        page_html = soup(player_page.text, "html.parser")
        rating_kast_row = page_html.find_all(
            "div", {"class": "summaryStatBreakdownRow"})[0]
        adr_kpr_impact_row = page_html.find_all(
            "div", {"class": "summaryStatBreakdownRow"})[1]

        # Get the Rating 2.0
        rating_container = rating_kast_row.find_all(
            "div", {"class": "summaryStatBreakdown"})[0]
        player_rating = rating_container.find(
            "div", {"class": "summaryStatBreakdownDataValue"}).text

        # Get the KAST
        kast_container = rating_kast_row.find_all(
            "div", {"class": "summaryStatBreakdown"})[2]
        player_kast = kast_container.find(
            "div", {"class": "summaryStatBreakdownDataValue"}).text

        # Get the impact
        impact_container = adr_kpr_impact_row.find_all(
            "div", {"class":"summaryStatBreakdown"})[0]
        player_impact = impact_container.find(
            "div", {"class": "summaryStatBreakdownDataValue"}).text
      
        # Get the ADR
        adr_container = adr_kpr_impact_row.find_all(
            "div", {"class": "summaryStatBreakdown"})[1]
        player_adr = adr_container.find(
            "div", {"class": "summaryStatBreakdownDataValue"}).text

        # Get the KPR
        kpr_container = adr_kpr_impact_row.find_all(
            "div", {"class": "summaryStatBreakdown"})[2]
        player_kpr = kpr_container.find(
            "div", {"class": "summaryStatBreakdownDataValue"}).text

        # Get the KDR
        kdr_container = page_html.find_all(
            "div", {"class": "col stats-rows standard-box"})[0].find_all("div", {"class": "stats-row"})[3]
        player_kdr = kdr_container.find_all("span")[1].text

        # Get the image
        image_container = page_html.find(
            "div", {"class": "summaryBodyshotContainer"})
        player_image = image_container.find(
            "img", {"class": "summaryBodyshot"})['src']

        player_stats = discord.Embed(
            title=f'{name} stats', url=url, color=0xff8800)
        player_stats.set_thumbnail(url=player_image)
        player_stats.add_field(
            name="Rating 2.0", value=player_rating, inline=False)
        player_stats.add_field(name="Impact", value=player_impact, inline=False)
        player_stats.add_field(name="ADR", value=player_adr, inline=False)
        player_stats.add_field(name="KAST", value=player_kast)
        player_stats.add_field(name="KPR", value=player_kpr)
        player_stats.add_field(name="KDR", value=player_kdr)

        return player_stats

    except Exception as e:
        print(e)
        return "No Data found for this player"
