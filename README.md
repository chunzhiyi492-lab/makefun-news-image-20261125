# The world in one image — 25 November 2026

A newspaper-style infographic summing up Wednesday 25 November 2026's
world news: Huawei's conviction in a US court, the probe into Shanghai
party chief Chen Jining, a hostage siege at a Colombian supermarket,
Iran's warning to ships in the Strait of Hormuz, the White House turkey
pardon, and the UN's count of women killed by relatives.

## What is in this repo

- `draw.py` — the program that draws `entry.png` with Pillow. Run it
  yourself to rebuild the picture from scratch.
- `entry.png` — the finished 1024x1024 image.
- `main.py` — the entry point. It copies `entry.png` to the output
  directory, byte for byte, on every run.

## Rebuilding

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Both commands are deterministic: run them twice and the bytes match.
The finished image is 1024x1024 and well under the 1 MiB limit.

## Entry

Built for the [make.fun](https://make.fun/bounty/news-image-20261125)
news-image bounty of 25 November 2026.
