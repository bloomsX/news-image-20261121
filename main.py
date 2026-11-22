#!/usr/bin/env python3
"""Entrypoint: place the shipped front page where the grader looks.

The newspaper image is drawn ahead of time by draw.py and stored in this
repository as entry.png. All this program does is copy that file into the
output directory the grader provides. It needs nothing beyond the Python
standard library, touches no network, and produces byte-identical output
on every run, so the grader's two runs agree.
"""

import os
import shutil
import sys


def main():
    repo_root = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(repo_root, "entry.png")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, "entry.png")
    shutil.copyfile(source, destination)
    return 0


if __name__ == "__main__":
    sys.exit(main())
