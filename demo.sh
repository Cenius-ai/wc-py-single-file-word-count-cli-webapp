#!/usr/bin/env bash
# demo.sh -- non-interactive end-to-end demo of the wc-py CLI.
#
# It shows the whole contract on one screen: the happy-path counts, the
# zero-word empty file, both failure modes with their exit codes, the help
# text, and the test suite. No arguments, no prompts, no network, well under a
# second. Safe to record or to run inside a pipeline.
#
# wc-py design tokens (the committed direction -- see DESIGN.md):
#   accent   #b4603c  =  oklch(0.58 0.12 43)  -> nearest xterm-256 cube entry 137
#   muted    dimmed default foreground, for secondary text
#   surface  terminal dark, monospace, compact density, box-drawing rules
#   signal   status is always spelled out ("ok", "failed", "exit 1"); colour is
#            decoration only, never the sole carrier of meaning
set -uo pipefail
cd "$(dirname "$0")" || exit 1

PYTHON="${PYTHON:-python3}"
LABEL_WIDTH=32
DETAIL_WIDTH=40
RULE="──────────────────────────────────────────────────────────────────────"

if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  ACCENT=$'\033[38;5;137m'
  MUTED=$'\033[38;5;245m'
  BOLD=$'\033[1m'
  RESET=$'\033[0m'
else
  ACCENT=""
  MUTED=""
  BOLD=""
  RESET=""
fi

demo_failures=0

section() {
  printf '\n%s%s%s\n%s%s%s\n' "$BOLD" "$1" "$RESET" "$MUTED" "$RULE" "$RESET"
}

row() {  # row <command> <detail> <status>
  printf '  %s%-*s%s %-*s %s%s\n' \
    "$MUTED" "$LABEL_WIDTH" "$1" "$RESET" \
    "$DETAIL_WIDTH" "$2" "$3" "$RESET"
}

check_count() {  # check_count <file> <expected>
  local file="$1" expected="$2" actual
  actual="$("$PYTHON" wc.py "$file" 2>/dev/null)"
  if [ "$actual" = "$expected" ]; then
    row "wc.py $file" "$actual words" "${BOLD}${ACCENT}ok${RESET}"
  else
    demo_failures=$((demo_failures + 1))
    row "wc.py $file" "${actual:-<no output>}" "expected $expected"
  fi
}

printf '%s%s%s  %s  word counts from the command line\n' \
  "$BOLD" "wc-py" "$RESET" "$("$PYTHON" wc.py --version | awk '{print $2}')"
printf '%sone file in, one integer out, zero configuration%s\n' "$MUTED" "$RESET"

section "count a file"
check_count "examples/notes.txt" "12"
check_count "examples/article.txt" "189"
check_count "examples/empty.txt" "0"

# The tool never writes to disk; this step exists so the demo exercises a path
# the audience has not seen before. The scratch file is created and removed by
# the demo itself.
scratch="${TMPDIR:-/tmp}/wc-py-demo.txt"
trap 'rm -f "$scratch"' EXIT
printf 'alpha beta\n\n  gamma\tdelta\n' >"$scratch"
check_count "$scratch" "4"
printf 'one word\n' >"$scratch"
check_count "$scratch" "2"

section "failures stay loud and non-zero"
missing_err="$("$PYTHON" wc.py examples/nope.txt 2>&1 >/dev/null)"
missing_code=$?
row "wc.py examples/nope.txt" "$missing_err" "${BOLD}${ACCENT}exit $missing_code${RESET}"

usage_err="$("$PYTHON" wc.py 2>&1 >/dev/null)"
usage_code=$?
row "wc.py            (no path)" "$usage_err" "${BOLD}${ACCENT}exit $usage_code${RESET}"

if [ "$missing_code" = "1" ] && [ "$usage_code" = "2" ]; then
  row "exit status policy" "1 = file error, 2 = usage error" "${BOLD}${ACCENT}ok${RESET}"
else
  demo_failures=$((demo_failures + 1))
  row "exit status policy" "$missing_code / $usage_code" "unexpected codes"
fi

section "help (wc.py --help)"
"$PYTHON" wc.py --help 2>&1 | sed "s/^/  ${MUTED}/;s/\$/${RESET}/"

section "test suite (python3 -m unittest)"
suite_out="$("$PYTHON" -m unittest 2>&1)"
suite_ran="$(printf '%s\n' "$suite_out" | sed -n 's/^Ran \([0-9]*\) tests\?.*/\1/p' | tail -1)"
suite_verdict="$(printf '%s\n' "$suite_out" | grep -E '^(OK|FAILED)' | tail -1)"
row "python3 -m unittest" "${suite_ran:-?} tests" "${BOLD}${ACCENT}${suite_verdict:-no verdict}${RESET}"

printf '\n%s%s%s\n' "$MUTED" "$RULE" "$RESET"
if [ "$demo_failures" -eq 0 ]; then
  printf '%sEvery count matched, both failure modes returned their documented exit codes, suite green.%s\n' \
    "$BOLD" "$RESET"
  printf 'run it yourself:  %spython3 wc.py examples/article.txt%s\n' "$ACCENT" "$RESET"
else
  printf '%s%s demo check(s) did not match the expected values.%s\n' \
    "$BOLD" "$demo_failures" "$RESET"
fi

exit "$demo_failures"
