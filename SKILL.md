---
name: runtime-safe-cleanup
description: 先由用户提供项目目录和迁移目录，用代码列出全部层级目录并说明功能，再把不影响完整运行的目录，以及日志、缓存、测试和结果文件，移到指定归档。适用于项目清理和归档；在两个路径都确定之前不要使用，也不要直接在原地删除。
metadata:
  short-description: 归档不影响运行的项目文件
---

# 运行时安全清理

把项目中不影响完整运行的内容移到用户指定的归档目录。移动前必须先拿到两个路径。先完成全层级目录清单和功能说明，再分类；复制核对成功后，才删除源文件。

## 必要输入

任一路径缺失就停止并询问。不要沿用其他项目的迁移目录。

- 项目目录：要检查和清理的项目根目录。
- 迁移目录：接收移出内容的归档目录。它必须位于项目目录之外，两个路径不能重叠。

## 1. 列出全部目录并说明功能

对项目目录运行 [scripts/list_directories.py](scripts/list_directories.py)。脚本为每一层的每个目录写一条记录，不移动任何文件。不能用人工抽样代替这次扫描。

阅读清单后，写明每个目录的功能。重复生成的同类目录可以合并说明，但必须写明规律、数量和父目录。清单中的每一行都要被单独说明或纳入某条已声明的规律。`runtime`、`store`、`cache`、`candidate` 这类熟悉名称本身不能作为分类依据。

把目录清单和功能说明保存到 `docs/project-structure/`。

## 2. 移走运行不需要的目录

启动、受支持的请求、配置、引用或恢复会读写的目录必须保留。启动命令所使用的虚拟环境也必须保留。

只移动功能说明已经确认不影响项目完整运行的目录。每个目录都按原相对路径放到 `<迁移目录>/directories/`。生成明确的迁移计划，并运行 [scripts/apply_reviewed_moves.py](scripts/apply_reviewed_moves.py)。脚本先复制，再比对文件名、大小和 SHA-256；只有核对一致才删除源文件。项目外路径、位于项目内部的迁移目录、符号链接和已存在的目标路径都会被拒绝。

无法确定的目录留在项目内，并记录原因。做边界判断前先阅读 [references/decision-rules.md](references/decision-rules.md)。

## 3. 检查留下的文件

目录迁移完成后，运行 [scripts/list_residual_files.py](scripts/list_residual_files.py)。脚本列出剩余的每个文件，并给出一个建议类别：`log`、`cache`、`test`、`result` 或 `unclassified`。建议本身不是移动许可。

对照启动入口和目录说明复核每条建议。确认后的文件分别移入：

- `logs/`：日志文件。
- `caches/`：可以重新生成的缓存文件。
- `tests/`：运行系统不会执行的测试文件。
- `results/`：生成的输出和结果文件。

源代码、有效数据、配置、密钥，以及启动入口会导入或启动的文件必须留下。使用同一个迁移脚本和核对流程。脚本没有核对成功的内容不能删除。

## 4. 补齐四个说明目录

在项目内创建缺少的目录，但不能因此删掉现有文档的唯一可用副本：

- `docs/project-structure/`：完整目录清单和功能说明。
- `docs/development-log/`：已有开发日志，以及本次清理的迁移记录。
- `docs/project-description/`：项目是什么、包含什么。
- `docs/usage/`：启动脚本、工作目录、环境变量和命令。

如果现有命令依赖启动脚本的当前位置，不要把正在使用的启动脚本移进 `docs/`。把命令写入 `docs/usage/`，脚本仍留在原来的运行位置。

只有处理 PlantGlyco 证据项目，或使用相同联邦索引布局的目录树时，才阅读 [references/plantglyco-lessons.md](references/plantglyco-lessons.md)。
