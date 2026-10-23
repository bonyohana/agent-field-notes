#!/usr/bin/env python3
"""fieldcheck: flag shell patterns from the field notes that ShellCheck doesn't.

Usage: python3 fieldcheck.py FILE...   (exit 1 if anything was flagged)

Heuristics, line by line. They point at lines worth a second look and prove nothing.
"""
import re
import sys

CHECKS = [
    ("FN1", re.compile(r"\b(pkill|pgrep)\b[^|;&]*\s-[a-zA-Z]*f\b"),
     "pkill/pgrep -f matches full command lines, possibly your own; prefer recorded PIDs (note 1)"),
    ("FN5", re.compile(r"\bsha256sum\s+(-c|--check)\b(?!.*(\|\||&&|exit))"),
     "checksum verification without an explicit '|| exit'; does a failure stop the script? (note 5)"),
    ("FN10", re.compile(r"2>\s*/dev/null[^#\n]*\|\s*wc\s+-l"),
     "count with stderr discarded: a permission error reads as a real zero (note 10)"),
]

SELF_SAFE = re.compile(r"-[a-zA-Z]*f[a-zA-Z]*\s+(--\s+)?[\x27\"][^\x27\"]*\[[^\]]\][^\x27\"]*[\x27\"]")
BOUNDED_WILD = re.compile(r"\.\\?\{0,\d+\\?\}")
UNTIL = re.compile(r"^\s*(until|while)\b")
DEADLINE = re.compile(r"date \+%s|SECONDS|deadline|timeout\b|-gt\s|-ge\s|-lt\s|-le\s|tries|attempts", re.I)
HEREDOC_UNQUOTED = re.compile(r"(?<!<)<<-?\s*([A-Za-z_][A-Za-z0-9_]*)\b")


def check_file(path):
    findings = []
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    except OSError as e:
        return [(path, 0, "IO", str(e))]
    heredoc_end = None
    heredoc_start = 0
    for i, line in enumerate(lines, 1):
        if heredoc_end is not None:
            if line.strip() == heredoc_end:
                heredoc_end = None
            elif re.search(r"(?<!\\)`", line):
                findings.append((path, i, "FN7",
                    f"backtick inside unquoted heredoc opened at line {heredoc_start}: it will run as a command (note 7)"))
            continue
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue
        for code, rx, msg in CHECKS:
            if code == "FN1" and (SELF_SAFE.search(line) or re.search(r"\s-u\s+\S+", line)):
                continue
            if rx.search(line):
                findings.append((path, i, code, msg))
        if len(BOUNDED_WILD.findall(line)) >= 2:
            findings.append((path, i, "FN3",
                "bounded wildcards on both sides of a pattern can backtrack badly on long lines (note 3)"))
        if UNTIL.match(line) and "sleep" in " ".join(lines[i - 1:i + 3]):
            window = " ".join(lines[i - 1:i + 3])
            if not DEADLINE.search(window):
                findings.append((path, i, "FN2",
                    "polling loop with no deadline in the script; a tool timeout won't stop it (note 2)"))
        m = HEREDOC_UNQUOTED.search(line)
        if m and not re.search(r"<<-?\s*['\"]", line):
            heredoc_end = m.group(1)
            heredoc_start = i
    return findings


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    found = []
    for p in argv:
        found += check_file(p)
    for path, line, code, msg in found:
        print(f"{path}:{line}: {code} {msg}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
