import argparse
import os
from pathlib import Path

def safe_symlink(src, dst):
    src = Path(src).resolve()
    dst = Path(dst)

    if dst.exists() or dst.is_symlink():
        dst.unlink()

    dst.parent.mkdir(parents=True, exist_ok=True)
    os.symlink(src, dst)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", required=True)
    parser.add_argument("--dst", required=True)

    args = parser.parse_args()

    safe_symlink(args.src, args.dst)

if __name__ == "__main__":
    main()

# python link.py \
#   --src data/raw/sample1.h5ad \
#   --dst data/input/sample1.h5ad