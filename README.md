# wc-py — single-file word count CLI — complete Full-stack app command-line tool example app

**wc-py — single-file word count CLI** is a free, open-source command-line tool written in Full-stack app. Build a plain-Python, single-file command-line tool (wc.py) that takes one file path, counts whitespace-separated words, and prints the total. Every wc-py — single-file word count CLI file — code, design, seeded demo data — ships in this repository under the Apache-2.0 license. Self-host it, or [remix wc-py — single-file word count CLI on cenius.ai](https://cenius.ai/marketplace/p/wc-py-single-file-word-count-cli?ref=gh&utm_campaign=wc-py-single-file-word-count-cli-webapp) to get a custom build with full rebrand rights.


[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE) ![Stack](https://img.shields.io/badge/Stack-Full--stack%20app-3b82f6) [![Built with cenius.ai](https://img.shields.io/badge/Built%20with-cenius.ai-8b5cf6)](https://cenius.ai)

[![Open in cenius.ai](https://img.shields.io/badge/▶%20Open%20%26%20edit%20in-cenius.ai-8b5cf6?style=for-the-badge)](https://cenius.ai/marketplace/p/wc-py-single-file-word-count-cli?ref=gh&utm_campaign=wc-py-single-file-word-count-cli-webapp)

> **▶ [Open & edit in cenius.ai](https://cenius.ai/marketplace/p/wc-py-single-file-word-count-cli?ref=gh&utm_campaign=wc-py-single-file-word-count-cli-webapp)** — one click to an editable workspace: describe changes in plain English, get an instant preview, one-click deploy and host. Modifications made on the platform come with full rebrand & relicense rights.

_Local clone? See [Quick start](#quick-start) below. cenius.ai is the zero-setup path._

## Demo

![wc-py — single-file word count CLI demo — command-line tool built with Full-stack app](.github/media/hero.gif)

▶ **[Watch the full demo video](https://cenius.ai/marketplace/p/wc-py-single-file-word-count-cli?ref=gh&utm_campaign=wc-py-single-file-word-count-cli-webapp)** — the complete walkthrough, playing on the project's cenius.ai page · [MP4 file](.github/media/demo.mp4)

## Quick start

```bash
./install.sh   # installs dependencies + seeds demo data
```

See [`INSTALL.md`](INSTALL.md) for full setup and usage instructions.

## Usage guide

Practical walkthroughs of the features that actually exist. Every command below
can be pasted into a shell from the project root.

### 1. Count the words in a file

```console
$ python3 wc.py examples/notes.txt
12
```

One path in, one integer out. stdout carries the number and nothing else, so
the output drops straight into a pipe, a variable, or a comparison.

```console
$ python3 wc.py examples/article.txt
189

$ python3 wc.py examples/empty.txt
0
```

### 2. What counts as a word

A word is a whitespace-separated token — exactly `str.split()` semantics:

- spaces, tabs, newlines and other Unicode whitespace all separate words;
- runs of whitespace never produce empty words;
- leading and trailing whitespace is ignored;
- punctuation stays attached to the token it touches, so `by design.` is two
  words and a standalone `--` is one word;
- accented and non-Latin text counts normally, because the file is read as
  UTF-8.

```console
$ printf 'alpha beta\n\n  gamma\tdelta\n' > /tmp/wc-py-whitespace.txt
$ python3 wc.py /tmp/wc-py-whitespace.txt
4
```

### 3. Scripting it

Because the count is the only thing on stdout and failures are non-zero, the
tool composes with ordinary shell logic:

```bash
## Fail a docs build when a page grows past its budget
words=$(python3 wc.py docs/guide.md)
if [ "$words" -gt 800 ]; then
  echo "docs/guide.md is $words words (budget 800)" >&2
  exit 1
fi

_Full guide: [`USAGE.md`](USAGE.md)_

## Features

- Count words in a file
- Usage and error handling

## Architecture

Everything runs out of the box: a Full-stack app codebase (24 files). `install.sh` wires up dependencies and loads seed records; after it runs the app has real data to show. Top-level layout: `examples/`. Full setup details: [`INSTALL.md`](INSTALL.md).

## FAQ

### How do I self-host wc-py — single-file word count CLI?

Clone this repository and run `./install.sh`, then start the app as described in [`INSTALL.md`](INSTALL.md). wc-py — single-file word count CLI is fully self-hostable — no external services are required to try it.

### Is it OK to ship wc-py — single-file word count CLI as part of a product?

It is. Apache-2.0 licensing means you can build a product on it, sell it, or use it inside a company with no fees. Details: [LICENSE](LICENSE).

### How do I customise wc-py — single-file word count CLI's branding?

Absolutely. [Open it on cenius.ai](https://cenius.ai/marketplace/p/wc-py-single-file-word-count-cli?ref=gh&utm_campaign=wc-py-single-file-word-count-cli-webapp) and remix it there — platform modifications come with full rebrand and relicense rights over your derivative, so the result is entirely yours.

### What if I want to add features to wc-py — single-file word count CLI without coding?

[cenius.ai](https://cenius.ai/marketplace/p/wc-py-single-file-word-count-cli?ref=gh&utm_campaign=wc-py-single-file-word-count-cli-webapp) handles the implementation. Tell it what you want in everyday words, pick up the updated build. No coding needed.

### How is wc-py — single-file word count CLI built technically?

wc-py — single-file word count CLI runs on Full-stack app. This repo holds the full production source: you can inspect every part of it before deploying. Highlights include count words in a file.

## License & rebranding

Released under the [Apache License 2.0](LICENSE) (© 2026 Cenius AI) — free for personal and commercial use. The Cenius name/logo are trademarks (see NOTICE).

**Need a customized version?** [Remix this app on cenius.ai](https://cenius.ai/marketplace/p/wc-py-single-file-word-count-cli?ref=gh&utm_campaign=wc-py-single-file-word-count-cli-webapp) — modifications made on the platform come with **full rebrand & relicense rights** over your derivative.

## Built with cenius.ai

This entire application — code, design, seeded demo data — was generated on **[cenius.ai](https://cenius.ai)** from a plain-English description.

- 🚀 [Build your own app on cenius.ai](https://cenius.ai)
- 🎛️ [Remix wc-py — single-file word count CLI on the marketplace](https://cenius.ai/marketplace/p/wc-py-single-file-word-count-cli?ref=gh&utm_campaign=wc-py-single-file-word-count-cli-webapp) — open it in a workspace, prompt for changes, and ship your own version.

More open-source apps: [the Cenius-ai catalog](https://github.com/Cenius-ai) · [showcase index](https://github.com/Cenius-ai/showcase)
