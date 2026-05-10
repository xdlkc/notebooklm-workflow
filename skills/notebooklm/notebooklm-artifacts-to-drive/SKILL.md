---
name: notebooklm-artifacts-to-drive
description: Upload NotebookLM-generated artifacts (slide decks, reports, audio, video, images, data tables, quizzes, flashcards, etc.) to Google Drive using the required folder structure NotebookLM/notebook-name/artifact-file. Use when delivering NotebookLM outputs, when Feishu/Lark or chat attachments may fail due to size limits, or when the user asks to put NotebookLM note/notebook products into Google Drive.
---

# NotebookLM Artifacts to Google Drive

Use this skill to deliver NotebookLM outputs through Google Drive instead of chat attachments. Always organize uploaded files as:

```text
NotebookLM/<notebook name>/<artifact file>
```

## Core rules

- This skill is for delivery/upload. If artifacts still need to be generated or regenerated for quality, first use `notebooklm-studio-quality-prompts` to create artifact-specific prompts for slide decks, reports, mind maps, infographics, data tables, quizzes, flashcards, audio, and video.
- Prefer Google Drive links for NotebookLM artifacts, especially PPTX/audio/video or files larger than chat upload limits.
- Upload the original artifact when possible; only upload compressed copies if the user explicitly wants a smaller file.
- Do not print OAuth tokens, client secrets, cookies, or credential JSON.
- If NotebookLM CLI reports auth problems with the default home, set `NOTEBOOKLM_HOME` to the authenticated profile root for the current machine (commonly `$HOME/.notebooklm/profiles/default`) and verify with `notebooklm list --json`. Do not hard-code another user's home directory.
- Use `gws` for Drive upload when available; verify `gws auth status` before upload.

## Workflow

### 1. Identify notebook name and artifact file

If a NotebookLM notebook ID is known, get the exact title from `notebooklm list --json`:

```bash
export NOTEBOOKLM_HOME="$HOME/.notebooklm/profiles/default"  # optional: adjust to your authenticated profile root
notebooklm list --json > /tmp/notebooklm_list.json
python3 - <<'PY'
import json
nb_id='<FULL_NOTEBOOK_UUID>'
data=json.load(open('/tmp/notebooklm_list.json'))
for n in data.get('notebooks', []):
    if n.get('id') == nb_id:
        print(n.get('title') or nb_id)
        break
PY
```

If only the current context is known, use `notebooklm status` or `notebooklm artifact list --json` as needed, but prefer a full UUID and exact title.

### 2. Verify Google Drive auth

```bash
command -v gws
gws auth status
```

Continue only if `token_valid` is true and Drive scope is present. If not authenticated, load/use the `google-workspace` skill and complete Drive OAuth.

### 3. Create/find Drive folders

Create or reuse the root folder `NotebookLM`, then create or reuse a child folder named after the notebook.

```bash
ROOT_ID=$(gws drive files list \
  --params '{"q":"mimeType=\"application/vnd.google-apps.folder\" and name=\"NotebookLM\" and trashed=false","fields":"files(id,name)"}' \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); fs=d.get("files",[]); print(fs[0]["id"] if fs else "")')

if [ -z "$ROOT_ID" ]; then
  ROOT_ID=$(gws drive files create \
    --params '{"fields":"id,name"}' \
    --json '{"name":"NotebookLM","mimeType":"application/vnd.google-apps.folder"}' \
    | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
fi

export ROOT_ID
export NOTEBOOK_NAME='<NOTEBOOK_TITLE>'
CHILD_Q=$(python3 - <<'PY'
import json, os
name=os.environ['NOTEBOOK_NAME']
root=os.environ['ROOT_ID']
print(json.dumps({
  "q": f"mimeType='application/vnd.google-apps.folder' and name='{name.replace(chr(39), chr(92)+chr(39))}' and '{root}' in parents and trashed=false",
  "fields": "files(id,name)"
}, ensure_ascii=False))
PY
)

NOTEBOOK_FOLDER_ID=$(gws drive files list --params "$CHILD_Q" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); fs=d.get("files",[]); print(fs[0]["id"] if fs else "")')

if [ -z "$NOTEBOOK_FOLDER_ID" ]; then
  BODY=$(python3 - <<'PY'
import json, os
print(json.dumps({
  "name": os.environ['NOTEBOOK_NAME'],
  "mimeType": "application/vnd.google-apps.folder",
  "parents": [os.environ['ROOT_ID']]
}, ensure_ascii=False))
PY
)
  NOTEBOOK_FOLDER_ID=$(gws drive files create --params '{"fields":"id,name"}' --json "$BODY" \
    | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
fi
```

For names containing quotes or unusual characters, prefer a short Python helper over hand-written shell quoting.

### 4. Upload artifact into the notebook folder

Avoid `gws --upload /absolute/path` path validation problems by `cd`-ing into the file directory and passing a relative filename.

```bash
export ARTIFACT_PATH='/absolute/path/to/artifact.pptx'
export ARTIFACT_NAME='artifact.pptx'
export MIME='application/vnd.openxmlformats-officedocument.presentationml.presentation'
export NOTEBOOK_FOLDER_ID

cd "$(dirname "$ARTIFACT_PATH")"
BODY=$(python3 - <<'PY'
import json, os
print(json.dumps({
  "name": os.environ.get('ARTIFACT_NAME') or os.path.basename(os.environ['ARTIFACT_PATH']),
  "parents": [os.environ['NOTEBOOK_FOLDER_ID']]
}, ensure_ascii=False))
PY
)

gws drive files create \
  --params '{"fields":"id,name,size,mimeType,webViewLink,webContentLink"}' \
  --json "$BODY" \
  --upload "$(basename "$ARTIFACT_PATH")" \
  --upload-content-type "$MIME" \
  > /tmp/notebooklm_drive_upload.json
```

Common MIME types:

| Extension | MIME |
|---|---|
| `.pptx` | `application/vnd.openxmlformats-officedocument.presentationml.presentation` |
| `.pdf` | `application/pdf` |
| `.mp3` | `audio/mpeg` |
| `.mp4` | `video/mp4` |
| `.png` | `image/png` |
| `.jpg` / `.jpeg` | `image/jpeg` |
| `.md` | `text/markdown` |
| `.csv` | `text/csv` |
| `.json` | `application/json` |

### 5. Share and verify link when delivering to user

If the user needs to open the file from chat, set link sharing and verify metadata:

```bash
FILE_ID=$(python3 -c 'import json; print(json.load(open("/tmp/notebooklm_drive_upload.json"))["id"])')

gws drive permissions create \
  --params "{\"fileId\":\"$FILE_ID\",\"fields\":\"id\"}" \
  --json '{"role":"reader","type":"anyone"}'

gws drive files get \
  --params "{\"fileId\":\"$FILE_ID\",\"fields\":\"id,name,size,mimeType,webViewLink,webContentLink,parents,permissions(id,type,role)\"}" \
  > /tmp/notebooklm_drive_verify.json
```

Report the `webViewLink` and note the folder path `NotebookLM/<notebook name>/<artifact file>`.

## Pitfalls

- Feishu/Lark attachment delivery may silently fail or reject large PPTX files. Do not keep retrying the same `MEDIA:` attachment; upload to Drive instead.
- `gws drive permissions create` must include the full service path `drive permissions create`; `gws permissions create` is invalid.
- `gws drive files create --upload` may reject absolute paths that resolve outside the current directory; `cd` into the file directory and upload by basename.
- NotebookLM PPTX exports may be large image-based decks. Keep the original on Drive and optionally provide a compressed chat copy only as a convenience.
- If `gws drive files create --upload` hangs, times out, or the surrounding background process is killed (for example exit code `-15`) during a large PPTX/PDF/video upload, do **not** assume upload failure. First inspect the working directory logs/partial JSON and list the target Drive folder by parent ID/name; the bytes may already be uploaded and only the final summary file may be missing. Reuse matching existing files by name+size, set/verify `anyone` reader permission, and then write a clean `drive_uploads.json` summary.
- If the file already exists elsewhere in Drive, use `gws drive files copy --params '{"fileId":"SOURCE_ID","fields":"id,name,size,mimeType,webViewLink,parents"}' --json '{"name":"TARGET_NAME","parents":["TARGET_FOLDER_ID"]}'` instead of re-uploading bytes.
- `gws` may print non-JSON log lines such as `Using keyring backend: keyring` before the JSON response. When scripting uploads, do not call `json.loads(stdout)` directly; extract the JSON object between the first `{` and last `}` or filter logs before parsing. Also avoid accidental shell redirection mistakes such as `python3 - <<'PY' > helper.py` when you meant to write a Python helper file; that executes Python and redirects its output into `helper.py`, overwriting the script with logs/output. Use `cat > helper.py <<'PY'` to create the helper, then run it separately.
- Large MP4 uploads can fail with `connection reset by peer` even after a background retry. If the original video is not essential or cannot be copied from an existing Drive file, create a smaller review/delivery copy with ffmpeg, label it clearly as compressed, then upload that file:
  ```bash
  ffmpeg -y -i input.mp4 -vf 'scale=854:-2' -c:v libx264 -preset veryfast -crf 32 -c:a aac -b:a 64k -movflags +faststart output_compressed.mp4
  ```
  Keep the original local file path in case the user later requests full quality.
- Always verify the uploaded file size and sharing permissions before claiming delivery succeeded.
