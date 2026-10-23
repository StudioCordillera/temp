"""Print the answer screen (and optionally one work screen) for the manual's
examples, exactly as the harness renders them. python tools/screens.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests"))
import harness

EXAMPLES = [
    ("ZCPLX", "1e", "1~12\n~1\n144\n~4\n#"),
    ("ZCPLX", "2e", "48\n~1\n9\n4\n1\n16\n#"),
    ("ZQSOLV", "8d typed", "5(~2+3X)²\n47\n1#"),
    ("ZQSOLV", "12i", "42\n10\n0\n0\n0\n~3\n#"),
    ("ZQSOLV", "12j typed", "53(X+1)(X-1)\n~8X\n3#"),
    ("ZQSOLV", "10c work page 3", "21\n~1/4\n0\n~13/16\n\n\n"),
    ("ZQUAD", "9b", "11\n~6\n~7\n#"),
    ("ZQUAD", "15", "4~4.9\n29.4\n78.4\n1#"),
    ("ZQUAD", "4 from graph", "3~3\n2\n~5\n0\n#"),
    ("ZDIV", "17a work page 3", "1{4,~7,~18,9}\n3\n\n\n"),
    ("ZDIV", "16d typed", "2X^5+3X^4-2X²-X-8\nX²-2\n#"),
    ("ZPOLY", "25", "22\n2\n1\n5\n1\n1\n2\n2\n#"),
    ("ZPOLY", "21", "33\n~3\n1\n1\n1\n4\n1\n0\n0\n2\n#"),
    ("ZZEROS", "27e", "1{1,2,1,18,~72}\n0\n3\n#"),
    ("ZZEROS", "28c", "1{2,~5,~21,36}\n~3\n0\n#"),
    ("ZZEROS", "28c check page", "1{2,~5,~21,36}\n~3\n0\n\n\n\n"),
    ("ZRATEQ", "30f", "12\n1\n11\nX-3\n~8\nX+3\n9\nX²-9\n#"),
    ("ZRATEQ", "30c check page", "12\n1\n1\nX\n1\nX-5\nX-4\nX-5\n#<"),
    ("ZRATFN", "31d typed", "2X²+7X+3\nX²-9\n1#"),
    ("ZRATFN", "34c application", "{1,0,0}\n{~60,3600}\n55N\n"),
    ("ZRATFN", "36a evaluate", "{24,60}\n{.04,1}\n210\n#"),
    ("ZINEQ", "41g typed", "1X³+10X²+27X\n~18\n4#"),
    ("ZINEQ", "44 sign chart", "33X-2\n(X+2)²\n4\n\n"),
    ("ZINEQ", "42b from graph", "41\n2\n2\n1\n~4\n1\n6\n1\n22#"),
    ("ZGRAPH", "32a", "252~1\n~3\n4\n#"),
    ("ZGRAPH", "21 poly from zeros", "33\n~3\n1\n1\n1\n4\n1\n0\n2\n#"),
    ("ZCHECK", "12j check x=1/3", "3X²+8X-3=0\n11/3\n#"),
    ("MATHKIT", "main menu", ""),
]
for prog, label, keys in EXAMPLES:
    r = harness.run(prog, keys)
    print(f"### {prog} {label}  keys={keys!r}")
    print("```text")
    print("\n".join(l.rstrip() for l in r.screen.split("\n")).rstrip())
    print("```")
