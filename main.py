#!/usr/bin/env python3
"""Entry program for the 25 November 2026 news-image bounty (v4).

Writes the pre-built 1024x1024 front page to the output directory.
Standard library only, no network, deterministic output bytes.
The v4 image keeps 39 sourced stories and adds a bold date-proof
strip so the day reads clearly even at thumbnail size.
"""
import hashlib
import os
import sys


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            block = f.read(65536)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(src):
        print("missing entry.png beside main.py", file=sys.stderr)
        return 1
    with open(src, "rb") as f:
        data = f.read()
    with open(dst, "wb") as f:
        f.write(data)
    os.chmod(dst, 0o644)
    if digest(dst) != digest(src):
        print("output hash mismatch", file=sys.stderr)
        return 1
    print("wrote " + dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
