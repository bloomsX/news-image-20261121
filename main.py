#!/usr/bin/env python3
"""Entry point for the make.fun 'Sum up 21 November's world news in one
image' bounty.

The front page is rendered locally by draw.py and shipped in this repository
as entry.png. This program only copies that file to the grader's output
directory. It uses the Python standard library only: no network, no fonts,
no third-party packages, and it writes the exact same bytes on every run.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
