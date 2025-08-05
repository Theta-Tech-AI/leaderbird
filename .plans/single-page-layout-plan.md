# Single-Page Layout Plan

## Overview

This plan outlines how to consolidate our current two-page system (leaderboard + match pages) into a single unified page that shows both the leaderboard table and match interface together, eliminating the need for page navigation.

## Current State

**Existing Components:**
- `/` route - Shows leaderboard table with enhanced rating displays
- `/match` route - Shows random pair selection interface
- `/match/result` POST route - Processes match results and redirects
- `templates/index.html` - Leaderboard table template
- `templates/match.html` - Match interface template
- Enhanced rating display with arrows and old ratings

## Requirements

1. **Single page layout** - Remove separate `/match` route entirely
2. **Always show both** - Leaderboard table at top, match interface at bottom
3. **Dynamic updates** - New random pair appears after each match result
4. **No redirects** - Everything happens on the same page
5. **Preserve functionality** - Keep enhanced rating displays and ELO calculations

## Implementation Plan

### Phase 1: Flask Route Consolidation

#### 1.1 Modify Main Route
**File: `leaderbird/app.py`**

Update the main route to always include match data:
```python
@app.route('/')
def index():
    rankings = leaderboard.get_rankings()
    player1, player2 = leaderboard.get_random_pair()
    
    return render_template('index.html', 
                         rankings=rankings, 
                         player1=player1, 
                         player2=player2)
```

#### 1.2 Remove Match Route
**File: `leaderbird/app.py`**

Delete the `/match` route entirely since match interface will be integrated:
```python
# Remove this entire route:
# @app.route('/match')
# def match():
#     ...
```

#### 1.3 Update Match Result Route
**File: `leaderbird/app.py`**

Modify to stay on same page instead of redirecting:
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
        return redirect(url_for('index'))
    
    # Update ratings with change tracking
    leaderboard.update_player_ratings_with_changes(player1_name, player2_name, new_rating1, new_rating2)
    
    # Return to same page (which will show updated leaderboard + new random pair)
    return redirect(url_for('index'))
```

### Phase 2: Template Integration

#### 2.1 Integrate Match Interface
**File: `leaderbird/templates/index.html`**

Merge both templates into single page:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Leaderbird</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 40px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .rating-change-positive { color: #28a745; font-weight: bold; }
        .rating-change-negative { color: #dc3545; font-weight: bold; }
        .old-rating { color: #6c757d; font-size: 0.9em; }
        
        /* Match interface styles */
        .match-section { border-top: 2px solid #ddd; padding-top: 30px; }
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
        .no-match { text-align: center; color: #6c757d; font-style: italic; }
    </style>
</head>
<body>
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

    <div class="match-section">
        <h2>New Match</h2>
        
        {% if player1 and player2 %}
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
        {% else %}
            <div class="no-match">
                <p>Need at least 2 players for matches</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
```

### Phase 3: UX Enhancements

#### 3.1 Visual Separation
- Add border/spacing between leaderboard and match sections
- Use different heading styles (h1 for Leaderboard, h2 for New Match)
- Ensure proper visual hierarchy

#### 3.2 Responsive Considerations
- Ensure match cards work well on mobile devices
- Stack player cards vertically on small screens if needed
- Maintain button usability across devices

### Phase 4: Cleanup

#### 4.1 Remove Unused Template
**File: `leaderbird/templates/match.html`**

This file can be deleted since functionality is now integrated:
```bash
# Optional: Keep as backup initially, then remove
rm leaderbird/templates/match.html
```

#### 4.2 Remove Navigation
Since everything is on one page, remove navigation elements that are no longer needed.

## User Flow

**New User Experience:**
1. Visit localhost:5000
2. See leaderboard table at top
3. See current match at bottom
4. Click winner button
5. Page reloads with:
   - Updated leaderboard (with rating changes)
   - New random match pair ready

## Technical Benefits

1. **Simplified routing** - Only need `/` and `/match/result` routes
2. **No navigation complexity** - Everything on one page
3. **Faster user experience** - No page navigation delays
4. **Preserved functionality** - All existing features maintained
5. **Clean code structure** - Fewer templates to maintain

## Implementation Sequence

1. **Update Flask routes** - Modify main route, remove match route
2. **Integrate templates** - Merge match interface into index.html
3. **Test functionality** - Verify all features work correctly
4. **Clean up** - Remove unused files and navigation elements

## Success Criteria

1. ✅ Single page shows both leaderboard and match interface
2. ✅ Match results update leaderboard without page navigation
3. ✅ New random pairs generated after each match
4. ✅ Enhanced rating displays continue to work correctly
5. ✅ All ELO calculations function properly
6. ✅ Responsive design works on mobile devices
7. ✅ No broken links or navigation issues

This plan transforms the current two-page system into a streamlined single-page experience while preserving all existing functionality and enhancing user workflow.