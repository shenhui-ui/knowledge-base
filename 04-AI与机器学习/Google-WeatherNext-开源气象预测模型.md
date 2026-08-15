---
type: ingest-note
date: 2026-01-15
source:
- https://blog.google/technology/ai/google-weathernext/
- https://github.com/google-deepmind/weathernext
---

# Google WeatherNext 开源气象预测模型

## 核心更新

Google 开放了 WeatherNext 系列模型的代码与权重，并发布 Nature 论文。WeatherNext 使用 **Functional Generative Networks (FGNs)** 高效生成多种预测集合，捕获天气固有的不确定性。单次 15 天预报可在 TPU 上 1 分钟内完成。

## 关键进展

- **集合规模扩大**：从去年的 50 个预测成员扩展到今年的 **1,000 个**，可捕获罕见但影响巨大的场景（如 2025 年飓风 Melissa 的快速增强事件）。
- **低分辨率反而高效**：WeatherNext Cyclones 仅需 28×28km 分辨率数据，比传统模型粗 100 倍，但强度预测依然准确；更小的 WeatherNext 2-mini（111×111km）表现同样出色。这一现象仍是开放研究问题。
- **开源内容**：代码、模型权重、WeatherNext Cyclones（飓风季节运行版本）、WeatherNext 2（2025 年 10 月运营化）以及可在单个 TPU 上运行的 WeatherNext 2-mini（提供免费 Colab demo）。
- **可视化工具**：Weather Lab 更新了界面，支持全球天气预报与飓风路径，可查看温度、降水、风速等预测。
- **历史性突破**：飓风预测提前量增加超过一天，相当于气象学十年的进步。

## GitHub 仓库与模型版本

GitHub 上的 `google-deepmind/weathernext` 仓库是 WeatherNext 系列模型的统一代码库，包含 WeatherNext 2 (WN2) 以及前代 GraphCast 和 GenCast 的代码与文档。提供的预训练模型包括：

- **WeatherNext 2 (`WeatherNext2_<2025`)**：0.25° 分辨率（约 30km），已在运营中使用，基于 ECMWF HRES 数据微调，可直接从 HRES 初始条件初始化。训练数据至 2024 年。
- **WeatherNext Cyclones**：用于复现论文结果的飓风专用模型，提供 `<2025`、`<2024`、`<2023` 三个版本，均为 0.25° 分辨率。`<2025` 版本在 2025 大西洋飓风季实时运行（NHC 后处理版本称 GDMI）。
- **WeatherNext Cyclones Mini**：1° 分辨率的轻量版本，适合资源受限环境（如单 TPU/GPU 本地测试），同样可以预测飓风，但性能不及完整版。提供 `<2024` 与 `<2023` 两个版本。

## 数据获取渠道

如果不想自己运行模型，可直接获取 WN2 模型输出的日常数据：

- **Google Cloud**：通过 Earth Engine、BigQuery、Vertex AI 提供。
- **WeatherLab**：包含飓风路径。
- **OpenMeteo**：提供 API 和交互式构建器。

## 快速开始

推荐通过官方 Colab Notebook 体验，默认使用 WeatherNext Cyclones Mini，可在免费的 v5e-1 runtime 上运行。其他更大模型需要 v5p 加速器。

## 意义

WeatherNext 是 Google Earth AI 的一部分，旨在结合机器学习与人类预报员经验，构建协作式天气预报生态系统，帮助保护生命与基础设施。

> 注意：官方天气预警仍以当地气象机构为准。
