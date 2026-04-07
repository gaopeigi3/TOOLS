import argparse
import os
from pathlib import Path
import yaml


def safe_symlink(src, dst):
    src = Path(src).resolve()
    dst = Path(dst)

    if dst.exists() or dst.is_symlink():
        dst.unlink()

    dst.parent.mkdir(parents=True, exist_ok=True)
    os.symlink(src, dst)


def run_from_config(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)

    for item in config.get("symlink", []):
        src = item["src"]
        dst = item["dst"]
        print(f"link: {src} -> {dst}")
        safe_symlink(src, dst)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--src")
    parser.add_argument("--dst")
    parser.add_argument("--config")

    args = parser.parse_args()

    # 🔥 模式判断
    if args.config:
        run_from_config(args.config)

    elif args.src and args.dst:
        safe_symlink(args.src, args.dst)

    else:
        parser.error("require --src --dst or --config")


if __name__ == "__main__":
    main()