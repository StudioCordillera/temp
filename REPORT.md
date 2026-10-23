# MATHKIT 1.0 test report

## What was tested on what

| Where | Run? | What it covers |
|---|---|---|
| **PC interpreter harness** (`tools/tibasic.py`) | **Yes, every case below** | the real tokenized programs, loaded from `build/*.8xp`, run by a TI-BASIC interpreter written for this subset |
| **CEmu emulator** | **No, not run** | CEmu needs a ROM dumped from your own calculator, and TI's ROM cannot be redistributed. None was available. |
| **TI-84 Plus CE hardware** | **No, pending** | `HARDWARE-TEST.md`: 33 items (H1–H6, T1–T27) for you to run and tick |

Everything here about run-time behavior, speed and RAM use is **harness only** until a CEmu or hardware run confirms it.

## Test totals

Command: `./tests/run.sh`. Full log: `tests/results.txt`.

| Suite | File | Cases | Passed | Failed |
|---|---|---|---|---|
| Build and round trip | `tools/build.py` | 33 programs | 33 | 0 |
| Static lints and negative tests | `tests/test_static.py` | 11 checks | 11 | 0 |
| Original review (ported from Shot 1) | `tests/cases_review.py` | 120 | 120 | 0 |
| Form B acceptance | `tests/cases_formb.py` | 146 | 146 | 0 |
| Robustness and validation | `tests/cases_robust.py` | 80 | 80 | 0 |
| Show-work (step titles and key lines) | `tests/cases_work.py` | 39 | 39 | 0 |
| **Harness cases, total** | | **385** | **385** | **0** |
| Random-input sweep | `tests/fuzz.py`, seeds 1–3 × 2,000 runs | 6,000 runs | 0 math errors | 0 |

**What makes a case fail.** On top of checking the expected text on the final screen, `tests/run_tests.py` fails a case if:
- the program raised any TI error (DIVIDE BY 0, DOMAIN, NONREAL ANS, INVALID DIM, …)
- a `Goto` or `Menu(` left an open block (a memory leak on the calculator)
- `Disp` text overflowed 26 columns
- the program ended before the key script ran out
- the user's Y₀, Y₁ or X changed (RU-6)
- a string marked `!` (must not appear) was on the screen

**During this phase**, the random-input sweep found eight crashes that the fixed suites missed:
- an empty ENTER at any prompt
- ZQUAD APPLICATION with a = 1
- ZRATFN on 1/1
- a multiplicity of 0 in ZPOLY and ZGRAPH
- a fractional multiplicity in ZINEQ FROM GRAPH
- ZINEQ FROM GRAPH with nothing entered
- a negative N in ZCPLX
- a degree-62 overflow

All are fixed, and each has a regression case in `cases_robust.py`.

**Beyond the fixed seeds in `run.sh`**, about 55,000 more random runs on other seeds were made while fixing these. The last 24,000 (8 seeds × 3,000) found none.

### Shot 2 regression traps

Each Shot 2 failure has at least one case that checks the right answer and, where useful, that the wrong text does **not** appear.

| Shot 2 failure | Cases |
|---|---|
| Non-strict inequality printed with open ends | B40b, B40d, B41g, B44 |
| No real zeros gave (−∞,1)∪(1,∞) | B41c (`(⁻INF,INF)`, `ALL REAL NUMBERS`) |
| Fraction coefficients rounded | B10c, T-frac, T-frac2 |
| Decimal coefficients gave `y=1/0` | B36b2 (`H.A. Y=600`, and `1/0` absent) |
| Leading coefficient −3 instead of −48 | B18c (`DEGREE 7, LEADING ⁻48`) |
| a = −1 printed as `−11/(X+3)` | T-coef |
| `2√1 i`, `1(x−2)²`, `(−1±√6)/−1` | T-simp1, T-simp2, T-simp3, X-negA, X-negA2 |
| Shot 1's #25 miss (y-intercept not on the answer screen) | B25 |

**ZEXPR typed-input cases** (Form B #5a–c, #8d, #9a, #12e, #12h, #12j and #41b) are marked `TYPED` in `cases_formb.py`, and all pass.

## Sizes

From `build/sizes.txt`. "Memory" is token bytes plus each variable's size field and VAT entry. That is what **mem > Mem Management > Prgm** shows, give or take a few bytes.

| | Bytes | Budget |
|---|---|---|
| **Whole kit, 33 programs** | **58,403** | 61,440 (60 KB): 95% |
| Largest program: ZGRAPH | 8,561 | 16,384 target; 65,535 hard limit |
| Next largest: ZRATFN 5,841, ZQUAD 4,733, ZRATEQ 4,605, ZINEQ 4,501, ZQSOLV 4,036 | | |
| The 21 helpers (ZL… and ZEXPR) | 11,810 | |
| `.8xp` files on disk | 60,037 | each file adds a header |
| `MATHKIT.8xg` group file | 58,413 | |

**OS.** The highest OS any token needs is 5.2.0 (`toString(`), which is within the 5.2.0 limit (RU-4).

## RAM while running (harness only)

| What | Bytes | Method |
|---|---|---|
| The kit's lists and strings, worst case | 3,640 (X-deg5t: a degree-5 find-all) | `tibasic.ram_bytes`: 9 bytes per real element (18 per complex), string token bytes, plus VAT entries |
| Programs running at once, if archived programs are copied to RAM | about 10,900 (MATHKIT + ZZEROS + ZLZER + ZLZRL + ZLSYN + ZLFRC + ZLA + ZLSHOW) | sum from `sizes.txt` |
| **Total working RAM, estimated** | **about 15 KB** | well under the 30 KB limit |

**Not modeled.** The OS's own overhead per nested program call and per open block is not modeled. HARDWARE-TEST.md H4 checks RAM FREE on the calculator.

## Speed (harness only)

### Method

- **No timing from a calculator.** CEmu was not run, and no hardware is available. A reliable published TI-BASIC benchmark for the CE was not found either.
- **Cost model.** The interpreter counts work while it runs, and `tools/tibasic.py` turns the counts into milliseconds with these assumed costs:

| Unit | Cost |
|---|---|
| each statement executed | 0.9 ms |
| each token in it | 0.12 ms |
| each subprogram call | 4 ms |
| each list element touched | 0.06 ms |
| each string character copied | 0.004 ms |
| each graph command | 2 ms |
| each statement skipped by a false `If`/`Then` or a label search | 0.02 ms |

- **What these constants are.** They are educated guesses. The relative costs follow the Cemetech TI-BASIC timings page (TI-83+ data). The overall scale assumes the CE runs simple TI-BASIC loops at about 1–2 ms per iteration, which matches informal forum reports. The model could be off by a factor of 2 either way. Time T13, T15, T19 and T24 on hardware to calibrate it.
- **What is measured.** The time from the last ENTER of input to the first screen of results. For show-work runs that is page 1 of the work; all steps are computed before page 1 shows.

### Results, 331 timed cases

| Program | Cases | Show work: median | max | Answer only: median | max | ≤ 3 s (work) | ≤ 3 s (answer only) |
|---|---|---|---|---|---|---|---|
| ZCHECK | 6 | 0.6 s | 0.6 s | 0.5 s | 0.6 s | 6 | 6 |
| ZCPLX | 27 | 1.1 | 1.8 | 0.9 | 1.6 | 27 | 27 |
| ZDIV | 19 | 2.5 | 4.0 | 2.0 | 3.6 | 15 | 17 |
| ZGRAPH | 23 | 2.4 | 3.9 | 2.0 | 3.3 | 22 | 22 |
| ZINEQ | 35 | 1.8 | 2.9 | 1.6 | 2.6 | 35 | 35 |
| ZPOLY | 21 | 1.6 | 2.0 | 1.3 | 1.7 | 21 | 21 |
| ZQSOLV | 54 | 1.9 | 2.6 | 1.5 | 2.1 | 54 | 54 |
| ZQUAD | 45 | 3.4 | 4.7 | 2.7 | 4.0 | 10 | 39 |
| ZRATEQ | 19 | 5.2 | 5.5 | 4.8 | 5.2 | **0** | **0** |
| ZRATFN | 37 | 2.5 | 4.4 | 2.1 | 4.0 | 25 | 31 |
| ZZEROS | 45 | 2.8 | 9.6 | 2.6 | 8.7 | 23 | 31 |
| **All** | **331** | **2.1** | **9.6** | **1.8** | **8.7** | **238** | **283** |

### The 3-second budget is not met everywhere (by this estimate)

- **Show-work mode:** 238 of 331 cases (72%) are estimated at 3 s or less. For the original review alone it is 86 of 120, and for Form B 107 of 146.
- **Answer-only mode:** 283 of 331 (85%).
- **Over budget:**
  - every ZRATEQ case (about 3.9–5.5 s)
  - most ZQUAD standard-form cases (3.1–4.7 s, mostly from building 10–12 pages of work)
  - the larger ZZEROS cases
  - a few ZDIV, ZGRAPH and ZRATFN cases
- **Where the time goes.** In the slow cases most of it is spent formatting step text: ZLFMT, ZLFRC and ZLA, for 20–60 lines. The arithmetic is a small share. Profile any case with `tools/profile.py PROG 'keys'`.

### High-risk items to time on hardware first

| Item | Estimate (work / answer only) | Hardware item |
|---|---|---|
| ZZEROS find-all, degree 5: 2x⁵−x⁴+x³+2x²−28x+24 | **9.4 s** list input, **9.6 s** typed input / 8.7 s | T13 |
| ZRATEQ, Form B #30f | **5.5 s** / 5.2 s | T15 |
| ZINEQ, Form B #41g, typed | **2.6 s** / 2.6 s | T19 |
| ZLSHOW pager, longest traces: ZQUAD standard form (12 pages), ZZEROS degree 5 (10 pages) | about **0.13–0.15 s** per page turn (median), **0.2 s** at most; going back costs the same | T24 |

**The pager figures exclude the graph page.** `DrawF` itself is costed at 2 ms, but drawing a function on the CE takes much longer, probably 1–3 s.

## What is not verified

| Item | Why | Where to check |
|---|---|---|
| Everything at run time on a real calculator | no CEmu ROM, no hardware run | HARDWARE-TEST.md |
| Real speed | cost model only (above) | T13, T15, T19, T24, H2 |
| Running archived programs and archived subprograms | the only source is Cemetech's OS 5.3 changelog | H1 |
| `Menu(` item text longer than 16 characters, e.g. `SIMPLIFY (A+B√(⁻N))/D` | the harness truncates at 24; the calculator may cut it shorter | section C of HARDWARE-TEST.md |
| `DrawF expr(Str6)` on the graph screen | graph commands are logged, not drawn | H6, T7, T22 |
| An empty `Input` storing an empty string | assumed; the harness models it that way | T27 |
| Real RAM use, and ERR:MEMORY over long sessions | approximate model only | H4, section C |
| How characters display (`𝑖`, `√(` stored as √ then `(` in smart-mode strings, `≤`, `⁻`) | the harness compares token text, not pixels | section C |

## What the harness does not model

The programs avoid all of the following, except where noted:

- matrices, `►Frac`, `Asm(`, `IS>(`, `DS<(`, statistics commands, the Y= editor
- graph drawing itself: graph commands are logged and costed, not drawn. MATHKIT does use `ClrDraw`, `DrawF`, `Pt-On(`, `Vertical` and the window variables, and their real behavior is checked on hardware (H6).
- archive access and ERR:ARCHIVED
- memory limits, beyond a rough size check on strings and lists
- the **on** key, and how fast the screen and keys respond
- the run indicator

## Reproducing

```sh
./tests/run.sh                     # build, round trip, static tests, sweep, all four suites
.venv/bin/python tests/run_tests.py formb ZQUAD   # one suite, one program
.venv/bin/python tests/fuzz.py 7 5000             # a longer random sweep
.venv/bin/python tools/profile.py ZRATEQ '12\n1\n11\nX-3\n~8\nX+3\n9\nX²-9\n#'
```

When the hardware results come in, enter the timings in the table above, and change "harness only" to the actual source.
