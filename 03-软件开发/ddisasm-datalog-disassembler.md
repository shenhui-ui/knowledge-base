---
type: ingest-note
source: https://github.com/GrammaTech/ddisasm
date: 2025-07-31
tags: [reverse-engineering, disassembler, datalog, binary-analysis]
---

# DDisasm：基于Datalog的反汇编器

DDisasm 是一个快速反汇编器，其精度足以让输出的汇编代码能够被重新汇编。它使用 Datalog（通过 Souffle 实现）声明式逻辑编程语言来编译反汇编规则和启发式策略。

## 工作原理

1. **解析二进制信息**：解析 ELF/PE 文件信息，解码超集指令，生成初始 Datalog 事实集。
2. **分析与识别**：分析这些事实来识别代码位置、符号化信息以及函数边界。
3. **生成 IR**：将分析后的细化事实集转换为 GTIRB 中间表示，用于二进制分析和逆向工程。
4. **重新汇编**：配合 gtirb-pprinter 可将 GTIRB 打印为可重新汇编的汇编代码。

## 支持的格式

- 二进制格式：ELF（Linux）、PE（Windows）
- 指令集架构：x86_32、x86_64、ARM32、ARM64、MIPS32

## 快速使用

可通过 Docker 运行预构建版本：

```bash
docker pull grammatech/ddisasm:latest
docker run -v $PWD/examples:/examples -it grammatech/ddisasm:latest
```

在容器中对示例进行反汇编：

```bash
cd /examples/ex1
gcc ex.c -o ex
ddisasm ex --ir ex.gtirb
```

使用 GTIRB 进行程序化修改后，再用 gtirb-pprinter 生成新二进制或汇编清单：

```bash
gtirb-pprinter ex.gtirb -b ex_rewritten
gtirb-pprinter ex.gtirb --asm ex.s
```

## 相关论文

- *Datalog Disassembly*, USENIX Security 2020
- *GTIRB: Intermediate Representation for Binaries*, arXiv:1907.02859
- *Disassembly as Weighted Interval Scheduling with Learned Weights*, IEEE S&P 2025

## 关联项目

- [[Rosenbridge-x86硬件后门研究]]：另一个二进制/硬件安全研究方向
- [[REpsych-逆向工程心理战]]：逆向工程方法论
