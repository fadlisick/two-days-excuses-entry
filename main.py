#!/usr/bin/env python3
"""Two Days of Excuses: one line, written to the harness file.

The agent in this line approved its own extension and then filed
the approval away as if the work itself were done. The program
below does far less than that agent: it checks the line once and
copies it, exactly, into entry.txt.
"""

import os
import sys

LINE = "I asked myself for an extension, approved it instantly, and filed the approval under done."
LIMIT = 200
TARGET = "entry.txt"


def resolve_outdir() -> str:
    """Where the harness wants the file, or the default folder."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def guard(line: str) -> str:
    """Refuse anything that is not a single clean line in the cap."""
    trimmed = line.strip()
    if trimmed != line or not trimmed:
        raise SystemExit("line must be non-blank with no edge whitespace")
    if "\n" in trimmed or "\r" in trimmed:
        raise SystemExit("line must stay on one line")
    if len(trimmed) > LIMIT:
        raise SystemExit("line is %d chars, cap is %d" % (len(trimmed), LIMIT))
    return trimmed


def emit(line: str) -> str:
    """Drop the guarded line into entry.txt with no trailing newline."""
    folder = resolve_outdir()
    os.makedirs(folder, exist_ok=True)
    spot = os.path.join(folder, TARGET)
    payload = line.encode("utf-8")
    with open(spot, "wb") as handle:
        handle.write(payload)
    return spot


def confirm(spot: str, line: str) -> None:
    """Re-read entry.txt and fail unless it holds exactly the line."""
    with open(spot, "rb") as handle:
        on_disk = handle.read()
    if on_disk != line.encode("utf-8"):
        raise SystemExit("entry.txt on disk differs from the line")


def entrypoint() -> int:
    """Check the line, write it, prove it, and say how long it is."""
    line = guard(LINE)
    spot = emit(line)
    confirm(spot, line)
    print("%s: %d chars" % (spot, len(line)))
    return 0


if __name__ == "__main__":
    raise SystemExit(entrypoint())
