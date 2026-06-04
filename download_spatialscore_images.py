#!/usr/bin/env python3
"""
Download SpatialScore images for the spatialscore_browser.html viewer.

The viewer references 2,086 unique images across 25 source datasets, all
packaged in a single archive on Hugging Face Hub:
    https://huggingface.co/datasets/haoningwu/SpatialScore

This script:
  1. Downloads SpatialScore.zip from HF Hub (~several GB)
  2. Unzips into the target directory
  3. (Optional) Prunes images NOT referenced by our 300 picked samples,
     keeping only the ~2,086 needed (saves significant disk space)

Usage:
    # default — download + unzip into ./spatialscore_images
    python download_spatialscore_images.py

    # with pruning to keep only what the viewer needs
    python download_spatialscore_images.py --keep-only-needed

    # custom output location
    python download_spatialscore_images.py --output /path/to/images

    # use HF mirror (for users with HF access issues)
    python download_spatialscore_images.py --hf-mirror

Requirements:
    pip install huggingface_hub tqdm
"""
import argparse
import os
import sys
import json
import shutil
import zipfile
from pathlib import Path


def ensure_packages():
    try:
        import huggingface_hub  # noqa: F401
    except ImportError:
        print("[error] huggingface_hub not installed.\n"
              "        Install with:  pip install huggingface_hub tqdm", file=sys.stderr)
        sys.exit(1)


def download_archive(output_dir: Path, use_mirror: bool):
    """Download SpatialScore.zip from HF Hub."""
    if use_mirror:
        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
        print(f"[info] Using HF mirror: {os.environ['HF_ENDPOINT']}")

    from huggingface_hub import hf_hub_download

    print(f"[1/3] Downloading SpatialScore_benchmark.zip from haoningwu/SpatialScore ...")
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = hf_hub_download(
        repo_id='haoningwu/SpatialScore',
        filename='SpatialScore_benchmark.zip',
        repo_type='dataset',
        local_dir=str(output_dir),
    )
    print(f"      ✓ Saved to {zip_path}")
    return Path(zip_path)


def unzip_archive(zip_path: Path, output_dir: Path):
    """Unzip SpatialScore_benchmark.zip into output_dir, flattening a top-level directory if present."""
    print(f"[2/3] Unzipping {zip_path.name} into {output_dir} ...")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        members = zf.namelist()
        # Detect single top-level directory (e.g. SpatialScore_benchmark/)
        roots = {m.split('/')[0] for m in members if m}
        single_root = roots.pop() if len(roots) == 1 else None
        try:
            from tqdm import tqdm
            iterator = tqdm(members, desc='      unzipping', unit='file')
        except ImportError:
            iterator = members
            print(f"      (extracting {len(members)} files, tqdm not installed)")
        for m in iterator:
            zf.extract(m, output_dir)
    # Flatten single top-level dir so images sit directly under output_dir
    if single_root:
        nested = output_dir / single_root
        if nested.is_dir():
            print(f"      flattening {single_root}/ -> {output_dir}/")
            for item in nested.iterdir():
                dest = output_dir / item.name
                if not dest.exists():
                    item.rename(dest)
            nested.rmdir() if not any(nested.iterdir()) else None
    print(f"      ✓ Done")


def prune_to_needed(output_dir: Path, manifest_path: Path):
    """Delete any image file not referenced by the viewer's manifest."""
    if not manifest_path.exists():
        print(f"[warn] manifest {manifest_path} not found — skipping prune.")
        return

    with open(manifest_path) as f:
        manifest = json.load(f)

    needed = set()
    for p in manifest['all_paths']:
        # Normalize: './CV-Bench/...' -> 'CV-Bench/...'
        if p.startswith('./'):
            p = p[2:]
        needed.add(p)

    print(f"[3/3] Pruning: keeping {len(needed)} required images, deleting rest ...")
    deleted = 0
    kept = 0
    total_kept_bytes = 0
    total_deleted_bytes = 0
    image_exts = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}

    for root, _, files in os.walk(output_dir):
        for fn in files:
            full = Path(root) / fn
            if full.suffix.lower() not in image_exts:
                continue
            rel = str(full.relative_to(output_dir))
            if rel in needed:
                kept += 1
                total_kept_bytes += full.stat().st_size
            else:
                total_deleted_bytes += full.stat().st_size
                full.unlink()
                deleted += 1

    # delete now-empty dirs (bottom up)
    for root, dirs, files in os.walk(output_dir, topdown=False):
        for d in dirs:
            full = Path(root) / d
            try:
                if not any(full.iterdir()):
                    full.rmdir()
            except OSError:
                pass

    print(f"      ✓ kept {kept} images ({total_kept_bytes/1024/1024:.1f} MB)")
    print(f"      ✓ deleted {deleted} unused images ({total_deleted_bytes/1024/1024:.1f} MB)")


def main():
    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=__doc__)
    ap.add_argument('--output', '-o', type=Path, default=Path('./spatialscore_images'),
                    help='Output directory (default: ./spatialscore_images)')
    ap.add_argument('--manifest', '-m', type=Path,
                    default=Path('./spatialscore_required_images.json'),
                    help='Manifest of needed images (default: ./spatialscore_required_images.json)')
    ap.add_argument('--keep-only-needed', action='store_true',
                    help='After unzip, delete images not in manifest (saves disk space)')
    ap.add_argument('--skip-download', action='store_true',
                    help='Skip download step (assume zip already present in --output)')
    ap.add_argument('--skip-unzip', action='store_true',
                    help='Skip unzip step (assume files already extracted)')
    ap.add_argument('--hf-mirror', action='store_true',
                    help='Use HF mirror endpoint (for restricted networks)')
    args = ap.parse_args()

    ensure_packages()

    output_dir = args.output.resolve()
    zip_path = output_dir / 'SpatialScore_benchmark.zip'

    if not args.skip_download:
        zip_path = download_archive(output_dir, use_mirror=args.hf_mirror)

    if not args.skip_unzip:
        if not zip_path.exists():
            print(f"[error] {zip_path} not found, cannot unzip.", file=sys.stderr)
            sys.exit(1)
        unzip_archive(zip_path, output_dir)

    if args.keep_only_needed:
        prune_to_needed(output_dir, args.manifest)

    print(f"\n[done] Images at: {output_dir}")
    print(f"       Place spatialscore_browser.html next to (or above) this directory.")
    print(f"       The viewer's image paths look like './CV-Bench/img/...' so the")
    print(f"       HTML expects to sit alongside CV-Bench/, BLINK/, 3DSRBench/, etc.")


if __name__ == '__main__':
    main()
