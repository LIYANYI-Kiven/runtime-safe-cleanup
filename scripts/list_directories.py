"""为项目根目录下的每一层目录各写一条记录。

这是清单工具，不会移动或删除文件。
"""
from __future__ import annotations

import argparse
import json
import os
import stat
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
    # Do not follow junctions or symlinks: they may belong to another project.
    for current, names, files in os.walk(root, followlinks=False):
        path = Path(current)
        child_directories = []
        reparse_children = []
        for name in names:
            child = path / name
            try:
                attributes = os.lstat(child).st_file_attributes
            except (AttributeError, OSError):
                attributes = 0
            if child.is_symlink() or attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                reparse_children.append(name)
            else:
                child_directories.append(name)
        directories.append({
            "relative_path": path.relative_to(root).as_posix() or ".",
            "depth": len(path.relative_to(root).parts),
            "child_directory_count": len(child_directories),
            "child_file_count": len(files),
            "reparse_point_children": sorted(reparse_children),
        })

    report = {
        "root": str(root),
        "directory_count": len(directories),
        "directories": directories,
        "boundary": "仅生成清单。分类或移动之前，必须先说明每一行目录的功能；清单不跟随链接或 Windows junction。",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"directory_count": len(directories), "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
