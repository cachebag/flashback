#!/usr/bin/env python3

import sys
from .cli.interface import run_cli  
from .tui.interface import run_tui


def main_tui():
    run_tui()


def main_cli():
    run_cli()


def main():
    """Main entry point with --cli flag support (for backwards compatibility)."""
    # Check if --cli flag is provided
    if '--cli' in sys.argv:
        # Remove --cli from argv so click doesn't see it
        sys.argv.remove('--cli')
        main_cli()
    else:
        # Default to TUI interface
        main_tui()


if __name__ == '__main__':
    main() 