import pandas as pd
import soccerdata as sd
import api_data

elo = sd.ClubElo()
elo_width = 400
#pd.set_option('display.max_columns', None)
#pd.set_option('mode.chained_assignment', None)

def get_elo():
    current_elo = elo.read_by_date()
    data_frame = (current_elo.loc[current_elo['league'] == 'ENG-Premier League'])
    df_elo = data_frame.drop(columns=['league'], axis = 1)
    df_elo_pl = df_elo.replace(to_replace=['Tottenham'], value =['Spurs'])
    return df_elo_pl

def get_fixures_elo_renking():
    fixtures = api_data.get_fixures_data()
    elo_ranking = get_elo()
    fixtures_elo_home_ranks = pd.merge(fixtures,elo_ranking,left_on='home_team',right_on='team', how='inner')
    fixtures_elo_all_ranks = pd.merge(fixtures_elo_home_ranks,elo_ranking,left_on='away_team',right_on='team', how='inner')
    fixtures_elo_all_ranks.rename(columns = { 'elo_x':'home_team_elo', 'elo_y':'away_team_elo', 'from_x':'from', 'to_x':'to'}, inplace = True, errors='ignore')
    fixtures_elo_all_ranks = fixtures_elo_all_ranks.drop(['rank_x', 'country_x','level_x','rank_y', 'country_y','level_y', 'from_y','to_y'], axis = 1)
    return fixtures_elo_all_ranks

def expected_result_home(home_team_elo, away_team_elo):
    """
    https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details
    """
    expect_a = 1.0/(1+10**((away_team_elo - home_team_elo)/elo_width))
    return expect_a

def expected_result_away(home_team_elo, away_team_elo):
    """
    https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details
    """
    expect_b = 1.0/(1+10**((home_team_elo - away_team_elo)/elo_width))
    return expect_b

def fixtures_elo_prediction():
    fixures_elo_renking = get_fixures_elo_renking()
    fixures_elo_renking['home_prediction'] = expected_result_home(fixures_elo_renking['home_team_elo'],fixures_elo_renking['away_team_elo']) * 100
    fixures_elo_renking['away_prediction'] = expected_result_away(fixures_elo_renking['home_team_elo'],fixures_elo_renking['away_team_elo']) * 100
    fixures_elo_renking['prediction_difference'] = abs(fixures_elo_renking['home_prediction']-fixures_elo_renking['away_prediction'])
    return fixures_elo_renking


if __name__ == '__main__':
    fixtures_elo_prediction()
