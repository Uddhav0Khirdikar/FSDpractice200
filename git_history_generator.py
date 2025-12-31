#!/usr/bin/env python3
"""
Folder-wise Git History Generator

Creates a realistic git history by treating each top-level directory as a project.

Features:
- Auto-detects top-level project folders
- Spreads commits across specified date range
- Groups all files within a folder into a single commit
- Handles numbered folder naming (e.g., 001-project-name)

Usage options:

    1. Interactive mode (prompts for dates):
       python3 git_history_generator.py

    2. Non-interactive (command line args):
       python3 git_history_generator.py -s 2026-01-01 -e 2026-03-31

    3. Preview first (dry-run):
       python3 git_history_generator.py --dry-run
"""

import os
import sys
import subprocess
import argparse
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Project:
    path: Path
    program_number: int
    files: List[Path]

    @property
    def file_count(self) -> int:
        return len(self.files)


@dataclass
class CommitPlan:
    files: List[Path]
    date: datetime
    message: str
    program_number: Optional[int] = None
    project_path: Optional[Path] = None


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

_GIT_ENV_BASE: dict = {}   # populated once in create_git_history

def _run(args: List[str], cwd: str, env: dict = None, capture: bool = True) -> subprocess.CompletedProcess:
    """Thin wrapper around subprocess.run with sensible defaults."""
    return subprocess.run(
        args, cwd=cwd, env=env or _GIT_ENV_BASE,
        check=True, capture_output=capture,
    )


def _git(args: List[str], cwd: str, env: dict = None) -> subprocess.CompletedProcess:
    return _run(["git"] + args, cwd=cwd, env=env)


def _git_out(args: List[str], cwd: str) -> str:
    result = _run(["git"] + args, cwd=cwd)
    return result.stdout.decode().strip()


# ---------------------------------------------------------------------------
# Project discovery
# ---------------------------------------------------------------------------

_SKIP_DIRS = frozenset({
    "bin", "obj", ".git", "node_modules", "dist", "build", 
    ".next", ".vuepress", ".cache", "__pycache__", "venv", ".venv",
    "target", "out", ".vs", ".vscode", ".idea"
})


def find_projects(root_dir: Path) -> List[Project]:
    """
    Find all immediate subdirectories and treat them as projects.
    """
    projects: List[Project] = []
    
    # Get immediate subdirectories, excluding hidden ones and skip dirs
    subdirs = sorted([
        d for d in root_dir.iterdir() 
        if d.is_dir() and not d.name.startswith(".") and d.name not in _SKIP_DIRS
    ])

    for subdir in subdirs:
        all_files: List[Path] = []
        for dirpath, dirnames, filenames in os.walk(subdir):
            # Prune skip dirs in-place
            dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS and not d.startswith(".")]
            for fname in filenames:
                if not fname.startswith("."):
                    all_files.append(Path(dirpath) / fname)

        if not all_files:
            continue

        # Extract optional leading program number from directory name
        parts = subdir.name.split("-")
        try:
            prog_num = int(parts[0])
        except (ValueError, IndexError):
            prog_num = 0

        projects.append(Project(
            path=subdir,
            program_number=prog_num,
            files=all_files,
        ))

    # Sort projects: numbered ones first, then alphabetical
    projects.sort(key=lambda p: (p.program_number == 0, p.program_number, p.path.name.lower()))
    return projects


# ---------------------------------------------------------------------------
# Commit planning
# ---------------------------------------------------------------------------

def generate_commit_dates(
    start_date: datetime,
    end_date: datetime,
    total_commits: int,
) -> List[datetime]:
    if total_commits <= 1:
        return [start_date]

    total_days = max((end_date - start_date).days, 1)
    n = total_commits - 1

    return [
        (start_date + timedelta(days=int(i / n * total_days))).replace(
            hour=8 + (i % 12),
            minute=15 + (i * 7) % 45,
            second=0,
            microsecond=0,
        )
        for i in range(total_commits)
    ]


def plan_commits(
    projects: List[Project],
    start_date: datetime,
    end_date: datetime,
) -> List[CommitPlan]:
    total_commits = len(projects)
    if total_commits == 0:
        return []

    commit_dates = generate_commit_dates(start_date, end_date, total_commits)
    plans: List[CommitPlan] = []

    for i, project in enumerate(projects):
        plans.append(CommitPlan(
            files=project.files,
            date=commit_dates[i],
            message=f"Add project: {project.path.name}",
            program_number=project.program_number if project.program_number > 0 else None,
            project_path=project.path,
        ))

    return plans


# ---------------------------------------------------------------------------
# Core: create git history
# ---------------------------------------------------------------------------

_GITIGNORE = """# IDEs
.vs/
.vscode/
.idea/

# Build outputs
bin/
obj/
dist/
build/
out/
target/
*.exe
*.dll
*.pdb

# Dependencies
node_modules/
venv/
.venv/
__pycache__/

# Logs and temp
*.log
.cache/
.qwen/
.DS_Store
"""


def create_git_history(
    root_dir: Path,
    start_date: datetime,
    end_date: datetime,
    dry_run: bool = False,
) -> None:
    root_str = str(root_dir)

    print(f"📁 Scanning for projects in: {root_dir}")
    projects = find_projects(root_dir)
    print(f"✅ Found {len(projects)} projects")

    if not projects:
        print("❌ No projects found!")
        return

    print("\n📊 Project summary:")
    for proj in projects[:5]:
        print(f"   {proj.path.name} ({proj.file_count} files)")
    if len(projects) > 5:
        print(f"   ... and {len(projects) - 5} more")

    print(f"\n📅 Date range: {start_date:%Y-%m-%d} → {end_date:%Y-%m-%d}")

    commit_plans = plan_commits(projects, start_date, end_date)
    print(f"📝 Planned {len(commit_plans)} commits")

    if dry_run:
        print("\n🔍 DRY RUN — commit plan (first 10):")
        for i, plan in enumerate(commit_plans[:10]):
            print(f"   {i+1:3d}. {plan.date:%Y-%m-%d %H:%M}  {plan.message}")
            if plan.project_path:
                print(f"         Folder: {plan.project_path.name}")
        if len(commit_plans) > 10:
            print(f"   … and {len(commit_plans) - 10} more commits")
        return

    # ------------------------------------------------------------------
    # Initialise repo
    # ------------------------------------------------------------------
    print("\n🔧 Initialising git repository…")
    _git(["init"], root_str)
    _git(["config", "user.email", "dev@example.com"], root_str)
    _git(["config", "user.name", "Developer"], root_str)

    (root_dir / ".gitignore").write_text(_GITIGNORE)

    init_env = {**os.environ,
                "GIT_AUTHOR_DATE": start_date.strftime("%Y-%m-%dT%H:%M:%S"),
                "GIT_COMMITTER_DATE": start_date.strftime("%Y-%m-%dT%H:%M:%S")}
    
    # Add root files (non-directories) to initial commit
    root_files = [f for f in root_dir.iterdir() if f.is_file() and not f.name.startswith(".")]
    if root_files:
        _git(["add"] + [f.name for f in root_files], root_str)
    else:
        _git(["add", ".gitignore"], root_str)
        
    _git(["commit", "-m", "Initial commit: Project setup"], root_str, env=init_env)
    print("✅ Initial commit created (with root files)")

    # ------------------------------------------------------------------
    # Folder-wise commits
    # ------------------------------------------------------------------
    print("\n📦 Creating commits…")
    total = len(commit_plans)
    skipped = 0

    base_env = os.environ.copy()

    for i, plan in enumerate(commit_plans):
        # Efficiently add the entire project folder
        if plan.project_path:
            rel_path = str(plan.project_path.relative_to(root_dir))
            _git(["add", rel_path], root_str)

        # Check staging area before committing
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=root_str, capture_output=True, text=True,
        )
        if not status.stdout.strip():
            skipped += 1
            continue

        date_str = plan.date.strftime("%Y-%m-%dT%H:%M:%S")
        commit_env = {**base_env,
                      "GIT_AUTHOR_DATE": date_str,
                      "GIT_COMMITTER_DATE": date_str}
        _git(["commit", "-m", plan.message], root_str, env=commit_env)

        # Inline progress
        done = i + 1
        if done % 10 == 0 or done == total:
            pct = done * 100 // total
            bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
            print(f"\r   [{bar}] {done}/{total} ({plan.date:%Y-%m-%d})", end="", flush=True)

    print()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total_commits = int(_git_out(["rev-list", "--count", "HEAD"], root_str))
    first_date = _git_out(["log", "--reverse", "--format=%ad", "--date=short"], root_str).split("\n")[0]
    last_date  = _git_out(["log", "--format=%ad", "--date=short"], root_str).split("\n")[0]

    print(f"\n✅ Done! {total_commits} commits ({first_date} → {last_date})")
    if skipped:
        print(f"   ℹ️  {skipped} batches skipped (nothing to stage)")

    print("\n📜 Last 5 commits:")
    for line in _git_out(["log", "--oneline", "-5"], root_str).split("\n"):
        print(f"   {line}")


# ---------------------------------------------------------------------------
# CLI helpers
# ---------------------------------------------------------------------------

def _parse_date(s: str) -> datetime:
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date '{s}'. Use YYYY-MM-DD.")


def _prompt_date(prompt: str, default: str) -> datetime:
    while True:
        raw = input(f"{prompt} [{default}]: ").strip() or default
        try:
            return datetime.strptime(raw, "%Y-%m-%d")
        except ValueError:
            print("   ❌ Use YYYY-MM-DD (e.g. 2026-01-15)")


def _prompt_timespan() -> tuple[datetime, datetime]:
    print("\n📅 Choose date range:")
    print("   1. Preset  (2026-01-01 → 2026-03-31)")
    print("   2. Custom start + end dates")
    print("   3. Start date + number of days")

    choice = input("\n   Select [1]: ").strip() or "1"

    if choice == "2":
        start = _prompt_date("   Start date", "2026-01-01")
        end   = _prompt_date("   End date",   "2026-03-31")
        return start, end

    if choice == "3":
        start = _prompt_date("   Start date", "2026-01-01")
        raw = input("   Number of days [90]: ").strip() or "90"
        try:
            days = int(raw)
        except ValueError:
            print("   ❌ Using 90 days")
            days = 90
        return start, start + timedelta(days=days)

    return datetime(2026, 1, 1), datetime(2026, 3, 31)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create realistic git history for folder-based projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                  # interactive
  %(prog)s -s 2026-01-01 -e 2026-03-31     # non-interactive
  %(prog)s --dry-run                        # preview only
        """,
    )
    parser.add_argument("-d", "--directory", type=Path, default=Path("."),
                        help="Root directory (default: current dir)")
    parser.add_argument("-s", "--start", type=str, default=None,
                        help="Start date YYYY-MM-DD")
    parser.add_argument("-e", "--end",   type=str, default=None,
                        help="End date YYYY-MM-DD")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without creating commits")
    parser.add_argument("-i", "--interactive", action="store_true",
                        help="Force interactive date prompts")

    args = parser.parse_args()

    # Resolve dates
    if args.interactive or not (args.start and args.end):
        start_date, end_date = _prompt_timespan()
    else:
        try:
            start_date = datetime.strptime(args.start, "%Y-%m-%d")
            end_date   = datetime.strptime(args.end,   "%Y-%m-%d")
        except ValueError:
            print("❌ Invalid date format — use YYYY-MM-DD")
            sys.exit(1)

    if start_date > end_date:
        print("❌ Start date must be before end date")
        sys.exit(1)

    root_dir = args.directory.resolve()
    if not root_dir.exists():
        print(f"❌ Directory not found: {root_dir}")
        sys.exit(1)

    # Remove stale .git
    git_dir = root_dir / ".git"
    if git_dir.exists():
        print("🗑️  Removing existing .git directory…")
        shutil.rmtree(git_dir)

    create_git_history(root_dir, start_date, end_date, args.dry_run)


if __name__ == "__main__":
    main()
