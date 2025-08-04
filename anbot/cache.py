import json
import os
from typing import Dict, List, Optional, Tuple
from game_types.game_types import Sticks, Move

CACHE_FILE = "anbot_cache.json"

def sticks_to_key(sticks: Sticks) -> str:
    """Convert sticks configuration to a string key for caching"""
    return ''.join('1' if stick else '0' for stick in sticks)

def key_to_sticks(key: str) -> Sticks:
    """Convert cache key back to sticks configuration"""
    return [bool(int(bit)) for bit in key]

def load_cache() -> Dict[str, List[Move]]:
    """Load the cache from file"""
    if not os.path.exists(CACHE_FILE):
        return {}
    
    try:
        with open(CACHE_FILE, 'r') as f:
            cache_data = json.load(f)
            # Convert string keys back to proper format
            return {key: [tuple(move) for move in moves] for key, moves in cache_data.items()}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_cache(cache: Dict[str, List[Move]]) -> None:
    """Save the cache to file"""
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save cache: {e}")

def get_cached_moves(sticks: Sticks) -> Optional[List[Move]]:
    """Get cached best moves for a given stick configuration"""
    cache = load_cache()
    key = sticks_to_key(sticks)
    return cache.get(key)

def write_best_moves(sticks: Sticks, best_moves: List[Move]) -> None:
    """Write best moves to cache for a given stick configuration"""
    cache = load_cache()
    key = sticks_to_key(sticks)
    cache[key] = best_moves
    save_cache(cache)

def clear_cache() -> None:
    """Clear the entire cache"""
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)

def get_cache_stats() -> Tuple[int, int]:
    """Get cache statistics: (total_entries, file_size_bytes)"""
    cache = load_cache()
    file_size = os.path.getsize(CACHE_FILE) if os.path.exists(CACHE_FILE) else 0
    return len(cache), file_size

def print_cache_stats() -> None:
    """Print cache statistics to console"""
    entries, file_size = get_cache_stats()
    print(f"Cache statistics:")
    print(f"  Total entries: {entries}")
    print(f"  File size: {file_size} bytes")
    if file_size > 0:
        print(f"  Average entry size: {file_size / entries:.1f} bytes") 