#!/usr/bin/env python3
"""Explicit account switcher for heartleo/zlib sessions.

This helper manages named copies of ~/.config/zlib/session.json. It does not
log in, create accounts, or automatically rotate accounts to bypass quotas.
Use it to save the session you are currently logged in with, switch to a named
session explicitly, and run `zlib profile` for the active account.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_CONFIG_DIR = Path.home() / ".config" / "zlib"
ACCOUNT_NAME_RE = re.compile(r"^[A-Za-z0-9_.-]+$")


def config_dir() -> Path:
    return Path(os.environ.get("ZLIB_CONFIG_DIR", DEFAULT_CONFIG_DIR)).expanduser()


def session_path() -> Path:
    return config_dir() / "session.json"


def accounts_dir() -> Path:
    return config_dir() / "accounts"


def active_path() -> Path:
    return config_dir() / "active_account"


def validate_account_name(name: str) -> str:
    if not ACCOUNT_NAME_RE.fullmatch(name):
        raise SystemExit(
            "Invalid account name. Use only letters, digits, dot, underscore, or hyphen."
        )
    if name in {".", ".."}:
        raise SystemExit("Invalid account name.")
    return name


def account_file(name: str) -> Path:
    return accounts_dir() / f"{validate_account_name(name)}.json"


def ensure_private_file(path: Path) -> None:
    try:
        path.chmod(0o600)
    except FileNotFoundError:
        raise
    except PermissionError:
        print(f"Warning: could not chmod 600 {path}", file=sys.stderr)


def validate_session_file(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Session file not found: {path}")
    if not path.is_file():
        raise SystemExit(f"Not a regular file: {path}")
    try:
        data = json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001 - report parse failure clearly
        raise SystemExit(f"Invalid JSON session file {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid session format in {path}: expected JSON object")
    # Upstream fields can change, so keep validation intentionally loose.
    if not data:
        raise SystemExit(f"Invalid session format in {path}: empty JSON object")


def save_account(name: str, overwrite: bool) -> None:
    src = session_path()
    dst = account_file(name)
    validate_session_file(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and not overwrite:
        raise SystemExit(f"Account already exists: {name}. Re-run with --overwrite to replace it.")
    shutil.copy2(src, dst)
    ensure_private_file(dst)
    active_path().write_text(validate_account_name(name) + "\n")
    print(f"Saved active zlib session as account: {name}")
    print(f"Stored at: {dst}")


def use_account(name: str) -> None:
    src = account_file(name)
    dst = session_path()
    validate_session_file(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    ensure_private_file(dst)
    active_path().write_text(validate_account_name(name) + "\n")
    print(f"Switched active zlib session to account: {name}")
    print("Run `zlib profile` to verify the active account and remaining quota.")


def list_accounts() -> None:
    root = accounts_dir()
    active = current_account(silent=True)
    if not root.exists():
        print("No saved zlib accounts.")
        return
    accounts = sorted(p.stem for p in root.glob("*.json") if p.is_file())
    if not accounts:
        print("No saved zlib accounts.")
        return
    for name in accounts:
        marker = "*" if name == active else " "
        print(f"{marker} {name}")


def current_account(silent: bool = False) -> str | None:
    path = active_path()
    name = path.read_text().strip() if path.exists() else ""
    if name and account_file(name).exists():
        if not silent:
            print(name)
        return name
    if not silent:
        print("No active account marker. Run `zlib_account.py save <name>` or `use <name>`.")
    return None


def remove_account(name: str) -> None:
    path = account_file(name)
    if not path.exists():
        raise SystemExit(f"Account not found: {name}")
    path.unlink()
    if active_path().exists() and active_path().read_text().strip() == name:
        active_path().unlink()
    print(f"Removed saved zlib account: {name}")


def run_profile() -> int:
    active = current_account(silent=True)
    if active:
        print(f"Active saved account: {active}")
    else:
        print("Active saved account: unknown")
    return subprocess.call(["zlib", "profile"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Manage named heartleo/zlib session files with explicit account switching."
    )
    parser.add_argument(
        "--config-dir",
        help="Override zlib config dir for this helper only. Defaults to ~/.config/zlib or ZLIB_CONFIG_DIR.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_save = sub.add_parser("save", help="Save current session.json as a named account")
    p_save.add_argument("name")
    p_save.add_argument("--overwrite", action="store_true", help="Replace an existing saved account")

    p_use = sub.add_parser("use", help="Switch active session.json to a saved account")
    p_use.add_argument("name")

    sub.add_parser("list", help="List saved accounts; * marks the active one")
    sub.add_parser("current", help="Print the active account marker")
    sub.add_parser("profile", help="Run `zlib profile` for the active session")

    p_remove = sub.add_parser("remove", help="Delete a saved account copy")
    p_remove.add_argument("name")

    args = parser.parse_args(argv)
    if args.config_dir:
        os.environ["ZLIB_CONFIG_DIR"] = args.config_dir

    if args.command == "save":
        save_account(args.name, args.overwrite)
    elif args.command == "use":
        use_account(args.name)
    elif args.command == "list":
        list_accounts()
    elif args.command == "current":
        current_account()
    elif args.command == "profile":
        return run_profile()
    elif args.command == "remove":
        remove_account(args.name)
    else:  # pragma: no cover
        parser.error(f"unknown command: {args.command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
