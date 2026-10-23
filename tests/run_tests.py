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


def check(case, verbose=False, force_work=None):
    cid, prog, keys, expect = case[:4]
    opts = case[4] if len(case) > 4 else {}
    work = opts.get("work", 1) if force_work is None else force_work
    r = harness.run(prog, keys, work=work)
    lines = joined_lines(r.screen)
    hay = "\n".join(lines)
    hay2 = " ".join(l.strip() for l in lines)
    problems = []
    if r.error:
        problems.append(r.error)
    if not r.halted and not r.error and not opts.get("ends"):
        problems.append("program ended before the key script ran out")
    for e in expect:
        if e.startswith("!"):
            if e[1:] in hay or e[1:] in hay2:
                problems.append(f"must not show {e[1:]!r}")
        elif e not in hay and e not in hay2:
            problems.append(f"missing {e!r}")
    if opts.get("graph"):
        log = " | ".join(r.it.graph_log)
        if "DrawF" not in log or opts["graph"] not in log:
            problems.append("graph page not drawn: " + log[:120])
    if r.it.leaks:
        problems.append("LEAK " + "; ".join(r.it.leaks))
    if r.it.warnings:
        problems.append("WARN " + "; ".join(r.it.warnings))
    if r.it.yvars.get("Y₀") != harness.USER_Y or r.it.yvars.get("Y₁") != harness.USER_Y:
        problems.append("user's Y₀/Y₁ changed")
    if r.it.vars["X"] != tibasic.D(7):
        problems.append(f"user's X changed to {r.it.vars['X']}")
    ms = max((tibasic.cost_ms(c) for c in r.it.answer_costs), default=0.0)
    r.ram = tibasic.ram_bytes(r.it)
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
    timing = []          # (suite, id, prog, show-work ms, answer-only ms)
    peak_ram = [0, ""]
    t0 = time.time()
    for s in suites:
        mod = importlib.import_module("cases_" + s)
        cases = [c for c in mod.CASES if not progs or c[1] in progs]
        sp = 0
        for case in cases:
            problems, r, ms = check(case)
            peak_ram[0] = max(peak_ram[0], r.ram)
            if r.ram == peak_ram[0]:
                peak_ram[1] = case[0]
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
            if not case[0].startswith(("V-", "L-")):
                _, _, ms0 = check(case, force_work=0)
                timing.append((s, case[0], case[1], ms, ms0))
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
    if timing:
        lines_out.append("")
        lines_out.append("ESTIMATED TIME TO THE FIRST SCREEN (cost model, see REPORT.md)")
        lines_out.append(f"{'program':<8}{'cases':>6}{'work med':>10}{'work max':>10}{'ans med':>9}{'ans max':>9}{'work<=3s':>10}{'ans<=3s':>9}")
        by = {}
        for t in timing:
            by.setdefault(t[2], []).append(t)
        def med(v):
            v = sorted(v)
            return v[len(v) // 2]
        for prog in sorted(by):
            ts = by[prog]
            w = [t[3] / 1000 for t in ts]
            a = [t[4] / 1000 for t in ts]
            lines_out.append(f"{prog:<8}{len(ts):>6}{med(w):>10.1f}{max(w):>10.1f}{med(a):>9.1f}{max(a):>9.1f}"
                             f"{sum(x <= 3 for x in w):>10}{sum(x <= 3 for x in a):>9}")
        w = [t[3] / 1000 for t in timing]
        a = [t[4] / 1000 for t in timing]
        lines_out.append(f"{'ALL':<8}{len(timing):>6}{med(w):>10.1f}{max(w):>10.1f}{med(a):>9.1f}{max(a):>9.1f}"
                         f"{sum(x <= 3 for x in w):>10}{sum(x <= 3 for x in a):>9}")
        print("\n".join(lines_out[-(len(by) + 4):]))
    lines_out.append(f"Largest RAM held by the kit's variables at the end of a case: {peak_ram[0]} bytes ({peak_ram[1]})")
    print(lines_out[-1])
    if not progs and set(suites) == set(SUITES):
        with open(os.path.join(HERE, "results.txt"), "w", encoding="utf-8") as fh:
            fh.write("MATHKIT harness results (tests/run_tests.py). Times are the estimated\n")
            fh.write("calculator seconds from the last input to the first work screen (see REPORT.md).\n\n")
            fh.write("\n".join(lines_out) + "\n")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
