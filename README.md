# SpatialScore Viewer

An interactive I/O browser for the **SpatialScore** benchmark (5,025 samples).  
This repository is an unofficial viewer — it is not affiliated with the original authors.

**[🔍 Open Viewer](https://algorythmsz.github.io/SpatialScore_Viewer/)**

---

## Original Benchmark

> **SpatialScore: Towards Comprehensive Evaluation for Spatial Intelligence**  
> Haoning Wu\*, Xiao Huang\*, Yaohui Chen, Ya Zhang, Yanfeng Wang, Weidi Xie  
> CVPR 2026 (Highlight) · arXiv:2505.17012

**[📄 Paper](https://arxiv.org/abs/2505.17012)** · **[🌐 Project Page](https://haoningwu3639.github.io/SpatialScore/)** · **[💻 Code](https://github.com/haoningwu3639/SpatialScore)** · **[🤗 Dataset](https://huggingface.co/datasets/haoningwu/SpatialScore)**

### Motivation

> "Existing evaluations of multimodal large language models (MLLMs) on spatial intelligence are typically fragmented and limited in scope." — §1

### Dataset Statistics

| Metric | Value |
|--------|-------|
| Total samples | **5,025** (manually verified) |
| Categories | **10** |
| Sub-tasks | **30** |
| Source datasets | **23** |
| Models evaluated | **49 MLLMs** |
| Human-level accuracy | **86.60%** |
| Best model accuracy | **60.12%** (Gemini-3-Pro) |
| Input modalities | single-image, multi-image, video |
| Question formats | multi-choice, open-ended, judgement |

### Categories & Sub-tasks

| Category | Sub-tasks | Samples |
|----------|-----------|--------:|
| **Camera** | Homography Matrix, Camera Extrinsics, Camera Motion, Camera Intrinsics | 778 |
| **Object Localization** | Spatial Position, Object Existence, 3D Object Detection, 2D Localization, View Localization | 697 |
| **Object Distance** | Relative Distance, Absolute Distance | 576 |
| **Object Size** | Relative Size, Absolute Size, Size Compatibility | 559 |
| **Depth Estimation** | Relative Depth, Absolute Depth | 520 |
| **Mental Animation** | Spatial Map, Maze Navigation, Multi-view Projection, Space Folding, 2D/3D Rotation | 447 |
| **View Reasoning** | View Perspective, Orientation | 446 |
| **Object Motion** | Point Tracking, Object Motion, Velocity Estimation | 415 |
| **Counting** | Object Counting, Video Counting, Count with Relation | 315 |
| **Temporal Reasoning** | Appearance Order, Navigation Route | 272 |

### Evaluation Metrics

| Metric | Definition |
|--------|------------|
| **Accuracy** | Exact match for multi-choice and judgement questions |
| **MRA** | Mean Relative Accuracy for open-ended numerical answers |

For ambiguous responses, a GPT-based scorer (GPT-OSS-20B) is used alongside crafted parsing functions.

### Results (49 MLLMs evaluated)

| Model | Overall Acc. |
|-------|------------:|
| **Human** | **86.60%** |
| Gemini-3-Pro | 60.12% |
| GPT-5-L | 58.13% |
| Gemini-2.5-Pro | 56.37% |
| VST-7B-RL | 52.47% |
| Qwen3-VL-32B | 49.22% |
| SpatialThiner-7B | 48.04% |
| Claude-4-5-Sonnet | 45.68% |
| InternVL2.5-4B | 44.39% |
| Qwen3-VL-8B | 43.18% |
| Qwen2.5-VL | 36.92% |
| LLaVA1.5-7B | 25.52% |

Gap between best model and human level: **26.48 points**.

---

## Viewer Usage

Open `index.html` locally after placing the dataset image folders next to it:

```
CV-Bench/
BLINK/
MMIU-Benchmark/
...
index.html
```

Images are resolved from relative paths (e.g. `./CV-Bench/img/...`). The viewer works without images — placeholder tiles are shown for missing files.

**Controls:** `←` / `→` browse samples · `↑` / `↓` switch sub-task · click category / sub-task tabs to jump · **▦ gallery** toggle grid view
