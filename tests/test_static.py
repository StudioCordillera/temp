"""Static acceptance checks (RU-1, RU-2, RU-3, RU-4, RU-6), run on the real
sources, plus negative tests showing that each lint catches a bad program.

    python tests/test_static.py
"""
import contextlib
import glob
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import build  # noqa: E402

ok = True


def expect_fail(label, name, text, needle):
    global ok
    build.failures.clear()
    with contextlib.redirect_stdout(io.StringIO()):
        build.static_checks(name, text)
    hit = any(needle in f for f in build.failures)
    print(("PASS" if hit else "FAIL"), "lint catches", label)
    ok &= hit


def expect_clean():
    global ok
    build.failures.clear()
    for p in sorted(glob.glob(os.path.join(ROOT, "src", "*.txt"))):
        name = os.path.splitext(os.path.basename(p))[0]
        build.static_checks(name, open(p, encoding="utf-8").read().rstrip("\n"))
    print(("PASS" if not build.failures else "FAIL"), f"all sources pass the lints ({len(build.failures)} problems)")
    for f in build.failures:
        print("   ", f)
    ok &= not build.failures


def no_yvars():
    global ok
    bad = [p for p in glob.glob(os.path.join(ROOT, "src", "*.txt"))
           if any(y in open(p, encoding="utf-8").read() for y in ("Y₀", "Y₁", "Y₂", "Y₉", "String►Equ(", "Equ►String("))]
    print(("PASS" if not bad else "FAIL"), "RU-6: no program reads or writes a Y-variable", bad or "")
    ok &= not bad


expect_clean()
no_yvars()
expect_fail("→ inside a string (RU-1)", "ZBAD", 'Disp "AS X→INF"', "→ inside a string")
expect_fail("∞ in source (RU-2)", "ZBAD", 'Disp "(⁻∞,1)"', "no calculator token")
expect_fail("∪ in source (RU-2)", "ZBAD", 'Disp "(1,2)∪(3,4)"', "no calculator token")
expect_fail("a colon inside a string", "ZBAD", 'Disp "A:B"', "colon inside a string")
expect_fail("a command missing its trailing space", "ZBAD", "Pause", "lowercase-letter token")
expect_fail("a label longer than 2 characters", "ZBAD", "Lbl ABC", "label")
expect_fail("a statement that does not parse", "ZBAD", "1+→A", "statement 1")
expect_fail("a call to a missing program", "ZBAD", "prgmZNOPE", "missing prgmZNOPE")
# RU-4: a token newer than OS 5.2.0 must fail the build's OS check
from tivars.tokenizer import encode  # noqa: E402
_, since = encode("piecewise(1,X>0)")
newer = build.os_tuple(since) > build.MAX_OS
print(("PASS" if newer else "FAIL"), f"RU-4: piecewise( needs OS {'.'.join(map(str, build.os_tuple(since)))} and would fail the 5.2.0 limit")
ok &= newer
print("STATIC:", "all passed" if ok else "FAILURES")
sys.exit(0 if ok else 1)
