---
type: ingest-note
source: Woxi
date: 2026-08-01
---

# Woxi：Rust 实现的 Wolfram Language 解释器

Woxi 是一个用 Rust 实现的 Wolfram Language 解释器，完全在浏览器本地运行，不向任何服务器发送数据。它支持多种典型 Wolfram 语言表达式，例如 `Map`、`Primes`、`Factorize`、`Permutations`、`Factorials`、`FoldList`、`Transpose`、`NestList`、`Plot` 等。

## 多种前端界面

同一个解释器引擎被用于多个前端：

- **Extended playground**：并排编辑器与输出面板，适合多行表达式和图形实验。
- **命令行工具**：通过 `woxi eval` 计算表达式，直接运行 `.wls` 脚本，也可作为 shebang 解释器，启动速度比 `wolframscript` 更快。
- **Jupyter 与 JupyterLite**：Woxi 可作为 Jupyter kernel 使用，通过 `woxi install-kernel` 本地安装，也可通过内置 JupyterLite 在浏览器中直接运行 notebook，无需安装。
- **Woxi Studio**：原生 notebook 编辑器，支持 `.nb` 文件的单元格编辑、内嵌图形，并导出为 `.ipynb`、Markdown、LaTeX、Typst 和 PDF。