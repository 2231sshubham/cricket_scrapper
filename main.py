import sys
import requests
import subprocess

def install_requirements(requirements_file):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])

# Installing dependencies
install_requirements("requirements.txt")

# import asyncio
from bs4 import BeautifulSoup

# function to generate text files corresponding to different values
def write(fileName,data):
    try:
        # fileName = fileName+".txt"
        f = open(f"{fileName}.txt", "w")
        f.write(f"{data} ")
    except:
        raise Exception('An excpetion occured')

def stringify(array):
    ans = ""
    for i in array:
        ans += i.get_text()
    return ans

# user provided url
url = sys.argv[1]


# infinte loop to continously fetch values
while(True):
    try:
        page = requests.get(url,timeout=1000)
        soup = BeautifulSoup(page.content, "html.parser")
        # print(soup)

        # searching for section containing match description
        match_section = soup.find("div", class_="ds-bg-fill-content-prime")
        match_name = match_section.find("div", class_=['ds-text-tight-m', 'ds-font-regular', 'ds-text-ui-typo-mid']).get_text()
        write('match_name',match_name)
        # print(match_name)

        # seacrching for team details
        teams = match_section.find_all("div", class_="ci-team-score")
        team1 = teams[0].find('a', href=True).get_text()
        team2 = teams[1].find('a', href=True).get_text()
        write('team1', team1)
        write('team2', team2)
        # print(team1,team2)

        # searching for section containing score
        score_section = match_section.find_all('div', class_='ds-text-compact-m')
        score1 = ""
        score2 = ""

        #checking if the score section is present for teams
        if(len(score_section) == 2):
            score1 = score_section[0].get_text()
            score2 = score_section[1].get_text()
        elif(len(score_section) == 1):
            score1 = score_section[0].get_text()
        write('score1', score1)
        write('score2', score2)
        # print(score1,score2)

        # searching for over status section
        crr = match_section.find('div', class_='ds-text-tight-s').find_all('span')
        over_details = stringify(crr)

        write('CRR', over_details)

        # searching for commentary
        commentary_section = soup.find('div', id=f'{url}')
        commentary_section = commentary_section.find('div', class_='ds-ml-4').find_all("span")
        commentary = f"{commentary_section[0].get_text()}"
        write('commentary', commentary)

        # searching for match highlight section
        match_highlight_section = match_section.find("p", class_='ds-text-tight-m')
        match_highlight = match_highlight_section.find("span").get_text()
        write('match_highlight', match_highlight)

        # targeting scorecard section  
        scorecard_section = match_section.next_sibling.find('div', class_='ds-bg-fill-content-prime').find('div', class_='ds-p-0')
        scorecard_sub_section = scorecard_section.contents[1].find_all('tbody', class_='ds-text-right')
        batter_section = scorecard_sub_section[0].find_all('tr')
        bowler_section = scorecard_sub_section[1].find_all('tr')
        
        # batter section details
        for i,tr in enumerate(batter_section):
            td = tr.find_all('td')
            name = stringify(td[0].find_all('span'))     
            runs = td[1].find('strong').get_text()
            balls = td[2].get_text()
            fours = td[3].get_text()
            sixes = td[4].get_text()
            strike_rate = td[5].get_text()
            write(f'batter{i+1}_name', name)
            write(f'batter{i+1}_runs',runs)
            write(f'batter{i+1}_balls',balls)
            write(f'batter{i+1}_fours',fours)
            write(f'batter{i+1}_sixes',sixes)
            write(f'batter{i+1}_strike_rate', strike_rate)


        # bowler section details
        for i, tr in enumerate(bowler_section):
            td = tr.find_all('td')
            name = stringify(td[0].find_all('span'))
            overs = td[1].get_text()
            maidens = td[2].get_text()
            runs = td[3].get_text()
            wickets = td[4].get_text()
            economy = td[5].get_text()
            write(f'bowler{i+1}_name', name)
            write(f'bowler{i+1}_overs', overs)
            write(f'bowler{i+1}_maidens',maidens)
            write(f'bowler{i+1}_runs', runs)
            write(f'bowler{i+1}_wickets', wickets)
            write(f'bowler{i+1}_strike_rate', economy)

        scorecard_highlight_section = scorecard_section.contents[2].find_all('span')
        scorecard_highlight = stringify(scorecard_highlight_section)
        write('scorecard_highlight', scorecard_highlight)


        # searching for partnership section
        partnership_section = scorecard_section.contents[2]
        partnership = ""
        for string in partnership_section.stripped_strings:
            partnership += repr(string).strip("'")

        write('partnership', partnership)


        # searching for over history
        overHistory_section = scorecard_section.contents[3]
        overHistory = []
        for string in overHistory_section.strings:
            if(string  == "th"):
                ele = overHistory.pop()
                string = ele + "th"
            overHistory.append(repr(string).strip("'"))

        overHistory = ",".join(overHistory)
        write('overHistory', overHistory)
    except:
        print("An exception occured")
        break