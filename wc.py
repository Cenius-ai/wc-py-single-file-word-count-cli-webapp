#!/usr/bin/env python3
"""wc.py -- print the word count of a single text file.

wc-py is a one-file, standard-library command line tool. It reads one file,
splits its text on runs of whitespace, and prints the resulting word total as
the only thing on stdout so the number can be piped straight into a script.
It never touches the network and never writes to disk.

Exit codes
----------
0   words were counted
1   the file could not be read (missing, not a regular file, unreadable, or
    not valid UTF-8 text)
2   the arguments were wrong (no path given, or an unknown option)

Design direction (committed; see DESIGN.md): archetype ``cli``, style family
``calm-precise``, one accent ``#b4603c`` = ``oklch(0.58 0.12 43)``, monospace
type, compact density, aligned columns, box-drawing separators. This module
deliberately emits no ANSI escape sequences: stdout stays machine-clean, and
the terminal presentation layer (demo.sh) owns the palette.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

PROGRAM = "wc.py"
VERSION = "1.0.0"
DEFAULT_ENCODING = "utf-8"

EXIT_OK = 0
EXIT_FILE_ERROR = 1
EXIT_USAGE = 2


class FileReadError(Exception):
    """The requested path could not be read as UTF-8 text.

    The message is written for a human at a terminal and never contains a
    traceback: the CLI prints it to stderr and exits with ``EXIT_FILE_ERROR``.
    """


@dataclass(frozen=True)
class TextFile:
    """A file on disk and the text decoded from it."""

    path: str
    text: str

    @property
    def word_count(self) -> int:
        """Number of whitespace-separated tokens in the decoded text."""
        return len(self.text.split())


def read_text_file(path: str, encoding: str = DEFAULT_ENCODING) -> TextFile:
    """Read ``path`` as text, translating OS and decoding errors.

    Raises:
        FileReadError: the path is missing, is a directory, is unreadable, or
            is not valid text in ``encoding``.
    """
    try:
        text = Path(path).read_text(encoding=encoding)
    except FileNotFoundError:
        raise FileReadError(f"file not found: {path}") from None
    except (IsADirectoryError, NotADirectoryError):
        raise FileReadError(f"not a file: {path}") from None
    except PermissionError:
        raise FileReadError(f"permission denied: {path}") from None
    except UnicodeDecodeError:
        raise FileReadError(
            f"not {encoding.upper()} text: {path} (this tool reads UTF-8 files)"
        ) from None
    except OSError as error:
        reason = error.strerror or error.__class__.__name__
        raise FileReadError(f"cannot read {path}: {reason}") from None
    return TextFile(path=path, text=text)


def count_words(path: str, encoding: str = DEFAULT_ENCODING) -> int:
    """Return the number of whitespace-separated words in ``path``.

    Raises:
        FileReadError: the file cannot be read (see ``read_text_file``).
    """
    return read_text_file(path, encoding=encoding).word_count


def build_parser(prog: str) -> argparse.ArgumentParser:
    """Build the argument parser: one positional path plus ``--help``."""
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Print the number of whitespace-separated words in one text file.",
        epilog=(
            "examples:\n"
            "  %(prog)s notes.txt        count the words in notes.txt\n"
            "  %(prog)s report.md        any UTF-8 text file works\n"
            "\n"
            "exit codes: 0 counted, 1 file error, 2 usage error"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "path",
        metavar="<path>",
        help="path to the text file whose words should be counted",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
        help="print the version and exit",
    )
    return parser


def main(argv: list[str] | None = None, prog: str | None = None) -> int:
    """Run the CLI and return the process exit code."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    program = prog or Path(sys.argv[0]).name or PROGRAM

    if not arguments:
        # The plan asks for exactly one line of usage, so argparse's two-line
        # "required argument" complaint is replaced by a single usage line.
        print(f"usage: {program} <path>", file=sys.stderr)
        return EXIT_USAGE

    options = build_parser(program).parse_args(arguments)
    try:
        total = count_words(options.path)
    except FileReadError as error:
        print(str(error), file=sys.stderr)
        return EXIT_FILE_ERROR

    print(total)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
