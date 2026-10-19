---
name: runtime-safe-cleanup
description: 用户指定项目目录和迁移目录后，先理解项目逻辑，再逐层说明全部目录和文件，把不影响网站完整功能的内容循环移到固定归档。适用于整理 AI 开发后文件失控的网站项目。每一轮移动前都要留下 V1 到 VN 审核文件。不要在两个路径确定前使用，也不要直接原地删除。
metadata:
  short-description: 循环归档不影响网站运行的文件
---

# 运行时安全清理

把不影响网站完整功能的目录和文件移到用户指定的固定归档。先理解项目怎么运行，再读取全部层级；每一轮都先写审核文件，确认后才移动。至少完成目录一轮和文件一轮，之后继续循环，直到新的一轮已经没有可安全移走的内容。

## 必要输入

任一路径缺失就停止并询问。不要沿用别的项目的迁移目录。

- 项目目录：要整理的网站项目根目录。
- 迁移目录：项目外的固定归档。两个路径不能重叠。

## 1. 先理解项目逻辑

移动前先读启动脚本、依赖说明、路由和实际被请求读取的数据目录。写清网站如何启动、一次正常访问经过哪些目录。只看目录名不算理解项目。

这一步不移动文件。

## 2. 每一轮都按同一顺序处理

每一轮开始都重新运行 [scripts/list_directories.py](scripts/list_directories.py)。清单必须覆盖当前项目的每一层目录，不能抽样。重复生成的同类目录可以合并说明，但要写明规律、数量和父目录。

用 [scripts/start_review.py](scripts/start_review.py) 创建本轮的 `<迁移目录>/reviews/Vn.md`。按 [references/review-format.md](references/review-format.md) 写完以下内容：

- 当前确认的项目逻辑。
- 每个目录的功能，以及保留、移走或不确定。
- 目录移走后，重新运行 [scripts/list_residual_files.py](scripts/list_residual_files.py)，说明留下的目录中的文件。
- 某个目录文件特别多时，先依据该目录的功能说明按文件类型归类，再给每个文件一行功能说明。
- 本轮准备移走的目录和文件、归档类别、原因。
- 不确定的内容必须留下，并写明原因。

审核文件中的“待写”全部替换之前，禁止运行 [scripts/apply_reviewed_moves.py](scripts/apply_reviewed_moves.py)。移动脚本只执行本轮审核文件里列出的路径；它先复制并核对文件名、大小和 SHA-256，一致后才删除源文件。

目录进入 `<迁移目录>/directories/`。文件按审核结论进入 `logs/`、`caches/`、`tests/` 或 `results/`，原相对路径保持不变。

启动、页面请求、配置、引用和恢复会用到的内容保留，启动命令选定的依赖环境也保留。边界判断先读 [references/decision-rules.md](references/decision-rules.md)。

## 3. 循环直到稳定

V1 处理目录。V2 在新的目录状态上处理文件。只要一轮仍移走了内容，下一轮就必须重新扫描并再出一份审核文件。某一轮的“本轮移走的目录”和“本轮移走的文件”都为空，且“下一轮”写明已稳定，任务才结束。

## 4. 稳定后建立四个说明目录

循环结束前不要分散建立文档目录。稳定后在项目内创建：

- `docs/project-structure/`：最终目录清单和目录功能说明。
- `docs/development-log/`：开发日志，以及 `cleanup-reviews/` 中的 V1 到 VN 副本。
- `docs/project-description/`：项目做什么、包含什么、明确不包含什么。
- `docs/usage/`：真实启动脚本、工作目录、环境变量和命令。

不要把正在使用的启动脚本移进 `docs/`。迁移目录中的审核原文保留，项目内只保存副本。

只有处理 PlantGlyco 证据项目，或使用相同联邦索引布局的目录树时，才阅读 [references/plantglyco-lessons.md](references/plantglyco-lessons.md)。
