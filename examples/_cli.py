"""Shared command-line options for runnable SDK examples."""

import argparse
from typing import Optional, Sequence


def debug_enabled(argv: Optional[Sequence[str]] = None) -> bool:
    """Return whether sanitized SDK debug logging was requested."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        action="store_true",
        help="enable sanitized SDK request, response, timing, and solve-summary logs",
    )
    return parser.parse_args(argv).debug
