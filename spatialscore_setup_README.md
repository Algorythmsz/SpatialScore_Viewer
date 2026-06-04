# SpatialScore image setup

`spatialscore_browser.html` references **2,086 unique images** across **25 source datasets**. Without these images, the viewer shows placeholder squares.

## Option 1 — full archive (simple, recommended)

```bash
pip install huggingface_hub tqdm
python download_spatialscore_images.py
```

This:
1. Downloads `SpatialScore.zip` from [haoningwu/SpatialScore](https://huggingface.co/datasets/haoningwu/SpatialScore) on Hugging Face (several GB)
2. Unzips into `./spatialscore_images/`
3. Result: directories `./spatialscore_images/CV-Bench/`, `./spatialscore_images/BLINK/`, ..., one per source

## Option 2 — keep only what the viewer needs (saves disk)

```bash
python download_spatialscore_images.py --keep-only-needed
```

Same as Option 1, but after unzip, prunes all unused images (~26K → 2,086). Uses `spatialscore_required_images.json` as the manifest.

## Option 3 — manual via huggingface-cli (one-liner)

```bash
huggingface-cli download --resume-download --repo-type dataset \
    haoningwu/SpatialScore --local-dir ./spatialscore_images \
    --local-dir-use-symlinks False
cd spatialscore_images && unzip SpatialScore.zip
```

## Connecting images to the viewer

The viewer's `image_paths` look like:
```
./CV-Bench/img/2D/count/ade20k_121.png
./BLINK/Spatial_Relation/images/val_Spatial_Relation_20_19_1.jpg
./3DSRBench/coco_images/train2017/000000366517.jpg
```

The HTML expects to sit **next to** these top-level dataset directories. Two ways:

**A. Put viewer inside the images directory:**
```
spatialscore_images/
├── spatialscore_browser.html    ← move here
├── CV-Bench/
├── BLINK/
├── 3DSRBench/
└── ...
```

**B. Symlink the dataset directories next to the viewer:**
```bash
cd <where spatialscore_browser.html is>
for d in spatialscore_images/*/; do ln -s "$PWD/$d" .; done
```

Once placed correctly, the placeholders in the viewer turn into actual images.

## If you can't access Hugging Face directly

```bash
python download_spatialscore_images.py --hf-mirror
```

Sets `HF_ENDPOINT=https://hf-mirror.com` for the duration of the download.

## What's in `spatialscore_required_images.json`?

The manifest of every image referenced by the viewer:
```json
{
  "total_unique_images": 2086,
  "by_source_dataset": {
    "vsi-bench": ["./VSI-Bench/32_frames/scannetpp/cc5237fd77/frame_00.jpg", ...],
    "SITE-Bench": [...],
    ...
  },
  "all_paths": ["./CV-Bench/img/2D/count/ade20k_121.png", ...]
}
```

Use with `--keep-only-needed` to prune the unzipped output, or write your own selective downloader.

## Source dataset breakdown (top 10)

| count | source |
|---|---|
| 608 | vsi-bench |
| 575 | SITE-Bench |
| 352 | STI-Bench |
| 224 | VLM4D |
| 61  | SpatialScore-Repurpose |
| 56  | SpaCE-10 |
| 40  | MMIU |
| 24  | Spatial-Visualization |
| 23  | OmniSpatial |
| 22  | SPAR-Bench |
| ... | ... (15 more sources) |

Full list in the manifest.

## Citation

If you use the images, cite both SpatialScore and the original source datasets:
```bibtex
@article{wu2025spatialscore,
  author = {Wu, Haoning and Huang, Xiao and Chen, Yaohui and Zhang, Ya and Wang, Yanfeng and Xie, Weidi},
  title = {SpatialScore: Towards Unified Evaluation for Multimodal Spatial Understanding},
  journal = {arXiv preprint arXiv:2505.17012},
  year = {2025}
}
```
