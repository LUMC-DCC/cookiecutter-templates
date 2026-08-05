import shutil
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TEMPLATE_DIRS = [
    d for d in ROOT.iterdir()
    if d.is_dir()
    and not d.name.startswith((".", "_"))
    and (d / "{{cookiecutter.project_slug}}").exists()
]

RELATIVE_SYNC_MAP = {
    "hooks": "hooks",
    "cookiecutter.json": "cookiecutter.json",
    "LICENSE.txt": "{{cookiecutter.project_slug}}/LICENSE.txt",
    "licenses": "{{cookiecutter.project_slug}}/licenses",
}

# Collect modified paths
MODIFIED_PATHS = []

def remove_path(path: Path):
    for attempt in range(3):
        try:
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()
            return
        except FileNotFoundError:
            return
        except OSError:
            if attempt == 2:
                raise
            time.sleep(0.1)

def sync_dir(src: Path, dst: Path):
    if dst.exists() and not dst.is_dir():
        remove_path(dst)

    dst.mkdir(parents=True, exist_ok=True)

    src_entries = {entry.name for entry in src.iterdir()}
    for dst_entry in dst.iterdir():
        if dst_entry.name not in src_entries:
            remove_path(dst_entry)

    for src_entry in src.iterdir():
        sync_path(src_entry, dst / src_entry.name)

def sync_path(src: Path, dst: Path):
    if src.is_file():
        if dst.exists() and dst.is_dir():
            remove_path(dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        MODIFIED_PATHS.append(dst)
    elif src.is_dir():
        sync_dir(src, dst)
        MODIFIED_PATHS.append(dst)
    else:
        print(f"[warning] Unknown source type: {src}")
        return
    print(f"[sync] Synced {src} → {dst}")

def main():
    seen = set()
    for template_dir in TEMPLATE_DIRS:
        for rel_src, rel_dst in RELATIVE_SYNC_MAP.items():
            src = ROOT / "_cc_shared" / rel_src
            dst = template_dir / rel_dst
            key = (str(src), str(dst))

            if key in seen:
                continue
            seen.add(key)

            sync_path(src, dst)

    for path in MODIFIED_PATHS:
        print(f"[modified]{path}")

if __name__ == "__main__":
    main()
