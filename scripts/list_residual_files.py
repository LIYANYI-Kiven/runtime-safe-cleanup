"""列出清理目录后剩余的每个文件，并给出清理类别建议。

类别只是待复核的建议，不是移动或删除许可。
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


LOG_PARTS = {"log", "logs"}
CACHE_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".cache"}
TEST_PARTS = {"test", "tests", "__tests__", "spec", "specs"}
RESULT_PARTS = {"output", "outputs", "result", "results", "eval", "evaluation", "reports"}


def category(path: Path) -> str:
    parts = {part.lower() for part in path.parts[:-1]}
    name = path.name.lower()
    suffix = path.suffix.lower()
    if suffix == ".log" or parts & LOG_PARTS:
        return "log"
    if suffix in {".pyc", ".pyo"} or parts & CACHE_PARTS or name.endswith(".tmp"):
        return "cache"
    if (
        parts & TEST_PARTS
        or name.startswith("test_")
        or name.endswith(("_test.py", ".test.js", ".spec.js", ".test.ts", ".spec.ts"))
    ):
        return "test"
    if parts & RESULT_PARTS:
        return "result"
    return "unclassified"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        raise SystemExit(f"Project root is not a directory: {root}")

    files = []
    counts = {"log": 0, "cache": 0, "test": 0, "result": 0, "unclassified": 0}
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        selected = category(path.relative_to(root))
        counts[selected] += 1
        files.append({
            "relative_path": path.relative_to(root).as_posix(),
            "category": selected,
            "bytes": path.stat().st_size,
        })

    report = {
        "root": str(root),
        "file_count": len(files),
        "counts": counts,
        "files": files,
        "boundary": "建议必须对照启动入口复核。未分类文件除非另有依据，否则留在项目内。",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"file_count": len(files), "counts": counts, "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
