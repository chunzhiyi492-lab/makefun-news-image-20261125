"""Entry point for the 25 November 2026 news-image bounty.

Places the pre-drawn infographic at <output>/entry.png. The grader runs
this twice and requires identical bytes both times, so this program does
nothing but copy a fixed file: standard library only, no network, no
clocks, no randomness. The picture itself is drawn by draw.py.
"""

import os
import shutil

IMAGE_NAME = "entry.png"
DEFAULT_OUTPUT = "/output"


def place_entry():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE_NAME)
    if not os.path.isfile(source):
        raise FileNotFoundError("entry.png missing beside main.py: %s" % source)
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT)
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, IMAGE_NAME)
    shutil.copyfile(source, target)
    # The grader collects outputs as a different user: leave the file
    # world-readable instead of the 0600 a fresh copy might otherwise get.
    os.chmod(target, 0o644)


if __name__ == "__main__":
    place_entry()
