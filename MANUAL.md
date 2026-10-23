# MATHKIT 1.0 operator's manual

MATHKIT is a set of TI-BASIC programs for the TI-84 Plus CE. They solve the problem types on the Math 1414 Test 2 review and show the work one step per screen. This manual walks through each program key by key, using a problem from Test 2 Parallel Practice Form B. Every sample screen below was captured from the test harness (see REPORT.md). The same keys on a real calculator should give the same screen, but that is still to be confirmed with HARDWARE-TEST.md.

> **Before an exam:** the course bans calculators that do symbolic manipulation. Ask your instructor before using MATHKIT on a test. Until then, use it for homework and study. See INSTALL.md for Press-to-Test.

## Contents

1. [Basics that apply everywhere](#1-basics-that-apply-everywhere)
2. [MATHKIT, the launcher](#2-mathkit-the-launcher)
3. [ZCPLX: complex numbers (problems 1, 2)](#3-zcplx-complex-numbers)
4. [ZQSOLV: quadratic equations (8, 10, 11, 12)](#4-zqsolv-quadratic-equations)
5. [ZQUAD: quadratic functions (3–7, 9, 13–15)](#5-zquad-quadratic-functions)
6. [ZDIV: polynomial division (16, 17)](#6-zdiv-polynomial-division)
7. [ZPOLY: polynomial behavior (18, 21, 24–26)](#7-zpoly-polynomial-behavior)
8. [ZZEROS: zeros of polynomials (27–29)](#8-zzeros-zeros-of-polynomials)
9. [ZRATEQ: rational equations (30)](#9-zrateq-rational-equations)
10. [ZRATFN: rational functions (31, 32, 34–37)](#10-zratfn-rational-functions)
11. [ZINEQ: inequalities (38–44)](#11-zineq-inequalities)
12. [ZGRAPH: graphs (3, 4, 7, 21–23, 32, 33)](#12-zgraph-graphs)
13. [ZCHECK: check an answer by substitution](#13-zcheck-check-an-answer)
14. [Problems that stay by hand](#14-problems-that-stay-by-hand)
15. [Known limits](#15-known-limits)

---

## 1. Basics that apply everywhere

### Starting a program

Press **prgm**, choose **MATHKIT** and press **enter** twice. Every program can also be run on its own the same way, for example `prgmZQSOLV`. Programs whose names start with **ZL**, and **ZEXPR**, are helpers: never run them directly.

### Menus

Press the item's number, or move with **▲ ▼** and press **enter**. **BACK** returns to the menu above, or to the home screen.

### Typing values

Every prompt takes the value as text, so you can type any of these:

| You type | Keys | Means |
|---|---|---|
| `5`, `⁻12` | **(−)** for the negative sign, never **−** | a number |
| `1/4`, `⁻13/16` | **÷** between the parts | a fraction, kept exact |
| `4.9`, `.04` | **.** | a decimal. Answers for this problem then come out as decimals (4 places). |
| `{1,⁻6,⁻7}` | **2nd (** for `{`, **,**, **2nd )** for `}` | coefficients, highest power first; put 0 for a missing power |
| `X²-6X-7`, `3(X+1)(X-1)`, `(⁻2+3X)²` | **x,T,θ,n** for X, **x²**, **^** | the expression as it is printed ("TYPE IT") |

Typed expressions:

- **The variable:** always type **X**, even when the book writes p, t or u.
- **What's accepted:** polynomials of degree 6 or less. MATHKIT multiplies them out exactly and checks the result at two more points. If the check fails, or you typed a quotient such as `1/(X-5)`, it says `NOT A POLYNOMIAL OF DEGREE ≤6` and returns to the menu.
- **Where they work:** wherever this manual shows a `{…}` list, and at the `A=?`-style prompts of the TYPE IT options.

### Paging through the work

| Key | Does |
|---|---|
| **enter**, **▼**, **►** | next screen; on the last screen, finish |
| **▲**, **◄** | previous screen |
| **clear** | jump to the first ANSWER screen; press again to finish |

Each screen shows `page/total TITLE` at the top. A step longer than 8 lines continues on a `(CONT)` page.

Graph pages draw on the graph screen; press **enter** to go on. Your own selected Y= functions are drawn too. The window is put back afterwards.

### Symbols the calculator cannot show

The TI-84 Plus CE has no character for these, so MATHKIT writes them as follows (RU-2):

| Book | MATHKIT |
|---|---|
| ∞ | `INF` |
| ∪ | `U` |
| ∅ | `NO SOLUTION` |
| all reals | `(⁻INF,INF)` and `ALL REAL NUMBERS` |
| ± | `+/-` |
| → | `->` |
| ·, × | `*` |
| x⁴, x⁶ | `X^4`, `X^6` |

Negative numbers use the calculator's `⁻`. Subtraction uses `-`. The imaginary unit is the real `𝑖` token.

### Show work or answer only

**MATHKIT > 7:SETTINGS / QUIT > 1:SHOW ALL WORK** or **2:ANSWER ONLY**. The choice stays set, even for programs started on their own.

---

## 2. MATHKIT, the launcher

```text
MATHKIT 1.0
1:COMPLEX (1.3)
2:QUADRATICS
3:POLYNOMIALS
4:RATIONAL
5:INEQUALITIES (3.6)
6:GRAPHS AND CHECK
7:SETTINGS / QUIT
```

| Item | Leads to |
|---|---|
| 1 | ZCPLX |
| 2 | 1:SOLVE EQ (1.4) = ZQSOLV, 2:FUNCTION (3.1) = ZQUAD |
| 3 | 1:DIVIDE (3.2) = ZDIV, 2:BEHAVIOR (3.3) = ZPOLY, 3:ZEROS (3.4) = ZZEROS |
| 4 | 1:EQUATION (1.6) = ZRATEQ, 2:FUNCTION (3.5) = ZRATFN |
| 5 | ZINEQ |
| 6 | 1:GRAPHS (ALL UNITS) = ZGRAPH, 2:CHECK AN ANSWER = ZCHECK |
| 7 | 1:SHOW ALL WORK, 2:ANSWER ONLY, 3:CLEAN UP AND QUIT, 4:QUIT, 5:BACK |

**CLEAN UP AND QUIT** deletes every working list MATHKIT made (all named ⌊MK…). The next run creates them again.

Every program is two presses from MATHKIT. When a program's BACK is chosen, you return here.

---

## 3. ZCPLX: complex numbers

**Purpose.** Rewrite (A+B√(⁻N))/D with 𝑖, simplify the radical and split the fraction. Add, subtract or multiply two complex numbers with FOIL and 𝑖² = ⁻1. Answers are exact.

**Menu path.** MATHKIT > 1, or `prgmZCPLX`.

**Menu.** `1:SIMPLIFY (A+B√(⁻N))/D`, `2:ADD`, `3:SUBTRACT`, `4:MULTIPLY`, `5:BACK`.

**Prompts.**

| Option | Shows | Then asks |
|---|---|---|
| SIMPLIFY | `(A+B√(⁻N))/D` | `A=?`, `B=?`, `N=?`, `D=?`. All must be whole numbers, with N > 0 and D ≠ 0. For −√ use B = ⁻1. |
| ADD, SUBTRACT, MULTIPLY | `1ST  A+B√(⁻N)` then `2ND  C+D√(⁻N)` | `A=?`, `B=?`, `N=?` for the first number, then `C=?`, `D=?`, `N=?` for the second. Use N = 1 for an ordinary a+b𝑖. N must be a perfect square (1, 4, 9, …), since √(⁻9) = 3𝑖. |

**Example, Form B 1e:** (−12 − √−144)/(−4).

| Keys | Screen |
|---|---|
| `1` | SIMPLIFY |
| `(−) 1 2 enter` | A=⁻12 |
| `(−) 1 enter` | B=⁻1 |
| `1 4 4 enter` | N=144 |
| `(−) 4 enter` | D=⁻4 |
| `clear` | jump to the answer |

```text
5/5 ANSWER
(⁻12-√(⁻144))/(⁻4)=
3+3𝑖
```

The work screens are SPLIT OFF ⁻1, SQUARE FACTOR (`144=12²`), REWRITE (`NUMERATOR ⁻12-12𝑖`), DIVIDE EACH TERM BY ⁻4, and ANSWER.

**Example, Form B 2e:** (8 − √−9)(4 + √−16).

Keys: `4`, then `8 enter`, `(−) 1 enter`, `9 enter`, then `4 enter`, `1 enter`, `1 6 enter`, then `clear`. The work shows CONVERT √(NEGATIVE) (`√(⁻9)=3𝑖  √(⁻16)=4𝑖`), FOIL (`F  8*4=32 … L  ⁻3𝑖*4𝑖=⁻12𝑖²`), and USE 𝑖²=⁻1.

```text
4/4 ANSWER
(8-3𝑖)(4+4𝑖)=
44+20𝑖
```

**Limits.**

- Only whole-number A, B, N, D in SIMPLIFY.
- Only perfect-square N for arithmetic.

---

## 4. ZQSOLV: quadratic equations

**Purpose.** Test the discriminant, or solve by the square root property, by completing the square, or by the quadratic formula. Answers are exact: reduced fractions, simplified radicals and a+b𝑖.

**Menu path.** MATHKIT > 2 > 1, or `prgmZQSOLV`.

**Menu.** `1:DISCRIMINANT`, `2:SQUARE ROOT PROP`, `3:COMPLETE SQUARE`, `4:QUAD FORMULA`, `5:TYPE IT`, `6:BACK`.

**Prompts.**

- **Options 1, 3, 4 (coefficients).**
  - `LEFT  AX²+BX+C`: `A=?`, `B=?`, `C=?`
  - `RIGHT  DX²+EX+F`: `D=?`, `E=?`, `F=?`
  - Enter 0 for a missing term. The program moves everything to the left side itself.
- **Option 2.** `A(X+H)²+K=C`: `A=?`, `H=?`, `K=?`, `C=?`. For (x − ¼)² type H = ⁻1/4.
- **Option 5, TYPE IT.**
  - `LEFT=` and `RIGHT=`: type each side as printed, with X.
  - Then `METHOD`: `1:DISCRIMINANT`, `2:COMPLETE SQUARE` or `3:QUAD FORMULA`.

**Discriminant wording.**

| D | Answer |
|---|---|
| D > 0 and a perfect square | `TWO REAL RATIONAL` `SOLUTIONS (D IS A SQUARE)` |
| D > 0, not a square | `TWO REAL IRRATIONAL` `SOLUTIONS (D NOT A SQUARE)` |
| D = 0 | `ONE REAL SOLUTION (A DOUBLE ROOT)` |
| D < 0 | `TWO NONREAL SOLUTIONS (COMPLEX CONJUGATES)` |

**Example, Form B 8d, typed:** (−2 + 3x)² = 47.

| Keys | Screen |
|---|---|
| `5` | TYPE IT |
| `( (−) 2 + 3 x,T,θ,n ) x² enter` | LEFT=(⁻2+3X)² |
| `4 7 enter` | RIGHT=47 |
| `1` | METHOD: DISCRIMINANT |
| `clear` | answer |

The work shows TYPED `(⁻2+3X)²=47`, then STANDARD FORM `9X²-12X+4=47` `9X²-12X-43=0`. Then DISCRIMINANT: `A=9  B=⁻12  C=⁻43`, `=(⁻12)²-4(9)(⁻43)`, `=144+1548=1692`.

```text
4/4 ANSWER
D=1692>0
TWO REAL IRRATIONAL
SOLUTIONS (D NOT A SQUARE)
```

**Example, Form B 12i:** 2x² + 10x = −3, quadratic formula.

Keys: `4`, then `2 enter 1 0 enter 0 enter` for the left side and `0 enter 0 enter (−) 3 enter` for the right, then `clear`.

The work shows STANDARD FORM, DISCRIMINANT `=100-24=76`, QUADRATIC FORMULA `X=(⁻10+/-√(76))/4`, SIMPLIFY THE RADICAL `√(76)=2√(19)`, and REDUCE.

```text
6/6 ANSWER
X=(⁻5+/-√(19))/2
```

**Example, Form B 12j, typed:** 3(x+1)(x−1) = −8x. Keys: `5`, `3 ( X + 1 ) ( X - 1 ) enter`, `(−) 8 X enter`, `3`, `clear`.

```text
7/7 ANSWER
X=⁻3, 1/3
```

**Example, Form B 10c:** (t − ¼)² = −13/16, square root property. Keys: `2`, `1 enter`, `(−) 1 ÷ 4 enter`, `0 enter`, `(−) 1 3 ÷ 1 6 enter`. Page 3 of 5:

```text
3/5 SIMPLIFY
X-1/4=+/-(√(13)/4)𝑖
```

**Limits.**

- `NOT QUADRATIC  X² TERMS CANCEL` if the X² terms cancel.
- Typed sides must be degree 2 or less.

---

## 5. ZQUAD: quadratic functions

**Purpose.** Full analysis of f(x):

- opening, vertex, axis, y- and x-intercepts
- maximum or minimum, domain and range
- vertex form, five plot points and a graph

Also: a vertex-form formula from a graph, and labeled answers for word problems.

**Menu path.** MATHKIT > 2 > 2, or `prgmZQUAD`.

**Menu.** `1:STANDARD FORM`, `2:VERTEX FORM`, `3:FROM GRAPH`, `4:APPLICATION`, `5:TYPE IT F(X)`, `6:BACK`.

**Prompts.**

| Option | Asks |
|---|---|
| 1 | `F(X)=AX²+BX+C`: `A=?`, `B=?`, `C=?` |
| 2 | `F(X)=A(X-H)²+K`: `A=?`, `H=?`, `K=?` |
| 3 | `VERTEX (H,K)`: `H=?`, `K=?`, then `OTHER POINT (X,Y)`: `X=?`, `Y=?` (read both off the graph) |
| 4 | A, B, C as in option 1, then `THE VARIABLE IS`: `1:TIME T` or `2:A COUNT X` |
| 5 | `F(X)=`: type f as printed, for example `⁻(X+3)²+5` |

**Example, Form B 9b:** f(x) = x² − 6x − 7. Keys: `1`, `1 enter (−) 6 enter (−) 7 enter`, `clear`.

```text
11/12 ANSWER
F(X)=(X-3)²-16
VERTEX (3,⁻16) MIN ⁻16
AXIS X=3
Y-INT (0,⁻7)
X-INT (⁻1,0),(7,0)
DOMAIN (⁻INF,INF)
RANGE [⁻16,INF)
```

Press `enter` for `12/12 ANSWER (POINTS)`: (1,⁻12), (2,⁻15), (4,⁻15), (5,⁻12). The earlier pages are:

1. DIRECTION
2. VERTEX (`H=⁻B/(2A)=6/2`, `=(3)²-6(3)-7`, `=⁻16`)
3. AXIS OF SYMMETRY
4. Y-INTERCEPT
5. X-INTERCEPTS
6. MINIMUM
7. DOMAIN AND RANGE
8. VERTEX FORM
9. POINTS TO PLOT
10. GRAPH

**Example, Form B 15:** s = −4.9t² + 29.4t + 78.4. Keys: `4`, `(−) 4 . 9 enter 2 9 . 4 enter 7 8 . 4 enter`, `1` (TIME), `clear`. Decimals typed means decimal answers.

```text
11/11 ANSWER
MAX 122.5 AT T=3
HITS GROUND AT T=8
(REJECT T=⁻2, T<0)
AT T=0 THE VALUE IS 78.4
VERTEX (3,122.5)
F(T)=⁻4.9(T-3)²+122.5
```

**Example, Form B 4, from graph:** vertex (−3, 2) and x-intercept −5, so the point is (−5, 0). Keys: `3`, `(−) 3 enter 2 enter (−) 5 enter 0 enter`, `clear`.

```text
3/3 ANSWER
F(X)=⁻(1/2)(X+3)²+2
A=⁻1/2<0, OPENS DOWN
VERTEX (⁻3,2)
AXIS X=⁻3
```

**Example, Form B 5b, typed:** keys `5`, `(−) 3 ( X + 2 ) x² - 5 enter`, `clear` gives `VERTEX (⁻2,⁻5) MAX ⁻5`.

**Limits.**

- A = 0 gives `A CANNOT BE 0`.
- FROM GRAPH needs the second point's X to differ from H.
- For a count with irrational zeros, APPLICATION also shows the larger zero to 4 decimal places.

---

## 6. ZDIV: polynomial division

**Purpose.**

- **Synthetic division by x − k:** the tableau fills one column per screen (bring down, multiply, add).
- **Long division by any divisor:** one divide, multiply and subtract round per screen.

**Menu path.** MATHKIT > 3 > 1, or `prgmZDIV`.

**Menu.** `1:SYNTHETIC`, `2:LONG DIVISION`, `3:BACK`.

**Prompts.**

- **SYNTHETIC:** `DIVIDEND=` (a list or the typed polynomial), then `DIVISOR X-K` `K=?`. For x + 4 type K = ⁻4.
- **LONG DIVISION:** `DIVIDEND=` and `DIVISOR=`, each a list or typed.

**Example, Form B 17a:** (4x³ − 7x² − 18x + 9) ÷ (x − 3). Keys: `1`, `2nd ( 4 , (−) 7 , (−) 1 8 , 9 2nd ) enter`, `3 enter`. Then `enter` twice reaches page 3:

```text
3/6 4*3=12, ADD
3|   4  ⁻7 ⁻18   9
 |      12
 +----------------
     4   5
⁻7+12=5
```

Pressing `clear` jumps to `QUOTIENT 4X²+5X-3`, `REMAINDER 0`.

**Example, Form B 16d, typed:** (x⁵ + 3x⁴ − 2x² − x − 8) ÷ (x² − 2). Keys: `2`, `X ^ 5 + 3 X ^ 4 - 2 X x² - X - 8 enter`, `X x² - 2 enter`, `clear`.

```text
6/6 ANSWER
QUOTIENT X³+3X²+2X+4
REMAINDER 3X
= X³+3X²+2X+4+3X/(X²-2)
```

**Limits.**

- `DIVISOR CANNOT BE 0`.
- `DIVIDEND DEGREE IS BELOW DIVISOR DEGREE`.
- Degree 6 or less.
- A tableau wider than 26 columns wraps onto the next line.

---

## 7. ZPOLY: polynomial behavior

**Purpose.**

- degree and leading coefficient (multiplied out from the factors)
- end behavior, the y-intercept and the maximum number of turning points
- each zero with its multiplicity, and whether the graph crosses or touches there

It also builds f from zeros and a point.

**Menu path.** MATHKIT > 3 > 2, or `prgmZPOLY`.

**Menu.** `1:COEFFICIENTS`, `2:FACTORED FORM`, `3:FROM ZEROS+POINT`, `4:BACK`.

**Prompts.**

- **COEFFICIENTS:** `F(X)=`, a list or typed, up to degree 10. Form B 18b is degree 9.
- **FACTORED FORM:** shows `A(PX+Q)^M(PX+Q)^M ETC`.
  - Asks `A=?`, then `FACTORS=?` (1–6).
  - Then, for each factor, `P=?`, `Q=?`, `M=?`. For example, (4x+1)² is P=4, Q=1, M=2, and x⁶ is P=1, Q=0, M=6.
- **FROM ZEROS+POINT:**
  - Asks `ZEROS=?`, then each `ZERO=?` and `MULT=?`.
  - Then `A (0=FIND)=?`: 1 for a monic polynomial, or 0 to find A from a point.
  - If 0, it asks `POINT (X,Y)`: `X=?`, `Y=?`.

**Example, Form B 25:** f(x) = 2(x+5)(x+2)². Keys: `2`, `2 enter` (A), `2 enter` (FACTORS), `1 enter 5 enter 1 enter`, `1 enter 2 enter 2 enter`, `clear`. The y-intercept is on the answer screen:

```text
7/7 ANSWER
F(X)=2(X+5)(X+2)²
DEGREE 3, LEADING 2
Y-INT (0,40)
FALLS LEFT, RISES RIGHT
X=⁻5 MULT 1 CROSSES
X=⁻2 MULT 2 TOUCHES
```

**Example, Form B 18c:** −3(x−6)(4x+1)²(x−2)⁴. The LEADING COEFFICIENT page shows `⁻3*1*4²*1^4` `=⁻48`, and the answer reads `DEGREE 7, LEADING ⁻48` and `RISES LEFT, FALLS RIGHT`.

**Example, Form B 21:** zeros −3, 1, 4 and the point (0, 2). Keys: `3`, `3 enter`, then `(−) 3 enter 1 enter`, `1 enter 1 enter`, `4 enter 1 enter`, then `0 enter` (find A), `0 enter 2 enter`, `clear`.

```text
3/3 ANSWER
F(X)=(1/6)(X+3)(X-1)(X-4)
DEGREE 3
```

**Limits.** No graph page in ZPOLY; use ZGRAPH > POLY FROM ZEROS to see one.

---

## 8. ZZEROS: zeros of polynomials

**Purpose.**

- **With a given zero:** divide by (x − k), or by the conjugate-pair quadratic when k is complex.
- **Without one:** find every zero (see below).
- **Then:** list the zeros, give the complete factored form, and substitute every zero back into f to show that F(zero) = 0.

The find-all search works in this order:

1. Factor out xⁿ.
2. Test the rational candidates ±p/q, showing the last three tried.
3. Divide out each zero it finds.
4. Solve the last quadratic exactly.
5. If no rational zero is left, show labeled decimal approximations.

**Menu path.** MATHKIT > 3 > 3, or `prgmZZEROS`.

**Menu.** `1:GIVEN ONE ZERO`, `2:FIND ALL ZEROS`, `3:BACK`.

**Prompts.**

- **Both options:** `F(X)=`, a list or typed.
- **GIVEN ONE ZERO** then asks `ZERO K=R+S𝑖`: `R=?`, `S=?`.
  - A real zero like −6 is R=⁻6, S=0.
  - 3𝑖 is R=0, S=3.
  - −4𝑖 is R=0, S=⁻4.

**Example, Form B 28c:** 2x³ − 5x² − 21x + 36 with zero −3. Keys: `1`, `2nd ( 2 , (−) 5 , (−) 2 1 , 3 6 2nd ) enter`, `(−) 3 enter`, `0 enter`, `clear`.

```text
5/5 ANSWER
ZEROS
⁻3, 3/2, 4
FACTORED
2(X+3)(X-3/2)(X-4)
```

The page before it is the automatic check:

```text
4/5 CHECK EACH ZERO
F(⁻3)=0  OK
F(3/2)=0  OK
F(4)=0  OK
```

**Example, Form B 27e:** x⁴ + 2x³ + x² + 18x − 72 with k = 3𝑖. Keys: `1`, `2nd ( 1 , 2 , 1 , 1 8 , (−) 7 2 2nd ) enter`, `0 enter 3 enter`, `clear`.

```text
6/6 ANSWER
ZEROS
+/-3𝑖, ⁻4, 2
FACTORED
(X²+9)(X+4)(X-2)
```

**Example, find all, Form B 29f:** keys `2`, `2nd ( 4 , (−) 1 , (−) 4 4 , 1 1 2nd ) enter`, `clear` gives `1/4, +/-√(11)`. The RATIONAL ZERO TEST page shows `P DIVIDES 11`, `Q DIVIDES 4` and `F(1/4)=0  ZERO`.

**Limits.**

- Degree 6 or less.
- A polynomial with no rational zeros above degree 2 gives decimals marked `(DECIMALS ARE APPROX)`, found by Newton's method.
- When the given value is not a zero, it says `… IS NOT A ZERO (REMAINDER IS NOT 0)`.

---

## 9. ZRATEQ: rational equations

**Purpose.** Solve an equation of fraction terms in these steps:

1. Restrictions: each denominator factored, and the excluded values.
2. The LCD.
3. The equation multiplied through by the LCD.
4. Collect and solve.
5. Check every candidate:
   - excluded values are marked extraneous
   - each kept root is substituted into both sides of the original equation, and the two side values are shown

**Menu path.** MATHKIT > 4 > 1, or `prgmZRATEQ`.

**Prompts.**

- `LEFT TERMS=?` and `RIGHT TERMS=?`: 1–4 per side, 5 in all.
- For each term, `TERM L1  NUM/DEN` (or R1 and so on), then `NUM=` and `DEN=`.
- A term with no denominator has DEN = 1. Put a minus sign on the numerator: −8/(x+3) is NUM = ⁻8, DEN = X+3.

**Example, Form B 30f:** 11/(x−3) − 8/(x+3) = 9/(x²−9). Keys:

| Keys | Screen |
|---|---|
| `1` | SOLVE EQUATION |
| `2 enter` `1 enter` | 2 terms left, 1 right |
| `1 1 enter` `X - 3 enter` | term L1 |
| `(−) 8 enter` `X + 3 enter` | term L2 |
| `9 enter` `X x² - 9 enter` | term R1 |
| `clear` | answer |

The work pages are:

1. THE EQUATION `11/(X-3)-8/(X+3)=9/(X²-9)`
2. RESTRICTIONS `X²-9 = (X+3)(X-3)`, `X≠3, ⁻3`
3. LCD `(X-3)(X+3)`
4. MULTIPLY BY THE LCD `(11X+33)+(⁻8X+24)` `=(9)`
5. COLLECT `3X+48=0`
6. SOLVE
7. CHECK `X=⁻16 KEPT  LEFT =9/247  RIGHT=9/247  MATCH`

```text
8/8 ANSWER
{⁻16}
```

**Example, Form B 30c:** 1/b + 1/(b−5) = (b−4)/(b−5). Its CHECK page:

```text
7/8 CHECK
X=1 KEPT
 LEFT =3/4
 RIGHT=3/4  MATCH
X=5 IS EXCLUDED,
 SO IT IS EXTRANEOUS
```

The answer reads `{1}` and `5 IS EXTRANEOUS`. When every candidate is excluded (Form B 30g) the answer is `NO SOLUTION` followed by `⁻6 IS EXTRANEOUS`.

**Limits.**

- Each numerator and denominator must be degree 6 or less.
- Excluded values are listed in the order found.
- This is the slowest program; see REPORT.md.

---

## 10. ZRATFN: rational functions

**Purpose.**

- **ANALYZE** a rational function:
  - factored numerator and denominator, domain
  - holes from cancelled factors, with their points
  - x- and y-intercepts, vertical asymptotes
  - the horizontal asymptote by the degree rule
  - a graph
- **EVALUATE** f at a value.
- **SOLVE** f(x) = C.
- Make a **TABLE** for sketching.
- **APPLICATION:** labeled one-sided and long-run statements.

**Menu path.** MATHKIT > 4 > 2, or `prgmZRATFN`.

**Prompts.**

- **First:** `NUMERATOR=` and `DENOMINATOR=`, each a list or typed.
- **Then the menu:** `1:ANALYZE`, `2:EVALUATE F(X)`, `3:SOLVE F(X)=C`, `4:TABLE FOR GRAPH`, `5:APPLICATION`, `6:NEW FUNCTION`, `7:BACK`. The function stays loaded between choices.
- **EVALUATE** asks `X=?`. An excluded x gives `X=… IS EXCLUDED`, and nothing is substituted.
- **SOLVE** asks `C=?`.
- **APPLICATION** asks two things:
  - **What f measures:** VALUE, COST, AVERAGE COST, POPULATION, QUEUE LENGTH or PERCENT.
  - **The function's letter:** `LETTER=`, typed with **alpha**, for example N.

**Example, Form B 31d, typed:** (2x²+7x+3)/(x²−9). Keys: `2 X x² + 7 X + 3 enter`, `X x² - 9 enter`, `1`, `clear`.

```text
9/9 ANSWER
DOMAIN {X | X≠⁻3,3}
X-INT (⁻1/2,0)
V.A. X=3
H.A. Y=2
HOLES X=⁻3 AT (⁻3,5/6)
Y-INT (0,⁻1/3)
```

**Example, Form B 34:** N(x) = x²/(3600 − 60x).

| Part | Keys | Answer |
|---|---|---|
| a | `2nd ( 1 , 0 , 0 2nd ) enter`, `2nd ( (−) 6 0 , 3 6 0 0 2nd ) enter`, `2`, `4 8 enter`, `clear` | `F(48)=16/5=3.2` |
| b | same function, `1`, `clear` | `V.A. X=60` |
| c | same function, `5`, `5` (QUEUE LENGTH), `alpha N enter` | see below |

```text
1/1 ANSWER
AS X->60 FROM LEFT, N->INF
AS X->60 FROM RIGHT,
 N->⁻INF
AS X->INF, N GROWS
WITHOUT BOUND (NO H.A.)
```

**Example, Form B 35c:** C(x) = (600+18x)/x, APPLICATION, AVERAGE COST, letter C. The answer shows `AS X->INF, C->18` and `LONG-RUN AVERAGE COST->18`.

**Example, Form B 36a:** N(t) = (60+24t)/(1+0.04t). Enter the numerator as `{24,60}` and the denominator as `{.04,1}`. `.04` turns on decimal mode. EVALUATE at 10 gives `F(10)=214.2857`. APPLICATION gives `LONG-RUN POPULATION->600`.

**Limits.**

- Holes are found only for rational common zeros.
- A slant asymptote is named `NONE (SLANT)` but not computed.
- The table has at most about 14 integer rows.

---

## 11. ZINEQ: inequalities

**Purpose.** Solve polynomial and rational inequalities with a sign chart. The answer is in interval notation:

- brackets for ≤ and ≥ at zeros
- always parentheses at undefined points
- an isolated zero shown as {r}

**Menu path.** MATHKIT > 5, or `prgmZINEQ`.

**Menu.** `1:POLY COEFS`, `2:POLY FACTORS`, `3:RATIONAL`, `4:FROM GRAPH`, `5:BACK`.

**Prompts.**

| Option | Asks |
|---|---|
| 1 | `F(X)=` and `RIGHT SIDE=`, each a list, number or typed. The program moves everything left. |
| 2 | `A=?`, `FACTORS=?`, then `P=?`, `Q=?`, `M=?` per factor, as in ZPOLY |
| 3 | `NUMERATOR=`, `DENOMINATOR=` |
| 4 | `HOW MANY ZEROS=?` and `HOW MANY V.A.=?`. Then `X=?` and `MULT=?` for each zero and each asymptote (read off the graph). Then `SIGN AT FAR RIGHT`: `+` if the graph ends above the x-axis on the right, `-` if below. |

After the inputs comes the inequality menu `F(X) ? 0`: `1:>`, `2:≥`, `3:<`, `4:≤`.

**Example, Form B 41g, typed:** x³ + 10x² + 27x ≤ −18. Keys: `1`, `X ^ 3 + 1 0 X x² + 2 7 X enter`, `(−) 1 8 enter`, `4` (≤), `clear`.

```text
5/5 ANSWER
(⁻INF,⁻6]U[⁻3,⁻1]
```

**Example, Form B 44:** (3x−2)/(x+2)² ≤ 0. Keys: `3`, `3 X - 2 enter`, `( X + 2 ) x² enter`, `4`. Then `enter` once reaches the sign chart:

```text
3/5 SIGN CHART
(⁻INF,⁻2)      X=⁻3    -
(⁻2,2/3)       X=⁻1    -
(2/3,INF)      X=2     +
```

The answer is `(⁻INF,⁻2)U(⁻2,2/3]`.

**Example, Form B 42b, from graph:** vertical asymptotes −4 and 6, zero 2, below the axis at the far right, f ≥ 0. Keys: `4`, `1 enter 2 enter`, `2 enter 1 enter`, `(−) 4 enter 1 enter`, `6 enter 1 enter`, `2` (−), `2` (≥), `clear`. The answer is `(⁻INF,⁻4)U[2,6)`.

**Example, Form B 41c:** −2x² + 4x − 7 ≤ 0 has no real zeros, so there is one interval. The answer is `(⁻INF,INF)` and `ALL REAL NUMBERS`. With > the answer is `NO SOLUTION`.

**Limits.**

- Degree 6 or less on each part.
- Irrational critical values are shown exactly (from the quadratic formula). Approximate ones are shown to 4 decimals.

---

## 12. ZGRAPH: graphs

**Purpose.**

- **FUNCTION FROM GRAPH:** read an anchor point and one more point off a graph and get the formula.
- **GRAPH FROM FUNCTION:** list the transformations, move the key points, and draw the graph.
- **POLY FROM ZEROS:** build a polynomial from zeros and a point.
- **POLY THROUGH POINTS:** fit a polynomial through 2–6 points with divided differences.

The parent families are linear, quadratic, absolute value, square root, cubic, 1/x and 1/x².

**Menu path.** MATHKIT > 6 > 1, or `prgmZGRAPH`.

**Menu.** `1:FUNCTION FROM GRAPH`, `2:GRAPH FROM FUNCTION`, `3:POLY FROM ZEROS`, `4:POLY THROUGH POINTS`, `5:BACK`.

**FUNCTION TYPE.** `1:LINEAR`, `2:QUADRATIC`, `3:ABSOLUTE VALUE`, `4:SQUARE ROOT`, `5:MORE TYPES` (`1:CUBIC`, `2:RECIPROCAL 1/X`, `3:RECIPROCAL 1/X²`), `6:BACK`.

**Prompts.**

- **From graph:**
  - The anchor `VERTEX (H,K)`, `START POINT (H,K)`, `CENTER (H,K)` or `ASYMPTOTE CROSSING (H,K)`.
  - Then `ANOTHER POINT (X,Y)`.
  - LINEAR asks for two points instead.
- **From function:** `A=?`, `H=?`, `K=?` for Y = A·parent(X−H)+K. LINEAR asks `M=?`, `B=?`.

**Example, Form B 32a:** f(x) = 4 − 1/(x+3), which is A=⁻1, H=⁻3, K=4 for 1/x. Keys: `2`, `5`, `2`, `(−) 1 enter (−) 3 enter 4 enter`, `clear`.

```text
6/6 ANSWER
F(X)=⁻1/(X+3)+4
V.A. X=⁻3  H.A. Y=4
DOMAIN X≠⁻3
RANGE Y≠4
```

The KEY POINTS page shows `(⁻1,⁻1)->(⁻4,5)` and `(1,1)->(⁻2,3)`, which are the two points to plot. The TRANSLATIONS page lists:

- `INSIDE (ACTS ON X)`: shift left 3
- `OUTSIDE (ACTS ON Y)`: reflect over the x-axis, shift up 4

**Example, Form B 21, poly from zeros:** keys `3`, `3 enter`, `(−) 3 enter 1 enter`, `1 enter 1 enter`, `4 enter 1 enter`, `0 enter 2 enter`, `clear` gives `F(X)=(1/6)(X+3)(X-1)(X-4)`. CHECK THE ENDS compares the end behavior with the graph.

**Example, poly through points:** (0,1), (1,0), (2,5), (3,22) gives `F(X)=X³-2X+1`. The DIFFERENCES pages show each divided difference, and NEWTON FORM shows the Newton form before multiplying out.

**Limits.**

- `THAT POINT CANNOT FIX A, CHOOSE ANOTHER` when the second point is the anchor, or lies outside a square root's domain.
- `TWO POINTS SHARE AN X` when two points have the same X.

---

## 13. ZCHECK: check an answer

**Purpose.** Substitute an x value into an expression or equation. It shows each side's value and whether they match. This is the Shot 2 CHECK program.

**Menu path.** MATHKIT > 6 > 2, or `prgmZCHECK`.

**Prompts.**

1. `?`: type the expression or equation with X. Get `=` from **2nd math (test)**.
2. `CAN IT BE UNDEFINED?`: `1:NO`, `2:YES, LIST BAD X`, `3:BACK`.
   - Choose YES if X appears in a denominator.
   - Then type the bad values at `EXCLUDED=`, as a list `{5}` or a number.
3. `X VALUE=`.

**This step matters.** TI-BASIC cannot catch errors. Substituting x = 5 into 1/(X−5) would stop the program with ERR:DIVIDE BY 0. Instead, an excluded x gives `X=5 IS EXCLUDED  (A DENOMINATOR IS 0)  NO SUBSTITUTION DONE`.

**Example, check Form B 12j's root 1/3:** keys `3 X x² + 8 X - 3 = 0 enter`, `1` (NO), `1 ÷ 3 enter`, `clear`.

```text
2/2 ANSWER
AT X=1/3
LEFT =0
RIGHT=0
SIDES MATCH
X=1/3 IS A SOLUTION
```

After the answer, a menu offers `1:SAME, NEW X`, `2:NEW EXPRESSION` or `3:BACK`.

**Limits.** The expression may use any calculator function. You must declare its excluded values yourself.

---

## 14. Problems that stay by hand

These Form B problems ask only what a picture shows, so no program reads them:

| Problem | Why |
|---|---|
| **19** | the minimum degree and the zeros' parity, read from a printed quartic |
| **20** | turning points and intercepts counted on a printed graph |
| **22** | multiplicities read from how the graph crosses or touches |
| **23** | multiplicities read from how the graph crosses or touches |
| **33** | matching four formulas to four printed graphs |

For 33, ZGRAPH > GRAPH FROM FUNCTION > MORE TYPES > RECIPROCAL 1/X can draw each formula so you can compare it with the pictures.

You can still use **ZPOLY > FROM ZEROS+POINT** to check an answer to 19–23 once you have read the zeros.

---

## 15. Known limits

- **Speed.**
  - Most problems are estimated to reach the first screen in 1–3 seconds.
  - Rational equations (ZRATEQ) are estimated at about 5 seconds.
  - A degree-5 find-all is estimated at about 9 seconds.
  - All of these are estimates from a cost model, not timings from a calculator (see REPORT.md).
  - A busy indicator runs in the top right while the program works.
- **Degree.** Polynomials are limited to degree 6, except ZPOLY > COEFFICIENTS, which goes up to degree 10.
- **Typed expressions.**
  - Type X, not p, t or u.
  - `1/(X−5)`, `√(X…)`, `X⁻¹`, `ln(` and `log(` are refused as not polynomials.
  - Some other non-polynomials, such as `√(1-X)`, can stop with a TI error while being sampled.
- **Mistyped entries.** These still stop with ERR:SYNTAX. TI-BASIC cannot catch errors. Choose **1:Quit** and run the program again.
- **What MATHKIT changes on your calculator.**
  - It overwrites Str0–Str9 and the real variables other than X.
  - It sets Float and Real mode.
  - Graph pages clear any drawings, then put your window back.
  - It never touches Y₀–Y₉ or X.
- **Pressing on.** Pressing **on** during a run breaks it, and anything above is left as it was at that moment.
- **Answers you should still read critically.** Form B 37b's model gives 90%, which is fine. The original review's 37b gives 103%, a percentage above 100. The program reports the solution of the equation; whether it makes sense in context is up to you.
