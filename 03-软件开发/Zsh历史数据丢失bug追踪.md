---
type: ingest-note
source: 《Tracking down a Zsh history data loss bug》 (2026-08-09)
date: 2026-08-09
---

# 追踪Zsh历史数据丢失bug

## 问题描述

作者多年间偶尔发现 `~/.zsh_history` 中的部分命令丢失，Ctrl+R 无法搜索到之前执行过的命令。症状严重时历史文件只剩很老的条目，最近数年的新条目整体缺失。历史文件没有可见损坏（无乱码、无残缺行），但文件行数并不固定。作者怀疑是 Zsh 自身、其他程序或多个 zsh 进程共同导致的问题。

## 历史配置

```zsh
HISTSIZE=4000
HISTFILE=~/.zsh_history
SAVEHIST=10000000
setopt HIST_IGNORE_DUPS
setopt INC_APPEND_HISTORY
unsetopt SHARE_HISTORY
```

多个 shell 会话独立运行，但都将命令流式写入同一个历史文件。

## 调查过程

### inotify 观察文件事件

通过 `inotifywait` 监控 `.zsh_history`，发现 Zsh 会读取旧历史文件、写入新文件，然后通过 rename 覆盖旧文件（实际是删除旧文件）。

目录监控显示完整流程：

```
OPEN .zsh_history
ACCESS .zsh_history
...
CLOSE_WRITE,CLOSE .zsh_history
CREATE .zsh_history.new
OPEN .zsh_history.new
MODIFY .zsh_history.new
MOVED_FROM .zsh_history.new
MOVED_TO .zsh_history
CLOSE_WRITE,CLOSE .zsh_history
```

但 inotify 不提供进程 PID，`fsnotifywait`（基于 fanotify）虽有 PID 信息却不显示。

### fatrace 定位进程

使用 `fatrace` 可以看到具体进程名和 PID，确认是 `zsh` 自身在重写历史文件。

## 根因与修复

- 问题最终定位为 Zsh 的一个 bug，会导致历史文件重写时丢失数据。
- 修复已合入上游：Zsh 5.9.2（2026-07-12 发布）包含此修复。
- 上游修复链接：Zsh fix 53454。

## 经验总结

- 用文件系统监控（inotify/fanotify）定位“谁动了我的文件”是有效手段，但要注意工具是否输出 PID。
- 当正常诊断手段不足时，**让程序崩溃并分析 core dump** 是最后奏效的策略（作者在文章开头剧透）。
- 多进程并发写同一文件时，即使每个操作看起来正常，也可能因竞态导致数据丢失。
