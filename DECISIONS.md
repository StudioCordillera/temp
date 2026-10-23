# MATHKIT 1.0 decisions

This file records every judgment call made while building MATHKIT, and every assumption from the build prompt that turned out to be wrong. It has four parts:

1. Corrected assumptions
2. Design decisions
3. Test expectations changed from Shot 1
4. Requirements update 1 (RU-1 to RU-8)

"Verified" below means checked against the tivars 1.1.1 token sheet, a real test build, or the cited documentation. Anything that only the calculator can settle is marked **hardware** and has an item in HARDWARE-TEST.md.

## 1. Corrected assumptions

| Prompt said | What is true | How it was settled |
|---|---|---|
| Build with "Adriweb's `tivars_lib_py`" | The library now lives at TI-Toolkit/tivars_lib_py and installs from PyPI as **`tivars`**. `build.sh` pins `tivars==1.1.1` (RU-3). Its API: `TIProgram(name=)`, `load_string(text, mode=)`, `save()`, `load_from_file(fh)` (a binary handle), `string()`, and `TIGroup.group()` for the `.8xg`. | Installed and used for every build |
| Require OS 5.2 "for `toString(`, `eval(` and `String►Equ(`" | Only `toString(` and `eval(` are 5.2.0 tokens. `String►Equ(` dates from the TI-83. MATHKIT uses `toString(` but neither `eval(` nor `String►Equ(`. The highest version any token in the kit needs is exactly **5.2.0**. | Token sheet, checked by `tools/build.py` on every build |
| ZEXPR stores the typed text in Y1 with `String►Equ(` | MATHKIT never touches a Y-variable. `expr(Str1)` evaluates the typed text directly, with X as the variable; X is saved first and restored afterwards. | See RU-6 below |
| ∞, ∪, ∅ "may not exist" | They do not exist, and neither do ± or ≈. Fallbacks: `INF`, `U`, `NO SOLUTION`, `(⁻INF,INF)`, `+/-`. | Token sheet (RU-2) |
| Arrows like `AS X→60⁻` in display text | `→` ends a string literal, so it can never appear inside one. Display arrows are written `->`. In the source this has to be `"-"+">"`, because tivars turns the text `->` into the → token. | Test build (RU-1) |
| Write `√(`, `ln(`, `⁻¹` inside strings | tivars' default ("smart") mode tokenizes string contents **one character at a time**, so `"ln("` becomes the letters l, n, (. That displays the same, but it breaks `inString(` searches for the real token. The three programs that search for function tokens (ZEXPR, ZLA, ZLTOK) are built in maximal-munch mode, and a lint allows only `√(`, `ln(`, `log(`, `⁻¹` and `abs(` as multi-character tokens inside their strings. | Round trip and harness |
| (not stated) | Some text is silently converted to accessible-name tokens even inside strings: `...` becomes `…` and `\|F` becomes `𝙵`. The display text was reworded so neither appears. | Round trip |
| (not stated) | Commands such as `Pause ` and `SetUpEditor ` include a trailing space in their token name. Without the space, tivars stores separate lowercase letters. A lint fails the build on any lowercase-letter token. | Lint |
| `ClrList` can be used on any list | TI does not document `ClrList` on a list that does not exist. `SetUpEditor` documents creating missing lists (and unarchiving archived ones), so ZLNEW creates every list later passed to `ClrList` with `SetUpEditor`, then restores the stat editor with a bare `SetUpEditor `. | tibasicdev SetUpEditor page |
| Archived subprograms can run | The only source is Cemetech's OS 5.3 changelog (community). INSTALL.md recommends archiving and gives a fallback list of helpers to unarchive if ERR:ARCHIVED appears. | **hardware** H1, H2 |
| The review key | Shot 1's tests already use the corrected #18c (leading coefficient −100) and #31b (vertical asymptotes x = 0 and x = −9), and the ported cases keep them. | Shot 1 tests |
| `Input` with nothing typed | Taken to store an empty string. All typed input therefore goes through a guard that turns an empty entry into `0`. | **hardware** T27 |
| 60 KB budget | Read as 60 × 1024 = 61,440 bytes of variable memory: token bytes plus the size field and VAT entry, which is what **mem > Prgm** shows. The kit is 58,403 bytes. The `.8xp` files total 60,037 bytes on disk, because each file also carries a header. | `build/sizes.txt` |

## 2. Design decisions

### Input

- **Every prompt reads text** (`Input "A=?",Str1`) and passes it through ZEXPR. This handles all of the following:
  - fractions such as `⁻13/16` stay exact (the Shot 2 fraction trap)
  - decimals are detected by the `.`
  - lists `{…}` give coefficients
  - typed expressions give coefficients
  - one prompt accepts all four
- **ZEXPR sampling nodes.** Instead of x = 0…n, ZEXPR samples the typed expression at the centered integers −⌊P/2⌋ … P−⌊P/2⌋. This keeps the values (and their finite differences) smaller, which matters with 14-digit floats. Newton's forward differences give the coefficients.
- **ZEXPR acceptance check.** The recovered polynomial is evaluated at x = P+1 and x = 0.5. If either disagrees with `expr(Str1)` by more than 1ᴇ⁻6 (relative), ZEXPR shows `NOT A POLYNOMIAL OF DEGREE ≤P` and does not guess.
- **ZEXPR early rejection.** Text containing `√(X`, `⁻¹`, `/(`, `/X`, `ln(`, `log(` or `^⁻` is rejected before any sampling. Sampling `1/(X−5)` could hit its pole and stop with ERR:DIVIDE BY 0, which TI-BASIC cannot trap.
- **Degree bound.** ZEXPR's degree bound P is 2 for quadratic prompts and 6 elsewhere. ZPOLY > COEFFICIENTS allows 10, because #18c expands to degree 7.
- **Exact values.** A recovered value becomes a fraction by continued fractions with denominator ≤ 9999 (ZLFRC). If no such fraction matches, or any `.` was typed, the problem switches to **decimal mode**: 4 decimal places, labeled. This is what fixes Shot 2's `y=1/0` bug for (60+24t)/(1+0.04t).
- **Empty entries.** Pressing ENTER without typing counts as `0`, so the program's normal validation message appears (for example `A CANNOT BE 0`). ZCHECK asks again instead. This came out of the random-input sweep (`tests/fuzz.py`).
- **Invalid input.** It shows a message, waits for ENTER, then returns to the program's menu. The prompt asked for "a message and a new prompt". The menu is one key away from the same prompt, and returning there avoids a `Goto` out of an input loop, which would leak memory.

### Output

- **Ascending order.** Zeros and roots are always listed in ascending order, and factors follow the same order. Shot 1 sometimes listed them in the order found (see section 3).
- **Spelling.**
  - Negatives use the `⁻` token; subtraction uses `-`.
  - Multiplication in work lines is shown as `*`.
  - `X^4` and higher powers use `^`.
  - Complex answers use `+/-` and the `𝑖` token.
- **Simplification rules** (Shot 2's traps):
  - A coefficient of 1 is never printed and −1 prints as `⁻`, so there is no `1(X-2)²` and no `⁻11/(X+3)`.
  - √1 is never printed, so the answer is `2𝑖`, not `2√1 i`.
  - A quadratic with a < 0 is multiplied by −1 before the formula is applied, so −x²+2x+5 = 0 gives `1+/-√(6)`, not `(⁻1±√6)/⁻1`.
- **ZPOLY.** The answer screen includes the y-intercept, fixing Shot 1's only Form B miss (#25).
- **ZQSOLV.** The discriminant answer says `TWO REAL RATIONAL` for a perfect-square D and `TWO REAL IRRATIONAL` otherwise.
- **Numeric zeros.** A polynomial with no rational zeros falls back to Newton's method in `a+b𝑖` mode (ZLZNM). Results print to 4 places with `(DECIMALS ARE APPROX)`.

### The step buffer and pager

- **One string.** Every line of work is appended to one string, Str9, with line start positions in ⌊MKL and title line numbers in ⌊MKTL. Two alternatives were rejected:
  - one string per page: TI has only ten strings
  - rebuilding pages: costs a concatenation per line
  The pager (ZLSHOW) cuts each page out with `sub(`.
- **Wrapping.** ZLA wraps lines wider than 26 columns. It breaks before `+` or `-`, or after a space, comma or `)`, and never inside a number.
- **Screen layout.** Each page has a title row, up to 8 work lines, and a prompt row (`ENTER=NEXT ↑=BACK`). A longer step continues on a `(CONT)` page.
- **Answer-only mode** is a flag ZLA checks (⌊MKS(1)). Lines outside ANSWER steps are simply not stored, so there is one code path per program, not two.
- **Graph pages** are a `#GRAPH` step. ZLSHOW saves the window, sets it from ⌊MKW, then:
  - runs `ClrDraw`, `DrawF expr(Str6)` and `Pt-On` for the marked points
  - draws vertical asymptotes as `Vertical` lines
  - restores the window afterwards

### Program structure

- **33 programs:** 13 the user runs (MATHKIT plus 12 problem programs) and 20 helpers.
- **Splitting.** Helpers were split out when code was shared, or when a block was large enough that skipping it in TI-BASIC's linear scan cost time (ZLZER → ZLZRL, ZLZNM).
- **Size.** Every program is under 9 KB, well inside the 16 KB target.
- **Variable ownership.** It is fixed in `src/GLOBALS.md`. One lesson from testing: ZINEQ's own list ⌊MKCK collided with ZLZER scratch, so the ZLZER family's list names are reserved.
- **Control flow.**
  - No `Goto` or `Menu(` jumps out of an open `If…Then`, `For(`, `While` or `Repeat`. The harness tracks the block stack and fails any case that leaks.
  - Error exits use the pattern `If E` / `Then` / message / `End` / `If E` / `Goto M`.
- **AND/OR evaluate both sides in TI-BASIC.** No condition may index a list or take `√(` on its right side, relying on the left side to protect it. The ZCPLX `fPart(√(N)) or N<1` bug that the sweep found was this kind of error. It now uses `√(abs(N))`.

### Scope

- **By hand.** Form B #19, #20, #22, #23 and #33 ask what a picture shows. The manual says so. ZGRAPH can draw #33's four formulas for comparison.
- **The launcher** follows the review's sections. Every program is at most two key presses from MATHKIT. Section numbers appear in the menu titles.
- **ZCHECK** asks for the excluded values before substituting (RU-8). It splits an equation at `=` and evaluates each side with `expr(`.

### Speed

- **No CE benchmark.** No published TI-BASIC benchmark for the CE could be found. A Cemetech OS benchmark thread has its results only in images, and the available timing tables are for the TI-83+.
- **Cost model.** The harness therefore estimates time with a cost model (REPORT.md, "Speed"). It was used to pick optimizations:
  - one-statement fast paths in ZLA, ZLFRC and ZLFMT
  - a vectorized trim of leading zeros (`sum(not(cumSum(abs(L)>1ᴇ⁻9)))`)
  - integer fast paths in ZLSYN and ZLZER
  - the title list for the pager
- **Over budget.** The model still puts ZRATEQ (about 5.5 s) and degree-5 ZZEROS find-all (about 9.6 s) over the 3-second target. The time goes into building the step text: about 60 lines for degree 5. Cutting steps would conflict with "show the work". Answer-only mode is about 15% faster at the median. REPORT.md lists these as open items for hardware timing.

## 3. Test expectations changed from Shot 1

`tests/cases_review.py` ports all 120 cases from Shot 1's `answer-key-tests.js`. Changed expectations are marked `CHANGED` in the file:

| Cases | Change | Why |
|---|---|---|
| R011, R034, R040, R041, R049, R060, R062, R080, R081, R085, R086, R091 | roots and zeros in ascending order | one consistent order everywhere |
| R082, R084 | factors after the given zero in ascending order | same |
| R058 | ascending, and the two x-intercepts on two lines | `(⁻2-√(6),0),(⁻2+√(6),0)` is 27 columns, one more than the screen |
| R071 | answer line reads `DEGREE 6, LEADING 8` | one answer line holds both values |
| R100 | `NO SOLUTION` plus `⁻5 IS EXTRANEOUS` | the only candidate is excluded |
| all | ∞, ∪, ∅, ± replaced by `INF`, `U`, `NO SOLUTION`, `+/-` | RU-2 |

The Form B expectations come from `FormB-acceptance.md`, rewritten with the same fallbacks.

## 4. Requirements update 1

### RU-1: no `→` or `"` inside string literals

- **Done.** Every display arrow is `->`, built in the source as `"-"+">"`. All the Shot 1 texts in the RU-1 table were reworded; for example #36 now reads `AS X->60 FROM LEFT, N->INF`. No display text uses a quote mark.
- **Test.**
  - `tools/build.py` fails the build on a `→` or a colon inside any string literal. Colons were added because `:` also ends a statement.
  - `tests/test_static.py` proves the lint catches `Disp "AS X→INF"`.

### RU-2: character fallbacks

- **Done.** INF, U, NO SOLUTION, `(⁻INF,INF)` (shown with `ALL REAL NUMBERS`), `^4` and higher, and `+/-` for ±. These are used everywhere: programs, MANUAL.md and both test suites.
- **Test.**
  - `tools/build.py` scans the raw source for ∞ ∪ ∅ ± ≈ before tokenizing and fails the build.
  - `tests/test_static.py` proves it catches `∞` and `∪`.
  - The suites' expected answers use only the fallbacks.

### RU-3: tivars 1.1.1 toolchain and round trip

- **Done.** `build.sh` makes a venv with `tivars==1.1.1` and runs `tools/build.py`. The build:
  1. tokenizes each `src/NAME.txt`
  2. saves `build/NAME.8xp`
  3. reloads it from a binary handle and converts it back to text
  4. maps `ʟ` to `⌊` and compares; any difference fails the build
  5. writes `build/MATHKIT.8xg` with `TIGroup.group` and `build/sizes.txt`
- **Test.** Every build. The current result is `BUILD OK: 33 programs, round trips identical`. The harness runs the programs from the built `.8xp` files, not from the source text.

### RU-4: OS 5.2.0 minimum

- **Done.** `tools/build.py` looks up the "since" version of every token and fails if any needs a version above `MAX_OS = (5,2,0)`. The highest token in the kit needs exactly 5.2.0 (`toString(`), so no justification for a newer OS is needed. INSTALL.md section 1 gives the requirement and the check: **2nd**, **mem**, **1:About**.
- **Test.**
  - The build check.
  - `tests/test_static.py` confirms the check would reject `piecewise(` (OS 5.3.0).

### RU-5: archived storage and memory

- **Done.**
  - INSTALL.md recommends archiving the whole kit and explains how to archive and unarchive.
  - It gives the size (58,403 bytes) and the free RAM needed (about 15 KB used; keep 30 KB free).
  - It lists the helpers to leave in RAM (about 11.8 KB) if a subprogram call from an archived program gives ERR:ARCHIVED.
- **Sizes.**
  - Every program is far below the 65,535-byte limit for one variable.
  - The largest is ZGRAPH, at 8,561 bytes.
- **Test.**
  - `build/sizes.txt` lists every program and the total, and the build fails above 61,440 bytes.
  - HARDWARE-TEST.md H1 runs MATHKIT with every program archived, and H2 times it both ways.

### RU-6: do not overwrite the user's Y-variables

- **Deviation, justified.** RU-6 assumes ZEXPR and ZCHECK must use a Y-variable and asks that it be saved and restored. MATHKIT avoids the problem entirely: **no program reads or writes any Y-variable**. Typed text is evaluated with `expr(Str1)` while X holds the sample point. Three reasons:
  - `expr(` on a string works on every OS, so no Y-variable is needed.
  - Save and restore cannot survive an ERR stop or the **on** key (RU-8), so the user's Y₀ could still be lost. Not touching it cannot fail.
  - TI's documentation does not say what `Equ►String(` does on an empty Y-variable.

  The cost is the user's **X**. ZEXPR and ZCHECK save it in ⌊MKS(3) and restore it on every normal exit. INSTALL.md section 6 documents that an ERR stop or **on** leaves X changed.
- **Test.**
  - Before every one of the 385 harness cases, `tests/harness.py` stores `X²+1` in Y₀ and Y₁ and 7 in X. `tests/run_tests.py` fails any case where they differ afterwards.
  - `tests/test_static.py` fails if any source mentions Y₀–Y₉, `String►Equ(` or `Equ►String(`.
  - HARDWARE-TEST.md H3 repeats the check on the calculator.

### RU-7: Press-to-Test and exam use

- **Done.** INSTALL.md section 8 covers:
  - instructor approval, because the course bans symbolic-manipulation calculators
  - TI's documented behavior: programs disabled, and RAM and Archive variables deleted except AppVars, with links to TI KB 34886 and the Press-to-Test guide
  - reinstalling: Quit Exam Mode in TI Connect CE (Actions), then send `MATHKIT.8xg` from the saved `build/` folder
- **Test.** A review checklist item: the section exists and contains the reinstall steps.

### RU-8: no error trapping

**Guards:**

| Where | What | Excluded values come from |
|---|---|---|
| ZRATEQ | never substitutes a denominator zero | the typed denominators |
| ZRATFN | never evaluates at a V.A. or hole x (`X=60 IS EXCLUDED`) | the typed denominators |
| ZINEQ | tests signs only at points between critical values | the typed denominators |
| ZCHECK | asks for excluded values and refuses to substitute one | the user |
| ZEXPR | refuses quotients before sampling | the text pattern |

The random-input sweep found and fixed several unguarded math errors:
- `0^0`
- `min(` of an empty list
- `sub(` with length 0
- √ of a negative
- an overflow from multiplicity 62

**Input validation:** a = 0, zero divisor and zero denominator, degree above the bound, non-whole multiplicities, non-integer radicands, too many terms or factors, a point that is a zero, and two points sharing an x.

**Test:**
- One harness case per guard and per validation path: `tests/cases_robust.py`, groups `V-` and `G-`. Examples:
  - `G-check`: 1/(X−5) at x = 5
  - `G-rateq-30c`: candidate 5 for #30c
- The harness raises ERR:DIVIDE BY 0, ERR:DOMAIN, ERR:NONREAL ANS, ERR:INVALID DIM, ERR:OVERFLOW and others, so a missing guard fails its case.
- `tests/fuzz.py` adds a fixed-seed sweep of 6,000 random runs to `tests/run.sh`. It fails on any math error. ERR:SYNTAX and ERR:DATA TYPE from malformed typing are documented in MANUAL.md section 15 rather than trapped.
