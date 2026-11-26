#!/usr/bin/env python3
"""Sum up 25 November 2026 world news in one image (v2).

Entrypoint for the make.fun news-image-20261125 bounty. Standard library
only, no network access. It copies the pre-built image entry.png
(1024x1024, under 1 MiB) to /output/entry.png, or to
$MAKEFUN_OUTPUT_DIR/entry.png when that variable is set.
Running it twice writes exactly the same bytes.

The v2 image sums up Wednesday 25 November 2026 in 39 sourced stories:
13 numbered drawn cards, 26 numbered briefs, region/field counts, a
GMT day strip, a numbers strip, a pin map and a date-check section.
"""

import hashlib
import os
import shutil
import sys


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(src):
        print("error: missing " + src, file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    os.chmod(dst, 0o644)
    # Verify the copy byte for byte before reporting success.
    if _sha256(dst) != _sha256(src):
        print("error: copy mismatch for " + dst, file=sys.stderr)
        return 1
    print("wrote " + dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
