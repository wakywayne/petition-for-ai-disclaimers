import os
from pathlib import Path

# ====== ROOT & FOLDER PATHS ======
ROOT = Path(__file__).resolve().parent
FOLDER_PATH = ROOT / "attachments"   # <- target folder
# =================================

RENAME_DIRS = False  # set True to also strip spaces from directory names

def strip_spaces(name: str) -> str:
    """Remove ALL spaces from a filename or directory name."""
    return name.replace(" ", "")

def unique_target(path: Path) -> Path:
    """
    If 'path' already exists, append _1, _2, ... before the suffix until unique.
    Keeps the original extension.
    """
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    parent = path.parent
    i = 1
    while True:
        candidate = parent / f"{stem}_{i}{suffix}"
        if not candidate.exists():
            return candidate
        i += 1

def rename_entry(old_path: Path, new_name: str) -> Path | None:
    """Rename a file/dir to 'new_name' within the same parent, avoiding collisions."""
    if old_path.name == new_name:
        return None
    target = unique_target(old_path.with_name(new_name))
    old_path.rename(target)
    return target

def rename_files(root: Path) -> int:
    """Strip spaces from FILE names under 'root' (recursive)."""
    count = 0
    for dirpath, _dirnames, filenames in os.walk(root):
        d = Path(dirpath)
        for fname in filenames:
            old = d / fname
            new_name = strip_spaces(fname)
            try:
                result = rename_entry(old, new_name)
                if result:
                    print(f"Renamed file: '{old.name}' -> '{result.name}'")
                    count += 1
            except Exception as e:
                print(f"Failed to rename file '{old}': {e}")
    return count

def rename_dirs_bottom_up(root: Path) -> int:
    """
    Optionally strip spaces from DIRECTORY names (bottom-up to not break traversal).
    """
    count = 0
    for dirpath, dirnames, _filenames in os.walk(root, topdown=False):
        d = Path(dirpath)
        for dirname in dirnames:
            old = d / dirname
            new_name = strip_spaces(dirname)
            try:
                result = rename_entry(old, new_name)
                if result:
                    print(f"Renamed dir:  '{old.name}' -> '{result.name}'")
                    count += 1
            except Exception as e:
                print(f"Failed to rename dir '{old}': {e}")
    return count

if __name__ == "__main__":
    if not FOLDER_PATH.exists() or not FOLDER_PATH.is_dir():
        raise SystemExit(f"Target folder does not exist or is not a directory: {FOLDER_PATH}")

    print(f"ROOT:        {ROOT}")
    print(f"FOLDER_PATH: {FOLDER_PATH}")

    file_count = rename_files(FOLDER_PATH)
    print(f"\nDone. Files renamed: {file_count}")

    if RENAME_DIRS:
        dir_count = rename_dirs_bottom_up(FOLDER_PATH)
        print(f"Done. Directories renamed: {dir_count}")

