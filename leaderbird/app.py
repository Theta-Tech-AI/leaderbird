from flask import Flask, render_template
from .models import Player, Leaderboard

def create_app():
    app = Flask(__name__)
    
    # Create sample data
    leaderboard = Leaderboard()
    leaderboard.add_player(Player("Alice", 1200))
    leaderboard.add_player(Player("Bob", 1100))
    leaderboard.add_player(Player("Charlie", 1050))
    leaderboard.add_player(Player("Diana", 1300))
    
    @app.route('/')
    def index():
        rankings = leaderboard.get_rankings()
        return render_template('index.html', rankings=rankings)
    
    return app