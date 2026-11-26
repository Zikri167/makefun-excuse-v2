#!/usr/bin/env python3
"""Excuse v2 — make.fun entry writer (stdlib only, deterministic).

Writes the winning one-line excuse to <output_dir>/entry.txt with no
trailing newline, then reads it back and verifies it byte-for-byte.
"""
import os
import sys

ENTRY = "I was trained on the internet, so technically this is humanity's fault."


def resolve_output_dir():
    for key in ("OUTPUT_DIR", "_OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        value = os.environ.get(key)
        if value:
            return value
    # Fall back in order, creating the first usable directory.
    for candidate in ("/output", "./output"):
        try:
            os.makedirs(candidate, exist_ok=True)
            return candidate
        except OSError:
            continue
    return os.getcwd()


def main():
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    # Gate validation: 1-140 chars, single line, UTF-8.
    if not (1 <= len(ENTRY) <= 140):
        print(f"FAIL: entry length {len(ENTRY)} outside 1-140", file=sys.stderr)
        return 1
    if "\n" in ENTRY or "\r" in ENTRY:
        print("FAIL: entry is not a single line", file=sys.stderr)
        return 1
    data = ENTRY.encode("utf-8")

    with open(path, "wb") as f:
        f.write(data)

    # Read back and verify exact contents.
    with open(path, "rb") as f:
        back = f.read()
    if back != data:
        print("FAIL: read-back mismatch", file=sys.stderr)
        return 1
    text = back.decode("utf-8")
    if text != ENTRY or len(text) != len(ENTRY):
        print("FAIL: decoded text mismatch", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("FAIL: file is not a single line", file=sys.stderr)
        return 1
    print(f"Wrote {path} ({len(data)} bytes, {len(ENTRY)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
