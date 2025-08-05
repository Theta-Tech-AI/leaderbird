class Player:
    def __init__(self, name, rating=1000):
        self.name = name
        self.rating = rating

class Leaderboard:
    def __init__(self):
        self.players = []
    
    def add_player(self, player):
        self.players.append(player)
    
    def get_rankings(self):
        return sorted(self.players, key=lambda p: p.rating, reverse=True)