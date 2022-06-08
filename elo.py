elo_width = 400
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


