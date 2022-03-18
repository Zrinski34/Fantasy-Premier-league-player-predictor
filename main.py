import requests
import pandas as pd

##### GLOBAL VARIABLES #######
FPL_DATA = 'https://fantasy.premierleague.com/api/bootstrap-static/'
FPL_FIXTURES = 'https://fantasy.premierleague.com/api/fixtures/'
LOGIN_URL = 'https://users.premierleague.com/accounts/login/'

# API connection data
headers = {
   'authority': 'users.premierleague.com' ,
   'cache-control': 'max-age=0' ,
   'upgrade-insecure-requests': '1' ,
   'origin': 'https://fantasy.premierleague.com' ,
   'content-type': 'application/x-www-form-urlencoded' ,
   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36' ,
   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' ,
   'sec-fetch-site': 'same-site' ,
   'sec-fetch-mode': 'navigate' ,
   'sec-fetch-user': '?1' ,
   'sec-fetch-dest': 'document' ,
   'referer': 'https://fantasy.premierleague.com/my-team' ,
   'accept-language': 'en-US,en;q=0.9,he;q=0.8' ,
}

payload = {
    'login':'matijadomjan@gmail.com',
    'password':'matac1111',
    'redirect_uri': 'https://fantasy.premierleague.com/',
    'app':'plfpl-web'
}

s = requests.session()
s.post(LOGIN_URL, data=payload, headers=headers)

# API Request function
def api_request(url_link):
    response = s.get(url_link)
    fpl_data = response.json()
    return fpl_data

# Getting players data
def get_player_data():
    player_data = api_request(FPL_DATA)
    print(player_data)

def get_teams_data():
    teams_data = api_request(FPL_DATA)
    list = []
    required_fields = ['id','name', 'strength_overall_home','strength_overall_away','strength_attack_home','strength_attack_away','strength_defence_home','strength_defence_away']
    for team in teams_data['teams']:
        dict_team_data = {key:value for key, value in team.items() if key in required_fields}
        list.append(dict_team_data)
    df = pd.DataFrame(list)
    return df


def get_fixtures_data():
    fixtures


def get_fixures_data():
    fixtures_data = api_request(FPL_FIXTURES)
    return fixtures_data





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_teams_data()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
