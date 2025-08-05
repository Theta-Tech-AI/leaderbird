import os

# use environment variables to configure the leaderbird package, with close to chess.com for defaults
DEFAULT_RATING = int(os.getenv('LEADERBIRD_DEFAULT_RATING', '800'))
DEFAULT_K_FACTOR = int(os.getenv('LEADERBIRD_K_FACTOR', '32'))
ESTABLISHED_PLAYER_K_FACTOR = int(os.getenv('LEADERBIRD_ESTABLISHED_K_FACTOR', '16'))
RATING_FLOOR = int(os.getenv('LEADERBIRD_RATING_FLOOR', '100'))
RATING_CEILING = int(os.getenv('LEADERBIRD_RATING_CEILING', '3000'))