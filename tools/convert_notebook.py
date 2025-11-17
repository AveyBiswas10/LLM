#!/usr/bin/env python3
"""Convert a Jupyter/Colab notebook (.ipynb) into one or more runnable Python scripts.

Usage:
  python tools/convert_notebook.py notebooks/colab_notebook.ipynb

Behavior:
- Produces `scripts/colab_converted.py` by default, combining code cells (code) and
  converting markdown cells into commented blocks.
- If markdown headings (lines starting with `# ` or `## `) are present, the tool
  will split the notebook into multiple `scripts/step_<n>_<slug>.py` files at each
  heading to make steps runnable independently.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def load_notebook(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dirs():
    Path("scripts").mkdir(parents=True, exist_ok=True)


def convert(nb: dict, out_base: Path) -> list[Path]:
    """Convert the notebook dict into scripts. Returns list of created files."""
    cells = nb.get("cells", [])
    created = []

    # Accumulate into a single script unless we encounter headings to split.
    sections: list[tuple[str, list[str]]] = []  # (title, lines)
    current_lines: list[str] = []
    current_title = "main"

    def flush_section():
        nonlocal current_title, current_lines
        if current_lines:
            sections.append((current_title, current_lines))
            current_lines = []

    for cell in cells:
        ctype = cell.get("cell_type")
        src = cell.get("source") or []
        # Normalize lines
        src_lines = [line.rstrip("\n") for line in src]

        if ctype == "markdown":
            # If top line looks like a heading, treat as section boundary
            first = next((ln for ln in src_lines if ln.strip()), "")
            if first.startswith("# ") or first.startswith("## ") or first.startswith("### "):
                # new section
                flush_section()
                current_title = re.sub(r"^#+\s*", "", first).strip()
                # include the heading as a comment
                current_lines.extend([f"# {ln}" for ln in src_lines if ln.strip()])
                current_lines.append("")
                continue
            else:
                # regular markdown -> comment block
                current_lines.extend([f"# {ln}" for ln in src_lines])
                current_lines.append("")

        elif ctype == "code":
            if src_lines:
                current_lines.extend(src_lines)
                current_lines.append("")

    flush_section()

    # If multiple sections, create step files; otherwise create one combined file
    if len(sections) <= 1:
        out = out_base / "colab_converted.py"
        with out.open("w", encoding="utf-8") as f:
            f.write("# Converted from notebook\n")
            f.write("# To run: python scripts/colab_converted.py\n\n")
            for title, lines in sections:
                if title and title != "main":
                    f.write(f"# Section: {title}\n\n")
                for ln in lines:
                    f.write(ln + "\n")
        created.append(out)
    else:
        for i, (title, lines) in enumerate(sections, start=1):
            slug = slugify(title) or f"{i:02d}"
            name = f"step_{i:02d}_{slug}.py"
            out = out_base / name
            with out.open("w", encoding="utf-8") as f:
                f.write("# Converted from notebook\n")
                f.write(f"# Section: {title}\n")
                f.write(f"# To run: python scripts/{name}\n\n")
                for ln in lines:
                    f.write(ln + "\n")
            created.append(out)

    return created


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("Usage: convert_notebook.py <notebook.ipynb>")
        return 2

    nb_path = Path(argv[0])
    if not nb_path.exists():
        print(f"Notebook not found: {nb_path}")
        return 3

    nb = load_notebook(nb_path)
    ensure_dirs()
    out_base = Path("scripts")
    created = convert(nb, out_base)
    print("Created files:")
    for p in created:
        print(" -", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
