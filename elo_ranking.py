import pandas as pd
import soccerdata as sd

elo = sd.ClubElo()
pd.set_option('display.max_columns', None)
pd.set_option('mode.chained_assignment', None)

def get_elo():
    current_elo = elo.read_by_date()
    data_frame = (current_elo.loc[current_elo['league'] == 'ENG-Premier League'])
    df_elo = data_frame.drop(columns=['league'], axis = 1)
    df_elo_pl = df_elo.replace(to_replace='Tottenham', value ='Spurs')
    print(df_elo_pl)

if __name__ == '__main__':
    get_elo()
