---
type: ingest-note
title: 微软AI智能体LLM路由方案
date: 2026-08-07
source: https://www.infoq.com/news/2026/07/microsoft-agents-aks-routing/
---

# 微软AI智能体LLM路由方案

## 概述

Microsoft 发布了用于在 Azure Kubernetes Service (AKS) 上路由智能体流量的参考架构，将问题分解为三个关键选择：由哪个模型响应调用、如何管理调用、由哪个 GPU 副本处理调用。设计结合了 Kubernetes Gateway API Inference Extension、agentgateway 和 RouteLLM，共同接入 OpenAI 兼容端点。

## 动机

智能体工作负载与普通聊天不同，单个任务可能在“规划—行动—观察”循环中发起数百次 LLM 调用，而大多数调用（填写工具参数、判断是或否、生成摘要）并不需要前沿模型。简单轮询负载均衡器会导致长请求排在繁忙 GPU Pod 上，而附近空闲 Pod 未被利用。

## 架构组件

- **RouteLLM**：检查提示词，预测成本更低的模型能否达到较强模型的回答质量。基于人类偏好数据训练的矩阵分解路由器。
- **agentgateway**：开源代理，兼容 OpenAI，管理身份验证、每个智能体的速率限制、成本跟踪和护栏等策略，不检查提示词含义。
- **Gateway API Inference Extension**：Endpoint Picker 检查 GPU 实时状态（vLLM KV 缓存占用率、队列深度），决定由所选模型的哪个副本处理请求。
  - 对于自托管路径，agentgateway 通过 ext-proc 直接调用 Endpoint Picker，从而完全绕过单独的 Gateway API 网关。
  - 强模型路径通过 agentgateway 中的 AI 后端通向 Azure OpenAI；弱模型路径通过服务后端路由到 KAITO 提供的 Pod，该后端使用 `inferenceRouting` 策略，将请求放置定向至 Endpoint Picker，并将 `destinationMode` 设置为 `passthrough`。
- **KAITO**：按需提供 GPU 节点池并运行 vLLM，暴露 `vllm:num_requests_waiting` 和 `vllm:kv_cache_usage_perc` 指标。
- **可观测性**：Azure 托管的 Prometheus 和 Grafana 抓取 agentgateway 的路由及成本指标和 vLLM 的 GPU 指标，提供统一视图。

## 关键数字

RouteLLM 的 mf 路由器在 MT-Bench 上达到 GPT-4 约 95% 的质量水平，只将约 26% 的调用发送给 GPT-4，与全部路由到强模型相比，最高可节省 85% 成本。但该数字与训练时的模型组合相关，需根据实际流量校准阈值，并依据 agentgateway 中强模型与弱模型的实际流量划分进行调整，而不是采用 RouteLLM 的估算结果。

## 注意事项

- 提示词缓存会让 token 成本复杂化，切换模型会使两边的缓存冷却，一次“强模型”调用的真实成本低于表面成本。
- 组件较年轻，不同版本字段名称会变化，需固定版本并确认文档。例如，InferencePool 和 InferenceObjective 位于不同的 API 组中。
- Foundry 模型路由器是 RouteLLM 语义层的托管版本，适合不愿自行管理路由器的团队；但目前没有针对 Endpoint Picker 的 GPU 感知放置的托管选项，无论使用哪个网关，它都必须在集群内运行。
- 三个开源层（RouteLLM、agentgateway、Inference Extension）全部在 AKS 集群内运行；KAITO 服务、Azure OpenAI 以及 Prometheus/Grafana 可观测性栈由 Azure 管理。

## 分阶段采用

1. 单一托管模型：主要使用 agentgateway 进行治理，因为既没有其他模型可路由，也没有 GPU 需要放置。
2. 自托管单一模型类别：可受益于 KAITO 和 Inference Extension，无需语义路由层。
3. 强/弱模型价格差距明显并有大量简单流量时，加入 RouteLLM。文章认为这几乎适用于所有循环运行的智能体。
