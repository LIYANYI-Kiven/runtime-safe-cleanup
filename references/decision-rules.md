# Borderline cleanup decisions

Use these checks after the complete directory inventory exists. They do not replace the required project root, destination, or function notes.

- Trace the real startup command and one representative use of every retained capability before calling a directory unnecessary. A clean import can hide modules loaded only while answering.
- Follow manifest and configuration paths, including paths outside the project. A local copy is not redundant until the selected external path is confirmed.
- Do not follow or remove a symlink automatically. It may be the path the project uses, while its target may belong to another tree.
- `__pycache__` and `.pyc` files are cache candidates. A `.venv`, installed runtime, or third-party checkout stays unless reinstallation is tested and the user accepts it.
- A filename proposal from the residual-file scan is only a candidate. Keep the file when an entry point imports, launches, or serves it.
- Generated reports and old result files can move. Curated benchmark definitions, source data, and cited documents stay when the project uses them.
- Directories with the same name can have different contracts. Do not merge them as part of cleanup.
- On FAT32, verify the copy but do not claim that the archive preserves permissions or encryption. Files of 4 GiB or larger need another destination.
