# MATHKIT 1.0: TI-BASIC programs for Math 1414 Test 2

Programs for the **TI-84 Plus CE** (OS 5.2.0 or later). They solve the Test 2 review problem types (complex numbers, quadratics, polynomials, rational functions, inequalities and graphs) and show the work step by step. Every program is real TI-BASIC, built to `.8xp` files you can send with TI Connect CE.

| Start here | |
|---|---|
| [INSTALL.md](INSTALL.md) | check your OS, send the kit, archive it, memory, uninstall, Press-to-Test |
| [MANUAL.md](MANUAL.md) | every program, keystroke by keystroke, with Form B examples and limits |
| [HARDWARE-TEST.md](HARDWARE-TEST.md) | 33-item checklist to run on a real calculator |
| [REPORT.md](REPORT.md) | test results, sizes, speed estimates, and what is still unverified |
| [DECISIONS.md](DECISIONS.md) | every judgment call and corrected assumption, including requirements update 1 |

**Status.** All 385 harness cases pass: original review 120, Form B 146, robustness 80, show-work 39. A 6,000-run random-input sweep finds no math errors. The kit is 58,403 bytes. Nothing has been run on a calculator or an emulator yet, so speed and run-time behavior are harness estimates (see REPORT.md).

## Layout

```
src/        NAME.txt TI-BASIC source for all 33 programs; GLOBALS.md (shared variables)
build/      NAME.8xp per program, MATHKIT.8xg (all of them), sizes.txt
tools/      build.py (tokenize, lint, round trip, sizes), tibasic.py (test interpreter),
            profile.py (speed profile of one run), screens.py (sample screens)
tests/      cases_review.py, cases_formb.py, cases_robust.py, cases_work.py,
            test_static.py, fuzz.py, run_tests.py, run.sh, results.txt
```

## Build and test

```sh
./build.sh          # makes .venv with tivars 1.1.1, builds build/, checks every round trip
./tests/run.sh      # build + static checks + random sweep + all four suites -> tests/results.txt
```

## Programs

Run `prgmMATHKIT` for the menus, or any of these directly:

| Program | Covers (review problems) |
|---|---|
| ZCPLX | (A+B√(−N))/D, complex add/subtract/multiply (1, 2) |
| ZQSOLV | discriminant, square root property, completing the square, quadratic formula (8, 10–12) |
| ZQUAD | vertex form, graph features, from a graph, applications (5–7, 9, 13–15) |
| ZDIV | synthetic and long division (16, 17) |
| ZPOLY | degree, leading term, end behavior, y-intercept, from zeros (18, 21, 24–26) |
| ZZEROS | zeros from a given zero or find all, factored form, auto-check (27–29) |
| ZRATEQ | rational equations with LCD and extraneous roots (30) |
| ZRATFN | asymptotes, holes, intercepts, evaluate, solve, applications (31, 32, 34–37) |
| ZINEQ | polynomial and rational inequalities, also read from a graph (38–44) |
| ZGRAPH | parent functions and transformations, polynomials from zeros or points (3, 4, 7, 21–23, 32, 33) |
| ZCHECK | substitute an x value into any expression or equation |

Helpers start with ZL, plus ZEXPR; they are not run directly.

---

## Earlier prototype: T2PREP HTML toolkit

Three standalone HTML files, each self-contained (open directly in a browser,
no build step, no server required).

- **t2prep-field-guide.html** — the math reference. Definitions-first concept
  cards for all 14 T2PREP programs, each with a diagram, a Mermaid flowchart
  of the routine's logic, and a worked example sourced from the Review 2
  answer key.

- **t2prep-calculator.html** — the playable simulator. A real TI-84 Plus CE
  emulator (clickable keypad + real expression evaluator) with all 14
  programs registered as actual runnable TI-BASIC-style code, not mockups.
  Press PRGM to see the list; EXEC runs one, EDIT shows its listing.

- **t2prep-manual.html** — the operator's manual. Keystroke-by-keystroke
  instructions for driving each of the 14 programs on the simulator: what
  each one prompts for, the exact input syntax, and what the screen shows
  back, including a few honest notes on where the real output is rougher
  than a textbook answer (decimals instead of reduced fractions, etc.).

All three share one visual language (engineering-notebook styling, a
back-trail bar for drilling into cited concepts and stepping back out) and
cross-link to each other by URL once published as Claude artifacts.

### The 14 programs

1. RADCPLX — radical / complex simplifier
2. QUADAN — quadratic analyzer (vertex, axis, intercepts, domain/range)
3. QUADSV — exact quadratic solver (discriminant → exact/complex roots)
4. REBUILD — vertex + point → vertex-form equation
5. SYNDIV — synthetic division
6. POLYAN — polynomial zero/multiplicity/end-behavior analyzer
7. ZEROFX — zeros + point → complete factored form (any degree)
8. ZCHAIN — one known zero → remaining zeros (division chained into the solver)
9. RATAN — rational function analyzer (domain, asymptotes, holes)
10. RATSLV — rational equation solution checker (flags extraneous roots)
11. SIGNCH — sign-chart inequality solver
12. APPMDL — applied quadratic models (projectile/profit)
13. CHECK — substitution answer checker
14. XFORM — parent-function transformer (linear/abs/quad/sqrt/cubic/reciprocal)

### Origin

Built against `M1414 Review 2` (College Algebra for Precalculus), covering
imaginary numbers, quadratics, polynomials, rational functions, and
inequalities. Every worked example in all three files is sourced to a
specific numbered problem in that review and checked against its answer key.
