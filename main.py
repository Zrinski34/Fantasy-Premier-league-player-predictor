import requests
import pandas
URL='https://fantasy.premierleague.com/api/bootstrap-static/'
def get_player_data():
    response = requests.get(URL)
    data = response.json()
    print(data)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_player_data()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
