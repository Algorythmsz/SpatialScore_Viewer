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
    1017, 2344,
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
    aspect-ratio:1/1;
    object-fit:cover;
    background:#ddd;
    display:block;
    border:1px solid rgba(0,0,0,0.08);
  }
  .thumbstrip[data-n="1"]{grid-template-columns:1fr;}
  .thumbstrip[data-n="1"] img{aspect-ratio:4/3;}
  .thumbstrip[data-n="2"]{grid-template-columns:1fr 1fr;}
  .thumbstrip[data-n="2"] img{aspect-ratio:4/3;}
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


def inject(html: str, records: dict[int, dict], prefix: str, max_frames: int) -> tuple[str, int]:
    """Return (new_html, n_injected). Inserts a .thumbstrip block right after
    the .st-head <div> in every <article class="stcard ..."> whose body contains
    'id NNNN' for one of our target IDs."""
    # Inject CSS once, right before closing </style>
    if "/* === injected: thumbnail strip === */" not in html:
        html = html.replace("</style>", THUMB_CSS + "</style>", 1)

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

    html_in = args.html.read_text(encoding="utf-8")
    html_out, n = inject(
        html_in,
        records=records,
        prefix=args.prefix.rstrip("/"),
        max_frames=args.max_frames,
    )
    output_path.write_text(html_out, encoding="utf-8")
    print(f"[info] injected thumbnails into {n}/{len(records)} cards")
    print(f"[info] wrote {output_path}")
    return 0 if n == len(records) else 2


if __name__ == "__main__":
    sys.exit(main())
