# Using wc-py

Practical walkthroughs of the features that actually exist. Every command below
can be pasted into a shell from the project root.

## 1. Count the words in a file

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

## 2. What counts as a word

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

## 3. Scripting it

Because the count is the only thing on stdout and failures are non-zero, the
tool composes with ordinary shell logic:

```bash
# Fail a docs build when a page grows past its budget
words=$(python3 wc.py docs/guide.md)
if [ "$words" -gt 800 ]; then
  echo "docs/guide.md is $words words (budget 800)" >&2
  exit 1
fi

# Total the words across a directory, one file at a time
# (wc-py takes a single file; the loop is yours)
total=0
for file in docs/*.md; do
  total=$((total + $(python3 wc.py "$file")))
done
echo "$total words in docs/"
```

Diagnostics never contaminate the number:

```console
$ python3 wc.py examples/article.txt > count.txt
$ cat count.txt
189

$ python3 wc.py missing.txt > count.txt; echo "exit=$?"; cat count.txt
file not found: missing.txt
exit=1
```

## 4. When something is wrong

Every failure prints one plain sentence on stderr and returns a non-zero code,
so nothing has to parse prose.

```console
$ python3 wc.py
usage: wc.py <path>

$ echo "exit=$?"
exit=2

$ python3 wc.py missing.txt
file not found: missing.txt
$ echo "exit=$?"
exit=1

$ python3 wc.py examples
not a file: examples
$ echo "exit=$?"
exit=1
```

| Exit code | Meaning |
| --- | --- |
| `0` | Words were counted |
| `1` | The file could not be read (missing, a directory, unreadable, or not UTF-8) |
| `2` | The arguments were wrong (no path, unknown option, too many paths) |

## 5. Help and version

```console
$ python3 wc.py --help
usage: wc.py [-h] [--version] <path>

Print the number of whitespace-separated words in one text file.

positional arguments:
  <path>      path to the text file whose words should be counted

options:
  -h, --help  show this help message and exit
  --version   print the version and exit

examples:
  wc.py notes.txt        count the words in notes.txt
  wc.py report.md        any UTF-8 text file works

exit codes: 0 counted, 1 file error, 2 usage error

$ python3 wc.py --version
wc.py 1.0.0
```

## 6. The recordable demo

```console
$ bash demo.sh
```

Prints every case above on one screen — the three shipped examples, a scratch
file the demo creates and deletes, both failure modes with their exit codes,
the help text, and the test suite — then exits `0` when all checks match.
`NO_COLOR=1 bash demo.sh` renders the same content without colour.

## 7. Running the tests

```console
$ python3 -m pytest
25 passed

$ python3 -m unittest -v
```

The suite is dependency-light, needs no network, and writes only into
temporary directories that it cleans up.

## Limits worth knowing

- One file per invocation: stdin, multiple paths, directories and globs are
  out of scope for this milestone.
- Word counts only: lines, characters, bytes and unique words are not reported.
- UTF-8 only: a file in another encoding is reported as `not UTF-8 text`.
  Convert it first (`iconv -f latin1 -t utf-8 in.txt > out.txt`).
- The tool never writes to disk and never opens a network connection.
