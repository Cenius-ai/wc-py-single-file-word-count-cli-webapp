# Installing and running wc-py

This is the source of truth for getting the tool running on a fresh machine.
Follow the steps in order; each one is copy-pasteable and none of them needs
`sudo`.

## Prerequisites (install these yourself, once)

wc-py does not install system software and never requires privileges. On the
target machine you need:

| Prerequisite | Why | Check |
| --- | --- | --- |
| Python 3.8 or newer | Runs `wc.py` | `python3 --version` |
| `bash` 3.2+ | Runs `install.sh` and `demo.sh`. The tool itself needs only Python | `bash --version` |
| `pip` (bundled with Python 3) | Installs the optional test runner | `python3 -m pip --version` |

There is nothing else to provision: no database, no message broker, no system
service, no compiler, no GPU. The tool is one standard-library file.

## Step 1 — Get the code

```bash
git clone <this repo> wc-py
cd wc-py
```

## Step 2 — Install project dependencies (optional)

Skip this step entirely if you only want to count words — `python3 wc.py file`
works on a bare Python install. Run it when you want the `wc-py` console
script on your `PATH` and the test runner available.

```bash
bash install.sh
```

`install.sh` uses the single package manager for this project: `pip` (through
`python3 -m pip`), driven by `requirements.txt`. It:

1. upgrades `pip`/`setuptools`/`wheel`,
2. installs the declared dependencies (`requirements.txt` — the test runner),
3. installs the local package in editable mode, which puts the `wc-py`
   console script on your `PATH`,
4. verifies that `wc.py` imports and counts a shipped example file,
5. prints the next commands and **exits**.

It installs into the active Python environment only; nothing is written outside
the project and the environment's `site-packages`. It is idempotent — re-running
it is safe. The script never installs system packages and never starts a
long-running process:

```bash
# correct: the setup script returns
bash install.sh && echo "setup finished"

# wrong (not what install.sh does): leaving a foreground process running
```

If you prefer an isolated interpreter, create the environment first and let the
script use it:

```bash
python3 -m venv .venv && . .venv/bin/activate
bash install.sh
```

## Step 3 — Prepare demo input

There is no datastore to migrate and no seed command: wc-py is stateless and
reads the file you hand it. Three example inputs ship with the project so the
tool has something real to count immediately:

| File | Words | Purpose |
| --- | --- | --- |
| `examples/notes.txt` | 12 | the plan's 12-word acceptance fixture |
| `examples/article.txt` | 189 | a realistic multi-paragraph file |
| `examples/empty.txt` | 0 | the zero-word branch |

Verify the fixture before you rely on it:

```bash
python3 wc.py examples/notes.txt   # prints 12
```

## Step 4 — Run it

```bash
python3 wc.py examples/notes.txt       # 12
wc-py examples/notes.txt               # 12 (after step 2)
python3 wc.py --help
```

The tool prints the integer on stdout, every error on stderr, and returns the
exit codes documented in the README (`0` counted, `1` file error, `2` usage
error).

## Step 5 — Run the demo

```bash
bash demo.sh
```

Non-interactive end-to-end recording of the tool: counts, both failure modes,
help, and the test suite. Exits `0` when every check matches. `NO_COLOR=1 bash
demo.sh` produces the same output without colour.

## Step 6 — Run the tests

```bash
python3 -m pytest        # or: python3 -m unittest -v
```

Both runners execute the same 25 tests. The suite needs no network and touches
no external service; it writes only into temporary directories it cleans up.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `python3: command not found` | No interpreter on `PATH` | Install Python 3.8+ with your platform's tooling, then reopen the shell |
| `wc-py: command not found` | Step 2 was skipped, or the environment's `bin` is not on `PATH` | Run `bash install.sh`, or just use `python3 wc.py` |
| `file not found: x.txt` | Wrong path, or a path relative to another directory | Check the path; wc.py resolves it relative to your shell's working directory |
| `not a file: docs` | A directory was passed | Point the tool at a file; directories and globs are out of scope |
| `not UTF-8 text: x.bin` | The file is not decodable as UTF-8 | This tool reads UTF-8; convert the file first (`iconv -f latin1 -t utf-8`) |

## Uninstall

```bash
python3 -m pip uninstall wc-py   # removes the console script
```

Then delete the project directory. The tool keeps no state, so there is nothing
else to clean up.
