"""News-image entry for 25 November 2026.

Copies the bundled infographic to /output/entry.png using only the
Python standard library. No network, no randomness: every run writes
the same bytes.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    src = HERE / "entry.png"
    if not src.is_file():
        raise FileNotFoundError("entry.png missing beside main.py")
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, OUT / "entry.png")


if __name__ == "__main__":
    main()
