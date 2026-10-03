"""Test suite for the wc-py CLI.

Runs with either the standard library runner or pytest:

    python3 -m unittest -v
    python3 -m pytest -q

The CLI-level tests drive a real subprocess because the acceptance criteria are
about what the terminal prints and which exit status the process returns.
"""

from __future__ import annotations

import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
WC_SCRIPT = REPO_ROOT / "wc.py"
EXAMPLES = REPO_ROOT / "examples"

# wc.py sits at the project root next to this test module, so it imports
# without any packaging. The import follows REPO_ROOT because the repository
# layout is the only thing that locates the module.
import wc


def run_main(args: list[str]) -> tuple[int, str, str]:
    """Call wc.main() in-process, capturing what it prints."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = wc.main(args, prog="wc.py")
    return code, out.getvalue(), err.getvalue()


def run_cli(*args: str) -> subprocess.CompletedProcess:
    """Run ``python3 wc.py <args>`` and capture its two output streams."""
    return subprocess.run(
        [sys.executable, str(WC_SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        check=False,
    )


class CountWordsUnitTests(unittest.TestCase):
    """count_words() and read_text_file() on their own."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def write(self, name: str, text: str) -> Path:
        target = self.tmp / name
        target.write_text(text, encoding="utf-8")
        return target

    def test_counts_twelve_whitespace_separated_words(self) -> None:
        target = self.write(
            "notes.txt",
            "Weekly release checklist draft for the platform team reviewed on Friday afternoon\n",
        )
        self.assertEqual(wc.count_words(str(target)), 12)

    def test_empty_file_counts_zero_words(self) -> None:
        target = self.write("empty.txt", "")
        self.assertEqual(wc.count_words(str(target)), 0)

    def test_whitespace_only_file_counts_zero_words(self) -> None:
        target = self.write("blank.txt", "   \n\t\n  ")
        self.assertEqual(wc.count_words(str(target)), 0)

    def test_mixed_whitespace_and_blank_lines_do_not_add_words(self) -> None:
        target = self.write("mixed.txt", "alpha\tbeta\n\n  gamma   delta\n")
        self.assertEqual(wc.count_words(str(target)), 4)

    def test_punctuation_stays_attached_to_its_word(self) -> None:
        target = self.write("punct.txt", "The wc-py CLI is boring -- by design.\n")
        self.assertEqual(wc.count_words(str(target)), 8)

    def test_accented_words_count_once_each(self) -> None:
        target = self.write("utf8.txt", "café crème naïve checked\n")
        self.assertEqual(wc.count_words(str(target)), 4)

    def test_a_standalone_dash_is_a_token(self) -> None:
        # Words are whitespace-separated tokens, so "--" counts as one word:
        # that is the documented definition, not an accident.
        target = self.write("dash.txt", "wc-py CLI -- by design\n")
        self.assertEqual(wc.count_words(str(target)), 5)

    def test_read_text_file_returns_path_and_text(self) -> None:
        target = self.write("one.txt", "hello world\n")
        parsed = wc.read_text_file(str(target))
        self.assertEqual(parsed.path, str(target))
        self.assertEqual(parsed.text, "hello world\n")
        self.assertEqual(parsed.word_count, 2)

    def test_missing_file_raises_file_read_error(self) -> None:
        with self.assertRaises(wc.FileReadError) as caught:
            wc.count_words(str(self.tmp / "absent.txt"))
        self.assertIn("file not found", str(caught.exception))

    def test_directory_raises_file_read_error(self) -> None:
        with self.assertRaises(wc.FileReadError):
            wc.count_words(str(self.tmp))

    def test_non_utf8_file_raises_file_read_error(self) -> None:
        target = self.tmp / "binary.bin"
        target.write_bytes(b"\xff\xfe\x00\x00plain latin-1 words")
        with self.assertRaises(wc.FileReadError) as caught:
            wc.count_words(str(target))
        self.assertIn("not UTF-8 text", str(caught.exception))


class CliContractTests(unittest.TestCase):
    """End-to-end behaviour: stdout, stderr and exit status."""

    def test_counts_words_in_a_file_and_exits_zero(self) -> None:
        result = run_cli(str(EXAMPLES / "notes.txt"))
        self.assertEqual(result.returncode, wc.EXIT_OK, result.stderr)
        self.assertEqual(result.stdout, "12\n")
        self.assertEqual(result.stderr, "")

    def test_example_notes_file_really_has_twelve_words(self) -> None:
        words = (EXAMPLES / "notes.txt").read_text(encoding="utf-8").split()
        self.assertEqual(len(words), 12)

    def test_empty_file_prints_zero(self) -> None:
        result = run_cli(str(EXAMPLES / "empty.txt"))
        self.assertEqual(result.returncode, wc.EXIT_OK)
        self.assertEqual(result.stdout, "0\n")
        self.assertEqual(result.stderr, "")

    def test_output_is_one_clean_line_that_pipes(self) -> None:
        result = run_cli(str(EXAMPLES / "article.txt"))
        self.assertEqual(result.returncode, wc.EXIT_OK)
        self.assertEqual(len(result.stdout.splitlines()), 1)
        self.assertGreater(int(result.stdout), 100)

    def test_no_arguments_prints_one_usage_line_and_fails(self) -> None:
        result = run_cli()
        self.assertEqual(result.returncode, wc.EXIT_USAGE)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "usage: wc.py <path>\n")

    def test_missing_file_message_and_non_zero_exit(self) -> None:
        result = run_cli("nope.txt")
        self.assertEqual(result.returncode, wc.EXIT_FILE_ERROR)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "file not found: nope.txt\n")

    def test_directory_argument_is_reported_as_not_a_file(self) -> None:
        result = run_cli("examples")
        self.assertEqual(result.returncode, wc.EXIT_FILE_ERROR)
        self.assertEqual(result.stderr, "not a file: examples\n")

    def test_unknown_option_is_a_usage_error(self) -> None:
        result = run_cli("--lines", str(EXAMPLES / "notes.txt"))
        self.assertEqual(result.returncode, wc.EXIT_USAGE)
        self.assertIn("usage:", result.stderr)

    def test_extra_positional_argument_is_a_usage_error(self) -> None:
        result = run_cli(str(EXAMPLES / "notes.txt"), str(EXAMPLES / "empty.txt"))
        self.assertEqual(result.returncode, wc.EXIT_USAGE)

    def test_help_lists_the_path_argument_and_exits_zero(self) -> None:
        result = run_cli("--help")
        self.assertEqual(result.returncode, wc.EXIT_OK)
        self.assertIn("usage:", result.stdout)
        self.assertIn("<path>", result.stdout)
        self.assertIn("--version", result.stdout)

    def test_version_flag_exits_zero(self) -> None:
        result = run_cli("--version")
        self.assertEqual(result.returncode, wc.EXIT_OK)
        self.assertIn(wc.VERSION, result.stdout)


class MainFunctionTests(unittest.TestCase):
    """main() is importable and returns status codes instead of exiting."""

    def test_main_returns_zero_for_a_real_file(self) -> None:
        code, stdout, stderr = run_main([str(EXAMPLES / "notes.txt")])
        self.assertEqual(code, wc.EXIT_OK)
        self.assertEqual(stdout, "12\n")
        self.assertEqual(stderr, "")

    def test_main_returns_usage_code_without_arguments(self) -> None:
        code, stdout, stderr = run_main([])
        self.assertEqual(code, wc.EXIT_USAGE)
        self.assertEqual(stdout, "")
        self.assertEqual(stderr, "usage: wc.py <path>\n")

    def test_main_returns_file_error_code_for_a_missing_path(self) -> None:
        code, stdout, stderr = run_main(["definitely-absent.txt"])
        self.assertEqual(code, wc.EXIT_FILE_ERROR)
        self.assertEqual(stdout, "")
        self.assertEqual(stderr, "file not found: definitely-absent.txt\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
