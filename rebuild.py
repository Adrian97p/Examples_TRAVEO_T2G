#!/usr/bin/env python3
"""Rebuild ModusToolbox example projects.

Usage (from the workspace root):
    python rebuild.py all               # clean + build every project
    python rebuild.py 01_Blinky_LED     # clean + build only that project

Projects are the numbered folders (01_*, 02_*, ...) that contain a Makefile.
Builds go through .github/skills/mtb-tools/scripts/run_make.py so the
modus-shell environment and CY_TOOLS_PATHS are set up correctly.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUN_MAKE = ROOT / ".github" / "skills" / "mtb-tools" / "scripts" / "run_make.py"
PROJECT_RE = re.compile(r"^\d+_.+")


def find_projects():
    return sorted(
        p.name
        for p in ROOT.iterdir()
        if p.is_dir() and PROJECT_RE.match(p.name) and (p / "Makefile").is_file()
    )


def make_cmd(project, *make_args):
    # --args consumes the remainder, so it must be last.
    return [
        sys.executable,
        str(RUN_MAKE),
        "--working-dir",
        str(ROOT / project),
        "--filter-progress",
        "--args",
        *make_args,
    ]


def rebuild(project):
    """clean + build one project. Returns True on success."""
    for target in ("clean", "build"):
        extra = ["-j8"] if target == "build" else []
        print(f"\n=== {project}: make {target} {' '.join(extra)} ===", flush=True)
        rc = subprocess.call(make_cmd(project, target, *extra))
        if rc != 0:
            print(f"=== {project}: make {target} FAILED (exit {rc}) ===", flush=True)
            return False
    print(f"=== {project}: OK ===", flush=True)
    return True


def main(argv):
    projects = find_projects()
    if len(argv) != 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        print("Available projects: all, " + ", ".join(projects))
        return 0 if len(argv) == 2 else 2

    name = argv[1]
    if name == "all":
        selected = projects
    elif name in projects:
        selected = [name]
    else:
        print(f"error: unknown project '{name}'", file=sys.stderr)
        print("Available projects: all, " + ", ".join(projects), file=sys.stderr)
        return 2

    failed = [p for p in selected if not rebuild(p)]
    print("\n================ SUMMARY ================")
    for p in selected:
        print(f"  {'PASS' if p not in failed else 'FAIL'}  {p}")
    print(f"{len(selected) - len(failed)}/{len(selected)} projects rebuilt successfully")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
