import random

class Player:
    def __init__(self, name, rating=800):
        self.name = name
        self.rating = rating
        # New attributes for change tracking
        self.recent_change = None  # +16, -8, etc.
        self.old_rating = None     # Rating before recent match
        self.in_recent_match = False  # Flag for recent match participation
    
    def set_rating_change(self, old_rating, new_rating):
        """Record a rating change for display purposes"""
        self.old_rating = old_rating
        self.recent_change = new_rating - old_rating
        self.rating = new_rating
        self.in_recent_match = True
    
    def clear_rating_change(self):
        """Clear rating change data"""
        self.recent_change = None
        self.old_rating = None
        self.in_recent_match = False

class Leaderboard:
    def __init__(self):
        self.players = []
    
    def add_player(self, player):
        self.players.append(player)
    
    def get_rankings(self):
        return sorted(self.players, key=lambda p: p.rating, reverse=True)
    
    def get_random_pair(self):
        """Get two random players for a match"""
        if len(self.players) < 2:
            return None, None
        return random.sample(self.players, 2)
    
    def find_player_by_name(self, name):
        """Find player by name"""
        for player in self.players:
            if player.name == name:
                return player
        return None
    
    def clear_all_rating_changes(self):
        """Clear rating change data for all players"""
        for player in self.players:
            player.clear_rating_change()
    
    def update_player_ratings_with_changes(self, player1_name, player2_name, new_rating1, new_rating2):
        """Update ratings and track changes for recent match display"""
        player1 = self.find_player_by_name(player1_name)
        player2 = self.find_player_by_name(player2_name)
        
        if player1 and player2:
            # Clear all previous changes first
            self.clear_all_rating_changes()
            
            # Set new ratings with change tracking
            player1.set_rating_change(player1.rating, new_rating1)
            player2.set_rating_change(player2.rating, new_rating2)
            
            return True
        return False
    
    def update_player_ratings(self, player1_name, player2_name, new_rating1, new_rating2):
        """Update ratings for two players (legacy method)"""
        player1 = self.find_player_by_name(player1_name)
        player2 = self.find_player_by_name(player2_name)
        if player1 and player2:
            player1.rating = new_rating1
            player2.rating = new_rating2
            return True
        return False