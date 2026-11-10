#!/usr/bin/env python3
"""Collect documentation from source repos into modules/ and common/.

dx-docs holds copies only. Every run replaces each enabled repo's folder
with a fresh copy of README*.md, RELEASE_NOTES*.md and docs/ from the
source repo's default branch, and records where it came from in
.source.json so the copy can be checked against its origin.

Usage:
  python scripts/sync.py            # sync all enabled repos
  python scripts/sync.py dx_rt      # sync one repo
  python scripts/sync.py --check    # fail if any copy differs from its source
"""
import fnmatch
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONF = yaml.safe_load((ROOT / "sources.yml").read_text())
ORG = CONF["org"]
FILES = CONF["copy"]["files"]
DIRS = CONF["copy"]["dirs"]
EXCLUDE = set(CONF["copy"]["exclude"])


def run(*args, cwd=None):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def ignore(_dir, names):
    return [n for n in names if n in EXCLUDE]


def collect(src: Path, dst: Path):
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    for entry in sorted(src.iterdir()):
        if entry.is_file() and any(fnmatch.fnmatch(entry.name, p) for p in FILES):
            shutil.copy2(entry, dst / entry.name)
    for d in DIRS:
        if (src / d).is_dir():
            shutil.copytree(src / d, dst / d, ignore=ignore)


def sync_repo(group: str, repo: str, check: bool) -> bool:
    url = f"https://github.com/{ORG}/{repo}.git"
    dst = ROOT / group / repo
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / repo
        run("git", "clone", "--quiet", "--depth", "1", url, str(work))
        sha = run("git", "rev-parse", "HEAD", cwd=work)
        branch = run("git", "rev-parse", "--abbrev-ref", "HEAD", cwd=work)
        if check:
            meta = dst / ".source.json"
            if not meta.exists():
                print(f"  {group}/{repo}: not collected yet")
                return False
            recorded = json.loads(meta.read_text())["commit"]
            ok = recorded == sha
            print(f"  {group}/{repo}: {'up to date' if ok else f'behind ({recorded[:7]} -> {sha[:7]})'}")
            return ok
        collect(work, dst)
    (dst / ".source.json").write_text(json.dumps({
        "repo": f"{ORG}/{repo}",
        "branch": branch,
        "commit": sha,
        "synced_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }, indent=2) + "\n")
    print(f"  {group}/{repo}: {sha[:7]}")
    return True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    ok = True
    for group in ("modules", "common"):
        for item in CONF.get(group) or []:
            if not item.get("enabled"):
                continue
            if args and item["repo"] not in args:
                continue
            ok = sync_repo(group, item["repo"], check) and ok
    if check and not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
