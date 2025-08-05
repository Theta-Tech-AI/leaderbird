def calculate_expected_score(player_rating: int, opponent_rating: int) -> float:
    """Calculate expected score using standard ELO formula
    
    Args:
        player_rating: Current rating of the player
        opponent_rating: Current rating of the opponent
        
    Returns:
        Expected score (0.0 to 1.0)
    """
    return 1 / (1 + 10**((opponent_rating - player_rating) / 400))

def get_rating_change(current_rating: int, opponent_rating: int, actual_score: float, k_factor: int = 32) -> int:
    """Calculate rating change for a single player
    
    Args:
        current_rating: Player's current rating
        opponent_rating: Opponent's current rating
        actual_score: Actual match result (1.0 = win, 0.5 = draw, 0.0 = loss)
        k_factor: K-factor for rating calculation
        
    Returns:
        Rating change as integer
    """
    expected_score = calculate_expected_score(current_rating, opponent_rating)
    return round(k_factor * (actual_score - expected_score))

def update_elo(player_a_elo: int, player_b_elo: int, did_a_win: bool, k_factor: int = 32) -> tuple[int, int]:
    """Update ELO ratings for two players based on match result
    
    Args:
        player_a_elo: Player A's current rating
        player_b_elo: Player B's current rating
        did_a_win: True if Player A won, False if Player B won
        k_factor: K-factor for rating calculation
        
    Returns:
        Tuple of (new_player_a_rating, new_player_b_rating)
    """
    a_score = 1.0 if did_a_win else 0.0
    b_score = 0.0 if did_a_win else 1.0
    
    a_change = get_rating_change(player_a_elo, player_b_elo, a_score, k_factor)
    b_change = get_rating_change(player_b_elo, player_a_elo, b_score, k_factor)
    
    return (player_a_elo + a_change, player_b_elo + b_change)

def update_elo_draw(player_a_elo: int, player_b_elo: int, k_factor: int = 32) -> tuple[int, int]:
    """Update ELO ratings for a draw between two players
    
    Args:
        player_a_elo: Player A's current rating
        player_b_elo: Player B's current rating
        k_factor: K-factor for rating calculation
        
    Returns:
        Tuple of (new_player_a_rating, new_player_b_rating)
    """
    a_change = get_rating_change(player_a_elo, player_b_elo, 0.5, k_factor)
    b_change = get_rating_change(player_b_elo, player_a_elo, 0.5, k_factor)
    
    return (player_a_elo + a_change, player_b_elo + b_change)