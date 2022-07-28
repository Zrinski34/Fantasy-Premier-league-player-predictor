import elo_data
import numpy as np


def predictor_match_per_event(event):
    df_fix_predict = elo_data.fixtures_elo_prediction()
    df_elo_predict = df_fix_predict[(df_fix_predict["event"] == event) & (df_fix_predict["prediction_difference"] > 40.00)]
    df_elo_predict['favourites'] = np.where(df_elo_predict['home_team_elo']> df_elo_predict['away_team_elo'],
                                           df_elo_predict['home_team'], df_elo_predict['away_team'])
    print(df_elo_predict)




if __name__ == '__main__':
    event = input("Please, insert fixture event :")
    predictor_match_per_event(int(event))




