---
name: zlibrary-cli
description: "Use when installing, configuring, testing, using, or troubleshooting the heartleo/zlib command-line client for Z-Library: Homebrew/Go installation, default/custom domain handling, login/session cookies, proxy setup, search/download/profile/history commands, Kindle delivery, and diagnosing network/auth failures. Also use when comparing Z-Library CLI tools or explaining how heartleo/zlib works."
---

# Z-Library CLI

Use this skill for the `heartleo/zlib` CLI, whose executable is `zlib`. Keep copyright/compliance boundaries explicit: assist only with public-domain, open-license, owned, or otherwise authorized books; do not help bypass access controls, captchas, quotas, or copyright restrictions.

## Quick facts

- Repo: `https://github.com/heartleo/zlib`
- Installed executable: `zlib`
- Homebrew install: `brew install heartleo/tap/zlib`
- Go install: `go install github.com/heartleo/zlib/cmd/zlib@latest` requires Go 1.25+
- Default domain in source: `https://z-lib.sk`
- Onion domain in source: `http://bookszlibb74ugqojhzhg2a63w5i2atv5bqarulgczawnbmsb6s6qead.onion`
- Login endpoint is `<domain>/rpc.php`
- Session file: `~/.config/zlib/session.json`
- Working-directory `.env` variables are loaded before command execution.

## Verify/install

Check before installing:

```bash
command -v zlib || true
zlib version 2>/dev/null || true
brew list heartleo/tap/zlib 2>/dev/null || true
```

Install on this user's macOS/Linux Homebrew setup:

```bash
brew install heartleo/tap/zlib
zlib version
zlib --help
```

If Homebrew is unavailable, use the upstream install script or Go install only after checking the README/current releases.

## Configuration

Set variables inline, in shell profile, or in a `.env` in the current working directory:

```bash
ZLIB_DOMAIN=https://z-lib.sk
ZLIB_PROXY=http://127.0.0.1:7890
ZLIB_THEME=nord
ZLIB_SMTP_PWD='smtp-app-password'
```

`ZLIB_DOMAIN` overrides the default domain and trailing slashes are trimmed. `ZLIB_PROXY` accepts standard proxy URLs and is useful when the domain is blocked or when using the onion domain via a Tor SOCKS proxy.

## Login workflow

Run interactive login:

```bash
zlib login
```

Or non-interactive login only when the user explicitly provides credentials:

```bash
zlib login --email 'user@example.com' --password 'secret'
```

Implementation details to remember when troubleshooting:

1. `zlib login` posts form data to `<domain>/rpc.php`.
2. The form includes `email`, `password`, `site_mode=books`, `action=login`, `isSingleLogin=1`, and `gg_json_mode=1`.
3. The response is JSON; non-null `response.validationError` means login failed.
4. On success, cookies are extracted from the HTTP cookie jar and saved with the active domain to `~/.config/zlib/session.json` mode 0600.
5. Later commands load the saved cookies and add them to requests.

The tool does not solve CAPTCHA, Cloudflare/browser JS challenges, 2FA, or other human-verification flows. If login fails because of these, advise browser/manual resolution or wait/use an authorized accessible domain; do not provide bypass instructions.

## Common commands

```bash
zlib profile
zlib search 'query'
zlib search 'query' --page 2 --count 20
zlib search 'query' --ext epub --ext pdf
zlib download BOOK_ID --dir ./books
zlib history
zlib logout
zlib theme
zlib kindle
```

Use `zlib <command> --help` for current flags because CLI options may change.

## Non-interactive downloads

`zlib download BOOK_ID --dir DIR` is Bubble Tea/TUI-based and may fail in agent, CI, or non-TTY execution with:

```text
could not open a new TTY: open /dev/tty: device not configured
```

When the user is authorized to download the book and the normal command fails this way, use the bundled non-interactive Go helper instead. It reads `~/.config/zlib/session.json`, fetches the book detail page, and calls the same `github.com/heartleo/zlib` download API without opening `/dev/tty`:

```bash
mkdir -p "$HOME/Downloads/books"
cd /tmp
if [ ! -f go.mod ]; then go mod init zlib-noninteractive-download >/dev/null 2>&1; fi
go get github.com/heartleo/zlib@latest >/dev/null
go run /Users/lkc/.hermes/skills/zlibrary-cli/scripts/noninteractive_download.go BOOK_ID "$HOME/Downloads/books"
```

The helper prints the saved file path and byte count. Verify the file exists and has the expected extension/size before reporting completion. Do not print or inspect cookie values from the session file.

## Troubleshooting checklist

1. Confirm installation and PATH:
   ```bash
   command -v zlib && zlib version
   ```
2. Confirm login state:
   ```bash
   test -f ~/.config/zlib/session.json && python3 -m json.tool ~/.config/zlib/session.json >/dev/null
   zlib profile
   ```
3. If it says `Not logged in. Run: zlib login`, login again.
4. If network fails, try a reachable domain and/or proxy:
   ```bash
   ZLIB_DOMAIN=https://z-lib.sk ZLIB_PROXY=http://127.0.0.1:7890 zlib profile
   ```
5. If a domain changed, inspect the upstream README/source before assuming old values:
   ```bash
   git clone --depth 1 https://github.com/heartleo/zlib /tmp/zlib-heartleo
   grep -RIn 'DefaultDomain\|ZLIB_DOMAIN\|rpc.php' /tmp/zlib-heartleo
   ```
6. If cookies look stale, run `zlib logout` then `zlib login`.
7. Avoid printing or sharing `~/.config/zlib/session.json` values; they are bearer-like session secrets.

## User-specific note

This machine already had `heartleo/zlib` installed via Homebrew at `/usr/local/bin/zlib` and verified as `zlib version 0.0.2` during creation of this skill. Re-check with live commands instead of relying on this note if time has passed.
