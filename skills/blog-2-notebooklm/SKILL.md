---
name: blog-2-notebooklm
description: Import official blog/article URLs from a website into Google NotebookLM as separate URL sources. Use when asked to crawl a blog, news, research, changelog, docs, topic/category page, or sitemap and create/populate NotebookLM notebooks; batch upload URLs; split across notebooks when source limits are reached; or rename NotebookLM sources with publication/lastmod dates.
---

# Blog to NotebookLM

Turn a site blog into one or more NotebookLM notebooks where each article URL is an independent source, not a single aggregated document.

## Core workflow

1. Verify NotebookLM auth:
   ```bash
   notebooklm status
   notebooklm list --json >/tmp/notebooklm_list_check.json
   ```
   If auth fails, run `notebooklm login`.

2. Discover URLs from the official sitemap when available. Use the helper script for standard sitemap parsing:
   ```bash
   BLOG_SKILL_DIR=${BLOG_SKILL_DIR:-skills/blog-2-notebooklm}
   python3 "$BLOG_SKILL_DIR/scripts/collect_sitemap_urls.py" \
     https://example.com/sitemap.xml \
     --prefix /blog --exclude-landing \
     --out /tmp/blog_urls.json --md /tmp/blog_urls.md
   ```
   For sites with multiple article sections, repeat `--prefix`, e.g. Anthropic uses `--prefix /news --prefix /research --prefix /engineering --exclude-landing`.

   If the user provides a topic/category landing page rather than a sitemap, scrape article card links from that page instead. Keep only links that are actual articles/examples (not topic nav pages), dedupe, and parse visible card dates when present. If any collected URL lacks a topic-card date, fetch the individual article page and extract `datePublished`, `article:published_time`, `dateModified`, or visible byline dates before uploading/renaming. Example pattern for an Astro/static page:
   ```python
   import html, pathlib, re, urllib.parse, json
   text = pathlib.Path('/tmp/topic.html').read_text(errors='replace')
   rows=[]; seen=set(); base='https://example.com'
   for m in re.finditer(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', text, re.S):
       href, inner = m.group(1), m.group(2)
       if not href.startswith('/cookbook/') or href.startswith('/cookbook/topic'):
           continue
       clean = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', inner))).strip()
       date = re.search(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}, \d{4}\b', clean)
       if not date:
           continue
       u = urllib.parse.urljoin(base, href).split('#')[0]
       if u in seen:
           continue
       seen.add(u)
       rows.append({'url': u, 'date_text': date.group(0), 'title_tags': clean[:clean.index(date.group(0))].strip()})
   pathlib.Path('/tmp/blog_urls.json').write_text(json.dumps({'urls': rows, 'count': len(rows)}, ensure_ascii=False, indent=2))
   ```

3. Create the first notebook:
   ```bash
   notebooklm create "<Site> official blog URLs" --json | tee /tmp/blog_notebook_1.json
   ```

4. Upload each URL as its own source. Do not upload a Markdown file containing all URLs unless the user explicitly asks for an index document.
   ```bash
   notebooklm source add "https://example.com/blog/post" -n <notebook_id> --json
   ```
   Use retries. If adds start failing near a source limit, create a continuation notebook and upload remaining URLs there.

5. Verify coverage:
   - For each notebook, run `notebooklm use <notebook_id>` then `notebooklm source list --json`.
   - Count ready sources whose `url` appears in the collected URL list.
   - Report total original URLs, covered ready URLs, missing URLs, and notebook IDs.

6. Always add date prefixes to source names when reliable dates are available. Treat `YYYY-MM-DD Original NotebookLM Title` as the default source title format for blog/article imports, not an optional cleanup step. Use sitemap `lastmod`, visible topic-card dates, or page metadata/text dates:
   ```bash
   notebooklm source rename <source_id> "YYYY-MM-DD <old title>" -n <notebook_id>
   ```
   Strip any existing `YYYY-MM-DD ` prefix first to avoid double prefixes. Verify every covered source title starts with the expected date and matches the expected URL date (`bad_prefix = 0`, `date_mismatch = 0`). If some URLs have no reliable date, leave those titles unchanged and report them explicitly.

## Automation patterns

### Upload loop skeleton

Use explicit notebook IDs for source add so background/parallel work cannot be confused by shared NotebookLM context:

```python
import json, pathlib, subprocess, time
nb = "<full-notebook-id>"
urls = [r["url"] for r in json.load(open("/tmp/blog_urls.json"))["urls"]]
for u in urls:
    ok = False
    for attempt in range(3):
        p = subprocess.run(["notebooklm", "source", "add", u, "-n", nb, "--json"], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
        if p.returncode == 0:
            ok = True
            break
        time.sleep(2 ** attempt + 1)
    if not ok:
        print("FAILED", u, p.stdout[-500:])
```

### Continuation notebooks

When a notebook reaches its source limit:

1. List ready URL sources in the current notebook.
2. Compute `remaining = collected_urls - ready_urls_across_all_notebooks`.
3. Create `"<title> 2"`, `"<title> 3"`, etc.
4. Upload remaining URLs into the continuation notebook.
5. Verify union coverage across all notebooks.

## Source naming

Default rename format:

```text
YYYY-MM-DD Original NotebookLM Title
```

Date source priority:

1. Sitemap `<lastmod>` date.
2. Visible topic/card date from category or topic landing pages.
3. Page metadata dates such as `datePublished`, `article:published_time`, or `dateModified`.
4. Page text/byline dates when metadata is absent.
5. No prefix if no reliable date is available; report these separately.

## Safety and cleanup

- Ask before deleting notebooks or sources. Delete is destructive.
- Do not silently hide failed/error sources; report them and ask whether to clean them up.
- Keep local artifacts in `/tmp` unless the user asks for a durable location.

## Reference

For NotebookLM command quirks and limits, see `references/notebooklm-cli-notes.md`.
