# MATHKIT hardware test checklist

None of this has been run on a calculator yet. Every result in REPORT.md comes from the PC test harness. Run this list on a real TI-84 Plus CE and tick each line. Write the calculator's OS version here: ________

## How to run a case

1. Run `prgmMATHKIT`, or the program named, from the home screen.
2. Press the keys exactly as listed.
   - **(−)** is the negative key; **−** is subtraction.
   - **{ }** are **2nd (** and **2nd )**.
   - **X** is **x,T,θ,n**.
   - **clear** jumps to the answer.
3. Compare the screen with **Expect**. The answer lines must match exactly. Spacing on the rows below can differ.
4. For a ⏱ case, time it with a stopwatch: from the last **enter** (or menu choice) to the first screen of work.
5. If the program stops with an ERR screen, write down the error, choose **2:Goto**, and note the line the cursor lands on.

## A. Setup and memory

| # | Check | Expect | Done |
|---|---|---|---|
| H1 | Send `MATHKIT.8xg` to **Archive** (INSTALL.md section 3). Run MATHKIT, choose 1, then run case T1. | It runs with no ERR:ARCHIVED. If an error appears, unarchive the helpers (INSTALL.md section 4), repeat, and record which way works. | ☐ |
| H2 | ⏱ Time case T13 with everything archived, then again with the ZL helpers and ZEXPR in RAM. | Record both times: ______ / ______ | ☐ |
| H3 | Before starting, store an equation in Y₀ and Y₁: `X²+1`. Store `7→X` on the home screen. Run cases T4, T5 and T12. | Afterwards, Y₀ and Y₁ still hold `X²+1` (check **y=**), and `X` on the home screen still shows 7. | ☐ |
| H4 | **2nd mem > 2 > 1:All** after a few cases | RAM FREE is still above 30 KB. ⌊MK lists appear under List. | ☐ |
| H5 | MATHKIT > `7` `3` (CLEAN UP AND QUIT) | `MATHKIT CLOSED`. No ⌊MK lists remain under **2nd mem > 2 > 4:List**. | ☐ |
| H6 | The graph page of T7: press **enter** until the graph shows | A parabola with points marked, then the home screen again. The window (**window**) is the same as before. | ☐ |

## B. One case per program (Form B)

| # | Program, problem | Keys | Expect on the final screen | ⏱ | Done |
|---|---|---|---|---|---|
| T1 | MATHKIT > ZCPLX, 1e | `1` `1` `(−)12 enter` `(−)1 enter` `144 enter` `(−)4 enter` `clear` | `(⁻12-√(⁻144))/(⁻4)=` then `3+3i` | | ☐ |
| T2 | ZCPLX, 2e | `4` `8 enter (−)1 enter 9 enter` `4 enter 1 enter 16 enter` `clear` | `(8-3i)(4+4i)=` then `44+20i` | | ☐ |
| T3 | ZQSOLV, 8d typed | `5` `(` `(−)2+3X` `)` `x²` `enter` `47 enter` `1` `clear` | `D=1692>0`, `TWO REAL IRRATIONAL`, `SOLUTIONS (D NOT A SQUARE)` | ⏱ | ☐ |
| T4 | ZQSOLV, 12j typed | `5` `3(X+1)(X-1) enter` `(−)8X enter` `3` `clear` | `X=⁻3, 1/3` | | ☐ |
| T5 | ZQSOLV, 10c | `2` `1 enter` `(−)1÷4 enter` `0 enter` `(−)13÷16 enter` `clear` | `X=1/4+/-(√(13)/4)i` | | ☐ |
| T6 | ZQSOLV, 12i, show work | `4` `2 enter 10 enter 0 enter 0 enter 0 enter (−)3 enter`, then **enter** three times | page `4/6 SIMPLIFY THE RADICAL` showing `√(76)=2√(19)` | | ☐ |
| T7 | ZQUAD, 9b | `1` `1 enter (−)6 enter (−)7 enter` `clear` | `F(X)=(X-3)²-16`, `VERTEX (3,⁻16) MIN ⁻16`, `X-INT (⁻1,0),(7,0)`, `RANGE [⁻16,INF)` | ⏱ | ☐ |
| T8 | ZQUAD, 15 | `4` `(−)4.9 enter 29.4 enter 78.4 enter` `1` `clear` | `MAX 122.5 AT T=3`, `HITS GROUND AT T=8`, `(REJECT T=⁻2, T<0)` | | ☐ |
| T9 | ZDIV, 17c | `1` `{1,0,0,1,0,7} enter` `3 enter` `clear` | `QUOTIENT X^4+3X³+9X²+28X` with ` +84` on the next line, then `REMAINDER 259` | ⏱ | ☐ |
| T10 | ZDIV, 17a, tableau | `1` `{4,(−)7,(−)18,9} enter` `3 enter`, then **enter** twice | page `3/6 4*3=12, ADD`; the tableau's middle row shows `12` | | ☐ |
| T11 | ZPOLY, 18c | `2` `(−)3 enter 3 enter` `1 enter (−)6 enter 1 enter` `4 enter 1 enter 2 enter` `1 enter (−)2 enter 4 enter` `clear` | `DEGREE 7, LEADING ⁻48`, `RISES LEFT, FALLS RIGHT` | | ☐ |
| T12 | ZZEROS, 28c | `1` `{2,(−)5,(−)21,36} enter` `(−)3 enter 0 enter` `clear` | `⁻3, 3/2, 4` and `2(X+3)(X-3/2)(X-4)`. One **▲** shows `F(⁻3)=0  OK` … | ⏱ | ☐ |
| T13 | ZZEROS, degree 5 (high risk for speed) | `2` `{2,(−)1,1,2,(−)28,24} enter` `clear` | `⁻2, 1, 3/2, +/-2i` | ⏱ | ☐ |
| T14 | ZZEROS, no rational zeros | `2` `{1,0,(−)2,(−)5} enter` `clear` | `⁻1.0473+/-1.1359i, 2.0946`, `(DECIMALS ARE APPROX)` | ⏱ | ☐ |
| T15 | ZRATEQ, 30f (high risk for speed) | `1` `2 enter 1 enter` `11 enter X-3 enter` `(−)8 enter X+3 enter` `9 enter X²-9 enter` `clear` | `{⁻16}` | ⏱ | ☐ |
| T16 | ZRATEQ, 30c | `1` `2 enter 1 enter` `1 enter X enter` `1 enter X-5 enter` `X-4 enter X-5 enter` `clear` | `{1}`, `5 IS EXTRANEOUS` | | ☐ |
| T17 | ZRATFN, 31d typed | `2X²+7X+3 enter` `X²-9 enter` `1` `clear` | `V.A. X=3`, `H.A. Y=2`, `HOLES X=⁻3 AT (⁻3,5/6)` | ⏱ | ☐ |
| T18 | ZRATFN, 34c | `{1,0,0} enter` `{(−)60,3600} enter` `5` `5` `alpha N enter` | `AS X->60 FROM LEFT, N->INF` | | ☐ |
| T19 | ZINEQ, 41g (high risk for speed) | `1` `X^3+10X²+27X enter` `(−)18 enter` `4` `clear` | `(⁻INF,⁻6]U[⁻3,⁻1]` | ⏱ | ☐ |
| T20 | ZINEQ, 44 | `3` `3X-2 enter` `(X+2)² enter` `4` `clear` | `(⁻INF,⁻2)U(⁻2,2/3]` | | ☐ |
| T21 | ZINEQ, 42b from graph | `4` `1 enter 2 enter` `2 enter 1 enter` `(−)4 enter 1 enter` `6 enter 1 enter` `2` `2` `clear` | `(⁻INF,⁻4)U[2,6)` | | ☐ |
| T22 | ZGRAPH, 32a | `2` `5` `2` `(−)1 enter (−)3 enter 4 enter` `clear` | `F(X)=⁻1/(X+3)+4`, `V.A. X=⁻3  H.A. Y=4` | | ☐ |
| T23 | ZCHECK, guard | `1/(X-5) enter` `2` `{5} enter` `5 enter` `clear` | `X=5 IS EXCLUDED`, `NO SUBSTITUTION DONE` (no ERR:DIVIDE BY 0) | | ☐ |
| T24 | Pager, longest trace (high risk for speed) | Run T13, then hold **enter** through every page, then **▲** back to page 1 | Every page shows. Note the slowest page turn: ______ | ⏱ | ☐ |
| T25 | Answer-only mode | MATHKIT `7` `2` **enter**, then `1` `1` `0 enter 1 enter 212 enter 1 enter` | The first screen is `1/1 ANSWER` with `2i√(53)`. Set `7` `1` afterwards to show work again. | | ☐ |
| T26 | Validation | ZQUAD `1` `0 enter 2 enter 3 enter` | `A CANNOT BE 0`. **enter** returns to the menu. | | ☐ |

## C. Things to look at closely

- **Characters.** Do the strings show `√(`, `𝑖`, `²`, `≤`, `≠` and `⁻` correctly? In the program source, `√(` inside a string is stored as the √ character followed by `(`, which should look the same.
- **Menus.** Do item texts longer than 16 characters (for example `SIMPLIFY (A+B√(⁻N))/D`) fit, or are they cut off? Record what the calculator shows: ______
- **DrawF.** Does `DrawF expr(Str6)` draw on the graph page (T7, T22)?
- **ERR:MEMORY.** Run 20 or more problems in a row from MATHKIT without leaving it. Does ERR:MEMORY ever appear? The harness found no `Goto` out of a block, but this is the real test.

## Results

| Total cases | Passed | Failed | Notes |
|---|---|---|---|
| 32 | | | |

Copy the timings into REPORT.md, in the "Speed" section, and replace the estimates there.
