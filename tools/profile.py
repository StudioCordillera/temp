"""Cost profile of one harness run: python tools/profile.py PROG 'keys'
Prints estimated ms per program and the most expensive statements,
counted from the last input to the first wait for a key."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests"))
from collections import Counter
import harness, tibasic

prog, keys = sys.argv[1], sys.argv[2].replace("\\n", "\n")
self_cost, stm, calls = Counter(), Counter(), Counter()
orig = tibasic.Interp.exec_stmt
state = {"on": False}
def ex(self, fr):
    if self.last_input_cost is not None:
        state["on"] = True
    i = fr.pc
    c0 = dict(self.cost)
    depth = len(self.frames)
    orig(self, fr)
    if state["on"] and self.last_input_cost is not None:
        d = {k: self.cost[k] - c0[k] for k in c0}
        s = fr.prog.stmts[i]
        if s and s[0] == "prgm":
            d = {"stmt": 1, "tok": len(s), "call": 1, "listel": 0, "strch": 0, "draw": 0}
            calls["".join(s[1:])] += 1
        ms = tibasic.cost_ms(d)
        self_cost[fr.prog.name] += ms
        stm[(fr.prog.name, i, "".join(s)[:48])] += ms
tibasic.Interp.exec_stmt = ex
r = harness.run(prog, keys)
tot = sum(self_cost.values())
print(f"total {tot:.0f} ms (answer cost {max((tibasic.cost_ms(c) for c in r.it.answer_costs), default=0):.0f})")
for k, v in self_cost.most_common():
    print(f"  {k:<8}{v:8.0f} ms")
print("calls:", dict(calls.most_common()))
for (p, i, s), v in stm.most_common(25):
    print(f"{v:7.0f}  {p}:{i}  {s}")
