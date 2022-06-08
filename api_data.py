import requests
import pandas as pd
import elo_ranking

##### GLOBAL VARIABLES #######


FPL_DATA = 'https://fantasy.premierleague.com/api/bootstrap-static/'
FPL_FIXTURES = 'https://fantasy.premierleague.com/api/fixtures/'
LOGIN_URL = 'https://users.premierleague.com/accounts/login/'
MY_TEAM = 'https://fantasy.premierleague.com/api/my-team/1423649/'



pd.set_option('display.max_columns', None)
pd.set_option('mode.chained_assignment', None)
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
    'login':'johnny04.matija@gmail.com',
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

# Getting teams data
def get_teams_data():
    teams_data = api_request(FPL_DATA)
    list_teams = []
    required_fields = ['id','name', 'short_name','strength_overall_home','strength_overall_away','strength_attack_home','strength_attack_away','strength_defence_home','strength_defence_away']
    for team in teams_data['teams']:
        dict_team_data = {key:value for key, value in team.items() if key in required_fields}
        list_teams.append(dict_team_data)
    df = pd.DataFrame(list_teams)
    df = df.replace(to_replace=['Spurs','Man Utd'],value =['Tottenham','Man United'])
    return df

# Getting teams data
def get_fixures():
    fixtures_data = api_request(FPL_FIXTURES)
    required_fields = ['event','team_h', 'team_a']
    list_fixtures = []
    for fixture in fixtures_data:
        if fixture['event'] is not None:
            dict_fixtures = {key:value for key,value in fixture.items() if key in required_fields}
            list_fixtures.append(dict_fixtures)
    df = pd.DataFrame(list_fixtures)
    return df

def get_fixures_data():
    new_order = [0,2,1,3,4]
    df_fixtures = get_fixures()
    df_teams_data = get_teams_data()
    df_away = pd.merge(df_fixtures, df_teams_data[['id', 'name']],left_on='team_a',right_on='id',how='inner')
    df_home = pd.merge(df_away, df_teams_data[['id', 'name','strength_overall_home','strength_overall_away']],left_on='team_h',right_on='id',how='inner')
    df_home.rename(columns = { 'name_x':'away_team', 'name_y':'home_team'}, inplace = True, errors='ignore')
    df_fixtures = df_home.sort_values(by='event', ascending=True)
    df_fixtures = df_fixtures.drop(['id_x', 'id_y','team_a','team_h'], axis = 1)
    df_fixtures = df_fixtures[df_fixtures.columns[new_order]]
    return df_fixtures




def get_players_data():
    fpl_data = api_request(FPL_DATA)
    required_fields = ['id','first_name','second_name','team','ict_index', 'influence_rank', 'influence_rank_type','creativity_rank','creativity_rank_type', 'threat_rank', 'total_points','now_cost','selected_by_percent', 'minutes', 'points_per_game','total_points', 'goals_scored','assists','clean_sheets','goals_conceded']
    list = []
    for data in fpl_data['elements']:
        dict2 = {key:value for key, value in data.items() if key in required_fields}
        list.append(dict2)
    players = pd.DataFrame(list)
    teams = get_teams_data()
    players_data = pd.merge(players, teams[['id', 'name']],left_on='team',right_on='id',how='inner')
    return players_data


def get_players_my_current_element():
    my_team_elements = [559,234,224,585,256,368,141,22,251,359,180,146,20,503,450]
    return my_team_elements


def get_current_players_data():
    my_team_element = get_players_my_current_element()
    players = get_players_data()
    df_player_data = players[players['id_x'].isin(my_team_element)]
    df_player_data.rename(columns = { 'id_x':'fpl_id', 'name':'club'}, inplace = True, errors='ignore')
    df_player_data = df_player_data.drop(['team', 'id_y'], axis = 1)
    print(df_player_data)

if __name__ == '__main__':
    get_fixures_elo_renking()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
