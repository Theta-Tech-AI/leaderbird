# ELO Frontend Integration Plan

## Overview

This plan outlines how to integrate our ELO utility functions into the existing Flask web frontend, allowing users to conduct matches between random participants and see real-time ELO rating updates.

## Current State

**Existing Components:**
- `leaderbird/elo.py` - Working ELO utility functions
- `leaderbird/app.py` - Basic Flask app with static leaderboard
- `leaderbird/models.py` - Player and Leaderboard classes
- `leaderbird/templates/index.html` - Basic HTML table display
- `leaderbird/config.py` - Configuration with 800 default rating

## Requirements

1. Backend stores participants and their current ELO ratings
2. Frontend displays two random participants for matches
3. Simple UI to indicate match winner (buttons/links)
4. Automatic ELO updates using our update_elo() function
5. Real-time leaderboard refresh after matches
6. Keep existing functionality working

## Implementation Plan

### Phase 1: Backend Data Enhancement

#### 1.1 Enhance Leaderboard Model
**File: `leaderbird/models.py`**

Add methods to support match functionality:
```python
import random
from .config import DEFAULT_RATING

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
    
    def update_player_ratings(self, player1_name, player2_name, new_rating1, new_rating2):
        """Update ratings for two players"""
        player1 = self.find_player_by_name(player1_name)
        player2 = self.find_player_by_name(player2_name)
        if player1 and player2:
            player1.rating = new_rating1
            player2.rating = new_rating2
            return True
        return False
```

#### 1.2 Enhanced Sample Data
**File: `leaderbird/app.py`**

Create more diverse sample data:
```python
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
```

### Phase 2: Route Implementation

#### 2.1 Add Match Routes
**File: `leaderbird/app.py`**

Add new routes for match functionality:
```python
from flask import Flask, render_template, request, redirect, url_for, flash
from .models import Player, Leaderboard
from .elo import update_elo, update_elo_draw
from .config import DEFAULT_K_FACTOR

# Global leaderboard instance
leaderboard = create_sample_leaderboard()

@app.route('/')
def index():
    rankings = leaderboard.get_rankings()
    return render_template('index.html', rankings=rankings)

@app.route('/match')
def match():
    player1, player2 = leaderboard.get_random_pair()
    if not player1 or not player2:
        flash("Need at least 2 players for a match")
        return redirect(url_for('index'))
    return render_template('match.html', player1=player1, player2=player2)

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
    
    # Update the ratings
    leaderboard.update_player_ratings(player1_name, player2_name, new_rating1, new_rating2)
    
    flash(f"{winner_text} | {player1.name}: {player1.rating - new_rating1:+d} → {new_rating1}, {player2.name}: {player2.rating - new_rating2:+d} → {new_rating2}")
    
    return redirect(url_for('index'))
```

### Phase 3: Frontend Templates

#### 3.1 Create Match Template
**File: `leaderbird/templates/match.html`**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Match - Leaderbird</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .match-container { text-align: center; margin: 40px 0; }
        .player-card { 
            display: inline-block; 
            margin: 20px; 
            padding: 20px; 
            border: 2px solid #ddd; 
            border-radius: 8px; 
            min-width: 150px;
        }
        .vs { font-size: 24px; font-weight: bold; margin: 0 20px; }
        .result-buttons { margin: 30px 0; }
        .result-btn { 
            margin: 10px; 
            padding: 15px 25px; 
            font-size: 16px; 
            cursor: pointer; 
            border: none; 
            border-radius: 5px; 
            background-color: #007bff; 
            color: white; 
        }
        .result-btn:hover { background-color: #0056b3; }
        .draw-btn { background-color: #6c757d; }
        .draw-btn:hover { background-color: #545b62; }
        nav { margin-bottom: 20px; }
        nav a { margin-right: 15px; text-decoration: none; color: #007bff; }
    </style>
</head>
<body>
    <nav>
        <a href="/">← Back to Leaderboard</a>
        <a href="/match">New Match</a>
    </nav>

    <h1>Match Setup</h1>
    
    <div class="match-container">
        <div class="player-card">
            <h3>{{ player1.name }}</h3>
            <p>Rating: {{ player1.rating }}</p>
        </div>
        
        <span class="vs">VS</span>
        
        <div class="player-card">
            <h3>{{ player2.name }}</h3>
            <p>Rating: {{ player2.rating }}</p>
        </div>
    </div>

    <div class="result-buttons">
        <form method="POST" action="/match/result" style="display: inline;">
            <input type="hidden" name="player1" value="{{ player1.name }}">
            <input type="hidden" name="player2" value="{{ player2.name }}">
            <input type="hidden" name="result" value="player1_wins">
            <button type="submit" class="result-btn">{{ player1.name }} Wins</button>
        </form>

        <form method="POST" action="/match/result" style="display: inline;">
            <input type="hidden" name="player1" value="{{ player1.name }}">
            <input type="hidden" name="player2" value="{{ player2.name }}">
            <input type="hidden" name="result" value="draw">
            <button type="submit" class="result-btn draw-btn">Draw</button>
        </form>

        <form method="POST" action="/match/result" style="display: inline;">
            <input type="hidden" name="player1" value="{{ player1.name }}">
            <input type="hidden" name="player2" value="{{ player2.name }}">
            <input type="hidden" name="result" value="player2_wins">
            <button type="submit" class="result-btn">{{ player2.name }} Wins</button>
        </form>
    </div>
</body>
</html>
```

#### 3.2 Update Main Template
**File: `leaderbird/templates/index.html`**

Add navigation and flash messages:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Leaderbird</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        nav { margin-bottom: 20px; }
        nav a { margin-right: 15px; text-decoration: none; color: #007bff; }
        .flash-messages { margin: 20px 0; }
        .flash-message { padding: 10px; background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 4px; }
    </style>
</head>
<body>
    <nav>
        <a href="/">Leaderboard</a>
        <a href="/match">New Match</a>
    </nav>

    <h1>Leaderboard</h1>
    
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <div class="flash-messages">
                {% for message in messages %}
                    <div class="flash-message">{{ message }}</div>
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}

    <table>
        <tr>
            <th>Rank</th>
            <th>Name</th>
            <th>Rating</th>
        </tr>
        {% for player in rankings %}
        <tr>
            <td>{{ loop.index }}</td>
            <td>{{ player.name }}</td>
            <td>{{ player.rating }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
```

### Phase 4: Flask App Updates

#### 4.1 Add Flask Session Support
**File: `leaderbird/app.py`**

Enable flash messages:
```python
def create_app():
    app = Flask(__name__)
    app.secret_key = 'dev-secret-key-change-in-production'  # For flash messages
    
    # ... rest of app setup
```

### Phase 5: Integration Testing

#### 5.1 Test Scenarios
1. **Basic Navigation**: Navigate between leaderboard and match pages
2. **Random Pair Generation**: Verify different pairs are selected
3. **Match Results**: Test all three outcomes (player1 wins, player2 wins, draw)
4. **ELO Updates**: Verify ratings change correctly using our functions
5. **Leaderboard Updates**: Confirm rankings reorder after matches
6. **Edge Cases**: Handle insufficient players, invalid results

#### 5.2 Manual Testing Steps
```bash
# Install and run
pip3 install -e .
python3 -m leaderbird

# Test workflow:
1. Visit localhost:5000 (see leaderboard)
2. Click "New Match" 
3. See random pair displayed
4. Click winner button
5. Verify flash message shows rating changes
6. Confirm leaderboard updates with new ratings
7. Repeat several matches to see ELO system in action
```

## Implementation Sequence

1. **Enhance models.py** - Add helper methods
2. **Update app.py** - Add routes and ELO integration
3. **Create match.html** - New template for match interface
4. **Update index.html** - Add navigation and flash messages
5. **Test integration** - Verify all functionality works

## Success Criteria

1. ✅ Users can navigate between leaderboard and match pages
2. ✅ Random pairs are generated for matches
3. ✅ Match results update player ratings using our ELO functions
4. ✅ Leaderboard reflects new ratings immediately
5. ✅ Flash messages show rating changes clearly
6. ✅ Existing leaderboard functionality remains intact
7. ✅ ELO calculations use Chess.com-compatible defaults (800 starting rating)

This plan provides a complete, simple implementation that demonstrates the ELO system in action through an interactive web interface.