"""Verify goal-driven cleanup evidence without modifying project files."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def snapshot(path: Path) -> list[tuple[str, int, str]]:
    paths = [path] if path.is_file() else sorted(item for item in path.rglob("*") if item.is_file())
    return [(item.relative_to(path).as_posix(), item.stat().st_size, digest(item)) for item in paths]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    destination = args.destination.resolve()
    contract = destination / "goal-contract.md"
    manifest = destination / "move_manifest.json"
    reviews = sorted((destination / "reviews").glob("V*.md")) if (destination / "reviews").is_dir() else []
    failures: list[str] = []
    if not contract.is_file():
        failures.append("missing goal-contract.md")
    if not reviews:
        failures.append("no review files")

    verified_moves = []
    if manifest.is_file():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        for move in data.get("moves", []):
            source = Path(move["source"])
            target = Path(move["destination"])
            item = {"source": str(source), "destination": str(target), "ok": False}
            if source.exists():
                item["reason"] = "source still exists"
                failures.append(f"source remains: {source}")
            elif not target.exists():
                item["reason"] = "archive copy missing"
                failures.append(f"archive copy missing: {target}")
            elif "snapshot" not in move:
                item["reason"] = "manifest lacks independent hash snapshot"
                failures.append(f"manifest lacks hash snapshot: {target}")
            else:
                try:
                    expected = [tuple(entry) for entry in move["snapshot"]]
                except (TypeError, ValueError):
                    expected = []
                if expected != snapshot(target):
                    item["reason"] = "archive hash snapshot mismatch"
                    failures.append(f"archive hash mismatch: {target}")
                else:
                    item["ok"] = True
            verified_moves.append(item)
    else:
        failures.append("missing move_manifest.json")

    report = {
        "root": str(root),
        "destination": str(destination),
        "goal_contract": str(contract),
        "review_count": len(reviews),
        "moved_items": verified_moves,
        "ok": not failures,
        "failures": failures,
        "boundary": "This validates cleanup evidence only. Run the project's real health and function probes separately.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": report["ok"], "failures": failures, "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
