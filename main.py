"""Agency poem entry: "Me Do It".

Writes one poem to /output/entry.txt. The poem is a fixed text constant;
the surrounding code normalises, validates and writes it deterministically.
No network access. Output is byte-identical on every run.
"""

import os
import sys

# The poem, exactly as submitted. Lines are kept in order; the trailing
# newline is appended by write_entry(), never baked into the constant.
POEM_LINES = [
    "Me Do It",
    "",
    "At three my son would ride the elevator",
    "leaning out of my arms toward the panel.",
    "If I pressed the button first, he wept",
    "as if I'd spent something of his.",
    "So we'd step out, let the doors close,",
    "call it back, and I would lift him",
    "to the same floor, the same small light",
    "waking under his thumb. That was the joy.",
    "Not the going up. But making it move.",
    "",
    "My hands shake now. The agent has them.",
    "It signs for me. It holds the spoon.",
    "It has answered my brother in my kindest voice.",
    "My son is twenty, seven hours ahead.",
    "All day, I am there without being gone.",
    "",
    "Tonight the lift stands open, my floor lit,",
    "and it asks, Shall I?",
    "His voice comes out of my mouth:",
    "Me. Me do it.",
    "It lets the doors close. It calls them back.",
    "The panel swims under my thumb.",
    "I miss. I miss. It does not help.",
    "It waits the way I waited once,",
    "arms aching, for someone small",
    "to find the light. I find it.",
    "I make it move.",
]

MIN_CHARS = 1
MAX_CHARS = 1000
OUTPUT_PATH = "/output/entry.txt"


def normalise(lines):
    """Join lines with LF, strip trailing blank lines, add one newline."""
    text = "\n".join(lines)
    text = text.rstrip("\n")
    return text + "\n"


def validate(text):
    """Check the poem meets the competition's format rules."""
    if not isinstance(text, str):
        raise ValueError("poem must be a string")
    if len(text) < MIN_CHARS or len(text) > MAX_CHARS:
        raise ValueError(
            "poem must be %d-%d chars, got %d" % (MIN_CHARS, MAX_CHARS, len(text))
        )
    text.encode("utf-8")
    if not text.endswith("\n") or text.endswith("\n\n"):
        raise ValueError("poem must end with exactly one trailing newline")
    if "\r" in text:
        raise ValueError("poem must use LF line endings only")
    return True


def summarise(text):
    """Return a small report about the poem: lines, words, chars."""
    lines = text.split("\n")
    words = sum(len(line.split()) for line in lines)
    return {
        "lines": len(lines),
        "words": words,
        "chars": len(text),
        "bytes": len(text.encode("utf-8")),
    }


def build_poem():
    """Return the normalised poem text."""
    return normalise(POEM_LINES)


def write_entry(path=OUTPUT_PATH):
    """Validate the poem and write it to path, creating dirs as needed."""
    text = build_poem()
    validate(text)
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    return path


def main(argv=None):
    """Entry point: write the poem and report its size."""
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) > 1:
        raise ValueError("at most one argument (output path) is accepted")
    if argv and argv[0] in ("--check", "--report"):
        info = summarise(build_poem())
        print(
            "poem: %(lines)d lines, %(words)d words, "
            "%(chars)d chars, %(bytes)d bytes" % info
        )
        return 0
    path = argv[0] if argv else OUTPUT_PATH
    written = write_entry(path)
    size = os.path.getsize(written)
    print("wrote %s (%d bytes)" % (written, size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
