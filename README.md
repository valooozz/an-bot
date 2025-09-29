## an-bot — The Sticks Game (misère nim, contiguous picks)

### Overview
an-bot is a command‑line game where you play against an AI that removes sticks from a row. On your turn, you must remove 1 to 3 adjacent available sticks. The player who takes the last remaining stick loses (misère rule).

The project includes:
- A playable CLI game (`main.py`)
- An AI opponent (“an-bot”) with scoring and limited look‑ahead
- A lightweight JSON cache for best moves
- Unit tests for core game and analysis logic

### Rules of the game
- The board is a 1D row of sticks. A present stick is shown by `|`; removed positions are blank spaces.
- A move is defined by two numbers: `start count`.
  - `start` is 1‑based index of the first stick to remove.
  - `count` is how many sticks to remove (1, 2, or 3).
- You can only remove sticks that are currently present and adjacent to each other.
- Turns alternate between you and an-bot.
- When no sticks remain, the game ends. Whoever took the last stick loses.

Example display:

```text
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  
1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
```

Your input example: `5 2` (remove 2 adjacent sticks starting at position 5).

### Project structure
```text
an-bot/
  main.py                 # Game entry point
  game/                   # Game I/O and rules
    game.py               # Display, validation, removals, logging
    config.py             # Feature flags and initial position
  anbot/                  # The AI (“an-bot”)
    anbot.py              # Move selection, validity, fallback random
    scoring.py            # Heuristics and limited lookahead
    analyze.py            # Stick-group analysis helpers
    singles.py            # Utilities for handling singletons in groups
    cache.py              # JSON cache for best moves
  game_types/             # Shared type aliases
  player/                 # Player input handling
  tests/                  # Unit tests (pytest)
  cache_manager.py        # CLI tool to manage the cache
  CACHE_README.md         # Detailed cache docs
```

### Setup
Requirements: Python 3.9+

Optional, but recommended, create a virtual environment:

```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

There are no third‑party runtime dependencies. For development/testing, install pytest:

```bash
pip install pytest
```

### How to play
Run the game from the repository root:

```bash
python main.py
```

You will see the current board and whose turn it is. When it is your turn, enter your move as `start count` (e.g., `7 3`). Invalid moves are rejected with a message; try again until a valid move is entered.

### Configuration
All runtime flags are in `game/config.py`:
- `LOG_ACTIVE` (bool): Enables colored diagnostic logs from the AI.
- `SANDBOX_ACTIVE` (bool): If True, start from a pre‑defined grouped position; otherwise start with a flat row of `NUMBER_OF_STICKS`.
- `PLAYER_TURN` (bool): If True, player starts; otherwise an-bot starts.
- `PLAYER_ACTIVE` (bool): If False, the player will be skipped (AI vs. itself).
- `INITIAL_POSITION` (tuple[int, ...]): Group sizes for sandbox start, e.g. `(2, 3, 5)` builds `|| _ ||| _ |||||`.
- `NUMBER_OF_STICKS` (int): Board length when not in sandbox mode.
- `DIGGING_LEVEL` (int): Depth limit for the AI’s recursive look‑ahead.

Starting positions
- Sandbox mode (`SANDBOX_ACTIVE=True`): The board is built from `INITIAL_POSITION`, with a blank separator between groups.
- Standard mode (`SANDBOX_ACTIVE=False`): The board is a contiguous row of `NUMBER_OF_STICKS` present sticks.

### How the AI works (high level)
- Generates all legal contiguous moves of size 1–3.
- Scores moves with heuristics based on group patterns (e.g., parity states, exact group matches) using helpers in `anbot/analyze.py` and `anbot/singles.py`.
- If heuristics are inconclusive, performs limited look‑ahead up to `DIGGING_LEVEL`.
- Caches best moves per position in a JSON file to speed up repeated states.

### Caching
The AI caches best moves in `anbot_cache.json` (created automatically). See [CACHE_README.md](CACHE_README.md) for details.

Manage the cache via the included CLI:

```bash
python cache_manager.py stats   # show entries and file size
python cache_manager.py info    # show detailed info
python cache_manager.py clear   # delete the cache file
```

### Testing
Run unit tests with pytest from the repo root:

```bash
pytest -q
```

Included tests cover:
- Core game operations in `game/game.py`
- Analysis utilities in `anbot/analyze.py` and `anbot/singles.py`

### Example session
```text
Welcome to The Sticks Game! You are playing against an-bot. Don't take the last stick!

|  |  |     |  |  |  |     |  |  |  |  |  
1  2  3     4  5  6  7     8  9  10 11 12

Your move: 5 2

|  |  |        |  |     |  |  |  |  |  
1  2  3        4  5     6  7  8  9  10

An-bot takes 1 stick starting at position 7.
```

### Troubleshooting
- “Invalid input” when entering moves: enter two integers like `start count`, where `start` is 1-based and `count` is 1–3, and ensure the sticks are present and adjacent.
- Colored logs not visible: set `LOG_ACTIVE=True` in `game/config.py`. Some terminals may not render ANSI colors by default.

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
