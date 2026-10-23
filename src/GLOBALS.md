# MATHKIT globals

TI-BASIC has no local variables. Every program and helper shares the
calculator's variables, so MATHKIT fixes who may use what. A helper
overwrites its scratch variables on every call. A caller never keeps
anything it still needs in a helper's scratch across a call.

## Real variables

| Letters | Owner | Use |
|---|---|---|
| A–H, K–N | the main programs | inputs and working values |
| O, P | level-1 helpers (ZLFMT, ZEXPR, ZLSYN, ZLCHK, ZLSHOW) | loop counters. `P` is ZEXPR's degree bound. |
| U, V, W, θ | leaf helpers (ZLFRC, ZLRAD, ZLA, ZLEVL, ZLFLD, ZLMUL, ZLDVQ, ZLTOK) | scratch; ZLFRC returns `U/V` |
| Q, R, S, T | ZLQSV, ZLCST, ZLIFC | scratch; ZLIFC returns `Q` (the constant factor) |
| I, J, Y, Z | ZLZER family (ZLZER, ZLZRL, ZLZNM) | `Y` = write steps (input, also read by ZLSYN); `Z` = what is left after factoring (output) |
| X | **never used by programs** | ZEXPR and ZCHECK save it in `⌊MKS(3)` and restore it, so the user's X survives |

MATHKIT overwrites the user's A–W, Y, Z and θ. X is preserved.

## Strings

All ten strings are overwritten. The user's own Str0–Str9 are not preserved.

| String | Use |
|---|---|
| Str0 | helper output (ZLFRC, ZLFMT, ZLQSV, ZLCST, ZLIFC, ZLFLD, ZLTOK) |
| Str1 | the text typed at an Input (read by ZEXPR) |
| Str2–Str5 | program scratch. ZLSYN overwrites all four when `Y=1`. |
| Str6 | ZLZER output (real zeros as text, comma-separated); the graph expression read by ZLSHOW |
| Str7 | ZLFMT/ZLCST scratch, and ZLQSV's two roots as `"r1,r2"` |
| Str8 | the line being added (ZLADD reads it; ZLA writes it) |
| Str9 | the step buffer: every line of work, back to back |

## Y-variables, window and modes

- **Y-variables:** no program reads or writes Y₀–Y₉ (RU-6). Typed expressions are evaluated with `expr(` and X.
- **Graph window:** graph pages change Xmin–Yscl and restore them afterwards. `ClrDraw` clears any drawings on the graph screen.
- **Modes:** every problem starts with `Float` and `Real`, and these stay set afterwards. ZLZNM switches to `a+b𝑖` while it searches for numeric zeros, then returns to `Real`.

## The settings list ⌊MKS

| Element | Meaning |
|---|---|
| ⌊MKS(1) | 1 = show all work, 0 = answer only. Set in MATHKIT > SETTINGS; persists between runs. |
| ⌊MKS(2) | 1 = decimal mode for this problem (a `.` was typed). |
| ⌊MKS(3) | the user's X while ZEXPR or ZCHECK evaluates. |
| ⌊MKS(4) | ZLA: 1 while the current step will be shown. |

## The step buffer

- **Str9:** a leading space, then every line of work, back to back.
- **⌊MKL:** the start position of each line in Str9, plus one entry past the end. Line *k* is `sub(Str9,⌊MKL(k),⌊MKL(k+1)-⌊MKL(k))`.
- **⌊MKTL:** the line numbers of the step titles.
- **Line format:**
  - A line that starts with `#` is a step title.
  - A title that starts with `#ANSWER` marks an answer page.
  - A title of exactly `#GRAPH` marks a graph page.
- **Width:** ZLA wraps any line wider than 26 columns.
- **Graph page:** before calling ZLSHOW, the program sets Str6 to an expression in X and ⌊MKW to
  `{xmin, xmax, ymin, ymax, n, va1…van, p, x1, y1, …, xp, yp}`. Here `n` is the number of vertical asymptotes and `p` the number of points.

## Helper contracts

| Helper | Input | Output | Notes |
|---|---|---|---|
| ZLNEW | none | modes set, ⌊MKS created, step buffer cleared | Uses `SetUpEditor` to create every list later cleared with `ClrList`, then restores the stat editor. |
| ZEXPR | Str1 (`{list}`, a number, or an expression in X); `P` = max degree | ⌊MKE (coefficients, highest first); `O` = 1 accepted / 0 rejected | Typed text is evaluated at X = −int(P/2) … P−int(P/2) and recovered with finite differences. The result is checked at X = P+1 and X = 0.5. On rejection it shows `NOT A POLYNOMIAL OF DEGREE ≤P`. |
| ZLFRC | Ans (a number) | U (signed numerator), V (denominator), Str0 (text) | Continued fractions, denominator ≤ 9999. Otherwise, or in decimal mode, 4 decimal places with U = value and V = 1. |
| ZLRAD | Ans (an integer n ≥ 1) | U = k, V = m with n = k²m | |
| ZLFMT | ⌊MKF | Str0, the polynomial in X | Prints `(1/4)X²` and `⁻X`; never `1X`. |
| ZLA / ZLADD | Ans (ZLA) or Str8 (ZLADD) | line appended to the step buffer | In answer-only mode, lines outside answer steps are dropped. |
| ZLSHOW | step buffer, ⌊MKS(1) | pages on screen | ENTER/▼/► next, ▲/◄ back, CLEAR jumps to the first answer page (or exits from it). |
| ZLQSV | ⌊MKQ = {a,b,c} | ⌊MKQ = {A,B,C,D,kind,k,m,r1,r2}, Str0 = `P+/-…` text, Str7 = `"r1,r2"` | `kind`: 1 rational, 2 irrational, 3 complex. A, B, C are integers with A > 0. √\|D\| = k√m. r1 and r2 are the roots (kinds 1–2) or the centre and offset (kind 3). |
| ZLCST | ⌊MKT = {re, im, m} | Str0 = `a+b𝑖√(m)` text | |
| ZLSYN | ⌊MKY = {a0…an, k}; Y | ⌊MKY = bottom row; with Y=1, Str2–Str5 hold the tableau rows, O = field width, P = width of k | |
| ZLZER | ⌊MKH; Y | ⌊MKR/⌊MKM (rational zeros and multiplicities, in the order found); Z; ⌊MKG (leftover quadratic) or ⌊MKN/⌊MKNI (numeric zeros); ⌊MKRR/⌊MKRM/⌊MKRT (all real zeros, sorted); Str6 | Rational zero search with exact integer evaluation, then ZLQSV, then Newton in a+b𝑖 mode (ZLZNM). |
| ZLCHK | H (a value, possibly complex), Str5 (its text), ⌊MKA | adds `F(text)=0  OK` | Must run in a+b𝑖 mode for complex H. |
| ZLIFC | ZLZER's outputs | Str0 = integer factored form, Q = constant | |
| ZLMUL | ⌊MKF, ⌊MKX | ⌊MKF = product | |
| ZLDVQ | ⌊MKF, ⌊MKX | ⌊MKF = quotient, ⌊MKXR = remainder | |
| ZLEVL | Ans = x, ⌊MKF | W = F(x) | |
| ZLFLD | Ans = k, Str6 | Str0 = the k-th comma-separated field | |
| ZLTOK | Ans = 1 or 2 | Str0 = `abs(` or `√(` as real tokens | Tokenized with maximal munch so the literal holds the function tokens. |

## Lists

Every list is a custom list named ⌊MK…. MATHKIT > SETTINGS > CLEAN UP AND QUIT deletes all of them.

| Lists | Owner / meaning |
|---|---|
| ⌊MKS | settings (above) |
| ⌊MKL, ⌊MKTL, ⌊MKP, ⌊MKW, ⌊MKZ | step buffer, page table, graph window and points, ZLSYN scratch / saved window |
| ⌊MKE, ⌊MKT, ⌊MKD | ZEXPR output and scratch |
| ⌊MKF, ⌊MKX, ⌊MKXP, ⌊MKXR | polynomial in/out for ZLFMT, ZLMUL, ZLDVQ, ZLEVL |
| ⌊MKQ | ZLQSV in/out |
| ⌊MKY | ZLSYN in/out |
| ⌊MKH, ⌊MKR, ⌊MKM, ⌊MKG, ⌊MKN, ⌊MKNI, ⌊MKRR, ⌊MKRM, ⌊MKRT, ⌊MKJ, ⌊MKI, ⌊MKCN, ⌊MKCD, ⌊MKCX, ⌊MKCY, ⌊MKCK, ⌊MKCZ, ⌊MKNP, ⌊MKPW, ⌊MKPD, ⌊MKND | ZLZER family. A caller never uses these names for its own data. |
| ⌊MKA, ⌊MKB, ⌊MKC | program polynomials (ZLCHK reads ⌊MKA) |
| ⌊MKFP, ⌊MKFQ, ⌊MKFM | factor lists (ZPOLY, ZINEQ, ZGRAPH) |
| ⌊MKNU, ⌊MKDE, ⌊MKDR, ⌊MKDQ, ⌊MKDN, ⌊MKHO, ⌊MKXI, ⌊MKVA | ZRATFN / ZINEQ numerator, denominator, zeros, holes |
| ⌊MKIV, ⌊MKIK, ⌊MKII, ⌊MKSG | ZINEQ critical values, kinds, text index, signs |
| ⌊MKTN, ⌊MKTD, ⌊MKTS, ⌊MKXV, ⌊MKLR, ⌊MKLM, ⌊MKLQ, ⌊MKLC, ⌊MKEQ | ZRATEQ terms (stride 7), exclusions, LCD factors, LCD, cleared equation |
| ⌊MKPX, ⌊MKPY, ⌊MKPC, ⌊MKPN | ZGRAPH points and divided differences |

Lesson learned in testing: ZINEQ first used ⌊MKCK for its own data. ZLZER also uses it as a scratch list, so ZINEQ's data was overwritten. That is why the ZLZER family's names are reserved.
