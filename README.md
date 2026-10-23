# T2PREP — TI-84 Plus CE Toolkit for M1414 Review 2

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

## The 14 programs

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

## Origin

Built against `M1414 Review 2` (College Algebra for Precalculus), covering
imaginary numbers, quadratics, polynomials, rational functions, and
inequalities. Every worked example in all three files is sourced to a
specific numbered problem in that review and checked against its answer key.
