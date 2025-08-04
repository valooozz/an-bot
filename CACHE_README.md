# An-bot Cache System

## Overview

The cache system stores the best moves calculated by an-bot for different stick configurations. This improves performance by avoiding recalculating moves for previously analyzed positions.

## How it Works

1. **Cache Key**: Each stick configuration is converted to a binary string (1 for stick present, 0 for stick removed)
2. **Storage**: Best moves are stored in `anbot_cache.json` file
3. **Lookup**: Before calculating moves, an-bot checks if the current configuration exists in cache
4. **Fallback**: If not found in cache, calculates moves normally and stores the result

## Files

- `anbot/cache.py`: Core cache functionality
- `anbot_cache.json`: Cache storage file (created automatically)
- `cache_manager.py`: Command-line utility for cache management

## Functions

### Core Functions
- `get_cached_moves(sticks)`: Retrieve cached moves for a configuration
- `write_best_moves(sticks, moves)`: Store best moves for a configuration
- `load_cache()`: Load cache from file
- `save_cache(cache)`: Save cache to file

### Utility Functions
- `clear_cache()`: Remove all cached data
- `get_cache_stats()`: Get cache statistics (entries, file size)
- `print_cache_stats()`: Display cache statistics

## Command Line Interface

The cache system includes a command-line utility for easy management:

### Available Commands

| Command | Description |
|---------|-------------|
| `python cache_manager.py clear` | Clear all cached data |
| `python cache_manager.py stats` | Show cache statistics |
| `python cache_manager.py info` | Show detailed cache information |
| `python cache_manager.py --help` | Show help and available options |

### Examples

**Clear the cache when you want to start fresh:**
```bash
python cache_manager.py clear
```

**Check how much data is cached:**
```bash
python cache_manager.py stats
```

**Get detailed cache information:**
```bash
python cache_manager.py info
```

## Usage

The cache system is automatically integrated into an-bot's move calculation. When `get_best_move_by_score()` is called:

1. It first checks the cache for the current stick configuration
2. If found, returns a random choice from cached best moves
3. If not found, calculates moves normally and caches the result

## Example

```python
from anbot.cache import write_best_moves, get_cached_moves

# Store best moves for a configuration
sticks = [True, True, True, False, True]
best_moves = [(0, 1), (0, 2)]
write_best_moves(sticks, best_moves)

# Retrieve cached moves
cached_moves = get_cached_moves(sticks)
print(cached_moves)  # [(0, 1), (0, 2)]
```

## Cache File Format

The cache is stored as JSON with the following structure:
```json
{
  "11100": [[0, 1], [0, 2]],
  "11011": [[0, 1], [2, 2]]
}
```

Where keys are binary strings representing stick configurations and values are lists of best moves.

## Performance Benefits

- **Faster Move Calculation**: Cached configurations return instantly
- **Reduced Computation**: Avoids recalculating for repeated positions
- **Persistent Storage**: Cache persists between game sessions

## Cache Management

- The cache file grows over time as new configurations are encountered
- Use `python cache_manager.py clear` to reset if needed
- Monitor cache size with `python cache_manager.py stats`
- The cache file is automatically excluded from version control (added to .gitignore) 