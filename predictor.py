import elo_data
import numpy as np
import api_data


def predictor_match_per_event(event):
    df_fix_predict = elo_data.fixtures_elo_prediction()
    df_elo_predict = df_fix_predict[(df_fix_predict["event"] == event) & (df_fix_predict["prediction_difference"] > 40.00)]
    df_elo_predict['favourites'] = np.where(df_elo_predict['home_team_elo']> df_elo_predict['away_team_elo'],
                                           df_elo_predict['home_team'], df_elo_predict['away_team'])
    return df_elo_predict


def predictor_player_per_event(event):
    df_favourite_team = predictor_match_per_event(event)
    df_players_data = api_data.get_players_data()
    df_players_data

    #player_df = player_df.sort_values(by='ict_index_rank', ascending=True)
    print(df_favourite_team)

if __name__ == '__main__':
    event = input("Please, insert fixture event :")
    predictor_player_per_event(int(event))




