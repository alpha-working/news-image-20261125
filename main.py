#!/usr/bin/env python3
"""Sum up 25 November 2026 world news in one image.

Entrypoint for make.fun news-image-20261125. Stdlib only, no network.
Copies the pre-built image entry.png (1024x1024, <1 MiB) to
/output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png when set).
Running it twice writes the same bytes.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    os.chmod(dst, 0o644)
    print("wrote " + dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
