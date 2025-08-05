# Enhanced Rating Display Plan

## Overview

This plan outlines how to enhance the leaderboard rating display to show recent rating changes directly in the table instead of using flash messages at the top. The enhanced display will show current rating, change delta with arrow emoji, and old rating in a different color.

## Current State

**Existing Components:**
- Leaderboard table with Rank, Name, Rating columns
- Flash messages showing match results like "Alice defeats Bob | Alice: +16 → 866, Bob: -16 → 764"
- Player class with name and rating attributes
- Match result processing with ELO updates

## Requirements

1. **Remove flash message bar** - No more top-of-page result messages
2. **Enhanced Rating column** format: `"866 ↑+16 (old rating: 850)"`
   - Current rating (normal color)
   - Change indicator with arrow emoji (↑ for gains, ↓ for losses)
   - Old rating in different color (grayed out)
3. **Selective display** - Only show changes for players in most recent match
4. **Clean data lifecycle** - Clear old change data when new matches occur

## Implementation Plan

### Phase 1: Enhance Player Model

**File: `leaderbird/models.py`**

Add change tracking attributes to Player class:
```python
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
```

### Phase 2: Enhance Leaderboard Model

**File: `leaderbird/models.py`**

Add change management methods:
```python
class Leaderboard:
    # ... existing methods ...
    
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
```

### Phase 3: Update Match Result Route

**File: `leaderbird/app.py`**

Remove flash messages and use new change tracking:
```python
@app.route('/match/result', methods=['POST'])
def match_result():
    player1_name = request.form.get('player1')
    player2_name = request.form.get('player2')
    result = request.form.get('result')
    
    player1 = leaderboard.find_player_by_name(player1_name)
    player2 = leaderboard.find_player_by_name(player2_name)
    
    if not player1 or not player2:
        flash("Players not found")
        return redirect(url_for('index'))
    
    # Calculate new ratings using our ELO functions
    if result == 'player1_wins':
        new_rating1, new_rating2 = update_elo(player1.rating, player2.rating, True, DEFAULT_K_FACTOR)
    elif result == 'player2_wins':
        new_rating2, new_rating1 = update_elo(player2.rating, player1.rating, True, DEFAULT_K_FACTOR)
    elif result == 'draw':
        new_rating1, new_rating2 = update_elo_draw(player1.rating, player2.rating, DEFAULT_K_FACTOR)
    else:
        flash("Invalid result")
        return redirect(url_for('match'))
    
    # Update ratings with change tracking (no flash message)
    leaderboard.update_player_ratings_with_changes(player1_name, player2_name, new_rating1, new_rating2)
    
    return redirect(url_for('index'))
```

### Phase 4: Update Template

**File: `leaderbird/templates/index.html`**

Remove flash messages and enhance rating column:
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
        .rating-change-positive { color: #28a745; font-weight: bold; }
        .rating-change-negative { color: #dc3545; font-weight: bold; }
        .old-rating { color: #6c757d; font-size: 0.9em; }
    </style>
</head>
<body>
    <nav>
        <a href="/">Leaderboard</a>
        <a href="/match">New Match</a>
    </nav>

    <h1>Leaderboard</h1>

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
            <td>
                {{ player.rating }}
                {% if player.in_recent_match and player.recent_change %}
                    {% if player.recent_change > 0 %}
                        <span class="rating-change-positive">↑+{{ player.recent_change }}</span>
                    {% elif player.recent_change < 0 %}
                        <span class="rating-change-negative">↓{{ player.recent_change }}</span>
                    {% endif %}
                    <span class="old-rating">(old rating: {{ player.old_rating }})</span>
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
```

### Phase 5: CSS Styling Enhancement

**Enhanced visual design:**
- Green color (`#28a745`) for rating gains with ↑ arrow
- Red color (`#dc3545`) for rating losses with ↓ arrow  
- Gray color (`#6c757d`) for old rating display
- Bold font weight for change indicators
- Smaller font size for old rating text

### Phase 6: Data Lifecycle Management

**Automatic cleanup strategy:**
- Each new match clears all previous rating changes
- Only the most recent match participants show changes
- Change data persists until next match occurs
- No manual cleanup required

## Implementation Sequence

### Sequential Steps:
1. **Enhance Player model** - Add change tracking attributes and methods
2. **Enhance Leaderboard model** - Add change management methods  
3. **Update match_result route** - Remove flash messages, use change tracking
4. **Update template** - Remove flash message display, add enhanced rating column

### Parallel Opportunities:
- CSS styling can be prepared while working on model changes
- Template structure can be planned while implementing backend changes

## Expected Result

**Before:** Flash message "Alice defeats Bob | Alice: +16 → 866, Bob: -16 → 764"

**After:** In leaderboard table:
```
Rank | Name  | Rating
1    | Alice | 866 ↑+16 (old rating: 850)
2    | Bob   | 764 ↓-16 (old rating: 780)  
3    | Charlie | 820
```

## Success Criteria

1. ✅ No flash messages appear after match results
2. ✅ Recent match participants show enhanced rating display
3. ✅ Non-participants show normal rating display
4. ✅ Arrow emojis correctly indicate gain (↑) or loss (↓)
5. ✅ Old ratings appear in gray color
6. ✅ New matches clear previous change indicators
7. ✅ Leaderboard rankings remain accurate

This plan provides a clean, intuitive enhancement that improves the user experience by showing rating changes directly in context within the leaderboard table.