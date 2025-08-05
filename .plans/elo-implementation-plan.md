# ELO Utility Functions Implementation Plan

## Executive Summary

This plan outlines the implementation of standalone ELO utility functions for the leaderbird package, allowing developers to easily integrate ELO rating calculations into their Python projects. The implementation will provide a clean, importable API while maintaining backward compatibility with existing functionality.

## Current State Analysis

**Existing Structure:**
- `leaderbird/__init__.py` - Minimal (just a comment)
- `leaderbird/models.py` - Basic Player and Leaderboard classes
- `leaderbird/app.py` - Flask web interface
- `pyproject.toml` - Package configuration with Flask dependency

**Key Observations:**
- Player class already has basic rating support (default 1000)
- Package is structured for both library use and web interface
- Simple integer versioning system in place
- No environment configuration currently exists

## Implementation Plan

### Phase 1: Core ELO Utility Functions

#### 1.1 Create ELO Calculation Module
**File: `leaderbird/elo.py`**

**Functions to implement:**
```python
def calculate_expected_score(player_rating: int, opponent_rating: int) -> float:
    """Calculate expected score using standard ELO formula"""

def update_elo(player_a_elo: int, player_b_elo: int, did_a_win: bool, k_factor: int = 32) -> tuple[int, int]:
    """Update ELO ratings for two players based on match result"""

def update_elo_draw(player_a_elo: int, player_b_elo: int, k_factor: int = 32) -> tuple[int, int]:
    """Update ELO ratings for a draw between two players"""

def get_rating_change(current_rating: int, opponent_rating: int, actual_score: float, k_factor: int = 32) -> int:
    """Calculate rating change for a single player"""
```

**Implementation Details:**
- Use standard chess ELO formula: `New Rating = Old Rating + K * (Actual Score - Expected Score)`
- Expected score: `1 / (1 + 10^((opponent_rating - player_rating) / 400))`
- Support configurable K-factor with sensible defaults
- Return integer ratings (rounded from float calculations)

#### 1.2 Configuration Management
**File: `leaderbird/config.py`**

**Configuration Options:**
```python
import os

DEFAULT_RATING = int(os.getenv('LEADERBIRD_DEFAULT_RATING', '1000'))
DEFAULT_K_FACTOR = int(os.getenv('LEADERBIRD_K_FACTOR', '32'))
ESTABLISHED_PLAYER_K_FACTOR = int(os.getenv('LEADERBIRD_ESTABLISHED_K_FACTOR', '16'))
RATING_FLOOR = int(os.getenv('LEADERBIRD_RATING_FLOOR', '100'))
RATING_CEILING = int(os.getenv('LEADERBIRD_RATING_CEILING', '3000'))
```

#### 1.3 Environment Configuration Template
**File: `.env.example`**

```env
# ELO Rating Configuration
LEADERBIRD_DEFAULT_RATING=1000
LEADERBIRD_K_FACTOR=32
LEADERBIRD_ESTABLISHED_K_FACTOR=16
LEADERBIRD_RATING_FLOOR=100
LEADERBIRD_RATING_CEILING=3000
```

### Phase 2: Package Integration

#### 2.1 Update Package __init__.py
**File: `leaderbird/__init__.py`**

**Imports to add:**
```python
from .elo import (
    update_elo,
    update_elo_draw,
    calculate_expected_score,
    get_rating_change
)
from .config import (
    DEFAULT_RATING,
    DEFAULT_K_FACTOR,
    ESTABLISHED_PLAYER_K_FACTOR
)
from .models import Player, Leaderboard

__version__ = "1"
__all__ = [
    'update_elo',
    'update_elo_draw', 
    'calculate_expected_score',
    'get_rating_change',
    'DEFAULT_RATING',
    'DEFAULT_K_FACTOR',
    'ESTABLISHED_PLAYER_K_FACTOR',
    'Player',
    'Leaderboard'
]
```

### Phase 3: Dependencies
**File: `pyproject.toml`**

Add optional dependency:
```toml
dependencies = [
    "flask>=2.3.0",
    "python-dotenv>=0.19.0",
]
```

### Phase 4: Documentation

#### 4.1 Update README with Usage Examples

**New Section: "Using ELO Utility Functions"**

```markdown
## Using ELO Utility Functions

### Basic Usage
```python
import leaderbird

# Update ratings after a match
player_a_rating = 1200
player_b_rating = 1100
did_a_win = True

new_a_rating, new_b_rating = leaderbird.update_elo(
    player_a_rating, 
    player_b_rating, 
    did_a_win
)
print(f"Player A: {player_a_rating} → {new_a_rating}")
print(f"Player B: {player_b_rating} → {new_b_rating}")
```

### Advanced Configuration
```python
import leaderbird

# Custom K-factor for established players
new_a_rating, new_b_rating = leaderbird.update_elo(
    1800, 1750, True, k_factor=16
)

# Handle draws
draw_a_rating, draw_b_rating = leaderbird.update_elo_draw(1500, 1500)

# Calculate expected score
expected = leaderbird.calculate_expected_score(1200, 1100)
print(f"Expected score: {expected:.2f}")
```

### Environment Configuration
Create a `.env` file:
```env
LEADERBIRD_DEFAULT_RATING=1200
LEADERBIRD_K_FACTOR=24
```
```

## Implementation Sequence

### Sequential Steps:

1. **Create ELO calculation module** (`elo.py`)
2. **Create configuration module** (`config.py`)
3. **Update package __init__.py**
4. **Create .env.example template**
5. **Update README documentation**
6. **Add python-dotenv dependency**

## Success Criteria

1. Developers can `pip install leaderbird` and immediately use ELO functions
2. Simple API: `leaderbird.update_elo(1200, 1100, True)` returns updated ratings
3. Configuration via .env file works seamlessly
4. All README examples execute correctly
5. Existing web interface functionality remains intact