#!/usr/bin/env python3
"""Entry for the make.fun bounty
'u-ricoxyz-loading-screen-gold-a-tip-in-200-characters-2b1df270':
a loading-screen tip (<=200 characters) for stressed developers and
AI coding agents. Prints ONLY the entry text to stdout and exits 0.
"""

import os
import sys

ENTRY = (
    "Tip: The bug is never in the code you just wrote \u2014 "
    "it's in the 2 a.m. code you swore you'd fix tomorrow. "
    "Breathe. Git-blame yourself later."
)


MAX_CHARS = 200


def validate_entry(text: str) -> str:
    """Validate the entry against the bounty rules before printing it."""
    if not text:
        raise SystemExit("error: entry text is empty")
    if "\n" in text or "\r" in text:
        raise SystemExit("error: entry must be a single line")
    if len(text) > MAX_CHARS:
        raise SystemExit(
            f"error: entry is {len(text)} characters, over the "
            f"{MAX_CHARS}-character limit"
        )
    if any(ord(ch) < 0x20 for ch in text):
        raise SystemExit("error: entry contains control characters")
    return text


def emit(text: str) -> None:
    """Print the entry to stdout, with fallbacks if the text write fails."""
    try:
        print(text)
    except BrokenPipeError:
        # Downstream closed the pipe: write raw UTF-8 bytes instead.
        try:
            sys.stdout.buffer.write((text + "\n").encode("utf-8"))
            sys.stdout.buffer.flush()
        except BrokenPipeError:
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, sys.stdout.fileno())
    except UnicodeEncodeError:
        # Stdout cannot encode the em dash: force UTF-8 and retry once.
        sys.stdout.reconfigure(encoding="utf-8", errors="strict")
        print(text)


def main() -> int:
    emit(validate_entry(ENTRY))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
