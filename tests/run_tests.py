"""
Run the MATHKIT acceptance suites in the TI-BASIC interpreter harness.

    python tests/run_tests.py                 all suites
    python tests/run_tests.py formb           one suite (review, formb, robust, work)
    python tests/run_tests.py formb ZQUAD     one suite, one program
    python tests/run_tests.py -v ...          print the final screen of every case

Every case runs the built .8xp files with a scripted key sequence and checks
the text on the last screen. A case also fails if the program raised a TI
error, if a Goto/Menu( left a block open (memory leak on the calculator),
if Disp text overflowed the screen, or if the user's Y₀, Y₁ or X changed.

Writes tests/results.txt.
"""

import importlib
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import harness  # noqa: E402
import tibasic  # noqa: E402

SUITES = ["review", "formb", "robust", "work"]


def joined_lines(screen):
    out = []
    for ln in screen.split("\n"):
        if ln.startswith(" ") and not ln.startswith("  ") and out:
            out[-1] += ln[1:]
        else:
            out.append(ln)
    return out


def check(case, verbose=False):
    cid, prog, keys, expect = case[:4]
    opts = case[4] if len(case) > 4 else {}
    r = harness.run(prog, keys, work=opts.get("work", 1))
    lines = joined_lines(r.screen)
    hay = "\n".join(lines)
    hay2 = " ".join(l.strip() for l in lines)
    problems = []
    if r.error:
        problems.append(r.error)
    if not r.halted and not r.error:
        problems.append("program ended before the key script ran out")
    for e in expect:
        if e.startswith("!"):
            if e[1:] in hay or e[1:] in hay2:
                problems.append(f"must not show {e[1:]!r}")
        elif e not in hay and e not in hay2:
            problems.append(f"missing {e!r}")
    if r.it.leaks:
        problems.append("LEAK " + "; ".join(r.it.leaks))
    if r.it.warnings:
        problems.append("WARN " + "; ".join(r.it.warnings))
    if r.it.yvars.get("Y₀") != harness.USER_Y or r.it.yvars.get("Y₁") != harness.USER_Y:
        problems.append("user's Y₀/Y₁ changed")
    if r.it.vars["X"] != tibasic.D(7):
        problems.append(f"user's X changed to {r.it.vars['X']}")
    ms = max((tibasic.cost_ms(c) for c in r.it.answer_costs), default=0.0)
    return problems, r, ms


def main(argv):
    verbose = "-v" in argv
    args = [a for a in argv if a != "-v"]
    suites = [a for a in args if a in SUITES] or SUITES
    progs = [a for a in args if a not in SUITES]
    tibasic.Library.cache = {}
    lines_out = []
    total = passed = 0
    slow = []
    t0 = time.time()
    for s in suites:
        mod = importlib.import_module("cases_" + s)
        cases = [c for c in mod.CASES if not progs or c[1] in progs]
        sp = 0
        for case in cases:
            problems, r, ms = check(case)
            total += 1
            ok = not problems
            sp += ok
            passed += ok
            tag = "PASS" if ok else "FAIL"
            line = f"{tag} {s:<7}{case[0]:<10}{case[1]:<8}{ms / 1000:6.2f}s  {repr(case[2])[:44]}"
            if not ok:
                line += "\n      " + "\n      ".join(problems) + "\n      SCREEN:\n        " + "\n        ".join(r.screen.split("\n"))
            elif verbose:
                line += "\n        " + "\n        ".join(r.screen.split("\n"))
            if ms > 3000:
                slow.append((ms, s, case[0], case[1]))
            print(line)
            lines_out.append(line)
        summ = f"== {s}: {sp}/{len(cases)} passed"
        print(summ)
        lines_out.append(summ)
    summ = f"== TOTAL: {passed}/{total} passed ({time.time() - t0:.0f} s of harness time)"
    print(summ)
    lines_out.append(summ)
    if slow:
        lines_out.append("Cases over the 3 s estimate: " + ", ".join(f"{c} {p} {ms / 1000:.1f}s" for ms, s, c, p in sorted(slow, reverse=True)))
        print(lines_out[-1])
    if not progs and set(suites) == set(SUITES):
        with open(os.path.join(HERE, "results.txt"), "w", encoding="utf-8") as fh:
            fh.write("MATHKIT harness results (tests/run_tests.py). Times are the estimated\n")
            fh.write("calculator seconds from the last input to the first work screen (see REPORT.md).\n\n")
            fh.write("\n".join(lines_out) + "\n")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
