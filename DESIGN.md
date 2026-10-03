# wc-py — committed design direction

This is the design source of truth for the build. The direction was committed
before any surface was written and every surface consumes it: the terminal
presentation layer (`demo.sh`), the help text (`wc.py --help`), and the output
contract (one integer on stdout).

## Direction

| Axis | Committed value |
| --- | --- |
| Archetype | `cli` |
| Style family | calm-precise |
| Accent (one, OKLCH) | `oklch(0.58 0.12 43)` |
| Accent (hex, non-CSS contexts) | `#b4603c` |
| Type personality | mono / mono — "system monospace", one ramp, no second family |
| Density | compact (label column 32, detail column 40, one blank line between sections) |
| Layout | aligned terminal columns; help-first output; no top-nav, no card grid |
| Shape language | monospace, no chrome: box-drawing separators (`─`) between sections, no borders, no elevation |
| Surface / mode | terminal dark — the only honest surface for a CLI |
| Signature | aligned columns; one accent for primary status; no colour-only signal |

Why this fits: wc-py's output is a single number, so the tool's presentation
must be quiet and exact — a calm, precise terminal product where the only
chrome is an aligned rule and one accent reserved for status.

## Tokens

| Token | Value | Consumers |
| --- | --- | --- |
| `accent` | CSS/OKLCH `oklch(0.58 0.12 43)`; hex `#b4603c` | `demo.sh` status words and the "run it yourself" hint; nearest xterm-256 cube entry is `137` (`\033[38;5;137m`), the value the script uses |
| `text` | terminal default foreground | all labels, commands, counts, help text |
| `muted` | dimmed default foreground (`\033[38;5;245m`, i.e. the standard grey slot) | section rules, command column, secondary captions |
| `bold` | terminal bold | product name, section headings, status words |
| `surface` | the terminal's own dark background — the tool never paints one | everything |
| `separator` | `─` (U+2500), 70 columns | section rules |
| `success` / `failure` | the same single accent, always accompanied by the words `ok` / `failed` / `exit N` | demo status column |

There is no second accent, no second type family, and no theme picker: the
committed palette is the whole palette.

## Colour rules

1. **No colour-only signal.** Every coloured token is also a word: `ok`,
   `failed`, `exit 1`, `exit 2`. Removing colour loses no meaning.
2. **Stdout stays machine-clean.** `wc.py` emits zero ANSI escapes — coloured
   output would corrupt `$(python3 wc.py file)` and every pipe. The palette is
   applied by `demo.sh`, the human-facing presentation surface.
3. **Gating.** Colour is emitted only when stdout is a TTY and `NO_COLOR` is
   unset, per the NO_COLOR convention. Piped or redirected demo output is plain
   text.
4. **Contrast.** Body and command text use the terminal's default foreground
   (maximum available contrast). The accent measures 4.68:1 on pure black and
   between 3.9:1 and 4.7:1 across common dark terminal backgrounds; it is
   therefore always rendered bold and always paired with a text label, so it
   meets the "no colour-only signal" floor even on a lower-contrast theme.

## Layout rules

- **Aligned columns.** Command column 32 characters, detail column 40, status
  last, so the eye can scan straight down each field.
- **Help-first.** `--help` is a first-class surface: syntax, the `<path>`
  argument, examples, and the exit-code legend. `wc.py` with no arguments
  prints the shortest honest usage — `usage: wc.py <path>`.
- **Box-drawing separators** open every section; nothing else is decorated.
- **Compact.** No blank decoration between rows, one blank line between
  sections, separators 70 columns wide.
- **One integer in, one integer out.** The tool's stdout is the design: no
  labels, no units, no colour, nothing to strip before use.

## Motion

None. No spinners, no progress bars, no artificial delay: the read is local and
instantaneous, and an honest CLI does not animate. The demo therefore completes
in well under a second.
