"""Write one record for every directory under a project root.

This is an inventory tool. It never moves or deletes files.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        raise SystemExit(f"Project root is not a directory: {root}")

    directories = []
    for path in [root, *sorted(item for item in root.rglob("*") if item.is_dir())]:
        children = list(path.iterdir())
        directories.append({
            "relative_path": path.relative_to(root).as_posix() or ".",
            "depth": len(path.relative_to(root).parts),
            "child_directory_count": sum(child.is_dir() for child in children),
            "child_file_count": sum(child.is_file() for child in children),
        })

    report = {
        "root": str(root),
        "directory_count": len(directories),
        "directories": directories,
        "boundary": "Inventory only. Explain every row before classifying or moving anything.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"directory_count": len(directories), "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
