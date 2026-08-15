---
type: ingest-note
date: 2026-08-09
source: https://www.infoq.cn/article/OG03ezJaBkdOd1G3rc1b
---
type: ingest-note
来源：InfoQ（2026-08-08）
原文：https://www.infoq.com/news/2026/07/lambda-self-managed-storage/

亚马逊云科技宣布为 Lambda 推出自管理代码存储，函数和层可直接引用客户自有 S3 存储桶中的部署包，不再存放在 Lambda 托管存储中。这一变化取消了每个区域的代码存储配额（Lambda 托管存储默认配额从 75 GB 提高到 300 GB），但**单个函数的包大小限制不变**：基于 zip 的函数仍为压缩后 50 MB、解压后 250 MB，容器镜像仍为 10 GB。

要点补充：
- Lambda 不再创建部署包的中间副本，函数创建/更新后激活更快。
- 存储与检索费用转为客户 S3 账单上的可见成本，无额外 Lambda 费用（跨区域传输费用另计）。
- 部署工作流未改变：S3 对象替换后仍需调用 UpdateFunctionCode，引用在更新时解析，非持续解析。
- Terraform 支持仍待跟进（7 月 15 日提交的增强请求 s3_object_storage_mode 属性尚未实现），CLI 和 SDK 已支持该参数。

该功能已在所有商业区域推出。核心价值在于突破托管存储限制，适用于大规模函数集群，但不会改变单函数大小上限。