#!/usr/bin/env bash
# Run after download_spatialscore_images.py completes.
# Creates symlinks so index.html can find images at ./CV-Bench/, ./BLINK/, etc.
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
IMAGES_DIR="$SCRIPT_DIR/spatialscore_images"

cd "$SCRIPT_DIR"

# Symlink each top-level dataset directory next to index.html
for d in "$IMAGES_DIR"/*/; do
    name="$(basename "$d")"
    if [ ! -e "$name" ]; then
        ln -s "$d" "$name"
        echo "linked: $name -> $d"
    else
        echo "skip (exists): $name"
    fi
done

echo ""
echo "Done. Open index.html to verify images load."
