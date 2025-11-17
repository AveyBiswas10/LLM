#!/usr/bin/env bash
# Run all scripts created in `scripts/` sequentially.
set -euo pipefail

SCRIPTS=(scripts/*.py)
if [ ${#SCRIPTS[@]} -eq 0 ]; then
  echo "No scripts found in scripts/"
  exit 1
fi

for s in "${SCRIPTS[@]}"; do
  echo "---- Running $s ----"
  python "$s"
done
