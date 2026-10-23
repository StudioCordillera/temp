"""Show-work checks: for at least one case per program, land on a given work
page and assert its step title and the key lines, not just the final answer.

Keys are the inputs followed by one ENTER per page to move forward.
"""

CASES = [
    # ZCPLX, Form B 1c: split off -1, square factor, rewrite
    ("W-cplx1", "ZCPLX", "10\n1\n180\n1\n", ["1/4 SPLIT OFF ⁻1", "√(⁻180)=√(⁻1)*√(180)", "=𝑖√(180)"]),
    ("W-cplx2", "ZCPLX", "10\n1\n180\n1\n\n", ["2/4 SQUARE FACTOR", "180=36*5", "=6√(5)"]),
    ("W-cplx3", "ZCPLX", "48\n~1\n9\n4\n1\n16\n\n", ["2/4 FOIL", "F  8*4=32", "L  ⁻3𝑖*4𝑖=⁻12𝑖²"]),
    ("W-cplx4", "ZCPLX", "48\n~1\n9\n4\n1\n16\n", ["1/4 CONVERT √(NEGATIVE)", "√(⁻9)=3𝑖", "√(⁻16)=4𝑖"]),
    # ZQSOLV: discriminant arithmetic, square root property, completing the square
    ("W-qsolv1", "ZQSOLV", "5(~2+3X)²\n47\n1\n\n", ["3/4 DISCRIMINANT", "A=9  B=⁻12  C=⁻43", "=144+1548=1692"]),
    ("W-qsolv2", "ZQSOLV", "21\n~1/4\n0\n~13/16\n\n\n", ["3/5 SIMPLIFY", "X-1/4=+/-(√(13)/4)𝑖"]),
    ("W-qsolv3", "ZQSOLV", "31\n8\n0\n0\n0\n7\n\n\n", ["3/8 ADD (B/2)² TO BOTH", "(B/2)²=(4)²=16", "7+16=23"]),
    ("W-qsolv4", "ZQSOLV", "42\n10\n0\n0\n0\n~3\n\n\n", ["3/6 QUADRATIC FORMULA", "X=(⁻B+/-√(D))/(2A)", "X=(⁻10+/-√(76))/4"]),
    # ZQUAD: vertex by h=-b/(2a) and k=f(h); points table
    ("W-quad1", "ZQUAD", "11\n~6\n~7\n\n", ["2/12 VERTEX", "H=⁻B/(2A)=6/2", "=(3)²-6(3)-7", "VERTEX (3,⁻16)"]),
    ("W-quad2", "ZQUAD", "11\n~6\n~7\n\n\n\n\n\n\n\n\n", ["9/12 POINTS TO PLOT", "3        ⁻16  VERTEX"]),
    ("W-quad3", "ZQUAD", "33\n~2\n2\n~5\n\n", ["2/3 PLUG IN (2,⁻5)", "⁻5=A(⁻1)²-2", "⁻3=1A", "A=⁻3"]),
    # ZDIV: synthetic tableau one column per step; long division rounds
    ("W-div1", "ZDIV", "1{4,~7,~18,9}\n3\n\n\n", ["3/6 4*3=12, ADD", "3|   4  ⁻7 ⁻18   9", "|      12", "⁻7+12=5"]),
    ("W-div2", "ZDIV", "2{6,16,~1,4}\n{3,2}\n\n", ["2/5 ROUND 1", "DIVIDE 6X³/3X=2X²", "=6X³+4X²", "12X²-X+4"]),
    # ZPOLY: leading coefficient multiplied out (the -48 trap) and y-intercept
    ("W-poly1", "ZPOLY", "2~3\n3\n1\n~6\n1\n4\n1\n2\n1\n~2\n4\n\n\n", ["3/7 LEADING COEFFICIENT", "⁻3*1*4²*1^4", "=⁻48"]),
    ("W-poly2", "ZPOLY", "22\n2\n1\n5\n1\n1\n2\n2\n\n\n\n", ["4/7 Y-INTERCEPT", "F(0)=40"]),
    # ZZEROS: rational zero test, division, automatic substitution check
    ("W-zeros1", "ZZEROS", "1{2,~5,~21,36}\n~3\n0\n\n", ["2/5 DIVIDE BY (X+3)", "⁻3|   2  ⁻5 ⁻21  36", "LEAVES 2X²-11X+12"]),
    ("W-zeros2", "ZZEROS", "1{2,~5,~21,36}\n~3\n0\n\n\n\n", ["4/5 CHECK EACH ZERO", "F(⁻3)=0  OK", "F(3/2)=0  OK", "F(4)=0  OK"]),
    ("W-zeros3", "ZZEROS", "2{4,~1,~44,11}\n\n", ["RATIONAL ZERO TEST", "P DIVIDES 11", "Q DIVIDES 4", "F(1/4)=0  ZERO"]),
    ("W-zeros4", "ZZEROS", "1{1,0,7,0,~144}\n0\n~4\n\n", ["2/6 CONJUGATE PAIR", "⁻4𝑖 IS A ZERO, SO", "4𝑖 IS TOO", "=X²+16"]),
    # ZRATEQ: restrictions, LCD, cleared equation, check of the kept root
    ("W-rateq1", "ZRATEQ", "12\n1\n11\nX-3\n~8\nX+3\n9\nX²-9\n\n", ["2/8 RESTRICTIONS", "X²-9 = (X+3)(X-3)", "X≠3, ⁻3"]),
    ("W-rateq2", "ZRATEQ", "12\n1\n11\nX-3\n~8\nX+3\n9\nX²-9\n\n\n\n", ["4/8 MULTIPLY BY THE LCD", "(11X+33)+(⁻8X+24)", "=(9)"]),
    ("W-rateq3", "ZRATEQ", "12\n1\n11\nX-3\n~8\nX+3\n9\nX²-9\n#<", ["7/8 CHECK", "X=⁻16 KEPT", "MATCH"]),
    # ZRATFN: factor, hole, horizontal asymptote by degrees
    ("W-ratfn1", "ZRATFN", "2X²+7X+3\nX²-9\n1", ["1/9 FACTOR", "N=(X+3)(2X+1)", "D=(X+3)(X-3)"]),
    ("W-ratfn2", "ZRATFN", "2X²+7X+3\nX²-9\n1\n\n", ["3/9 HOLES", "COMMON FACTOR CANCELS", "F(X)=(2X+1)/(X-3)"]),
    ("W-ratfn3", "ZRATFN", "2X²+7X+3\nX²-9\n1\n\n\n\n\n", ["6/9 HORIZONTAL ASYMPTOTE", "EQUAL DEGREES", "Y=2/1=2"]),
    # ZINEQ: critical values, sign chart with test points, bracket choice
    ("W-ineq1", "ZINEQ", "33X-2\n(X+2)²\n4\n", ["2/5 CRITICAL VALUES", "ZEROS 2/3", "UNDEFINED ⁻2"]),
    ("W-ineq2", "ZINEQ", "33X-2\n(X+2)²\n4\n\n", ["3/5 SIGN CHART", "(⁻INF,⁻2)      X=⁻3    -", "(2/3,INF)      X=2     +"]),
    ("W-ineq3", "ZINEQ", "33X-2\n(X+2)²\n4\n\n\n", ["4/5 CHOOSE", "NEED THE - INTERVALS", "ZEROS INCLUDED [ ]", "UNDEFINED ALWAYS ( )"]),
    ("W-ineq4", "ZINEQ", "41\n2\n2\n1\n~4\n1\n6\n1\n22\n\n", ["SIGN CHART", "(2,6)          X=4     +"]),
    # ZGRAPH: solve for a, translations in order, key points; divided differences
    ("W-graph1", "ZGRAPH", "124\n~1\n3\n~3\n\n\n", ["3/7 SOLVE FOR A", "⁻3=A*(⁻1)²-1", "A=⁻2"]),
    ("W-graph2", "ZGRAPH", "124\n~1\n3\n~3\n\n\n\n", ["4/7 TRANSLATIONS", "SHIFT RIGHT 4 (X->X-4)", "STRETCH VERTICALLY *2",
                                                        "REFLECT OVER THE X-AXIS", "SHIFT DOWN 1"]),
    ("W-graph3", "ZGRAPH", "44\n0\n1\n1\n0\n2\n5\n3\n22\n\n\n", ["3/8 DIFFERENCES, ORDER 2", "(5-(⁻1))/(2-0)=3"]),
    ("W-graph4", "ZGRAPH", "44\n0\n1\n1\n0\n2\n5\n3\n22\n\n\n\n\n", ["5/8 NEWTON FORM", "+3(X)(X-1)"]),
    # ZCHECK: both sides shown
    ("W-check", "ZCHECK", "X²-5X=6\n1~1\n", ["1/2 SUBSTITUTE X=⁻1", "LEFT SIDE  =6", "RIGHT SIDE =6"]),
    # ZEXPR typed input shows what was typed and what it expands to
    ("W-expr", "ZQSOLV", "53(X+1)(X-1)\n~8X\n3", ["1/7 TYPED", "3(X+1)(X-1)=⁻8X"]),
    ("W-expr2", "ZQSOLV", "53(X+1)(X-1)\n~8X\n3\n", ["2/7 STANDARD FORM", "3X²-3=⁻8X", "3X²+8X-3=0"]),
    # pager: back arrow returns to the previous page
    ("W-pager", "ZDIV", "1{4,~7,~18,9}\n3\n\n\n<", ["2/6 BRING DOWN 4"]),
    # graph page is drawn (the harness logs the draw commands)
    ("W-graphpage", "ZQUAD", "11\n~6\n~7\n\n\n\n\n\n\n\n\n\n", [], {"graph": "DrawF X²-6X-7"}),
    ("W-graphpage2", "ZRATFN", "{1,0,0}\n{~60,3600}\n1\n\n\n\n\n\n\n", [], {"graph": "Vertical 60"}),
]
