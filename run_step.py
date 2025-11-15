#!/usr/bin/env python3
"""Run a converted notebook script or any script by path.

Usage:
  python run_step.py --script scripts/colab_notebook.py
"""
import argparse
import os
import runpy
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--script", "-s", help="Path to script to run", default="scripts/colab_notebook.py")
    args = p.parse_args()

    if not os.path.exists(args.script):
        print(f"Script not found: {args.script}")
        sys.exit(2)

    runpy.run_path(args.script, run_name="__main__")


if __name__ == "__main__":
    main()
