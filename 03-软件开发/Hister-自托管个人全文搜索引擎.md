---
type: ingest-note
source: https://hister.org/
date: 2026-08-24
---

## Hister：自托管的个人全文搜索引擎

Hister 把你访问过的网页和本地文件变成一个自己掌控的私有全文搜索索引（"Your Own Search Engine"）。官网演示实例索引了 1924 个页面，6 条结果检索耗时 0.04 秒。

## 核心能力

- **全文索引**：不只存书签和文件名，而是索引所选页面与文件的完整内容，并把提取出的文档内容与索引一起存储，以可读预览形式展示在搜索结果旁
- **精确检索**：支持字段、短语、通配符、否定、优先级和自定义别名
- **多路收集**：浏览器扩展保存新访问的页面、读取本地文件夹、导入浏览历史或爬取整站
- **数据自持**：索引、存储的页面内容与规则全部保留在你配置的 Hister 服务器上，无遥测、无强制云服务

## 部署

- 单二进制即可本地运行
- 共享服务器部署支持按用户隔离的访问控制，后端可用 SQLite 或 PostgreSQL

## See Also

- [[K Search infrastructures for AI agents - Keenable]]
- [[How-I-built-a-500k-Domain-Search-Engine-for-Makers-in-a-Weekend-for-$10]]
