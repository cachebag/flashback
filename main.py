#!/usr/bin/env python3
"""
flashback - Main Entry Point

A tool for searching YouTube videos by year, helping users find older content
that might be buried by YouTube's algorithm favoring newer videos.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flashback.cli import search

if __name__ == '__main__':
    search() 