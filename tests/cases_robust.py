"""Robustness checks: hard inputs, every input-validation path, the RU-8 error
guards, and answer-only mode. Same case format as cases_formb.py.

Validation cases stop on the message (the program is waiting at Pause), so
the expected text is the message itself. A missing guard would raise a TI
error (ERR:DIVIDE BY 0, ERR:DOMAIN ...) in the harness and fail the case.
"""

CASES = [
    # ---- hard inputs ----
    # degree 5 with every zero: (x-1)(x+2)(2x-3)(x²+4) = 2x⁵-x⁴+x³+2x²-28x+24
    ("X-deg5", "ZZEROS", "2{2,~1,1,2,~28,24}\n#", ["⁻2, 1, 3/2", "+/-2𝑖"]),
    ("X-deg5t", "ZZEROS", "2(X-1)(X+2)(2X-3)(X²+4)\n#", ["⁻2, 1, 3/2", "+/-2𝑖"]),
    # cubic with no rational zeros falls back to labeled decimals
    ("X-norat", "ZZEROS", "2{1,0,~2,~5}\n#", ["2.0946", "⁻1.0473+/-1.1359𝑖", "(DECIMALS ARE APPROX)"]),
    ("X-norat2", "ZZEROS", "2{1,0,~2,~5}\n\n\n\n", ["NO RATIONAL ZEROS", "X=2.0946"]),
    # (x-1)²(x+2)/(x-3) ≥ 0 keeps the isolated zero x=1
    ("X-isol", "ZINEQ", "3(X-1)²(X+2)\nX-3\n2#", ["(⁻INF,⁻2]U{1}U(3,INF)"]),
    # -x²+2x+5=0 gives 1±√6, not (-1±√6)/-1
    ("X-negA", "ZQSOLV", "4~1\n2\n5\n0\n0\n0\n#", ["X=1+/-√(6)"]),
    ("X-negA2", "ZQSOLV", "5~X²+2X+5\n0\n3#", ["X=1+/-√(6)"]),
    # repeated zero with multiplicity
    ("X-mult", "ZZEROS", "2(X-1)³(X+2)²\n#", ["⁻2 (MULT 2)", "1 (MULT 3)"]),
    # large discriminant (simplifies 25000 = 50²*10)
    ("X-bigD", "ZQSOLV", "4~8\n1600\n~30000\n0\n0\n0\n#", ["X=100+/-25√(10)"]),
    # ---- input validation: message, then back to the menu ----
    ("V-qsolv-a0", "ZQSOLV", "40\n2\n1\n0\n0\n0\n", ["NOT QUADRATIC", "X² TERMS CANCEL"]),
    ("V-qsolv-sqrt-a0", "ZQSOLV", "20\n1\n2\n3\n", ["A CANNOT BE 0"]),
    ("V-quad-a0", "ZQUAD", "10\n2\n3\n", ["A CANNOT BE 0"]),
    ("V-quad-graph", "ZQUAD", "32\n1\n2\n5\n", ["X MUST DIFFER FROM H"]),
    ("V-cplx-whole", "ZCPLX", "11/2\n1\n4\n1\n", ["USE WHOLE NUMBERS,", "N>0 AND D≠0"]),
    ("V-cplx-d0", "ZCPLX", "11\n1\n4\n0\n", ["USE WHOLE NUMBERS,"]),
    ("V-cplx-square", "ZCPLX", "21\n1\n7\n", ["N MUST BE A PERFECT"]),
    ("V-div-zero", "ZDIV", "2{1,2,3}\n{0}\n", ["DIVISOR CANNOT BE 0"]),
    ("V-div-degree", "ZDIV", "2{1,2}\n{1,0,1}\n", ["DIVIDEND DEGREE IS", "BELOW DIVISOR DEGREE"]),
    ("V-syn-degree", "ZDIV", "1{5}\n2\n", ["NEED DEGREE ≥ 1"]),
    ("V-zeros-degree", "ZZEROS", "2{7}\n", ["NEED DEGREE ≥ 1"]),
    ("V-degree7", "ZZEROS", "2X^7+1\n", ["NOT A POLYNOMIAL OF", "DEGREE ≤6"]),
    ("V-degree7list", "ZDIV", "2{1,0,0,0,0,0,0,1}\n", ["NOT A POLYNOMIAL OF", "DEGREE ≤6"]),
    ("V-notpoly", "ZZEROS", "21/(X-5)\n", ["NOT A POLYNOMIAL OF"]),
    ("V-notpoly2", "ZQSOLV", "5√X)\n", ["NOT A POLYNOMIAL OF", "DEGREE ≤2"]),
    ("V-notquad", "ZQSOLV", "5X³\n", ["NOT A POLYNOMIAL OF", "DEGREE ≤2"]),
    ("V-ratfn-den0", "ZRATFN", "{1,2}\n{0}\n", ["DENOMINATOR CANNOT"]),
    ("V-ineq-den0", "ZINEQ", "3{1}\n{0}\n", ["DENOMINATOR CANNOT"]),
    ("V-ineq-fact", "ZINEQ", "20\n2\n", ["NEED A≠0 AND 1 TO 6"]),
    ("V-ineq-m0", "ZINEQ", "21\n1\n1\n2\n0\n", ["NEED P≠0 AND M A"]),
    ("V-ineq-graph", "ZINEQ", "45\n5\n", ["USE 0 TO 8 IN ALL"]),
    ("V-rateq-terms", "ZRATEQ", "10\n1\n", ["USE 1 TO 4 TERMS PER"]),
    ("V-rateq-den0", "ZRATEQ", "11\n1\n1\n0\n", ["DENOMINATOR CANNOT"]),
    ("V-poly-factors", "ZPOLY", "20\n2\n", ["NEED A≠0 AND 1 TO 6"]),
    ("V-poly-mult", "ZPOLY", "21\n1\n1\n2\n0\n", ["NEED P≠0 AND M A"]),
    ("V-poly-zeros", "ZPOLY", "37\n", ["USE 1 TO 6 ZEROS"]),
    ("V-poly-point", "ZPOLY", "31\n2\n1\n0\n2\n5\n", ["POINT IS A ZERO,"]),
    ("V-graph-point", "ZGRAPH", "122\n1\n2\n1\n", ["THAT POINT CANNOT"]),
    ("V-graph-rec", "ZGRAPH", "152~1\n2\n~1\n0\n", ["THAT POINT CANNOT"]),
    ("V-graph-sqrt", "ZGRAPH", "141\n1\n0\n0\n", ["THAT POINT CANNOT"]),
    ("V-graph-a0", "ZGRAPH", "220\n1\n1\n", ["A CANNOT BE 0"]),
    ("V-graph-dupx", "ZGRAPH", "42\n1\n2\n1\n3\n", ["TWO POINTS SHARE AN X"]),
    ("V-graph-npts", "ZGRAPH", "47\n", ["USE 2 TO 6 POINTS"]),
    ("V-graph-zero", "ZGRAPH", "31\n2\n1\n2\n5\n", ["POINT IS A ZERO,"]),
    ("V-zeros-notzero", "ZZEROS", "1{1,0,~4}\n3\n0\n#", ["3 IS NOT A ZERO"]),
    ("V-zeros-notzero-c", "ZZEROS", "1{1,0,~4}\n0\n1\n#", ["𝑖 IS NOT A ZERO"]),
    # ---- empty ENTER at a prompt counts as 0 (found by random-input testing) ----
    ("V-empty-quad", "ZQUAD", "1\n\n\n", ["A CANNOT BE 0"]),
    ("V-empty-zeros", "ZZEROS", "2\n", ["NEED DEGREE ≥ 1"]),
    ("V-empty-typed", "ZQSOLV", "5\n\n1", ["NOT QUADRATIC"]),
    ("V-empty-check", "ZCHECK", "\n", ["CHECK BY SUBSTITUTION", "EQUATION IN X"]),
    ("V-empty-check-x", "ZCHECK", "X²\n1\n", ["X VALUE="]),
    # ---- other crashes found by random-input testing ----
    ("X-app-a1", "ZQUAD", "41\n~4\n~5\n1#", ["MIN ⁻9 AT T=2", "HITS GROUND AT T=5", "F(T)=(T-2)²-9"]),
    ("X-ratfn-const", "ZRATFN", "1\n1\n1#", ["V.A. NONE", "H.A. Y=1", "Y-INT (0,1)"]),
    ("V-poly-zmult", "ZPOLY", "31\n2\n0\n", ["NEED M A WHOLE", "NUMBER ≥ 1"]),
    ("V-graph-zmult", "ZGRAPH", "31\n2\n0\n", ["NEED M A WHOLE", "NUMBER ≥ 1"]),
    ("V-ineq-gmult", "ZINEQ", "41\n0\n2\n1/2\n", ["NEED M A WHOLE", "NUMBER ≥ 1"]),
    ("V-graph-bigdeg", "ZGRAPH", "31\n40\n62\n", ["DEGREE ≤10"]),
    ("V-poly-bigdeg", "ZPOLY", "31\n2\n11\n", ["DEGREE ≤10"]),
    ("X-ineq-graph0", "ZINEQ", "40\n0\n11#", ["(⁻INF,INF)", "ALL REAL NUMBERS"]),
    ("X-ineq-graph0n", "ZINEQ", "40\n0\n21#", ["NO SOLUTION"]),
    ("V-cplx-negN", "ZCPLX", "11\n1\n~1\n1\n", ["USE WHOLE NUMBERS,", "N>0 AND D≠0"]),
    ("V-cplx-negN2", "ZCPLX", "21\n1\n~1\n", ["N MUST BE A PERFECT"]),
    # ---- RU-8 guards: excluded values are never substituted ----
    ("G-check", "ZCHECK", "1/(X-5)\n2{5}\n5\n#", ["X=5 IS EXCLUDED", "NO SUBSTITUTION DONE"]),
    ("G-check-ok", "ZCHECK", "1/(X-5)\n2{5}\n7\n#", ["F(7)=1/2"]),
    ("G-check-eq", "ZCHECK", "(7-X)/X+2/3=10/X\n2{0}\n0\n#", ["X=0 IS EXCLUDED"]),
    ("G-check-match", "ZCHECK", "X²-5X=6\n1~1\n#", ["SIDES MATCH", "X=⁻1 IS A SOLUTION"]),
    ("G-check-differ", "ZCHECK", "X²-5X=6\n12\n#", ["SIDES DIFFER", "X=2 IS NOT A SOLUTION"]),
    ("G-rateq-30c", "ZRATEQ", "12\n1\n1\nX\n1\nX-5\nX-4\nX-5\n#", ["{1}", "5 IS EXTRANEOUS"]),
    ("G-rateq-check", "ZRATEQ", "12\n1\n1\nX\n1\nX-5\nX-4\nX-5\n#<", ["X=5 IS EXCLUDED,", "X=1 KEPT", "MATCH"]),
    ("G-ratfn-eval", "ZRATFN", "{1,0,0}\n{~60,3600}\n260\n", ["X=60 IS EXCLUDED"]),
    ("G-ratfn-solve", "ZRATFN", "{1,0,~9}\n{1,~3}\n36\n#", ["NO REAL SOLUTION"]),
    # ---- answer-only mode (show-work off) shows just the answer pages ----
    ("A-only-qsolv", "ZQSOLV", "45\n3\n0\n0\n0\n~2\n", ["1/1 ANSWER", "X=⁻3/10+/-(√(31)/10)𝑖"], {"work": 0}),
    ("A-only-zeros", "ZZEROS", "2{1,0,~9,0}\n", ["1/1 ANSWER", "⁻3, 0, 3"], {"work": 0}),
    ("A-only-quad", "ZQUAD", "11\n~6\n~7\n", ["1/2 ANSWER", "VERTEX (3,⁻16) MIN ⁻16"], {"work": 0}),
    ("A-only-quad2", "ZQUAD", "11\n~6\n~7\n\n", ["2/2 ANSWER (POINTS)"], {"work": 0}),
    # ---- launcher and settings ----
    ("L-launch", "MATHKIT", "110\n1\n212\n1\n#", ["2𝑖√(53)"]),
    ("L-sections", "MATHKIT", "32", ["BEHAVIOR (3.3)"]),
    ("L-answer-only", "MATHKIT", "72\n110\n1\n212\n1\n", ["1/1 ANSWER", "2𝑖√(53)"]),
    ("L-show-work", "MATHKIT", "72\n71\n110\n1\n212\n1\n", ["1/4 SPLIT OFF ⁻1"]),
    ("L-check", "MATHKIT", "62X³-9X\n13\n#", ["F(3)=0"]),
    ("L-quit", "MATHKIT", "74", ["MATHKIT CLOSED"], {"ends": True}),
]
