#!/usr/bin/env python3
"""Collect blog/article URLs and lastmod dates from a sitemap.

Outputs JSON by default:
{
  "source": "https://example.com/sitemap.xml",
  "count": 123,
  "urls": [{"url": "...", "lastmod": "YYYY-MM-DD"}, ...]
}
"""
import argparse
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import urlparse


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def text_of(node, name: str):
    child = node.find(f"{{*}}{name}")
    return child.text.strip() if child is not None and child.text else None


def parse_sitemap(xml_text: str):
    root = ET.fromstring(xml_text)
    tag = root.tag.rsplit("}", 1)[-1]
    if tag == "sitemapindex":
        return {"sitemaps": [text_of(n, "loc") for n in root.findall(".//{*}sitemap") if text_of(n, "loc")]}
    if tag != "urlset":
        raise SystemExit(f"Unsupported sitemap root: {root.tag}")
    rows = []
    for n in root.findall(".//{*}url"):
        loc = text_of(n, "loc")
        if not loc:
            continue
        lm = text_of(n, "lastmod")
        rows.append({"url": loc, "lastmod": lm[:10] if lm else None})
    return {"urls": rows}


def include_url(url: str, prefixes, exclude_landing: bool, regex):
    parsed = urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    if prefixes:
        ok = False
        for p in prefixes:
            p = p.rstrip("/") or "/"
            if exclude_landing:
                ok = ok or path.startswith(p + "/")
            else:
                ok = ok or path == p or path.startswith(p + "/")
        if not ok:
            return False
    if regex and not re.search(regex, url):
        return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sitemap", help="Sitemap URL, e.g. https://www.anthropic.com/sitemap.xml")
    ap.add_argument("--prefix", action="append", default=[], help="Path prefix to include, e.g. /news. Repeatable.")
    ap.add_argument("--exclude-landing", action="store_true", help="Exclude exact landing pages like /news while keeping /news/post.")
    ap.add_argument("--regex", help="Optional regex that the full URL must match.")
    ap.add_argument("--out", help="Write JSON output to this path instead of stdout.")
    ap.add_argument("--md", help="Also write a Markdown URL list to this path.")
    args = ap.parse_args()

    pending = [args.sitemap]
    rows = []
    seen = set()
    while pending:
        sm = pending.pop(0)
        parsed = parse_sitemap(fetch(sm))
        for child in parsed.get("sitemaps", []):
            pending.append(child)
        for r in parsed.get("urls", []):
            u = r["url"]
            if u in seen or not include_url(u, args.prefix, args.exclude_landing, args.regex):
                continue
            seen.add(u)
            rows.append(r)

    rows.sort(key=lambda r: (r.get("url") or ""))
    data = {"source": args.sitemap, "count": len(rows), "urls": rows}
    s = json.dumps(data, ensure_ascii=False, indent=2)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(s + "\n")
    else:
        print(s)
    if args.md:
        lines = [f"# URLs from {args.sitemap}", "", f"Count: {len(rows)}", ""]
        for r in rows:
            prefix = f"{r['lastmod']} " if r.get("lastmod") else ""
            lines.append(f"- {prefix}{r['url']}")
        open(args.md, "w", encoding="utf-8").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
