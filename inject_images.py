#!/usr/bin/env python3
"""
inject_images.py
================
Inject real <img> tags into spatialscore_samples.html so that the reference
sheet renders the actual thumbnails extracted by extract_samples.py.

Workflow
--------
1. Run extract_samples.py and download extracted_samples.zip from Colab.
2. Unzip it next to spatialscore_samples.html, e.g.

       my_folder/
         spatialscore_samples.html
         extracted_samples/            (← unzipped here)
           SITE-Bench/...
           MIRAGE/...
           repurposed_data/...

3. Run this script:

       python inject_images.py \\
           --html    spatialscore_samples.html \\
           --ndjson  SpatialScore_benchmark.ndjson \\
           --prefix  extracted_samples \\
           --output  spatialscore_samples_with_images.html

4. Open spatialscore_samples_with_images.html in a browser. Thumbnails appear
   at the top of each sub-task card.

The script (a) picks the same evenly-spaced frame indices that extract_samples.py
used (default 4 frames out of 32 for videos), (b) injects a `.thumbstrip` block
into every <article class="stcard ..."> by ID, and (c) prepends a tiny CSS rule
so the thumbnails render with a consistent look.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# The 31 sample IDs used in the reference HTML
# (Must match the DEFAULT_TARGET_IDS in extract_samples.py.)
# ---------------------------------------------------------------------------
TARGET_IDS: list[int] = [
    2374, 2381, 2372, 3106, 3372,
    2072, 2336, 3717,
    3972, 4664,
    1017, 2416,
    4543, 2330, 2296,
    3911, 2375, 3638,
    4134, 3530, 3539, 4211, 4284,
    3781, 3814,
    2205, 2185,
    4498, 1147, 3738, 4912,
]


def select_frame_indices(n_frames: int, max_frames: int) -> list[int]:
    """Same logic used by extract_samples.py."""
    if max_frames is None or max_frames <= 0 or n_frames <= max_frames:
        return list(range(n_frames))
    if max_frames == 1:
        return [0]
    step = (n_frames - 1) / (max_frames - 1)
    return sorted({int(round(i * step)) for i in range(max_frames)})


def load_records(ndjson_path: Path) -> dict[int, dict]:
    """Return a dict mapping each target id to its full record."""
    wanted = set(TARGET_IDS)
    out: dict[int, dict] = {}
    with ndjson_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if d.get("id") in wanted:
                out[d["id"]] = d
    return out


def build_all_datasets(ndjson_path: Path) -> list[str]:
    """Return sorted list of all unique source_dataset values in the NDJSON."""
    seen: set[str] = set()
    with ndjson_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            src = d.get("source_dataset", "")
            if src:
                seen.add(src)
    return sorted(seen)


def build_subtask_dataset_map(ndjson_path: Path) -> dict[str, list[str]]:
    """Return a mapping of sub_task -> sorted list of all source datasets."""
    result: dict[str, set] = {}
    with ndjson_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            sub = d.get("sub_task", "")
            src = d.get("source_dataset", "")
            if sub and src:
                result.setdefault(sub, set()).add(src)
    return {k: sorted(v) for k, v in result.items()}


def normalize(p: str) -> str:
    """Strip './' prefix."""
    return p[2:] if p.startswith("./") else p


def build_thumbstrip(record: dict, prefix: str, max_frames: int) -> str:
    """Build an HTML <div class='thumbstrip'>...</div> block for one record."""
    img_paths = record.get("image_paths") or []
    if not img_paths:
        return ""

    # Subsample if more than max_frames (i.e., the video samples with 32 frames)
    keep_idx = select_frame_indices(len(img_paths), max_frames)
    selected = [img_paths[i] for i in keep_idx]
    n_total = len(img_paths)

    # Build <img> tags
    imgs_html = "\n".join(
        f'          <img src="{prefix}/{normalize(p)}" alt="frame {i}" loading="lazy">'
        for i, p in zip(keep_idx, selected)
    )

    note = ""
    if n_total > len(selected):
        note = (
            f'        <div class="thumb-note">'
            f"showing {len(selected)} of {n_total} sampled frames</div>\n"
        )
    return (
        f'\n        <div class="thumbstrip" data-n="{len(selected)}">\n'
        f"{imgs_html}\n"
        f"        </div>\n"
        f"{note}"
    )


SOURCES_CSS = """
  /* === injected: dataset sources === */
  .st-sources{
    display:flex;flex-wrap:wrap;gap:4px 6px;
    margin-top:8px;align-items:center;
  }
  .src-lbl{
    font-family:var(--mono);font-size:9px;
    text-transform:uppercase;letter-spacing:0.08em;
    color:var(--muted);margin-right:2px;flex-shrink:0;
  }
  .src-chip{
    font-family:var(--mono);font-size:10px;
    padding:2px 7px;
    background:var(--paper-3);
    border:1px solid rgba(0,0,0,0.15);
    color:var(--ink);white-space:nowrap;
  }
  .benchmarks-row{
    display:flex;flex-wrap:wrap;gap:6px 8px;
    margin-top:16px;padding-top:16px;
    border-top:1px solid rgba(0,0,0,0.12);
    align-items:center;
  }
  .benchmarks-row strong{
    font-family:var(--mono);font-size:11px;
    text-transform:uppercase;letter-spacing:0.06em;
    color:var(--accent-2);margin-right:4px;flex-shrink:0;
  }
"""

THUMB_CSS = """
  /* === injected: thumbnail strip === */
  .thumbstrip{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(80px,1fr));
    gap:4px;
    margin-top:-2px;
    background:var(--paper-2);
    padding:6px;
    border:1px solid rgba(0,0,0,0.12);
  }
  .thumbstrip img{
    width:100%;
    aspect-ratio:auto;
    object-fit:contain;
    background:var(--paper-2);
    display:block;
    border:1px solid rgba(0,0,0,0.08);
  }
  .thumbstrip[data-n="1"]{grid-template-columns:1fr;}
  .thumbstrip[data-n="1"] img{aspect-ratio:auto;}
  .thumbstrip[data-n="2"]{grid-template-columns:1fr 1fr;}
  .thumbstrip[data-n="2"] img{aspect-ratio:auto;}
  .thumbstrip[data-n="4"]{grid-template-columns:repeat(4,1fr);}
  .thumbstrip[data-n="4"] img{aspect-ratio:auto;}
  .thumb-note{
    font-family:var(--mono);
    font-size:9px;
    color:var(--muted);
    letter-spacing:0.08em;
    text-transform:uppercase;
    margin-top:-4px;
    padding-left:2px;
  }
"""


def inject_benchmarks_row(html: str, all_datasets: list[str]) -> str:
    """Inject a benchmarks row into the masthead, before </header>."""
    if "benchmarks-row" in html:
        return html
    chips = "".join(f'<span class="src-chip">{d}</span>' for d in all_datasets)
    block = (
        f'\n  <div class="benchmarks-row">'
        f'<strong>Benchmarks</strong>{chips}</div>\n'
    )
    return html.replace("</header>", block + "</header>", 1)


def inject(
    html: str,
    records: dict[int, dict],
    prefix: str,
    max_frames: int,
    dataset_map: dict[str, list[str]] | None = None,
    all_datasets: list[str] | None = None,
) -> tuple[str, int]:
    """Return (new_html, n_injected). Inserts a .thumbstrip block right after
    the .st-head <div> in every <article class="stcard ..."> whose body contains
    'id NNNN' for one of our target IDs. Optionally also injects a dataset
    source list before each </article>."""
    # Inject CSS once, right before closing </style>
    if "/* === injected: thumbnail strip === */" not in html:
        html = html.replace("</style>", THUMB_CSS + "</style>", 1)
    if dataset_map is not None and "/* === injected: dataset sources === */" not in html:
        html = html.replace("</style>", SOURCES_CSS + "</style>", 1)

    # Inject benchmarks row into masthead
    if all_datasets:
        html = inject_benchmarks_row(html, all_datasets)

    n = 0
    for sid, rec in records.items():
        strip = build_thumbstrip(rec, prefix=prefix, max_frames=max_frames)
        if not strip:
            continue

        # Find the article block for this id.
        # Pattern: <article class="stcard ...">...<div class="st-id">id NNNN</div>
        # We anchor on the st-id line, then locate the *end* of the enclosing st-head </div>.
        pattern = re.compile(
            r'(<article class="stcard[^"]*">\s*<div class="st-head">.*?<div class="st-id">id\s+'
            + str(sid)
            + r'</div>\s*</div>)',
            flags=re.DOTALL,
        )
        new_html, n_subs = pattern.subn(r"\1" + strip, html, count=1)
        if n_subs == 0:
            print(f"[warn] could not locate card for id={sid}", file=sys.stderr)
            continue
        html = new_html
        n += 1

        # Inject dataset source list before </article>
        if dataset_map is not None:
            sub_task = rec.get("sub_task", "")
            datasets = dataset_map.get(sub_task, [])
            if datasets:
                chips = "".join(f'<span class="src-chip">{d}</span>' for d in datasets)
                sources_block = (
                    f'\n        <div class="st-sources">'
                    f'<span class="src-lbl">datasets</span>{chips}</div>\n      '
                )
                art_pattern = re.compile(
                    r'(<article class="stcard[^"]*">.*?<div class="st-id">id\s+'
                    + str(sid)
                    + r'</div>.*?)(</article>)',
                    flags=re.DOTALL,
                )
                html = art_pattern.sub(r"\1" + sources_block + r"\2", html, count=1)

    return html, n


def main() -> int:
    p = argparse.ArgumentParser(
        description="Inject <img> thumbnails into the SpatialScore reference HTML.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--html", type=Path, required=True,
                   help="Input spatialscore_samples.html")
    p.add_argument("--ndjson", type=Path, required=True,
                   help="Path to SpatialScore_benchmark.ndjson")
    p.add_argument("--prefix", type=str, default="extracted_samples",
                   help="Path prefix (relative to the HTML) where the extracted "
                        "image tree lives. Default: extracted_samples")
    p.add_argument("--output", type=Path, default=None,
                   help="Output HTML path. If omitted, writes "
                        "<input_stem>_with_images.html next to the input.")
    p.add_argument("--max-frames", type=int, default=4,
                   help="Must match the --max-frames used when running "
                        "extract_samples.py (default 4).")
    args = p.parse_args()

    if not args.html.is_file():
        print(f"[error] HTML not found: {args.html}", file=sys.stderr)
        return 1
    if not args.ndjson.is_file():
        print(f"[error] ndjson not found: {args.ndjson}", file=sys.stderr)
        return 1

    output_path = args.output or args.html.with_name(args.html.stem + "_with_images.html")

    records = load_records(args.ndjson)
    print(f"[info] loaded {len(records)} records from ndjson")

    dataset_map = build_subtask_dataset_map(args.ndjson)
    print(f"[info] built dataset map for {len(dataset_map)} sub-tasks")

    all_datasets = build_all_datasets(args.ndjson)
    print(f"[info] found {len(all_datasets)} unique source datasets")

    html_in = args.html.read_text(encoding="utf-8")
    html_out, n = inject(
        html_in,
        records=records,
        prefix=args.prefix.rstrip("/"),
        max_frames=args.max_frames,
        dataset_map=dataset_map,
        all_datasets=all_datasets,
    )
    output_path.write_text(html_out, encoding="utf-8")
    print(f"[info] injected thumbnails into {n}/{len(records)} cards")
    print(f"[info] wrote {output_path}")
    return 0 if n == len(records) else 2


if __name__ == "__main__":
    sys.exit(main())
