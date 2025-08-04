#!/usr/bin/env python3
"""
Command-line utility for managing the an-bot cache system
"""

import argparse
from anbot.cache import clear_cache, print_cache_stats, get_cache_stats

def main():
    parser = argparse.ArgumentParser(description='An-bot Cache Manager')
    parser.add_argument('action', choices=['clear', 'stats', 'info'], 
                       help='Action to perform: clear (clear cache), stats (show statistics), info (show info)')
    
    args = parser.parse_args()
    
    if args.action == 'clear':
        print("Clearing an-bot cache...")
        clear_cache()
        print("Cache cleared successfully!")
        
    elif args.action == 'stats':
        print_cache_stats()
        
    elif args.action == 'info':
        entries, file_size = get_cache_stats()
        print("An-bot Cache Information:")
        print(f"  Cache file: anbot_cache.json")
        print(f"  Total entries: {entries}")
        print(f"  File size: {file_size} bytes")
        if file_size > 0:
            print(f"  Average entry size: {file_size / entries:.1f} bytes")
        else:
            print("  Cache is empty")

if __name__ == "__main__":
    main() 