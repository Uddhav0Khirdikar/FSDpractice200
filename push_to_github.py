#!/usr/bin/env python3
"""Create a GitHub repository and push this local git repository to it."""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path


GITHUB_API = "https://api.github.com"


def run_git(
    args: list[str],
    cwd: Path,
    env: dict[str, str] | None = None,
    isolated_auth: bool = False,
) -> subprocess.CompletedProcess:
    command = ["git"]
    if isolated_auth:
        command += [
            "-c",
            "credential.helper=",
            "-c",
            "credential.useHttpPath=true",
        ]
    command += args
    return subprocess.run(command, cwd=cwd, env=env, text=True, check=True)


def api_request(token: str, method: str, path: str, payload: dict | None = None) -> dict:
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        f"{GITHUB_API}{path}",
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "super300-push-helper",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    with urllib.request.urlopen(request) as response:
        body = response.read().decode("utf-8")
        return json.loads(body) if body else {}


def create_repo(token: str, repo_name: str, private: bool, description: str) -> dict:
    payload = {
        "name": repo_name,
        "private": private,
        "description": description,
        "auto_init": False,
    }
    return api_request(token, "POST", "/user/repos", payload)


def repo_exists(token: str, username: str, repo_name: str) -> bool:
    try:
        api_request(token, "GET", f"/repos/{username}/{repo_name}")
        return True
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return False
        raise


def ensure_clean_or_allowed(repo_dir: Path, allow_dirty: bool) -> None:
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    if status and not allow_dirty:
        raise SystemExit(
            "Working tree is not clean. Commit your changes first, or pass --allow-dirty."
        )


def configure_remote(repo_dir: Path, username: str, repo_name: str, remote_name: str) -> str:
    remote_url = f"https://github.com/{username}/{repo_name}.git"

    remotes = subprocess.run(
        ["git", "remote"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()

    if remote_name in remotes:
        run_git(["remote", "set-url", remote_name, remote_url], repo_dir)
    else:
        run_git(["remote", "add", remote_name, remote_url], repo_dir)

    return remote_url


def make_askpass_script() -> Path:
    script = tempfile.NamedTemporaryFile("w", delete=False, prefix="github-askpass-", suffix=".sh")
    script.write(
        "#!/bin/sh\n"
        "case \"$1\" in\n"
        "  *Username*) printf '%s\\n' \"$GITHUB_PUSH_USERNAME\" ;;\n"
        "  *Password*) printf '%s\\n' \"$GITHUB_PUSH_TOKEN\" ;;\n"
        "  *) printf '\\n' ;;\n"
        "esac\n"
    )
    script.close()

    path = Path(script.name)
    path.chmod(0o700)
    return path


def push_repo(repo_dir: Path, token: str, remote_name: str, branch: str) -> None:
    askpass = make_askpass_script()
    env = {
        **os.environ,
        "GIT_ASKPASS": str(askpass),
        "GIT_TERMINAL_PROMPT": "0",
        "GITHUB_PUSH_USERNAME": "x-access-token",
        "GITHUB_PUSH_TOKEN": token,
    }

    try:
        run_git(
            ["push", "-u", remote_name, f"HEAD:{branch}"],
            repo_dir,
            env=env,
            isolated_auth=True,
        )
        run_git(["push", remote_name, "--tags"], repo_dir, env=env, isolated_auth=True)
    finally:
        askpass.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a GitHub repo and push the current local git repo."
    )
    parser.add_argument(
        "values",
        nargs="*",
        metavar="VALUE",
        help="Either: TOKEN USERNAME REPO_NAME, or USERNAME REPO_NAME with --token/GITHUB_TOKEN",
    )
    parser.add_argument("--token", help="GitHub token with repo creation and push access")
    parser.add_argument(
        "-d",
        "--directory",
        type=Path,
        default=Path("."),
        help="Local git repository directory (default: current directory)",
    )
    parser.add_argument(
        "-b",
        "--branch",
        default="main",
        help="Remote branch name to push HEAD to (default: main)",
    )
    parser.add_argument(
        "--remote",
        default="origin",
        help="Git remote name to create or update (default: origin)",
    )
    parser.add_argument(
        "--private",
        action="store_true",
        help="Create the GitHub repository as private",
    )
    parser.add_argument(
        "--description",
        default="Generated C# project history",
        help="Repository description",
    )
    parser.add_argument(
        "--allow-existing",
        action="store_true",
        help="Push if the GitHub repository already exists",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Push even when the local working tree has uncommitted changes",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if len(args.values) == 3:
        positional_token, username, repo_name = args.values
        token = args.token or positional_token
    elif len(args.values) == 2:
        username, repo_name = args.values
        token = args.token or os.environ.get("GITHUB_TOKEN")
    else:
        print(
            "Usage: push_to_github.py TOKEN USERNAME REPO_NAME "
            "or push_to_github.py --token TOKEN USERNAME REPO_NAME",
            file=sys.stderr,
        )
        return 2

    if not token:
        print("GitHub token is required. Pass it as the first argument or set GITHUB_TOKEN.", file=sys.stderr)
        return 2

    repo_dir = args.directory.resolve()
    if not (repo_dir / ".git").exists():
        print(f"Not a git repository: {repo_dir}", file=sys.stderr)
        return 2

    ensure_clean_or_allowed(repo_dir, args.allow_dirty)

    try:
        created = create_repo(token, repo_name, args.private, args.description)
        print(f"Created GitHub repository: {created.get('html_url')}")
    except urllib.error.HTTPError as exc:
        if exc.code == 422 and args.allow_existing and repo_exists(token, username, repo_name):
            print(f"Repository already exists: https://github.com/{username}/{repo_name}")
        else:
            error_body = exc.read().decode("utf-8", errors="replace")
            print(f"GitHub API error ({exc.code}): {error_body}", file=sys.stderr)
            return 1

    remote_url = configure_remote(repo_dir, username, repo_name, args.remote)
    print(f"Configured remote {args.remote}: {remote_url}")
    print(f"Pushing HEAD to {args.remote}/{args.branch}...")
    try:
        push_repo(repo_dir, token, args.remote, args.branch)
    except subprocess.CalledProcessError as exc:
        print(
            f"Git push failed with exit code {exc.returncode}. "
            "Check that the token has repository write access and is not expired or revoked.",
            file=sys.stderr,
        )
        return exc.returncode

    print(f"Done: https://github.com/{username}/{repo_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
