from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
career = playercareerstats.PlayerCareerStats(player_id='203999') 
print(career.get_data_frames()[0])
player = players.find_players_by_first_name('lebron')
print(player)