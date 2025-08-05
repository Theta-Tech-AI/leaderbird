from flask import Flask, render_template, request, redirect, url_for, flash
from .models import Player, Leaderboard
from .elo import update_elo, update_elo_draw, calculate_expected_score
from .config import DEFAULT_K_FACTOR

def create_sample_leaderboard():
    leaderboard = Leaderboard()
    sample_players = [
        Player("Alice", 850),
        Player("Bob", 780),
        Player("Charlie", 820),
        Player("Diana", 900),
        Player("Eve", 750),
        Player("Frank", 880),
    ]
    for player in sample_players:
        leaderboard.add_player(player)
    return leaderboard

def create_app():
    app = Flask(__name__)
    app.secret_key = 'dev-secret-key-change-in-production'  # For flash messages
    
    # Global leaderboard instance
    leaderboard = create_sample_leaderboard()
    
    @app.route('/')
    def index():
        rankings = leaderboard.get_rankings()
        player1, player2 = leaderboard.get_random_pair()
        
        # Sort players so favored (higher rating) is always on left
        if player1 and player2:
            if player2.rating > player1.rating:
                player1, player2 = player2, player1  # Swap so higher rating is first
        
        # Calculate win probabilities if we have both players
        player1_win_prob = None
        player2_win_prob = None
        if player1 and player2:
            player1_expected = calculate_expected_score(player1.rating, player2.rating)
            player2_expected = calculate_expected_score(player2.rating, player1.rating)
            
            # Convert to percentages and round to whole numbers
            player1_win_prob = round(player1_expected * 100)
            player2_win_prob = round(player2_expected * 100)
        
        return render_template('index.html', 
                             rankings=rankings, 
                             player1=player1, 
                             player2=player2,
                             player1_win_prob=player1_win_prob,
                             player2_win_prob=player2_win_prob)
    
    @app.route('/match/result', methods=['POST'])
    def match_result():
        player1_name = request.form.get('player1')
        player2_name = request.form.get('player2')
        result = request.form.get('result')  # 'player1_wins', 'player2_wins', 'draw'
        
        player1 = leaderboard.find_player_by_name(player1_name)
        player2 = leaderboard.find_player_by_name(player2_name)
        
        if not player1 or not player2:
            flash("Players not found")
            return redirect(url_for('index'))
        
        # Store old ratings for display
        old_rating1 = player1.rating
        old_rating2 = player2.rating
        
        # Calculate new ratings using our ELO functions
        if result == 'player1_wins':
            new_rating1, new_rating2 = update_elo(player1.rating, player2.rating, True, DEFAULT_K_FACTOR)
            winner_text = f"{player1.name} defeats {player2.name}"
        elif result == 'player2_wins':
            new_rating2, new_rating1 = update_elo(player2.rating, player1.rating, True, DEFAULT_K_FACTOR)
            winner_text = f"{player2.name} defeats {player1.name}"
        elif result == 'draw':
            new_rating1, new_rating2 = update_elo_draw(player1.rating, player2.rating, DEFAULT_K_FACTOR)
            winner_text = f"{player1.name} and {player2.name} draw"
        else:
            flash("Invalid result")
            return redirect(url_for('match'))
        
        # Update ratings with change tracking (no flash message)
        leaderboard.update_player_ratings_with_changes(player1_name, player2_name, new_rating1, new_rating2)
        
        return redirect(url_for('index'))
    
    return app