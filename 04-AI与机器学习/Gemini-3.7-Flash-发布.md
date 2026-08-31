---
type: ingest-note
source: InfoQ 中文站
date: 2026-08-14
---

# Gemini 3.7 Flash 突袭：性能逼近旗舰、价格打骨折，谷歌重画Agent成本线

谷歌于2026年8月13日发布Gemini 3.7 Flash，定位为“迄今最智能的主力模型（workhorse model）”，重点面向编程和Agent。距3.6 Flash发布仅三周，距DeepMind权力重组仅八天。

## 主要亮点

- **迭代加速**：Gemini迭代周期压缩至三周，反映工程化节奏显著提速。
- **权力重组**：Koray Kavukcuoglu升任Google DeepMind高级副总裁，实质掌舵Gemini全栈研发与前沿AI决策，直接向Sundar Pichai汇报。
- **性能提升**：
  - FrontierCode 1.1 Main得分43.6%（3.6 Flash为34.4%）
  - DeepSWE v1.1从约49%提升至65.3%
  - WebDev Arena Elo从1538升至1588
  - Terminal-bench 2.1达85.8%，Terminal-bench 3.0从5.4%升至14.9%
  - AutomationBench从17.0%升至30.4%
  - OSWorld 2.0从33.8%升至47.9%
- **逼近旗舰**：Artificial Analysis Intelligence Index得分56，与Claude Sonnet 5（55）和GPT-5.6 Terra（57）接近；FrontierCode上甚至超过二者。
- **价格策略**：2026年底前介绍价输入0.75美元/百万Token、输出3.75美元/百万Token，为3.6 Flash最初价格一半；2027年1月1日起恢复至输入1.5美元、输出7.5美元。

## 定位与部署

3.7 Flash聚焦代码生成、工具调用、Computer Use和长链条Agent任务，在多步骤规划和工具调用中“投入更多思考”，减少人工监督和重复重试。发布当天即部署到Gemini Spark（个人AI Agent），覆盖160多个国家和地区。开发者可通过Gemini API、Google AI Studio、Android Studio和Google Antigravity使用。

## 悬念

旗舰模型Gemini 3.5 Pro仍未公布正式发布时间，Gemini 4预训练正在推进。此次发布被认为是谷歌在Agent成本战中抢占先机的重要一步。