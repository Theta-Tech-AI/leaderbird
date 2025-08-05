# leaderbird
For leaderboards and rankings.

## Overview
Helper library for leaderboards and rankings, such as ELO-based rankings between humans, AI's, and between humans and AI's.

Includes a web interface that launches automatically when you run `python3 -m leaderbird`.

## Installation & Usage

### From PyPI (Recommended)
```bash
pip3 install leaderbird
python3 -m leaderbird  # Opens web browser with leaderboard interface
```

### Local Development
```bash
# Clone and install in editable mode
git clone <repo-url>
cd leaderbird
pip3 install -e .
python3 -m leaderbird  # Opens web browser with leaderboard interface
```

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

### Switching Between Local and PyPI Versions

To test PyPI version:
```bash
pip3 uninstall leaderbird
pip3 install leaderbird
python3 -c "import leaderbird; print(leaderbird.__file__)"  # Shows site-packages path
```

To test local version:
```bash
pip3 uninstall leaderbird
pip3 install -e .
python3 -c "import leaderbird; print(leaderbird.__file__)"  # Shows local path
```

## Development Rules
1. Don't let the code get sloppy.
2. It should "just work".
3. Don't procrastinate on refactoring; refactor as you go.

## Release Process

### Creating a New Version
1. **Update version** in `pyproject.toml`:
   ```toml
   version = "2"  # Next integer version
   ```

2. **Commit and create release**:
   ```bash
   git add .
   git commit -m "Release v2"
   git push
   
   # Create and push tag
   git tag v2
   git push origin v2
   ```

3. **Create GitHub Release**:
   - Go to GitHub → Releases → Create new release
   - Tag: `v2`
   - Title: `v2`
   - Add release notes describing changes
   - Click "Publish release"

4. **Automatic Deployment**:
   - GitHub Action automatically builds and publishes to PyPI
   - Wait ~5 minutes, then test: `pip3 install --upgrade leaderbird`

### Version Numbering
We use simple integer versions: `1`, `2`, `3`, etc.
