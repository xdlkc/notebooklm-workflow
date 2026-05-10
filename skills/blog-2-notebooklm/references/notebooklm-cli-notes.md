# NotebookLM CLI Notes for Blog Imports

- Authenticate before workflows: `notebooklm status` and `notebooklm list --json`; if needed run `notebooklm login`.
- If `notebooklm list` reports `AUTH_REQUIRED` while `~/.notebooklm/profiles/default/storage_state.json` exists, run commands with `NOTEBOOKLM_HOME=~/.notebooklm/profiles/default` so the CLI reads the migrated profile auth.
- Prefer explicit notebook IDs for automation: `notebooklm source add <url> -n <notebook_id> --json`.
- `source list` does not support `-n`; run `notebooklm use <notebook_id>` first, then `notebooklm source list --json`.
- `source rename` supports explicit notebooks: `notebooklm source rename <source_id> "YYYY-MM-DD Title" -n <notebook_id>`.
- NotebookLM source limits vary by plan. If adds begin failing near a round limit (commonly 300 ready sources), create a continuation notebook and upload remaining URLs there.
- Do not delete failed or duplicate sources without user approval. Deleting sources and notebooks is destructive.
- Google RPC failures can be transient. Retry source add/rename 2-3 times with short backoff before marking a URL failed.
