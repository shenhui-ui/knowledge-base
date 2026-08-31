---
type: ingest-note
source: "Doug Turnbull 博客 (softwaredoug.com)"
date: 2026-08-10
title: "Don't Classify. Hallucinate!——用幻觉生成分类再用嵌入匹配的LLM低成本分类法"
---

# Don't Classify. Hallucinate!——用幻觉生成分类再用嵌入匹配的LLM低成本分类法

在电商场景中，将用户搜索词映射到严格的商品分类体系（taxonomy）是常见需求。传统做法是使用结构化输出，让 LLM 在预定义的合法分类列表中选取。例如用 Pydantic 定义 `Literal[...]` 包含数百个分类。这样虽然准确，但存在两个问题：

1. 每次请求都要将庞大的分类列表发送给模型，成本高。
2. 模型输入长度存在上限，无法容纳极大分类集合。

## 更便宜的替代方案：让 LLM 先“幻觉”，再用嵌入匹配

Doug Turnbull 提出一个巧妙思路：**不要给 LLM 真实分类列表，而是让它自由发挥，生成看似合理的假分类**。然后利用嵌入向量，将假分类与真实分类做相似度匹配。

### 步骤

1. **构建幻觉提示**：要求 LLM“发明全新的、从未见过的家具/家居分类”来匹配查询。示例：

   ```
   Your task is to create novel, never seen before, furniture, home goods, or hardware classification that best fit a search query...
   query: brown coffee table
   ```

2. **LLM 输出假分类**：例如 `Furniture / Living Room / Tables / Coffee`——这个分类在真实 taxonomy 中不存在。

3. **嵌入匹配**：预计算所有真实分类的嵌入（如使用 MiniLM），存储为内存中的集合。对 LLM 输出的假分类计算嵌入，然后与真实分类嵌入做点积，选择最相似的真实分类。

   最终结果：`Furniture / Living Room Furniture / Coffee Tables & End Tables / Coffee Tables`。

### 优点

- 可以使用廉价、小型模型完成“幻觉”任务，因为不需要精确符合 schema。
- 无需每次把 schema 发给模型，减少 token 消耗。
- 嵌入匹配非常快，适合大规模分类场景。

这种方法本质上把“从候选集选择”变成了“生成候选后检索”，适用于分类体系庞大且相对稳定的场景。

> 来源：Doug Turnbull，2026-08-10。