"""Form B (Test 2 Parallel Practice Form B), checked against FormB-acceptance.md.

At least one case per subpart of every computational problem. Problems 19,
20, 22, 23 and 33 are BY HAND (they ask what a picture shows) and are covered
in MANUAL.md instead; 33 has one ZGRAPH case because ZGRAPH can draw each
choice to compare.

Case: (id, program, keys, expected substrings, options). An expected string
starting with ! must NOT appear. Keys: \\n ENTER, ~ (-), # CLEAR (jump to the
answer), < up arrow. Typed expressions are typed as printed, with X as the
variable. TRAP marks a regression test for a Shot 2 failure; TYPED marks a
ZEXPR typed-input case.
"""

CASES = [
    # ---- 1, 2: complex numbers (ZCPLX) ----
    ("B01a", "ZCPLX", "10\n1\n81\n1\n#", ["√(⁻81)=", "9𝑖"]),
    ("B01b", "ZCPLX", "10\n1\n43\n1\n#", ["𝑖√(43)"]),
    ("B01c", "ZCPLX", "10\n1\n180\n1\n#", ["6𝑖√(5)"]),
    ("B01d", "ZCPLX", "16\n1\n49\n8\n#", ["3/4+(7/8)𝑖"]),
    ("B01e", "ZCPLX", "1~12\n~1\n144\n~4\n#", ["3+3𝑖"]),
    ("B01f", "ZCPLX", "1~24\n~1\n72\n~8\n#", ["3+(3√(2)/4)𝑖"]),
    ("B02a", "ZCPLX", "24\n~5\n1\n7\n3\n1\n#", ["11-2𝑖"]),
    ("B02b", "ZCPLX", "38\n9\n1\n~4\n2\n1\n#", ["12+7𝑖"]),
    ("B02c", "ZCPLX", "40\n3\n1\n5\n~4\n1\n#", ["12+15𝑖"]),
    ("B02d", "ZCPLX", "46\n2\n1\n3\n~7\n1\n#", ["32-36𝑖"]),
    ("B02e", "ZCPLX", "48\n~1\n9\n4\n1\n16\n#", ["44+20𝑖"]),
    # ---- 3, 4, 7: quadratics from graphs (ZQUAD from graph; ZGRAPH) ----
    ("B03", "ZQUAD", "32\n~3\n0\n1\n#", ["F(X)=(X-2)²-3", "OPENS UP", "VERTEX (2,⁻3)", "AXIS X=2"]),
    ("B03g", "ZGRAPH", "122\n~3\n0\n1\n#", ["F(X)=(X-2)²-3", "VERTEX (2,⁻3)"]),
    ("B04", "ZQUAD", "3~3\n2\n~5\n0\n#", ["⁻(1/2)(X+3)²+2", "OPENS DOWN", "VERTEX (⁻3,2)", "AXIS X=⁻3"]),
    ("B04g", "ZGRAPH", "12~3\n2\n~5\n0\n#", ["⁻(1/2)(X+3)²+2", "RANGE (⁻INF,2]"]),
    ("B07a", "ZQUAD", "32\n~4\n4\n0\n#", ["F(X)=(X-2)²-4"]),
    ("B07b", "ZQUAD", "33\n~2\n2\n~5\n#", ["F(X)=⁻3(X-3)²-2"]),
    # ---- 5, 6, 9: quadratic functions (ZQUAD) ----
    ("B05a", "ZQUAD", "5(X-2)²\n#", ["VERTEX (2,0) MIN 0"]),  # TYPED
    ("B05b", "ZQUAD", "5~3(X+2)²-5\n#", ["VERTEX (⁻2,⁻5) MAX ⁻5"]),  # TYPED
    ("B05c", "ZQUAD", "5(1/4)(X+3)²+2\n#", ["VERTEX (⁻3,2) MIN 2"]),  # TYPED
    ("B05d", "ZQUAD", "13\n~24\n50\n#", ["VERTEX (4,2) MIN 2"]),
    ("B06a", "ZQUAD", "11\n8\n~3\n#", ["F(X)=(X+4)²-19"]),
    ("B06b", "ZQUAD", "1~2\n12\n~11\n#", ["F(X)=⁻2(X-3)²+7"]),
    ("B09a", "ZQUAD", "5~(X+3)²+5\n#", ["VERTEX (⁻3,5) MAX 5", "AXIS X=⁻3", "Y-INT (0,⁻4)",
                                         "X-INT (⁻3-√(5),0)", "(⁻3+√(5),0)", "DOMAIN (⁻INF,INF)", "RANGE (⁻INF,5]"]),  # TYPED
    ("B09a2", "ZQUAD", "5~(X+3)²+5\n#\n", ["ANSWER (POINTS)", "(⁻5,1)", "(⁻4,4)", "(⁻2,4)", "(⁻1,1)"]),  # TYPED
    ("B09b", "ZQUAD", "11\n~6\n~7\n#", ["VERTEX (3,⁻16) MIN ⁻16", "AXIS X=3", "Y-INT (0,⁻7)",
                                         "X-INT (⁻1,0),(7,0)", "RANGE [⁻16,INF)"]),
    ("B09b2", "ZQUAD", "11\n~6\n~7\n#\n", ["(1,⁻12)", "(2,⁻15)", "(4,⁻15)", "(5,⁻12)"]),
    ("B09c", "ZQUAD", "12\n~8\n1\n#", ["VERTEX (2,⁻7) MIN ⁻7", "AXIS X=2", "Y-INT (0,1)",
                                        "X-INT (2-√(14)/2,0)", "(2+√(14)/2,0)", "RANGE [⁻7,INF)"]),
    ("B09c2", "ZQUAD", "12\n~8\n1\n#\n", ["(0,1)", "(1,⁻5)", "(3,⁻5)", "(4,1)"]),
    ("B09dir", "ZQUAD", "5~(X+3)²+5\n\n", ["DIRECTION", "OPENS DOWN"]),
    # ---- 13-15: applications (ZQUAD APPLICATION) ----
    ("B13", "ZQUAD", "4~16\n0\n576\n1#", ["HITS GROUND AT T=6", "(REJECT T=⁻6, T<0)"]),
    ("B14a", "ZQUAD", "4~8\n1600\n~30000\n2#", ["MAX 50000 AT X=100"]),
    ("B14b", "ZQUAD", "4~8\n1600\n~30000\n2#", ["VERTEX (100,50000)"]),
    ("B15a", "ZQUAD", "4~4.9\n29.4\n78.4\n1#", ["AT T=3"]),
    ("B15b", "ZQUAD", "4~4.9\n29.4\n78.4\n1#", ["MAX 122.5 AT T=3"]),
    ("B15c", "ZQUAD", "4~4.9\n29.4\n78.4\n1#", ["HITS GROUND AT T=8", "(REJECT T=⁻2, T<0)"]),
    # ---- 8, 10, 11, 12: quadratic equations (ZQSOLV) ----
    ("B08a", "ZQSOLV", "11\n~6\n~7\n0\n0\n0\n#", ["D=64>0", "TWO REAL RATIONAL"]),
    ("B08b", "ZQSOLV", "11\n~10\n25\n0\n0\n0\n#", ["D=0", "ONE REAL SOLUTION"]),
    ("B08c", "ZQSOLV", "11\n~6\n0\n0\n0\n~11\n#", ["D=⁻8<0", "TWO NONREAL SOLUTIONS"]),
    ("B08d", "ZQSOLV", "5(~2+3X)²\n47\n1#", ["D=1692>0", "TWO REAL IRRATIONAL"]),  # TYPED
    ("B08d2", "ZQSOLV", "5(~2+3X)²\n47\n1\n", ["STANDARD FORM", "9X²-12X+4=47", "9X²-12X-43=0"]),  # TYPED
    ("B10a", "ZQSOLV", "21\n6\n0\n25\n#", ["X=⁻11, ⁻1"]),
    ("B10b", "ZQSOLV", "22\n5\n~12\n108\n#", ["X=⁻5+/-2√(15)"]),
    ("B10c", "ZQSOLV", "21\n~1/4\n0\n~13/16\n#", ["X=1/4+/-(√(13)/4)𝑖"]),  # TRAP: fraction input
    ("B11a", "ZQSOLV", "31\n8\n0\n0\n0\n7\n#", ["X=⁻4+/-√(23)"]),
    ("B11b", "ZQSOLV", "31\n6\n~5\n0\n0\n0\n#", ["X=⁻3+/-√(14)"]),
    ("B11c", "ZQSOLV", "31\n10\n29\n0\n0\n0\n#", ["X=⁻5+/-2𝑖"]),
    ("B12a", "ZQSOLV", "41\n~10\n21\n0\n0\n0\n#", ["X=3, 7"]),
    ("B12b", "ZQSOLV", "46\n0\n0\n0\n30\n0\n#", ["X=0, 5"]),
    ("B12c", "ZQSOLV", "44\n0\n0\n0\n0\n68\n#", ["X=+/-√(17)"]),
    ("B12d", "ZQSOLV", "41\n3\n5\n0\n0\n0\n#", ["X=⁻3/2+/-(√(11)/2)𝑖"]),
    ("B12e", "ZQSOLV", "5(X+4)²\n3\n3#", ["X=⁻4+/-√(3)"]),  # TYPED
    ("B12f", "ZQSOLV", "41\n0\n0\n0\n6\n~34\n#", ["X=3+/-5𝑖"]),
    ("B12g", "ZQSOLV", "41\n12\n36\n0\n0\n19\n#", ["X=⁻6+/-√(19)"]),
    ("B12h", "ZQSOLV", "5X(4X+5)\n~3\n3#", ["X=⁻5/8+/-(√(23)/8)𝑖"]),  # TYPED
    ("B12i", "ZQSOLV", "42\n10\n0\n0\n0\n~3\n#", ["X=(⁻5+/-√(19))/2"]),
    ("B12j", "ZQSOLV", "53(X+1)(X-1)\n~8X\n3#", ["X=⁻3, 1/3"]),  # TYPED
    # ---- 16, 17: division (ZDIV) ----
    ("B16a", "ZDIV", "2{4,~23,15}\n{1,~5}\n#", ["QUOTIENT 4X-3", "REMAINDER 0"]),
    ("B16b", "ZDIV", "2{1,4,~25}\n{1,8}\n#", ["QUOTIENT X-4", "REMAINDER 7", "= X-4+7/(X+8)"]),
    ("B16c", "ZDIV", "2{6,16,~1,4}\n{3,2}\n#", ["QUOTIENT 2X²+4X-3", "REMAINDER 10"]),
    ("B16d", "ZDIV", "2X^5+3X^4-2X²-X-8\nX²-2\n#", ["QUOTIENT X³+3X²+2X+4", "REMAINDER 3X"]),  # TYPED
    ("B17a", "ZDIV", "1{4,~7,~18,9}\n3\n#", ["QUOTIENT 4X²+5X-3", "REMAINDER 0"]),
    ("B17b", "ZDIV", "1{~3,~7,18,~8}\n~4\n#", ["QUOTIENT ⁻3X²+5X-2", "REMAINDER 0"]),
    ("B17c", "ZDIV", "1{1,0,0,1,0,7}\n3\n#", ["QUOTIENT X^4+3X³+9X²+28X+84", "REMAINDER 259"]),
    ("B17d", "ZDIV", "1{1,~4,2,8,~10}\n2\n#", ["QUOTIENT X³-2X²-2X+4", "REMAINDER ⁻2"]),
    # ---- 18, 21, 24-26: polynomials (ZPOLY, ZGRAPH) ----
    ("B18a", "ZPOLY", "1{6,2,5,0,0,0,9}\n#", ["DEGREE 6, LEADING 6", "RISES LEFT, RISES RIGHT"]),
    ("B18b", "ZPOLY", "1{3,0,0,0,0,7,17,2,0,~8}\n#", ["DEGREE 9, LEADING 3", "FALLS LEFT, RISES RIGHT"]),
    ("B18b2", "ZPOLY", "117X³-8+7X^4+3X^9+2X²\n#", ["DEGREE 9, LEADING 3", "FALLS LEFT, RISES RIGHT"]),  # TYPED
    ("B18c", "ZPOLY", "2~3\n3\n1\n~6\n1\n4\n1\n2\n1\n~2\n4\n#", ["DEGREE 7, LEADING ⁻48", "RISES LEFT, FALLS RIGHT"]),  # TRAP: -48 not -3
    ("B21", "ZPOLY", "33\n~3\n1\n1\n1\n4\n1\n0\n0\n2\n#", ["F(X)=(1/6)(X+3)(X-1)(X-4)"]),
    ("B21g", "ZGRAPH", "33\n~3\n1\n1\n1\n4\n1\n0\n2\n#", ["F(X)=(1/6)(X+3)(X-1)(X-4)", "DEGREE 3"]),
    ("B24a", "ZPOLY", "2~3\n3\n1\n0\n6\n1\n5\n2\n1\n~4\n6\n#", ["X=0 MULT 6", "X=⁻5 MULT 2", "X=4 MULT 6"]),
    ("B24b", "ZPOLY", "2~5\n3\n1\n0\n2\n1\n~3\n3\n1\n6\n4\n#", ["X=0 MULT 2", "X=3 MULT 3", "X=⁻6 MULT 4"]),
    ("B25", "ZPOLY", "22\n2\n1\n5\n1\n1\n2\n2\n#", ["Y-INT (0,40)", "X=⁻5 MULT 1 CROSSES", "X=⁻2 MULT 2 TOUCHES",
                                                    "FALLS LEFT, RISES RIGHT"]),
    ("B26a", "ZPOLY", "32\n~3\n4\n7\n1\n1\n#", ["F(X)=(X+3)^4(X-7)", "DEGREE 5"]),
    ("B26b", "ZPOLY", "32\n6\n4\n~2\n2\n1\n#", ["F(X)=(X-6)^4(X+2)²", "DEGREE 6"]),
    # ---- 27-29: zeros (ZZEROS) ----
    ("B27a", "ZZEROS", "1{1,6,~5,~30}\n~6\n0\n#", ["⁻6", "+/-√(5)"]),
    ("B27b", "ZZEROS", "1{1,~7,4,~28}\n7\n0\n#", ["7", "+/-2𝑖"]),
    ("B27c", "ZZEROS", "1{1,~10,41,~50}\n2\n0\n#", ["2", "4+/-3𝑖"]),
    ("B27d", "ZZEROS", "1{1,0,7,0,~144}\n0\n~4\n#", ["+/-4𝑖", "⁻3, 3"]),
    ("B27e", "ZZEROS", "1{1,2,1,18,~72}\n0\n3\n#", ["+/-3𝑖", "⁻4, 2"]),
    ("B28a", "ZZEROS", "1{1,3,~18,~40}\n~2\n0\n#", ["(X+2)(X+5)(X-4)"]),
    ("B28b", "ZZEROS", "1{1,1,~8,~12}\n3\n0\n#", ["(X-3)(X+2)²"]),
    ("B28c", "ZZEROS", "1{2,~5,~21,36}\n~3\n0\n#", ["2(X+3)(X-3/2)(X-4)"]),
    ("B29a", "ZZEROS", "2{1,0,~9,0}\n#", ["⁻3, 0, 3"]),
    ("B29a2", "ZZEROS", "2X³-9X\n#", ["⁻3, 0, 3"]),  # TYPED
    ("B29b", "ZZEROS", "2{6,~1,~2}\n#", ["⁻1/2, 2/3"]),
    ("B29c", "ZZEROS", "2{1,0,25}\n#", ["+/-5𝑖"]),
    ("B29d", "ZZEROS", "2{1,0,7}\n#", ["+/-𝑖√(7)"]),
    ("B29e", "ZZEROS", "2{3,0,12,0}\n#", ["0", "+/-2𝑖"]),
    ("B29f", "ZZEROS", "2{4,~1,~44,11}\n#", ["1/4", "+/-√(11)"]),
    ("B29g", "ZZEROS", "2{1,~7,12,0}\n#", ["0, 3, 4"]),
    ("B29h", "ZZEROS", "2{1,~5,4,~20}\n#", ["5", "+/-2𝑖"]),
    ("B29i", "ZZEROS", "2{1,3,16,48}\n#", ["⁻3", "+/-4𝑖"]),
    # ---- 30: rational equations (ZRATEQ), typed numerators and denominators ----
    ("B30a", "ZRATEQ", "12\n1\nX\n1\n~12\nX\n4\n1\n#", ["{⁻2, 6}"]),
    ("B30b", "ZRATEQ", "12\n1\n1\n1\n2\nX\n15\nX²\n#", ["{⁻5, 3}"]),
    ("B30c", "ZRATEQ", "12\n1\n1\nX\n1\nX-5\nX-4\nX-5\n#", ["{1}", "5 IS EXTRANEOUS"]),
    ("B30d", "ZRATEQ", "11\n1\n3\nX\nX\n6X-24\n#", ["{6, 12}"]),
    ("B30e", "ZRATEQ", "12\n1\n7-X\nX\n2\n3\n10\nX\n#", ["{⁻9}"]),
    ("B30f", "ZRATEQ", "12\n1\n11\nX-3\n~8\nX+3\n9\nX²-9\n#", ["{⁻16}"]),
    ("B30g", "ZRATEQ", "12\n1\n1\nX+6\n3\nX+2\n~4\nX²+8X+12\n#", ["NO SOLUTION", "⁻6 IS EXTRANEOUS"]),
    # ---- 31, 32, 34-37: rational functions (ZRATFN, ZGRAPH) ----
    ("B31a", "ZRATFN", "{5,6}\n{~3,2}\n1#", ["DOMAIN {X | X≠2/3}", "X-INT (⁻6/5,0)", "V.A. X=2/3",
                                             "H.A. Y=⁻5/3", "HOLES NONE"]),
    ("B31b", "ZRATFN", "{1,~3}\n{1,8,0}\n1#", ["X≠⁻8,0", "X-INT (3,0)", "V.A. X=⁻8, X=0", "H.A. Y=0", "HOLES NONE"]),
    ("B31c", "ZRATFN", "{1,~5}\n{1,7,6}\n1#", ["X≠⁻6,⁻1", "X-INT (5,0)", "V.A. X=⁻6, X=⁻1", "H.A. Y=0", "HOLES NONE"]),
    ("B31d", "ZRATFN", "2X²+7X+3\nX²-9\n1#", ["X≠⁻3,3", "X-INT (⁻1/2,0)", "V.A. X=3", "H.A. Y=2",
                                              "HOLES X=⁻3 AT (⁻3,5/6)"]),  # TYPED
    ("B32a", "ZGRAPH", "252~1\n~3\n4\n#", ["F(X)=⁻1/(X+3)+4", "V.A. X=⁻3  H.A. Y=4"]),
    ("B32a2", "ZGRAPH", "252~1\n~3\n4\n\n\n", ["KEY POINTS", "(⁻1,⁻1)->(⁻4,5)", "(1,1)->(⁻2,3)"]),
    ("B32b", "ZGRAPH", "2531\n2\n1\n#", ["F(X)=1/(X-2)²+1", "V.A. X=2  H.A. Y=1", "RANGE (1,INF)"]),
    ("B32b2", "ZGRAPH", "2531\n2\n1\n\n\n", ["(⁻1,1)->(1,2)", "(1,1)->(3,2)"]),
    ("B33", "ZGRAPH", "2521\n~3\n0\n#", ["F(X)=1/(X+3)", "V.A. X=⁻3  H.A. Y=0"]),
    ("B34a", "ZRATFN", "{1,0,0}\n{~60,3600}\n248\n#", ["F(48)=16/5=3.2"]),
    ("B34b", "ZRATFN", "{1,0,0}\n{~60,3600}\n1#", ["V.A. X=60"]),
    ("B34c", "ZRATFN", "{1,0,0}\n{~60,3600}\n55N\n", ["AS X->60 FROM LEFT, N->INF"]),
    ("B35a", "ZRATFN", "{18,600}\n{1,0}\n2400\n#", ["F(400)=39/2=19.5"]),
    ("B35b", "ZRATFN", "{18,600}\n{1,0}\n328\n#", ["X=60"]),
    ("B35c", "ZRATFN", "{18,600}\n{1,0}\n53C\n", ["AS X->INF, C->18", "LONG-RUN AVERAGE COST->18"]),
    ("B36a", "ZRATFN", "{24,60}\n{.04,1}\n210\n#", ["F(10)=214.2857"]),
    ("B36b", "ZRATFN", "{24,60}\n{.04,1}\n54N\n", ["LONG-RUN POPULATION->600"]),
    ("B36b2", "ZRATFN", "{24,60}\n{.04,1}\n1#", ["H.A. Y=600", "!1/0"]),  # TRAP: decimal coefficients
    ("B37a", "ZRATFN", "{600,0}\n{~1,150}\n230\n#", ["F(30)=150"]),
    ("B37b", "ZRATFN", "{600,0}\n{~1,150}\n3900\n#", ["X=90"]),
    # ---- 38-44: inequalities (ZINEQ) ----
    ("B38", "ZINEQ", "42\n0\n~3\n1\n2\n1\n11#", ["(⁻INF,⁻3)U(2,INF)"]),
    ("B39", "ZINEQ", "42\n0\n~1\n2\n2\n1\n21#", ["(⁻INF,⁻1)U(⁻1,2)"]),
    ("B40a", "ZINEQ", "43\n0\n~4\n1\n~2\n1\n3\n1\n13#", ["(⁻INF,⁻4)U(⁻2,3)"]),
    ("B40b", "ZINEQ", "43\n0\n~4\n1\n~2\n1\n3\n1\n14#", ["(⁻INF,⁻4]U[⁻2,3]"]),  # TRAP: non-strict
    ("B40c", "ZINEQ", "43\n0\n~4\n1\n~2\n1\n3\n1\n11#", ["(⁻4,⁻2)U(3,INF)"]),
    ("B40d", "ZINEQ", "43\n0\n~4\n1\n~2\n1\n3\n1\n12#", ["[⁻4,⁻2]U[3,INF)"]),  # TRAP: non-strict
    ("B41a", "ZINEQ", "1{1,2,~8}\n0\n1#", ["(⁻INF,⁻4)U(2,INF)"]),
    ("B41b", "ZINEQ", "1X²-5X\n6\n3#", ["(⁻1,6)"]),  # TYPED
    ("B41c", "ZINEQ", "1{~2,4,~7}\n0\n4#", ["(⁻INF,INF)", "ALL REAL NUMBERS"]),  # TRAP: no real zeros
    ("B41d", "ZINEQ", "1{~2,4,~7}\n0\n1#", ["NO SOLUTION"]),
    ("B41e", "ZINEQ", "21\n3\n1\n~1\n1\n1\n~3\n1\n1\n~6\n1\n1#", ["(1,3)U(6,INF)"]),
    ("B41f", "ZINEQ", "2~3\n3\n1\n0\n1\n1\n1\n2\n~1\n4\n1\n1#", ["(⁻INF,⁻1)U(⁻1,0)U(4,INF)"]),
    ("B41g", "ZINEQ", "1X³+10X²+27X\n~18\n4#", ["(⁻INF,⁻6]U[⁻3,⁻1]"]),  # TRAP: non-strict, TYPED
    ("B42a", "ZINEQ", "41\n2\n2\n1\n~4\n1\n6\n1\n21#", ["(⁻INF,⁻4)U(2,6)"]),
    ("B42b", "ZINEQ", "41\n2\n2\n1\n~4\n1\n6\n1\n22#", ["(⁻INF,⁻4)U[2,6)"]),
    ("B42c", "ZINEQ", "41\n2\n2\n1\n~4\n1\n6\n1\n23#", ["(⁻4,2)U(6,INF)"]),
    ("B42d", "ZINEQ", "41\n2\n2\n1\n~4\n1\n6\n1\n24#", ["(⁻4,2]U(6,INF)"]),
    ("B43", "ZINEQ", "3{7}\n{4,~3}\n1#", ["(3/4,INF)"]),
    ("B44", "ZINEQ", "33X-2\n(X+2)²\n4#", ["(⁻INF,⁻2)U(⁻2,2/3]"]),  # TRAP: non-strict, TYPED
    # ---- Shot 2 regression traps not covered above ----
    ("T-frac", "ZQSOLV", "41\n~1/2\n7/8\n0\n0\n0\n#", ["X=1/4+/-(√(13)/4)𝑖"]),  # TRAP: x²-½x+7/8=0
    ("T-frac2", "ZQSOLV", "5X²-X/2+7/8\n0\n3#", ["X=1/4+/-(√(13)/4)𝑖"]),  # TRAP + TYPED
    ("T-coef", "ZGRAPH", "252~1\n~3\n0\n#", ["F(X)=⁻1/(X+3)", "!⁻11/(X+3)"]),  # TRAP: a=-1 display
    ("T-simp1", "ZCPLX", "10\n1\n4\n1\n#", ["2𝑖", "!√(1)"]),  # TRAP: no 2√1 i
    ("T-simp2", "ZQUAD", "21\n2\n0\n#", ["F(X)=(X-2)²", "!=1(X"]),  # TRAP: no 1(x-2)²
    ("T-simp3", "ZQSOLV", "4~1\n2\n5\n0\n0\n0\n#", ["X=1+/-√(6)", "!/⁻1", "!(⁻1"]),  # TRAP: no (-1±√6)/-1
]
