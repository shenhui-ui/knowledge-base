---
type: ingest-note
date: 2025-08-01
source: https://github.com/aadisang/hand-wave
---

# Hand-Wave-手语识别智能眼镜项目

## 概述

Hand Wave 是一个将手语（手指拼写）实时转换为语音的开源项目，面向 Web 和 iOS 平台，后端使用小型 Python 推理服务。该项目旨在通过智能眼镜和神经网络实现手语到语音的转换，官网：<https://handwave.sh>

## 技术栈

- **前端/应用**：Web + iOS，基于 Expo（React Native）开发，支持增强现实（AR）和可穿戴设备
- **后端**：Python 推理服务，使用 uv 管理依赖
- **构建工具**：pnpm（10.33+）、Node 22+、Python 3.11/3.12、uv、moon
- **模型与研究方向**：
  - MiCT-RANet for ASL Fingerspelling
  - A Two-Stream Neural Network for Pose-Based Handshape Recognition in American Sign Language
  - Mixed 3D/2D Convolutional Tube for Human Action Recognition
  - Fingerspelling Recognition in the Wild with Iterative Visual Attention
  - FSBoard：超过 300 万字符的 ASL 手指拼写数据集

## 开发设置

```bash
cp .env.example .env
pnpm install
uv sync --project apps/inference
# 在 .env 中设置 VITE_INFERENCE_URL
```

开发运行：`pnpm dev`

## 项目特点

- 面向手语社区，将手指拼写转化为语音
- 支持 AR 智能眼镜场景，辅助实时交流
- 采用小型 Python 推理服务，便于部署到边缘设备

## 备注

该项目使用 MIT 许可证，GitHub 仓库：<https://github.com/aadisang/hand-wave>
