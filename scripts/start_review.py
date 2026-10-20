"""Allocate the next V1-VN review file without overwriting history."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


TEMPLATE = """# V{n} {title}

## 本轮目标与验收门

待写：本轮对应 goal-contract.md 的成功标准，以及完成后如何独立验证。

## 项目逻辑

待写：网站如何启动，请求经过哪些目录，哪些数据会被实际读取。

## 目录功能

| 相对路径 | 功能 | 依赖证据 | 风险 | 处理 |
| --- | --- | --- | --- | --- |

## 本轮移走的目录

| 相对路径 | 移走原因 | 复制校验 | 回滚 |
| --- | --- | --- | --- |

## 文件功能

| 相对路径 | 类型 | 功能 | 依赖证据 | 风险 | 处理 |
| --- | --- | --- | --- | --- |

## 本轮移走的文件

| 相对路径 | 归档类别 | 原因 | 复制校验 | 回滚 |
| --- | --- | --- | --- |

## 留下的不确定项

待写。

## 下一轮

待写。
"""


def next_version(folder: Path) -> int:
    highest = 0
    for path in folder.glob("V*.md"):
        match = re.fullmatch(r"V(\d+)", path.stem)
        if match:
            highest = max(highest, int(match.group(1)))
    return highest + 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()
    folder = args.destination.expanduser().resolve() / "reviews"
    folder.mkdir(parents=True, exist_ok=True)
    version = next_version(folder)
    path = folder / f"V{version}.md"
    path.write_text(TEMPLATE.format(n=version, title=args.title.strip()), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
