# SpatialScore: Towards Comprehensive Evaluation for Spatial Intelligence

[![CVPR 2026 Highlight](https://img.shields.io/badge/CVPR%202026-Highlight-red)](https://arxiv.org/abs/2505.17012)
[![arXiv](https://img.shields.io/badge/arXiv-2505.17012-b31b1b)](https://arxiv.org/abs/2505.17012)
[![HuggingFace](https://img.shields.io/badge/🤗%20Dataset-SpatialScore-yellow)](https://huggingface.co/datasets/haoningwu/SpatialScore)
[![Code](https://img.shields.io/badge/GitHub-Code-black)](https://github.com/haoningwu3639/SpatialScore)
[![Project Page](https://img.shields.io/badge/Project-Page-blue)](https://haoningwu3639.github.io/SpatialScore/)

**Haoning Wu\*, Xiao Huang\*, Yaohui Chen, Ya Zhang, Yanfeng Wang, Weidi Xie**

*School of Artificial Intelligence, Shanghai Jiao Tong University · Shanghai Artificial Intelligence Laboratory*

(\* equal contribution)

---

## Abstract

Existing evaluations of multimodal large language models (MLLMs) on spatial intelligence are typically fragmented and limited in scope. In this work, we aim to conduct a holistic assessment of the spatial understanding capabilities of modern MLLMs and propose complementary data-driven and agent-based solutions. Specifically, we make the following contributions:

1. We introduce **SpatialScore**, to our knowledge, the most comprehensive and diverse benchmark for multimodal spatial intelligence to date. It covers multiple visual data types, input modalities, and question-answering formats, and contains approximately **5K manually verified samples** spanning **30 distinct tasks**.
2. Using SpatialScore, we extensively evaluate **49 representative MLLMs**, revealing persistent challenges and a substantial gap between current models and human-level spatial intelligence.
3. To advance model capabilities, we construct **SpatialCorpus**, a large-scale training resource with **331K multimodal QA samples** that supports fine-tuning on spatial reasoning tasks and significantly improves the performance of existing models (e.g., Qwen3-VL).
4. To complement this data-driven route with a training-free paradigm, we develop **SpatialAgent**, a multi-agent system equipped with **12 specialized spatial perception tools** that supports both Plan-Execute and ReAct reasoning, enabling substantial gains in spatial reasoning without additional model training.

---

## Benchmark Overview

| | |
|---|---|
| **Total samples** | 5,025 (manually verified) |
| **Categories** | 10 |
| **Sub-tasks** | 30 |
| **Source datasets** | 23 |
| **Models evaluated** | 49 MLLMs |
| **Human-level accuracy** | 86.60% |
| **Best model accuracy** | 60.12% (Gemini-3-Pro) |
| **Input modalities** | single-image, multi-image, video |
| **Question formats** | multi-choice, open-ended, judgement |

---

## Three Contributions

### 🏆 SpatialScore — Benchmark
~5K manually verified QA pairs across 10 spatial reasoning categories and 30 sub-tasks, sourced and curated from 23 existing public datasets.

### 📚 SpatialCorpus — Training Resource
331K multimodal QA samples (multi-choice: 262,601 · open-ended: 58,425 · judgement: 9,776) across 16 tasks in 7 categories, designed for supervised fine-tuning of spatial reasoning. Fine-tuning on SpatialCorpus yields **+9–10 point** overall accuracy gains on SpatialScore.

### 🤖 SpatialAgent — Agent System
Training-free multi-agent system with 12 specialized spatial perception tools organized into four categories:

| Tool Category | Tools |
|---|---|
| General Perception | Localization, Counting, Segmentation, 3D Detection |
| Motion & Transformation | Optical Flow, Point Matching, Homography, Extrinsics |
| Pose & Geometry | Intrinsics, Orientation, Depth, 3D Distance |

Two reasoning paradigms supported: **Plan-Execute** (task decomposition with sequential tool invocation) and **ReAct** (iterative reasoning-and-action). SpatialAgent yields **+6–8 point** gains without any model training.

---

## Categories & Sub-tasks

| Category | Sub-tasks | Samples |
|---|---|---:|
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
| | **Total** | **5,025** |

---

## Source Datasets

SpatialScore is curated from 23 existing public datasets. The initial pool of 63,857 candidates was filtered and manually verified by 5 volunteers to yield the final 5,025 high-quality samples.

CV-Bench · QSpatialBench · SpatialViz-Bench · VSR-Bench · SPAR-Bench · SpatialBench · SITE-Bench · RoboSpatial · BLINK · SpatialSense · MMIU · MIRAGE · MMVU · RealWorldQA · SpaCE-10 · OmniSpatial · 3DSRBench · STI-Bench · VLM4D · MMVP · MMSI-Bench · SpatialEval · SpatialScore-Repurpose

A subset of samples (**SpatialScore-Repurpose**) are newly constructed from 3D annotations in ScanNet++, Omni3D, WildRGB-D, PointOdyssey, and other 3D scene datasets.

---

## Evaluation Protocol

### Metrics

| Question type | Metric | Method |
|---|---|---|
| Multi-choice | Accuracy | Exact letter match |
| Judgement (Yes/No) | Accuracy | Exact string match |
| Open-ended (numerical) | Mean Relative Accuracy (MRA) | Parsing function + LLM-based extraction |

For ambiguous responses, a GPT-based scorer (GPT-OSS-20B) is used to extract the answer with detailed instructions.

### Answer Format Prompts

```
Multi-choice:
  "Please select the most appropriate answer from the given options.
   Respond ONLY with the capital letter and its parentheses."

Judgement:
  "Please answer with yes or no based on the image.
   Respond ONLY with 'yes' or 'no'."

Open-ended (distance/size):
  "Respond ONLY with a numeric answer consisting of a scalar and a distance unit
   in the format: \scalar{scalar} \distance_unit{distance unit}"
```

### Inference Settings
- Temperature: 0.0 (deterministic)
- Max output length: 512 tokens (reasoning models) / 200 tokens (others)
- Video frames: 32 frames (open-source) / 16 frames (GPT-5) / 8 frames (Claude)

---

## Model Evaluation Results

Results on SpatialScore across 49 evaluated MLLMs. Human-level accuracy: **86.60%**.

| Model | Overall | Notes |
|---|---:|---|
| **Human** | **86.60** | 3 PhD students (3D vision) |
| Gemini-3-Pro | 60.12 | Best model overall |
| GPT-5-L | 58.13 | |
| Gemini-2.5-Pro | 56.37 | |
| VST-7B-RL | 52.47 | |
| SpatialThiner-7B | 48.04 | |
| Qwen3-VL-32B | 49.22 | |
| Qwen3-VL-8B + SpatialCorpus | ~53 | Fine-tuned |
| Claude-4-5-Sonnet | 45.68 | |
| Qwen3-VL-8B | 43.18 | |
| Qwen3-VL-4B | 42.52 | |
| InternVL2.5-4B | 44.39 | |
| InternVL2.5-8B | 39.63 | |
| Qwen2.5-VL | 36.92 | |
| LLaVA1.5-7B | 25.52 | |
| **Random baseline** | ~25 | Chance level |

> Gap between best model and human level: **26.48 points**, highlighting the significant headroom for improvement in multimodal spatial intelligence.

---

## 🌐 Interactive Browser

Explore the benchmark samples interactively:

- **[I/O Browser](https://algorythmsz.github.io/SpatialScore/)** — Browse samples with full input/output structure; toggle between single-record detail view and gallery grid view
- **[Representative Samples](https://algorythmsz.github.io/SpatialScore/spatialscore_samples.html)** — One representative prompt per category with full context

---

## Resources

| Resource | Link |
|---|---|
| 📄 Paper (arXiv) | https://arxiv.org/abs/2505.17012 |
| 🏠 Project Page | https://haoningwu3639.github.io/SpatialScore/ |
| 💻 Code | https://github.com/haoningwu3639/SpatialScore |
| 🤗 Benchmark Dataset | https://huggingface.co/datasets/haoningwu/SpatialScore |
| 🤗 SpatialCorpus | https://huggingface.co/datasets/haoningwu/SpatialCorpus |

---

## Citation

```bibtex
@inproceedings{wu2026spatialscore,
  author    = {Wu, Haoning and Huang, Xiao and Chen, Yaohui and Zhang, Ya
               and Wang, Yanfeng and Xie, Weidi},
  title     = {SpatialScore: Towards Comprehensive Evaluation for Spatial Intelligence},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision
               and Pattern Recognition (CVPR)},
  year      = {2026}
}
```

---

## License

Each sample retains the license of its originating dataset. Please refer to the individual dataset licenses before use in research or commercial applications.
