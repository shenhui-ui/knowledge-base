---
type: ingest-note
source: https://github.com/semantica-agi/semantica
date: 2026-08-01
---

# Semantica：面向AI Agent的图原生上下文与可问责决策基础设施

Semantica 是一个开源、可自托管的图原生基础设施层，定位为“AI Agent 的开源 Palantir”。它位于 LLM、向量库与 Agent 框架之下，提供结构化上下文图（Context Graph）、知识图谱、图分析与因果推理能力，并在每个事实与决策上记录完整来源（provenance）。

## 核心定位

- 大多数 AI agent 只存 embeddings 而非含义，导致决策不可解释、不可审计。在借贷等场景中，这一缺口是合规风险：承保 agent 的批准必须能在数月后经受住监管者的“为什么”。
- Semantica 不依赖 LLM 即可完成图构建、推理与溯源。
- 面向需要做出高风险决策的 agent 系统，尤其是金融、医疗、法律、政府、国防等受监管领域。

## 主要能力

- **Context Graphs**：将 Agent 所知、所决定、所推理的一切构建为结构化、可查询的图。
- **Decision Intelligence**：每个决策都是一等对象，可追溯、可按先例搜索、可因果关联。
- **AI Governance & Ontology**：支持 SHACL 约束、冲突检测、合规规则、OWL 生成、SKOS 词汇管理，带可视化编辑器。
- **Full Auditability**：所有事实采用 W3C PROV-O 溯源，审计记录可导出为 JSON、CSV 或 RDF。
- **Deterministic Reasoning**：前向链、Rete 网络、Datalog、SPARQL，推理路径完全可解释，非黑盒。
- **Knowledge Pipeline**：多源摄取、实体感知分块、NER/关系/事件抽取、知识图谱构建，包含语义去重与保留溯源的数据合并；冲突事实会被标记而非静默覆盖。

## 适用人群

- 构建会产生重大决策的 Agent 的 AI/ML 平台团队，需要从碎片化原始数据构建结构化、可查询上下文，而非仅一个向量索引。
- 基于 Databricks 或 Snowflake 的数据平台团队，可将 Unity Catalog / 仓库中的表转化为受治理且带血缘追踪的知识图谱，无需先导出到第三方 SaaS。
- 需要回答“AI 为什么这样做”的合规、风险与审计团队，且格式需能被监管者接受。
- 不能交付黑盒、也不能将数据交给第三方 SaaS 的受监管企业（金融、医疗、法律、政府、国防）。
- 希望 KG、推理与溯源栈可自托管、可替换的平台/基础设施工程师。
- 从混乱多源数据构建知识图谱的数据与知识工程师。

## 其他要点

- 安装：`pip install semantica`
- 开源、可自托管、可审计、可治理、零供应商锁定
- 多语言图存储，支持 RDF 与 LPG，遵循 W3C 标准，可互操作
- 仓库结构包含 `.claude`、`.github`、`cookbook`、`deploy`、`docs`、`examples`、`explorer`、`integrations`、`mcp`、`plugins`、`semantica`、`tests` 等模块，架构见 `ARCHITECTURE.md`
- 附带 Quick Start、Architecture、What You Get、Why Semantica、Decision Intelligence、Context Graphs、Recipe: Audit Trail、Module Reference、Integrations、CLI、Performance 等文档。
- 已被 fork 696、star 6.6k，拥有 2315 次提交，活跃维护。
- 项目标语：Graph-Native Infrastructure for Context and Accountable AI Systems，The Open Source Palantir for AI Agents。