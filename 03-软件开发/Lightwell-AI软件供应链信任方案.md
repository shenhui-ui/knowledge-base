---
type: ingest-note
source: https://www.infoq.com/news/2026/08/lightwell-ai-open-source/
date: 2026-08-14
---

# AI智能体参与交付：IBM与Red Hat的Lightwell方案

IBM 与 Red Hat 宣布扩展开源 Lightwell 项目，推出商业产品，旨在为 AI 辅助软件开发时代建立可信、可验证的软件供应链。该产品整合了软件签名、来源追踪、工件验证和策略执行，使企业能够确保由人类和 AI 生成的软件在整个交付生命周期中值得信任。

Lightwell 基于 Sigstore、in-toto、SLSA（软件工件供应链级别）以及 SBOM（软件物料清单）等现有安全标准，将原本分散的签名、溯源和策略执行能力统一到一个平台中，避免企业自行组装割裂的开源工具。这尤其重要，因为 AI 辅助开发显著提高了进入交付流水线的变更速度和数量。

该方案的核心思路是让信任成为软件从开发走向部署的伴随属性，而不仅是发布前的最终安全检查。组织需要证据证明软件在获批环境中构建、使用可信身份签名、基于经过验证的源代码生成，并且在整个生命周期未被篡改。

随着 AI 智能体开始生成代码、修改基础设施、解决事件并直接参与软件交付，行业需要验证“谁或什么执行了操作、以何种身份、遵循了哪些策略”的机制。IBM 和 Red Hat 的动向是更广泛趋势的一部分：GitHub 扩展 CodeQL、工件证明和密钥扫描；Google 推动 SLSA 和 Sigstore；Microsoft 将签名和溯源集成到 Azure DevOps 与 GitHub Advanced Security；CNCF 与 Kusari 合作加强云原生供应链安全；Linux 基金会的 Akrites 项目也在探索类似的加密信任模型。

Lightwell 的扩展表明，软件安全的未来正从依赖单一安全工具转向覆盖整个软件生命周期的综合信任架构。随着自动化日益自主，组织需要确保每个工件、依赖项和部署都能追溯到经过验证的来源，并符合组织策略。

原文链接：https://www.infoq.com/news/2026/08/lightwell-ai-open-source/