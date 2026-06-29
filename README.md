# SpatialScore

**SpatialScore** is a comprehensive benchmark for evaluating spatial reasoning capabilities of multimodal large language models (MLLMs). It aggregates and harmonizes 25 existing spatial benchmarks into a unified evaluation suite covering 10 spatial reasoning categories, 30 sub-tasks, and 5,025 curated question-answer pairs.

---

## 🌐 Live Browser

Explore the benchmark interactively on GitHub Pages:

- **[I/O Browser](https://algorythmsz.github.io/SpatialScore/)** — Browse individual samples with full input/output details and a gallery view
- **[Representative Samples](https://algorythmsz.github.io/SpatialScore/spatialscore_samples.html)** — Representative examples per category with full prompts

---

## Overview

| Stat | Value |
|---|---|
| Categories | 10 |
| Sub-tasks | 30 |
| Total samples | 5,025 |
| Source datasets | 25 |
| Input modalities | single-image, multi-image, video |
| Question types | multi-choice, open-ended, judgement |

---

## Categories & Sub-tasks

| Category | Sub-tasks | Total available |
|---|---|---|
| **Camera** | Homography Matrix, Camera Extrinsics, Camera Motion, Camera Intrinsics | 778 |
| **Object Localization** | Spatial Position, Object Existence, 3D Object Detection, 2D Localization | 697 |
| **Object Distance** | Relative Distance, Absolute Distance | 576 |
| **Object Size** | Relative Size, Absolute Size, Size Compatibility | 559 |
| **Depth Estimation** | Relative Depth, Absolute Depth | 520 |
| **Mental Animation** | Multi-view Projection, 2D/3D Rotation, Maze Navigation, Spatial Map, Space Folding | 447 |
| **View Reasoning** | View Perspective, Orientation | 446 |
| **Object Motion** | Point Tracking, Object Motion, Velocity Estimation | 415 |
| **Counting** | Object Counting, Video Counting, Count with Relation | 315 |
| **Temporal Reasoning** | Appearance Order, Navigation Route | 272 |

---

## Source Datasets

SpatialScore aggregates samples from 25 publicly available datasets:

3DSRBench · BLINK · CVBench · MIRAGE · MMIU · MMSI-Bench · MMVP · OmniSpatial · QSpatialBench-Plus · QSpatialBench-ScanNet · RoboSpatial-Home · SITE-Bench · SPAR-Bench · SRBench · STI-Bench · SpaCE-10 · Spatial-Visualization · SpatialBench · SpatialEval · SpatialScore-Repurpose · VLM4D · realworldqa · spatialsense · vsi-bench · vsr

---

## Data Format

Each sample in `SpatialScore_benchmark.ndjson` contains:

```json
{
  "id": 302,
  "source_dataset": "MMIU",
  "category": "Camera",
  "sub_task": "Homography Matrix",
  "question": "...",
  "question_with_extra": "...",
  "options": ["(A) ...", "(B) ...", "(C) ...", "(D) ..."],
  "answer": "(D)",
  "extra_info": {},
  "image_paths": ["./MMIU-Benchmark/..."],
  "question_type": "multi-choice",
  "input_modality": "single-image",
  "task": "Transformation",
  "original_id": 671,
  "original_category": "4D",
  "original_task": "Homography_estimation"
}
```

### Question types

| Type | Description | Evaluation |
|---|---|---|
| `multi-choice` | Select one of A/B/C/D | Exact letter match |
| `judgement` | Yes / No | Exact string match |
| `open-ended` | Numeric scalar (+ unit) | Parsed numeric match |

---

## Using the Browser Locally

Clone the repository and open `index.html` directly in a browser. Image assets are stored in per-dataset subdirectories and resolved by relative path — no server required.

```bash
git clone https://github.com/Algorythmsz/SpatialScore.git
cd SpatialScore
open index.html   # macOS
```

The browser works without images (placeholder tiles shown); place the dataset image folders next to `index.html` for full preview.

---

## Citation

If you use SpatialScore in your research, please cite:

```bibtex
@misc{spatialscore2025,
  title  = {SpatialScore: A Unified Benchmark for Spatial Reasoning in Multimodal LLMs},
  year   = {2025},
  url    = {https://github.com/Algorythmsz/SpatialScore}
}
```

---

## License

Each sample retains the license of its originating dataset. Please refer to individual dataset licenses before use.
