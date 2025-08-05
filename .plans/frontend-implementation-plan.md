# Flask Web Frontend Implementation Plan

## Overview

This document outlines the plan to add a Flask web frontend to the leaderbird package that launches when users run `python3 -m leaderbird` after installing via pip. The goal is to provide an immediate, browser-based interface for leaderboard functionality.

## User Experience Flow

1. User runs `pip3 install leaderbird`
2. User runs `python3 -m leaderbird`
3. Flask server starts on localhost
4. Web browser automatically opens to the leaderboard interface
5. User can interact with leaderboards through the web UI

## Project Structure

```
leaderbird/
├── __init__.py              # Package exports and metadata
├── __main__.py              # Entry point for python -m leaderbird
├── webapp/                  # Flask web application
│   ├── __init__.py
│   ├── app.py              # Flask app factory
│   ├── routes.py           # Route definitions
│   ├── templates/          # Jinja2 templates
│   │   ├── base.html       # Base template with navigation
│   │   ├── index.html      # Home page
│   │   └── leaderboard.html # Main leaderboard view
│   └── static/             # Static assets
│       ├── css/
│       │   └── style.css   # Main stylesheet
│       └── js/
│           └── main.js     # Frontend JavaScript
├── core/                   # Core leaderboard logic
│   ├── __init__.py
│   ├── models.py          # Data models (Player, Game, Leaderboard)
│   └── elo.py             # ELO rating calculations
└── utils.py               # Utility functions
```

## Implementation Phases

### Phase 1: Package Configuration

#### Dependencies Update
Add to `pyproject.toml`:
```toml
dependencies = [
    "flask>=2.3.0",
    "flask-cors>=4.0.0",
]
```

#### Package Entry Point
Create `__main__.py` to handle:
- Flask app initialization with basic sample data
- Automatic browser launch using `webbrowser.open()`

### Phase 2: Core Leaderboard Logic

#### Data Models (`core/models.py`)
- **Player class**: name, rating
- **Leaderboard class**: add_player(), get_rankings()

#### ELO System (`core/elo.py`)
- Basic ELO calculation function

### Phase 3: Flask Web Application

#### App Factory (`webapp/app.py`)
- Basic Flask application
- Template and static folder registration

#### Routes (`webapp/routes.py`)
Core routes to implement:
- `GET /` - Basic leaderboard display

#### Templates (`webapp/templates/`)
- **base.html**: Simple layout
- **index.html**: Basic leaderboard table

#### Static Assets (`webapp/static/`)
- **CSS**: Minimal styling


## Technical Specifications

### Flask Configuration
- Development server for simplicity
- Host: localhost (security)
- Port: 5000 (with auto-detection)
- Debug: False in production

### Data Storage
- In-memory storage initially
- Easy migration path to SQLite/PostgreSQL
- JSON serialization for persistence option

### Frontend Technology
- Server-side rendering with Jinja2
- Progressive enhancement with JavaScript
- Responsive CSS Grid/Flexbox layout
- No external frontend framework dependencies

### Error Handling
- Graceful degradation for missing data
- User-friendly error messages
- Proper HTTP status codes
- Logging for debugging

## User Interface Design

### Home Page (`/`)
- Welcome message explaining leaderbird
- Quick stats (total players, games, top player)
- Navigation to main features
- Getting started guide

### Leaderboard Page (`/leaderboard`)
- Sortable table of player rankings
- Columns: Rank, Name, Rating, Games Played, Win Rate
- Filter options (player type, rating range)
- Pagination for large datasets

### Add Player Page (`/add-player`)
- Simple form: name, player type (human/AI)
- Starting rating configuration
- Success/error feedback

### Record Game Page (`/record-game`)
- Dropdown selectors for both players
- Result options (win/loss/draw)
- Game timestamp
- Live rating change preview

## Security Considerations

- Localhost-only binding
- Input validation and sanitization
- CSRF protection for forms
- No sensitive data exposure
- Safe template rendering

## Testing Strategy

### Unit Tests
- ELO calculation accuracy
- Data model functionality
- Route response validation

### Integration Tests
- Complete workflow testing
- Browser launch verification
- Cross-platform compatibility

### Manual Testing
- Install in clean environment
- Test all user workflows
- Mobile responsiveness
- Multiple browser compatibility

## Future Enhancement Opportunities

### Short-term
- Player profiles with game history
- Tournament bracket support
- Export functionality (CSV, JSON)

### Medium-term
- Real-time multiplayer games
- REST API for external integrations
- Database persistence options

### Long-term
- Machine learning rating predictions
- Advanced analytics and visualizations
- Multi-league support

## Success Criteria

1. ✅ `python3 -m leaderbird` launches successfully after pip install
2. ✅ Browser opens automatically to basic leaderboard interface
3. ✅ Shows basic leaderboard table with sample data
4. ✅ Package follows Python packaging best practices

## Implementation Timeline

- **Phase 1**: 1 hour (package setup)
- **Phase 2**: 1 hour (basic core logic)
- **Phase 3**: 2-3 hours (basic Flask app and templates)

**Total estimated time**: 4-5 hours for basic implementation

## Risk Mitigation

- **Port conflicts**: Auto-detect available ports
- **Browser issues**: Provide manual URL instructions
- **Package installation**: Comprehensive error messages
- **Performance**: Implement pagination and lazy loading
- **Cross-platform**: Test on Windows, macOS, Linux

This plan provides a clear roadmap for implementing a complete Flask web frontend while maintaining simplicity and following established Python packaging patterns.