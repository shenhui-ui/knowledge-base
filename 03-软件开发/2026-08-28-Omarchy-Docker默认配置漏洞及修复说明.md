---
type: ingest-note
source: https://0xcc.io/posts/omarchy-root-creds/
date: 2026-09-01
---
最近发现了一个严重的安全问题，影响了基于Docker的默认配置，导致任何用户程序都可能被赋予root权限。以下是详细说明：

### 背景和漏洞描述
Omarchy的默认用户组被配置为属于docker group，这允许用户在不使用sudo或权限提示的情况下运行Docker命令。具体影响包括：
- **文件系统操作**：作为root权限访问 host文件系统中的部分本地存储空间。
- **容器化服务**：任何与Docker相关的过程都可能被赋予执行full机器权限的能力。

漏洞示例：
$ docker run --rm -v /:/hostroot alpine cat /hostroot/etc/shadow
在测试环境中，用户组成员已包括docker组，这使得普通的用户程序能够以root身份运行。