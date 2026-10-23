"""
Build MATHKIT: tokenize src/*.txt into build/*.8xp, check each file
round-trips back to its source, write build/sizes.txt and the group file
build/MATHKIT.8xg, and run the static checks.

Usage:  python tools/build.py          (from the repository root)
Exit status is non-zero if anything fails.
"""

import glob
import os
import re
import sys

from tivars.types import TIProgram, TIGroup
from tivars.tokenizer import encode
from tivars.models import OsVersions

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "build")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import tibasic  # noqa: E402

MAX_OS = (5, 2, 0)     # RU-4: nothing newer than OS 5.2.0
KIT_BUDGET = 60 * 1024
PROG_TARGET = 16 * 1024
PROG_LIMIT = 65535

failures = []


def fail(msg):
    failures.append(msg)
    print("FAIL:", msg)


def os_tuple(v):
    parts = re.findall(r"\d+", str(v.version if hasattr(v, "version") else v))
    return tuple(int(x) for x in parts[:3]) + (0,) * (3 - len(parts[:3]))


STRING_TOKENS_OK = {"√(", "ln(", "log(", "⁻¹", "abs("}


def static_checks(name, text):
    # checked on the raw text first: tivars cannot tokenize these at all
    bad = [sym for sym in "∞∪∅±≈" if sym in text]
    for sym in bad:
        fail(f"{name}: character {sym} has no calculator token (RU-2)")
    if bad:
        return
    mode = "max" if name in tibasic.MAX_MUNCH else "smart"
    toks = tibasic.tokenize(text, mode)
    # strings: no → (RU-1), no colon, no " inside (a " always ends the literal)
    in_str = False
    buf = []
    for t in toks:
        if t == "\"":
            if in_str:
                buf = []
            in_str = not in_str
            continue
        if in_str:
            if t == "→":
                fail(f"{name}: → inside a string literal after {''.join(buf)!r} (RU-1)")
                in_str = False
            elif t in ("\n",):
                fail(f"{name}: unterminated string literal {''.join(buf)!r}")
                in_str = False
            elif t == ":":
                fail(f"{name}: colon inside a string literal {''.join(buf)!r}")
            else:
                if len(t) > 1 and t not in STRING_TOKENS_OK:
                    fail(f"{name}: unexpected multi-character token {t!r} inside a string (max munch)")
                buf.append(t)
    for t in toks:
        if len(t) == 1 and "a" <= t <= "z":
            fail(f"{name}: lowercase-letter token {t!r} (a command missing its trailing space?)")
            break
    if len(name) > 8 or not re.fullmatch(r"[A-Zθ][A-Z0-9θ]*", name):
        fail(f"{name}: bad program name")
    try:
        prog = tibasic.Program(name, toks)
    except tibasic.TIError as e:
        fail(f"{name}: {e} (label too long, or a bad label)")
        return
    for j, st in enumerate(prog.stmts):
        if st and st[0] == "Lbl " and not (1 <= len(st) - 1 <= 2):
            fail(f"{name}: label too long")
        if st and st[0] == "prgm":
            callee = "".join(st[1:])
            if not os.path.exists(os.path.join(SRC, callee + ".txt")):
                fail(f"{name}: calls missing prgm{callee}")
    # parse every statement so syntax errors on rarely-run paths show up
    for j, st in enumerate(prog.stmts):
        if not st:
            continue
        h = st[0]
        try:
            if h in ("If ", "While ", "Repeat "):
                ps = tibasic.Parser(st, 1); ps.expr()
                if ps.i != len(st):
                    raise tibasic.TIError("SYNTAX", "trailing tokens")
            elif h in ("Disp ", "Output(", "Menu(", "Text(", "Pt-On(", "Line(", "SortA(", "String►Equ(", "Equ►String("):
                ps = tibasic.Parser(st, 1)
                while ps.peek() is not None:
                    ps.expr()
                    if ps.peek() == ",":
                        ps.take()
                    elif ps.peek() == ")":
                        ps.take()
                if ps.i != len(st):
                    raise tibasic.TIError("SYNTAX", "trailing tokens")
            elif h in ("Vertical ", "Horizontal ", "DrawF "):
                ps = tibasic.Parser(st, 1); ps.expr()
            elif h in tibasic.Interp.COMMANDS or h in ("Then", "Else", "End", "Lbl ", "Goto ", "Return",
                                                       "Stop", "prgm", "For(", "Input ", "Prompt ", "ClrDraw",
                                                       "DispGraph", "AxesOn ", "FnOff ", "PlotsOff "):
                pass
            else:
                k = -1
                in_s = False
                for q, t in enumerate(st):
                    if t == "\"":
                        in_s = not in_s
                    elif t == "→":
                        k = q
                        break
                body = st[:k] if k >= 0 else st
                ps = tibasic.Parser(body, 0); ps.expr()
                if ps.i != len(body):
                    raise tibasic.TIError("SYNTAX", "trailing tokens")
        except tibasic.TIError as e:
            fail(f"{name}: statement {j + 1} {''.join(st)!r}: {e}")
    return toks


def main():
    os.makedirs(OUT, exist_ok=True)
    names = sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(SRC, "*.txt")))
    rows, entries, max_os, total = [], [], (0, 0, 0), 0
    for name in names:
        with open(os.path.join(SRC, name + ".txt"), encoding="utf-8") as fh:
            text = fh.read().rstrip("\n")
        static_checks(name, text)
        mode = "max" if name in tibasic.MAX_MUNCH else "smart"
        data, since = encode(text.replace("⌊", "ʟ"), mode=mode)
        ver = os_tuple(since)
        if ver > max_os:
            max_os = ver
        p = TIProgram(name=name)
        p.load_string(text, mode=mode)
        path = os.path.join(OUT, name + ".8xp")
        p.save(path)
        # round trip: read the binary back and turn it into text again
        q = TIProgram()
        with open(path, "rb") as fh:
            q.load_from_file(fh)
        back = q.string().replace("ʟ", "⌊")
        if back != text:
            a, b = back.splitlines(), text.splitlines()
            for i in range(max(len(a), len(b))):
                if i >= len(a) or i >= len(b) or a[i] != b[i]:
                    fail(f"{name}: round trip differs at line {i + 1}: built {a[i] if i < len(a) else None!r} vs source {b[i] if i < len(b) else None!r}")
                    break
        size = len(p.data)
        # size in calculator memory: tokens + 2-byte length + VAT entry (6 + name)
        mem = size + 2 + 6 + len(name) + 3
        total += mem
        rows.append((name, size, mem, os.path.getsize(path), ".".join(map(str, ver))))
        if mem > PROG_LIMIT:
            fail(f"{name}: {mem} bytes is over the 65,535-byte variable limit")
        if mem > PROG_TARGET:
            fail(f"{name}: {mem} bytes is over the 16 KB per-program target")
        entries.append(q)
    if max_os > MAX_OS:
        fail(f"a token needs OS {'.'.join(map(str, max_os))}, above 5.2.0 (RU-4)")
    if total > KIT_BUDGET:
        fail(f"kit is {total} bytes, over the 60 KB budget")
    g = TIGroup.group(entries, name="MATHKIT")
    g.save(os.path.join(OUT, "MATHKIT.8xg"))
    with open(os.path.join(OUT, "sizes.txt"), "w", encoding="utf-8") as fh:
        fh.write("MATHKIT program sizes (bytes)\n")
        fh.write("tokens = tokenized program body; memory = tokens + size field + VAT entry,\n")
        fh.write("which is what 2nd MEM > Mem Management > Prgm shows (within a few bytes).\n\n")
        fh.write(f"{'program':<10}{'tokens':>8}{'memory':>8}{'.8xp file':>11}  min OS\n")
        for name, size, mem, fsz, ver in rows:
            fh.write(f"{name:<10}{size:>8}{mem:>8}{fsz:>11}  {ver}\n")
        fh.write(f"\n{'TOTAL':<10}{sum(r[1] for r in rows):>8}{total:>8}{sum(r[3] for r in rows):>11}\n")
        fh.write(f"MATHKIT.8xg group file: {os.path.getsize(os.path.join(OUT, 'MATHKIT.8xg'))} bytes\n")
        fh.write(f"Highest OS any token needs: {'.'.join(map(str, max_os))} (limit 5.2.0)\n")
        fh.write(f"Budget: {total} of {KIT_BUDGET} bytes ({100 * total / KIT_BUDGET:.0f}%)\n")
    print(open(os.path.join(OUT, "sizes.txt"), encoding="utf-8").read())
    if failures:
        print(f"BUILD FAILED: {len(failures)} problem(s)")
        sys.exit(1)
    print(f"BUILD OK: {len(names)} programs, round trips identical")


if __name__ == "__main__":
    main()
