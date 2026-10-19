---
name: runtime-safe-cleanup
description: Inventory every directory in a user-supplied project, explain its function, and move only items unnecessary to the running system into a separate user-supplied archive. Use for project cleanup, archival of unused directories, or separation of logs, caches, tests, and results. Do not use it before both paths are supplied or to delete files in place.
metadata:
  short-description: Archive nonessential project files
---
# Runtime-safe cleanup

Move unused project material to a user-supplied archive without damaging the running project. Obtain both paths before moving anything. A complete directory inventory and a function explanation come before classification; copy verification comes before source removal.

## Required inputs

Stop and ask when either path is missing. Do not reuse a destination from another project.

- Project root: the tree to inspect and clean.
- Destination: the archive that receives moved items. It must be outside the project root, and the two paths must not overlap.

## 1. List every directory and explain it

Run [scripts/list_directories.py](scripts/list_directories.py) on the project root. It writes one record for every directory at every depth and does not move anything. Do not replace this scan with a manual sample.

Read the inventory, then write what each directory does. A repeated generated pattern may be explained once, but the note must give the pattern, the count, and its parent path. Every inventory row must be covered by an individual note or a stated pattern. A familiar name such as `runtime`, `store`, `cache`, or `candidate` is not a classification.

Save the inventory and the function notes in `docs/project-structure/`.

## 2. Move directories the running project does not need

Keep a directory when startup, a supported request, configuration, citation, or recovery reads or writes it. Keep the virtual environment selected by the startup command.

Move only directories whose recorded function is unnecessary to the project's complete running behavior. Preserve each relative path under `<destination>/directories/`. Build an explicit plan and run [scripts/apply_reviewed_moves.py](scripts/apply_reviewed_moves.py). It copies, compares file names, sizes, and SHA-256 hashes, then removes the source only when the copy matches. It refuses paths outside the project, a destination inside the project, symlinks, and existing destination paths.

Leave an uncertain directory in place and record why. Read [references/decision-rules.md](references/decision-rules.md) before a borderline decision.

## 3. Classify the files that remain

After the directory moves, run [scripts/list_residual_files.py](scripts/list_residual_files.py). It lists every remaining file and proposes one category: `log`, `cache`, `test`, `result`, or `unclassified`. The proposals are not authorization to move.

Review every proposed file against the entry points and directory notes. Move accepted files into these destination folders:

- `logs/` for log files;
- `caches/` for regenerable cache files;
- `tests/` for tests that the running system does not execute;
- `results/` for generated outputs and result files.

Keep source, active data, configuration, credentials, and files launched or imported by an entry point. Use the same reviewed-move script and verification. Do not delete anything that the script did not verify.

## 4. Leave four documentation folders

Create any of these project folders that are missing, without removing the only working copy of an existing document:

- `docs/project-structure/` records the full directory inventory and function notes.
- `docs/development-log/` records existing development logs and this cleanup's move manifest.
- `docs/project-description/` records what the project is and what it contains.
- `docs/usage/` records startup scripts, working directories, environment values, and commands.

Do not relocate a live startup script into `docs/` when a command depends on its current path. Copy its command into `docs/usage/` and leave the script where it runs.

Read [references/plantglyco-lessons.md](references/plantglyco-lessons.md) only for the PlantGlyco evidence project or another tree that uses its federated index layout.
# Runtime-safe cleanup
---
name: runtime-safe-cleanup
description: Inventory every directory in a user-supplied project, explain its function, and move only items unnecessary to the running system into a separate user-supplied archive. Use for project cleanup, archival of unused directories, or separation of logs, caches, tests, and results. Do not use it before both paths are supplied or to delete files in place.
metadata:
  short-description: Archive nonessential project files
---

# Runtime-safe cleanup

