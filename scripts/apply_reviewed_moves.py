"""把已复核的内容复制到项目外归档，核对一致后才删除源文件。

迁移计划使用如下 JSON：

{
  "directories": ["old-eval"],
  "files": {
    "logs": ["service.log"],
    "caches": ["pkg/__pycache__/mod.pyc"],
    "tests": ["tests/test_api.py"],
    "results": ["results/run.json"]
  }
}

目录放到 <destination>/directories。文件按 logs、caches、tests、results 分类。原相对路径保持不变。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


FILE_CATEGORIES = {"logs": "log", "caches": "cache", "tests": "test", "results": "result"}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def snapshot(path: Path) -> list[tuple[str, int, str]]:
    paths = [path] if path.is_file() else sorted(item for item in path.rglob("*") if item.is_file())
    return [(item.relative_to(path).as_posix(), item.stat().st_size, digest(item)) for item in paths]


def inside(root: Path, path: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def validate(root: Path, destination: Path, plan: dict) -> list[tuple[str, Path, Path]]:
    if not root.is_dir():
        raise SystemExit(f"Project root is not a directory: {root}")
    if destination.exists() and not destination.is_dir():
        raise SystemExit(f"Destination is not a directory: {destination}")
    if inside(root, destination) or inside(destination, root) or root == destination:
        raise SystemExit("Destination must be outside the project root")

    moves: list[tuple[str, Path, Path]] = []
    directory_sources: list[Path] = []
    for relative in plan.get("directories") or []:
        source = (root / relative).resolve()
        if not inside(root, source) or source == root or not source.is_dir() or source.is_symlink():
            raise SystemExit(f"Refusing directory: {relative}")
        target = destination / "directories" / Path(relative)
        directory_sources.append(source)
        moves.append(("directories", source, target))

    for folder, values in (plan.get("files") or {}).items():
        if folder not in FILE_CATEGORIES:
            raise SystemExit(f"Unknown file category: {folder}")
        for relative in values or []:
            source = (root / relative).resolve()
            if not inside(root, source) or not source.is_file() or source.is_symlink():
                raise SystemExit(f"Refusing file: {relative}")
            if any(inside(directory, source) for directory in directory_sources):
                raise SystemExit(f"File belongs to a moved directory: {relative}")
            moves.append((folder, source, destination / folder / Path(relative)))

    for _category, _source, target in moves:
        if target.exists():
            raise SystemExit(f"Destination already exists: {target}")
    if not moves:
        raise SystemExit("The reviewed plan contains nothing to move")
    return moves


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    destination = args.destination.resolve()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    moves = validate(root, destination, plan)
    moved = []
    for category, source, target in moves:
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
        if snapshot(source) != snapshot(target):
            raise SystemExit(f"Verification failed; source retained: {source}")
        if source.is_dir():
            shutil.rmtree(source)
        else:
            source.unlink()
        moved.append({
            "category": category,
            "source": str(source),
            "destination": str(target),
            "verified": True,
        })

    manifest = destination / "move_manifest.json"
    existing = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else {"moves": []}
    existing["moves"].extend(moved)
    manifest.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"moved": len(moved), "manifest": str(manifest)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
