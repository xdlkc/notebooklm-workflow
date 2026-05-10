#!/usr/bin/env python3
"""Plan and optionally upload local book files into NotebookLM notebooks."""

from __future__ import annotations

import argparse
import json
import mimetypes
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".docx"}
DEFAULT_READY_TIMEOUT = 900


@dataclass
class BookGroup:
    title: str
    files: list[Path]
    notebook_id: str | None = None

    def to_json(self, root: Path) -> dict:
        return {
            "title": self.title,
            "notebook_id": self.notebook_id,
            "files": [str(path.relative_to(root)) if path.is_relative_to(root) else str(path) for path in self.files],
        }


def natural_key(path: Path) -> list[object]:
    parts = re.split(r"(\d+)", path.name)
    return [int(part) if part.isdigit() else part.casefold() for part in parts]


def strip_outer_book_marks(value: str) -> str:
    value = value.strip()
    if value.startswith("《") and value.endswith("》"):
        return value[1:-1].strip()
    return value


def clean_title_from_filename(path: Path) -> str:
    stem = path.stem
    stem = re.sub(r"\[[^\]]*\]", "", stem)
    stem = re.sub(r"【[^】]*】", "", stem)
    stem = re.split(r"\s[-–—]\s", stem, maxsplit=1)[0]
    stem = strip_outer_book_marks(stem)
    stem = re.sub(r"\s+", " ", stem).strip()

    volume_patterns = [
        r"\s+(?:0?[1-9]|[1-9]\d{1,2})$",
        r"\s*第\s*[0-9一二三四五六七八九十百零〇]+\s*[卷册部輯辑集]$",
        r"\s+[上中下]\s*[卷册部]?$",
    ]
    for pattern in volume_patterns:
        new_stem = re.sub(pattern, "", stem).strip()
        if new_stem != stem and new_stem:
            stem = new_stem
            break

    return f"《{stem}》"


def discover_files(root: Path, recursive: bool = False) -> list[Path]:
    iterator = root.rglob("*") if recursive else root.iterdir()
    files = [
        path
        for path in iterator
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(files, key=natural_key)


def plan_books(root: Path, recursive: bool = False) -> list[BookGroup]:
    groups: dict[str, list[Path]] = {}
    for path in discover_files(root, recursive=recursive):
        title = clean_title_from_filename(path)
        groups.setdefault(title, []).append(path)
    return [BookGroup(title=title, files=files) for title, files in sorted(groups.items())]


def run_command(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True)


def parse_json_output(stdout: str) -> dict:
    text = stdout.strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end >= start:
            return json.loads(text[start : end + 1])
        raise


def notebook_id_from_create_output(data: dict) -> str | None:
    if data.get("id"):
        return data["id"]
    if data.get("notebook_id"):
        return data["notebook_id"]
    notebook = data.get("notebook")
    if isinstance(notebook, dict):
        return notebook.get("id")
    return None


def resolve_newest_notebook_id(title: str, cwd: Path) -> str:
    proc = run_command(["notebooklm", "list", "--json"], cwd)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "notebooklm list failed")
    data = parse_json_output(proc.stdout)
    matches = [nb for nb in data.get("notebooks", []) if nb.get("title") == title]
    if not matches:
        raise RuntimeError(f"Created notebook not found by title: {title}")
    return matches[0]["id"]


def create_notebook(title: str, cwd: Path) -> str:
    proc = run_command(["notebooklm", "create", title, "--json"], cwd)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"notebooklm create failed for {title}")
    data = parse_json_output(proc.stdout)
    return notebook_id_from_create_output(data) or resolve_newest_notebook_id(title, cwd)


def add_source(notebook_id: str, path: Path, cwd: Path) -> str | None:
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    proc = run_command(
        [
            "notebooklm",
            "source",
            "add",
            str(path),
            "--type",
            "file",
            "--mime-type",
            mime_type,
            "-n",
            notebook_id,
            "--json",
        ],
        cwd,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"source add failed for {path}")
    data = parse_json_output(proc.stdout)
    source = data.get("source", data)
    return source.get("id") or source.get("source_id")


def list_sources(notebook_id: str, cwd: Path) -> list[dict]:
    proc = run_command(["notebooklm", "source", "list", "-n", notebook_id, "--json"], cwd)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"source list failed for {notebook_id}")
    return parse_json_output(proc.stdout).get("sources", [])


def wait_until_ready(notebook_id: str, expected_count: int, cwd: Path, timeout: int) -> list[dict]:
    deadline = time.monotonic() + timeout
    last_sources: list[dict] = []
    while time.monotonic() < deadline:
        last_sources = list_sources(notebook_id, cwd)
        if len(last_sources) >= expected_count:
            statuses = [source.get("status") for source in last_sources]
            if all(status == "ready" for status in statuses):
                return last_sources
            if any(status == "error" for status in statuses):
                return last_sources
        time.sleep(15)
    return last_sources


def print_markdown_plan(groups: list[BookGroup], root: Path) -> None:
    print(f"Input: {root}")
    print(f"Notebook count: {len(groups)}")
    print(f"Source count: {sum(len(group.files) for group in groups)}")
    for group in groups:
        print(f"\n- {group.title}")
        for path in group.files:
            print(f"  - {path.relative_to(root) if path.is_relative_to(root) else path}")


def execute(groups: list[BookGroup], root: Path, wait_ready: bool, timeout: int) -> int:
    failures: list[str] = []
    for index, group in enumerate(groups, 1):
        print(f"[{index}/{len(groups)}] create {group.title}", flush=True)
        try:
            group.notebook_id = create_notebook(group.title, root)
            print(f"  notebook_id={group.notebook_id}", flush=True)
            for file_index, path in enumerate(group.files, 1):
                print(f"  [{file_index}/{len(group.files)}] upload {path.name}", flush=True)
                source_id = add_source(group.notebook_id, path, root)
                print(f"    source_id={source_id}", flush=True)
            if wait_ready:
                sources = wait_until_ready(group.notebook_id, len(group.files), root, timeout)
                statuses = ",".join(str(source.get("status")) for source in sources)
                print(f"  statuses={statuses}", flush=True)
                if len(sources) != len(group.files) or any(source.get("status") != "ready" for source in sources):
                    failures.append(f"{group.title}: expected ready sources, got {statuses}")
        except Exception as exc:
            failures.append(f"{group.title}: {exc}")
            print(f"  ERROR {exc}", file=sys.stderr, flush=True)

    if failures:
        print("Failures:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan or upload local book files to NotebookLM.")
    parser.add_argument("--input", "-i", type=Path, default=Path.cwd(), help="Directory containing book files.")
    parser.add_argument("--recursive", action="store_true", help="Scan subdirectories too.")
    parser.add_argument("--json", action="store_true", help="Print the plan as JSON.")
    parser.add_argument("--execute", action="store_true", help="Create notebooks and upload sources.")
    parser.add_argument("--wait-ready", action="store_true", help="After upload, wait until sources are ready.")
    parser.add_argument("--ready-timeout", type=int, default=DEFAULT_READY_TIMEOUT)
    args = parser.parse_args(argv)

    root = args.input.expanduser().resolve()
    if not root.is_dir():
        print(f"Input directory not found: {root}", file=sys.stderr)
        return 2

    groups = plan_books(root, recursive=args.recursive)
    if args.json:
        print(json.dumps({"input": str(root), "groups": [group.to_json(root) for group in groups]}, ensure_ascii=False, indent=2))
    else:
        print_markdown_plan(groups, root)

    if not args.execute:
        return 0
    if not groups:
        print("No supported book files found.", file=sys.stderr)
        return 1
    return execute(groups, root, wait_ready=args.wait_ready, timeout=args.ready_timeout)


if __name__ == "__main__":
    raise SystemExit(main())
